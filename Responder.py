import logging, sys, io, re, os
from urllib.parse import parse_qs

class Responder():
    def __init__(self, request, client, name):
        """Initialize our responder with defaults."""
        self.client = client
        self.name = name
        self.request = request
        self.success = 'HTTP/{} {} OK\r\n'\
                       'Content-Type: {}\r\n'\
                       'Content-Length: {}\r\n\r\n'
        self.mime_types = {
            '.ico': 'image/x-icon',
            '.html': 'text/html',
            '.jpeg': 'image/jpeg',
            '.jpg': 'image/jpg',
            '.png': 'image/png',
            '.css': 'text/css'
        }

    def readAndSend(self, filename, version, code, mime):
        with open(filename, 'rb') as f:
            content = f.read()
        success_header = self.success.format(version,
                                            code,
                                            mime,
                                            len(content)
                                            )
        print("===RESPONSE HEADER===\n", success_header)                                            
        response = success_header.encode() + content
        self.client.sendall(response)

    def sendGET(self):
        """Send a GET request, dynamically determine type of file."""
        ext = os.path.splitext(self.request.path)[1]
        self.readAndSend(
                        self.request.path,
                        self.request.version,
                        '200',
                        self.mime_types[ext]
                        )
    
    def sendPOST(self):
        header = self.request.header
        if header['Content-Type'] == 'application/x-www-form-urlencoded':
            try:
                self.saveForm(header['Payload'])
                self.readAndSend(
                                'testfiles/success.html',
                                self.request.version,
                                '201',
                                'text/html'
                                )             
            except Exception as e:
                print(e)
                
    def saveForm(self, content):
        if len(content) > 0:
            data = parse_qs(content)
            with open('data/survey_log.txt', 'a') as f:
                f.write("CLIENT: {}\n".format(self.name))
                for key, val in data.items():
                    f.write("\t {}: {}\n".format(key, val[0]))
                f.write("="*50 + "\n")

    def sendError(self, code):
        """
        400 - Bad Request
        403 - Forbidden
        404 - File not found
        408 - Request timeout
        500 - Internal Server Error ?
        """

