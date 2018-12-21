#!/usr/bin/env python3

import http.server
import socketserver
import sys
import cgi
import os
import stat

PORT = int(sys.argv[1])
# La carpeta donde se subiran los ficheros
FOLDER = sys.argv[2]
# La carpeta donde estan los ficheros HTML
HTML = sys.argv[3]
try:
    os.makedirs(FOLDER)
except:
    pass

class RetrodiosaServer(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print("GET " + self.path)
        if (self.path == '/') or (self.path == '/peticion.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/HTML; charset=utf-8')
            self.end_headers()
            with open(os.path.join(HTML, "peticion.html"), "rb") as fichero:
                self.wfile.write(fichero.read())
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        print("POST " + self.path)
        print(self.headers)
        if (self.path == '/subida.html'):
            ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
            pdict['boundary'] = pdict['boundary'].encode('latin1')
            pdict['CONTENT-LENGTH'] = self.headers['Content-Length']
            ficheros = cgi.parse_multipart(self.rfile, pdict)
            self.send_response(200)
            self.send_header('Content-type', 'text/HTML; charset=utf-8')
            self.end_headers()
            with open(os.path.join(HTML, "enviado.html"), "rb") as fichero:
                self.wfile.write(fichero.read())
            try:
                nombre = ficheros["nombre"][0].decode("utf-8")
            except:
                nombre = ficheros["nombre"][0]
            with open(os.path.join(FOLDER, nombre + ".jar"), "wb") as fichero:
                fichero.write(ficheros["juego"][0])
            with open(os.path.join(FOLDER, nombre + ".json"), "wb") as fichero:
                fichero.write(ficheros["json"][0])
            with open(os.path.join(FOLDER, nombre + ".sh"), "wb") as fichero:
                script = """#!/bin/bash
/opt/retropie/supplementary/runcommand/runcommand.sh 0 "bash /opt/retropie/supplementary/runcommand/run_libgdx_game.sh {:s} {:s}" "{:s}"
""".format(os.path.join(FOLDER, nombre + ".jar"), os.path.join(FOLDER, nombre + ".json"), nombre)
                fichero.write(script.encode("utf-8"))
            os.chmod(os.path.join(FOLDER, nombre + ".sh"), stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            return
        self.send_response(404)
        self.end_headers()

server_address = ('', PORT)
httpd = socketserver.TCPServer(server_address, RetrodiosaServer)
httpd.serve_forever()
