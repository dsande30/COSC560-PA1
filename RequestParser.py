"""
Basic HTTP server request parser.
Parses HTTP headers and determines GET/POST actions
Stores all header and content information in an object
"""

import logging
import sys
import io
import re
import os
from urllib.parse import unquote

class RequestParser:
    """Base object for parsing http headers."""

    def __init__(self, request):
        """Store all REQUEST data in the object."""
        self.error_code = 200
        self.action = ''
        self.version = 0
        self.path = ''
        self.header = {}
        self.request = request

    def parseRequest(self):
        """Parse given request."""
        try:
            # this try statement catches GET and FORM POST requests
            str_request = io.StringIO(self.request.decode())
            self.parseHeader(str_request, True)
        except:
            # the except statement catches multipart/form-data POST requests
            self.parseMultiPart()

    def parseMultiPart(self):
        """Parses multipart/form-data POST requests."""

        request = self.request

        # regex is used to separate header from content
        ct = re.compile(b'(Content-Type: )(\S+)\r\n\r\n')
        name = re.compile(b'(filename=)(\")(.*\.*)(\")')
        tmp_ct = ct.search(request).groups()[1]
        fname = name.search(request).groups()[2]
        end_header = request.find('\r\n\r\n'.encode())
        index = request.find(tmp_ct) + len(tmp_ct) + 4 # get to start of content

        # content and header are now determined based on regex results
        final_bound = 0
        final_bound = request[index:].find('------WebKitForm'.encode())
        if final_bound != 0:
            self.header['Payload'] = request[index:index+final_bound]
        else:
            self.header['Payload'] = request[index:]            
        self.header['Mime-Type'] = tmp_ct.decode()

        # populates the header dictionary   
        self.parseHeader(io.StringIO(request[:end_header].decode()), False)

        # file name to be uploaded
        self.path = './site/uploads/' + fname.decode()

    def parseHeader(self, header, check_payload):
        """Parses the header of any given request."""

        lines = header.readlines()
        last = lines[-1]

        # the header is converted to a string and parsed
        # each key: val line is converted into a dict representation
        for line in lines[1:]:
            if line is last and check_payload:
                self.header['Payload'] = line
            else:
                tmp = [x.strip() for x in line.split(':', 1)]
                if len(tmp) == 2:
                    if 'multipart/form-data' in tmp[1] and "Payload" not in self.header:
                        self.parseMultiPart()
                        return 0                    
                    self.header[tmp[0]] = tmp[1]

        self.checkData(lines[0].strip())

    def checkData(self, line):
        """Get request acion, pathname, and HTTP version from first line of a request."""
        
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
