import logging, sys, io, re

class Responder():
    def __init__(self, request, client):
        self.client = client
        self.request = request
        self.success = 'HTTP/1.1 200 OK\r\n '\
                       'Content-Type: text/html\r\n '\
                       'Content-Length: {}\r\n\r\n'
    
    def sendGET(self):
        with open(self.request.path, 'r') as f:
            content = f.read()
        success_header = self.success.format(len(content))
        response = success_header + content
        print(response)
        self.client.sendall(response.encode())
    
    def sendPOST(self):
        return 0
    
    def sendError(self, code):
        """
        400 - Bad Request
        403 - Forbidden
        404 - File not found
        408 - Request timeout
        500 - Internal Server Error ?
        """

