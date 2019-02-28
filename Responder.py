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
            '.css': 'text/css',
            '.csv': 'text',
            '.txt': 'text',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'
        }

    def readAndSend(self, filename, version, code, mime):
        if filename in ['/dir', '/uploads']:
            content = self.payload.encode()
        else:
            with open(filename, 'rb') as f:
                content = f.read()
        success_header = self.success.format(version,
                                            code,
                                            mime,
                                            len(content)
                                            )                                           
        response = success_header.encode() + content
        self.client.sendall(response)

    def sendGET(self):
        """Send a GET request, dynamically determine type of file."""
        if self.request.path == '/dir':
            self.payload = self.generate_tree('./site')
            self.readAndSend(
                            self.request.path,
                            self.request.version,
                            '200',
                            self.mime_types['.html']
                            )
        elif self.request.path == '/uploads':
            self.payload = self.generate_tree('./site/uploads')
            self.readAndSend(
                            self.request.path,
                            self.request.version,
                            '200',
                            self.mime_types['.html']
                            )
        else:            
            ext = os.path.splitext(self.request.path)[1].lower()
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
                                'site/success.html',
                                self.request.version,
                                '201',
                                'text/html'
                                )             
            except Exception as e:
                print(e)
        elif 'multipart/form-data' in header['Content-Type']:
            try:
                with open(self.request.path, 'wb') as f:
                    f.write(self.request.header['Payload'])
                self.readAndSend(
                                'site/success.html',
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

    def generate_tree(self, path):
        html = '<html><head><title>Directory Listing</title></head><body style="text-align:center;">'
        for root, dirs, files in os.walk(path, topdown=True):
            html += '<h1 style="text-align:center;">Directory Listing of {}</h1>'.format(root)
            if 'uploads' not in dirs:
                html += '<p>*We only allow downloading of the following mime types: '\
                        '.ico, .html, .jpeg, .jpg, .png, .css, .csv, .txt, .xls, .xlsx, .pdf, .doc, .docx, .pptx '\
                        '</p>'
            html += '<table border="1" style="width:50%;text-align:center;margin-left:auto;margin-right:auto"> '\
                    '<tr><th>File</th><th>Size</th></tr>'
            if 'uploads' in dirs:
                html += '<tr><td><a href="/uploads"><strong>uploads/</strong></a></td>'
            dirs[:] = [d for d in dirs if d != 'uploads']

            for f in sorted(files):
                ext = os.path.splitext(f)[1].lower()
                if ext in self.mime_types.keys():
                    name = root + os.path.sep + f
                    size = os.path.getsize(name)
                    if root == './site':
                        name = f
                    else:
                        name = 'uploads/' + f
                    if f != 'success.html':
                        html += '<tr><td><a href="{}"><strong>{}</strong></a></td>'.format(name, f)
                        html += '<td><strong>{}</strong> Bytes</td></tr>'.format(size)
        html += '</table><br><a href="./index.html">Back to Index</a></body></html>'
        return html

    def sendError(self, code):
        """
        400 - Bad Request
        403 - Forbidden
        404 - File not found
        408 - Request timeout
        500 - Internal Server Error ?
        """

