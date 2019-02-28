"""
Basic HTTP server request parser.

*Tentatively* Parses the following types of requests:
    1. GET
    2. POST
"""

import logging
import sys
import io
import re
import os
from urllib.parse import unquote

class RequestParser:
    """Base object for parsing http headers."""

    def __init__(self):
        self.error_code = 200
        self.action = ''
        self.version = 0
        self.path = ''
        self.header = {}

    def parseRequest(self, request):
        """Parse given request."""
        try:
            str_request = io.StringIO(request.decode())
            self.parseHeader(str_request, True) 
        except:
            ct = re.compile(b'(Content-Type: )(\S+)\r\n\r\n')
            ext = re.compile(b'(filename=)(\")(.*\.)([\w.]*)(\")')
            tmp_ct = ct.search(request).groups()[1]
            tmp_ext = ext.search(request).groups()[3]
            fname = ext.search(request).groups()[2]
            end_header = request.find('\r\n\r\n'.encode())
            index = request.find(tmp_ct) + len(tmp_ct) + 4 # get to start of content

            self.parseHeader(io.StringIO(request[:end_header].decode()), False)
            self.header['Mime-Type'] = tmp_ct.decode()
            self.header['Payload'] = request[index:]
            self.path = './site/uploads/' + (fname + tmp_ext).decode()

    def parseHeader(self, header, check_payload):
        lines = header.readlines()
        last = lines[-1]

        for line in lines[1:]:
            if line is last and check_payload:
                self.header['Payload'] = line
            else:
                tmp = [x.strip() for x in line.split(':', 1)]
                if len(tmp) == 2:
                    self.header[tmp[0]] = tmp[1]

        self.checkData(lines[0].strip())

    def checkData(self, line):
        """Get request acion, pathname, and HTTP version."""
        split_line = line.split()
        self.action = split_line[0]
        if split_line[1] == '/':
            self.path = os.path.normpath("site" + os.path.sep + "index.html")
            logging.debug(os.path.abspath(self.path))

        else:
            if split_line[1] in ['/dir', '/uploads']:
                self.path = split_line[1]
            else:
                self.path = unquote(os.path.abspath('.') + os.path.sep + "site" + split_line[1])

        version = split_line[2].split('/')
        self.version = version[1]