import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import http
def serverHtpp(hosts="127.0.0.1", port=8000, data="<h1>hola, este es mi server</h1>"):
    try:
        print("\n\n\n\nserver abierto en el host: " + str(hosts) + "\npor el puerto: " + str(port) + "\n\aurl para ti: http://" +str(hosts) + ":" + str(port)+"\n")
        print('Servidor iniciado, usa <Ctrl-C> para parar el servidor.\n')
        try:
            file = open(str(data), "r")
            data = file.read()
            file.close()
        except FileNotFoundError:
            print('no se pudo abrir el archivo por que no existe.')
            data="<h1>hola, este es mi server</h1>"
        print('el contenido de tu archivo es: \n'+data)

        class S(BaseHTTPRequestHandler):
            def _set_response(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

            def do_GET(self):
                logging.info("Solicitud GET,\nPath: %s\nHeaders:\n%s\n", str(
                    self.path), str(self.headers))
                self._set_response()
                self.wfile.write(str(data).format(self.path).encode('utf-8'))

            def do_POST(self):
                # <--- Gets the size of data
                content_length = int(self.headers['Content-Length'])
                # <--- Gets the data itself
                post_data = self.rfile.read(content_length)
                logging.info("solicitud POST,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(
                    self.path), str(self.headers), post_data.decode('utf-8'))
                self._set_response()
                self.wfile.write("Solicitud POST para {}".format(
                    self.path).encode('utf-8'))
        try:
            def run(hosts, port, server_class=HTTPServer, handler_class=S):
                logging.basicConfig(level=logging.INFO)
                server_address = (str(hosts), int(port))
                httpd = server_class(server_address, handler_class)
                logging.info('server Http iniciado...\n')
                try:
                    httpd.serve_forever()
                except:
                    httpd.server_close()
                logging.info('Stopping httpd...\n')

                # server.serve_forever()
        except:
            print('server cerrado.')
        hilo1 = threading.Thread(target=run(hosts, port))
        hilo1.setDaemon(True)
        hilo1.start()

    except KeyboardInterrupt:
        httpd.server_close()
        
        print("server finalizado")
        
serverHtpp(str(input('hoste el que abrir el server: ')), int(input('puerto en el que abrir el server: ')), str(input('archivo php o html: ')))
