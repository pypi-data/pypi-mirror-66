from apitracker_agent.conf.constants import EVENT
from apitracker_agent.instrumentation.packages.base import BaseInstrumentation
from uuid import uuid4
import time
import base64
from apitracker_agent.context import execution_context

is_python_2 = False
try:
    from httplib import HTTPConnection, HTTPSConnection, HTTPResponse
    is_python_2 = True
except ImportError as error:
    from http.client import HTTPConnection, HTTPSConnection, HTTPResponse

# Python 2 and 3: alternative 4
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class HttpLibInstrumentation(BaseInstrumentation):
    name = "httplib"

    def instrument(self):
        _install_httplib()


def _install_httplib():
    real_putrequest = HTTPConnection.putrequest
    real_putheader = HTTPConnection.putheader
    real_endheaders = HTTPConnection.endheaders
    real_getresponse = HTTPConnection.getresponse
    real_readresponse = HTTPResponse.read

    def putrequest(self, method, url, skip_host=0, skip_accept_encoding=0):
        host = self.host

        client = execution_context.get_client()
        if client is None or host not in client.config.api_ids:
            return real_putrequest(self, method, url, skip_host, skip_accept_encoding)

        port = self.port
        default_port = self.default_port
        real_url = url
        parsed_url = urlparse(url)

        if not real_url.startswith(("http://", "https://")):
            real_url = "%s://%s%s%s" % (
                default_port == 443 and "https" or "http",
                host,
                port != default_port and ":%s" % port or "",
                url,
            )
        request_received_at = int(round(time.time() * 1000000000))

        headers = dict()
        headers['Host'] = host
        self._apitracker_context = {
            "event": {
                "eventId": uuid4(),
                "apiId": client.config.api_ids[host],
                "request": {
                    "method": method,
                    "headers": headers,
                    "body": None,
                    "url": real_url,
                    "path": parsed_url.path,
                    "query": parsed_url.query,
                    "receivedAt": request_received_at
                }
            },
            "client": client
        }
        return real_putrequest(self, method, url, skip_host, skip_accept_encoding)

    def putheader(self, header, *values):
        apitracker_context = getattr(self, "_apitracker_context", None)

        if apitracker_context is None:
            return real_putheader(self, header, *values)
        apitracker_context['event']['request']['headers'][header] = values[0] if isinstance(values, (tuple, list)) else values
        return real_putheader(self, header, *values)

    def setBody(self, apitracker_context, message_body):
        if apitracker_context is None:
            return
        try:
            apitracker_context['event']['request']['body'] = base64.b64encode(message_body.encode('utf-8')) if message_body is not None else None
        except (UnicodeDecodeError, AttributeError):
            apitracker_context['event']['request']['body'] = base64.b64encode(message_body) if message_body is not None else None
        except:
            # try not to fail
            pass
        print apitracker_context['event']['request']['body']

    def endheaders2(self, message_body=None):
        apitracker_context = getattr(self, "_apitracker_context", None)
        setBody(self, apitracker_context, message_body)
        return real_endheaders(self, message_body)

    def getresponse(self, *args, **kwargs):
        """
        Hook into getresponse to further construct the event object that was started in _sendrequest.
        We can't read response body here because it'll close the body. We need to hook into HTTPResponse.read for that.
        So we have to save the event to the response object so when read is called, we can reference the event
        :param self:
        :param args:
        :param kwargs:
        :return:
        """
        apitracker_context = getattr(self, "_apitracker_context", None)

        if apitracker_context is None:
            return real_getresponse(self, *args, **kwargs)
        rv = real_getresponse(self, *args, **kwargs)

        response_received_at = int(round(time.time() * 1000000000))
        if is_python_2:
            # in python 2, HTTPResponse headers is a list of raw http header output, so turn them into a dict by splitting by : then
            # trimming \r\n
            headers = {c[0]: c[1][0:-2] for c in [h.split(': ') for h in rv.msg.headers]}
        else:
            headers = dict(rv.headers)
        apitracker_context['event']['response'] = {
            "headers": headers,
            "statusCode": rv.status,
            "receivedAt": response_received_at
        }
        rv._apitracker_context = apitracker_context
        return rv

    def readresponse(self, amt=None):
        rv = real_readresponse(self, amt)

        apitracker_context = getattr(self, "_apitracker_context", None)
        if apitracker_context is None or 'queued' in apitracker_context:
            return rv
        apitracker_context['event']['response']['body'] = base64.b64encode(rv) if rv else None
        apitracker_context['client'].queue(EVENT, apitracker_context['event'])
        # mark the event as queued so multiple read don't result in multiple events
        apitracker_context['queued'] = True

        return rv

    HTTPConnection.putrequest = putrequest
    HTTPConnection.putheader = putheader
    if is_python_2:
        HTTPConnection.endheaders = endheaders2
    else:
        def endheaders3(self, message_body=None, *args, **kwargs):
            apitracker_context = getattr(self, "_apitracker_context", None)
            setBody(self, apitracker_context, message_body)
            return real_endheaders(self, message_body, *args, **kwargs)
        HTTPConnection.endheaders = endheaders3

    HTTPConnection.getresponse = getresponse
    HTTPResponse.read = readresponse
