#!/usr/common/env python3
# -*- coding: utf-8 -*-
#
# describe:
# author: cg
# time: 2018-12-03 19:20


from http.server import HTTPServer, BaseHTTPRequestHandler

# HTTPServer--> socketserver.TCPServer--> socketserver.BaseServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')


intPort = 8000
httpd = HTTPServer(('localhost', intPort), SimpleHTTPRequestHandler)
print('server is running: http://127.0.0.1:' + str(intPort))
httpd.serve_forever()

