import sys
import ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Paths to the certificate and key files
SERVER_CERT = 'server.pem'
SERVER_KEY  = 'server.key'
CLIENT_CERT = 'client.pem'
#CA_CERT = 'ca.pem'

def create_ssl_context(mutual):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    if(mutual == True):
        print("--> Running server with mutual authentication")
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=CLIENT_CERT)    
    context.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
    #context.load_verify_locations(cafile=CA_CERT)
    return context

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, SSL client!")

def run_server(mutual, server_class=HTTPServer, handler_class=MyHandler, host='127.0.0.1', port=4443):
#def run_server(server_class=HTTPServer, handler_class=MyHandler, host='htrServer', port=4443):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    context = create_ssl_context(mutual)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print(f'Server listening on https://{host}:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    mutual = False
    arg_len = len(sys.argv)
    if arg_len != 1 and arg_len != 2:
        print("Usage:\n" + sys.argv[0] + " [mutual]")
        sys.exit(1)
    if arg_len == 2:
        if(sys.argv[1] == "mutual"):
            mutual = True
        else:
            print("Error: Unknown parameter: " + sys.argv[1])
            print("Usage:\n" + sys.argv[0] + " [mutual]")
            sys.exit(1)
    run_server(mutual)