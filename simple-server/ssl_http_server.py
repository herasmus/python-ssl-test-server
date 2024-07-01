from http.server import HTTPServer, SimpleHTTPRequestHandler
import ssl

# Paths to the certificate and key files
SERVER_CERT = 'server.pem'
SERVER_KEY = 'server.key'
#CA_CERT = 'ca.pem'

def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    #context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
    #context.load_verify_locations(cafile=CA_CERT)
    return context

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, SSL client!")

def run_server(server_class=HTTPServer, handler_class=MyHandler, host='127.0.0.1', port=4443):
#def run_server(server_class=HTTPServer, handler_class=MyHandler, host='htrServer', port=4443):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    context = create_ssl_context()
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print(f'Server listening on https://{host}:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()