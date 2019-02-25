"""
Basic HTTP server request parser.

*Tentatively* Parses the following types of requests:
    1. GET
    2. POST
"""

import logging, sys, io, re

class RequestParser:
    """Base object for parsing http headers."""

    def __init__(self):
        self.error_code = 200
        self.action = ''
        self.version = 0
        self.host = ''
        self.port = 0
        self.path = ''


    def parseRequest(self, request):
        """Parse given request."""
        str_request = io.StringIO(request)
        lines = str_request.readlines()
        self.checkData(lines[0].strip())
        self.checkHost(lines[1].strip())
        logging.debug("Error code: " + str(self.error_code))
        logging.debug("Action: " + str(self.action))
        logging.debug("Version: " + str(self.version))
        logging.debug("Host: " + str(self.host))
        logging.debug("Port: " + str(self.port))
        logging.debug("Path: " + str(self.path))



    def checkData(self, line):
        """Get request acion, pathname, and HTTP version."""
        split_line = line.split()
        self.action = split_line[0]
        self.path = split_line[1]

        version = split_line[2].split('/')
        self.version = version[1]


    def checkHost(self, line):
        """Gather hostname and port."""
        split_line = line.split(':')
        self.host = split_line[1]
        if len(split_line) > 2:
            self.port = split_line[2]


if __name__ == "__main__":
    """Note: run main only to debug!!"""
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    DEBUG_request = """GET / HTTP/1.1
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