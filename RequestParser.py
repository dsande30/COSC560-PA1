"""
Basic HTTP server request parser.

*Tentatively* Parses the following types of requests:
    1. GET
    2. POST
"""

import logging, sys, io, re

class RequestParser:
    """Base object for parsing http headers."""
    
    def parseRequest(self, request):
        """Parse given request."""
        logging.debug(request)
        str_request = io.StringIO(request)
        lines = str_request.readlines()
        for line in lines:
            self.checkType(line)


    def checkType(self, line):
        """Check if it's a GET or POST."""
        get_http_version = re.compile(r"^\w*\s\/\sHTTP\/")
        get_host = re.compile(r"^Host:\ ")


        """
        FIXME:
        Some thoughts:
            These regexes don't work, but I'm not sure how we want to fix them.
            https://url.spec.whatwg.org/#url-representation lays out the standard for how a browser
            parses a URL.
            We need to implement:
                check type (ftp, http, etc) and use default port
                allow for custom port using ':'
                
            I'll finish this up hopefully tomorrow night. Need to read up more and figure out how
            I wanna do this.
        """

        for m in get_http_version.finditer(line, re.IGNORECASE):
            logging.debug("HTTP VERSION: " + line[m.end():])
        for n in get_host.finditer(line, re.IGNORECASE):
            logging.debug("HOSTNAME:" + line[n.end():])


if __name__ == "__main__":
    """Note: run main only to debug!!"""
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    DEBUG_request = """
GET / HTTP/1.1
Host: localhost:8888
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: Phpstorm-19ce36aa=054a9f1e-e611-46ec-a0dd-3594013dd076
    """
    rp = RequestParser()
    rp.parseRequest(DEBUG_request)