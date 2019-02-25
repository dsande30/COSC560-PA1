import logging, sys, io, re

class Responder():
    def __init__(self, request):
        if (request.error_code != 200):
            self.sendError(request.error_code)
        self.request = request
    
    def sendGET(self):
        return 0
    
    def sendPOST(self):
        return 0
    
    def sendError(self, code):
        """
        400 - Bad Request
        404 - File not found
        408 - Request timeout
        500 - Internal Server Error ?
        """

