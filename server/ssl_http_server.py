import os
import ssl
import threading
import argparse
from socketserver import ThreadingMixIn

import keyboard
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def validate_filepath(filepath):
    if os.path.exists(filepath):
        return True
    else:
        logger.error(f"The path '{filepath}' does not exist.")
        return False


def validate_filepaths(args):
    res1 = validate_filepath(args.server_cert)
    res2 = validate_filepath(args.server_key)
    if args.ca_locations:
        res3 = validate_filepath(args.ca_locations)    
    else:
        res3 = True
    if not (res1 and res2 and res3):
        print("Error: Missing file(s)")
        exit(0)


def create_ssl_context(args):
    validate_filepaths(args)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    if args.client_cert:
        print("\n--> Running server with mutual authentication")
        context.verify_mode = ssl.CERT_REQUIRED
    if args.ca_locations:        
        print("\n--> CA locations: " + str(args.ca_locations) + "\n")        
        context.load_verify_locations(cafile=args.ca_locations)        
    context.load_cert_chain(certfile=args.server_cert, keyfile=args.server_key)
    return context


class MyHandler(SimpleHTTPRequestHandler):
    def handle_one_request(self):
        try:
            super().handle_one_request()
        except ssl.SSLError as ssl_error:
            logger.error(f"SSL error during request handling: {ssl_error}")
        except Exception as e:
            logger.error(f"Error during request handling: {e}")

    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Hello, SSL client!")
        except ssl.SSLError as ssl_error:
            logger.error(f"SSL error during request handling: {ssl_error}")
        except Exception as e:
            logger.error(f"Error during request handling: {e}")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

    def get_request(self):
        try:
            request, client_address = super().get_request()
            logger.info(f"Connection from {client_address}")
            return request, client_address
        except ssl.SSLError as ssl_error:
            logger.error(f"SSL error during get_request: {ssl_error}")
            raise
        except Exception as e:
            logger.error(f"Error during get_request: {e}")
            raise

    def process_request(self, request, client_address):
        try:
            super().process_request(request, client_address)
        except ssl.SSLError as ssl_error:
            logger.error(f"SSL error during process_request: {ssl_error}")
        except Exception as e:
            logger.error(f"Error during process_request: {e}")

def start_http_server(httpd):
    try:
        httpd.serve_forever()
    except Exception as e:
        logger.error(f"Server error: {e}")


def run_server(args, server_class=ThreadedHTTPServer, handler_class=MyHandler):
    server_address = (args.host, args.port)
    httpd = server_class(server_address, handler_class)
    context = create_ssl_context(args)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print(f'Server listening on https://{args.host}:{args.port}')
    print("--------------------------------------------")
    print('Press esc to exit')
    logger.error("Logging working")	

    # Create a daemon thread
    daemon_thread = threading.Thread(target=start_http_server, args=(httpd,))
    daemon_thread.daemon = True  # Set the thread as a daemon thread
    daemon_thread.start()
     
    keyboard.wait('esc')  # Press 'esc' to exit the program
    print('goodbye')


def configure_arg_parser():
    parser = argparse.ArgumentParser(description='Simple HTTP SSL server intended for SSL debugging')
    parser.add_argument('--host', default='127.0.0.1', help='Host address. Default = 127.0.0.1')
    parser.add_argument('--port', type=int, default=4443, help='Port number.  Default = 4443')
    parser.add_argument('server_cert', type=str, help='Server certificate')
    parser.add_argument('server_key', type=str, help='Server key')
    parser.add_argument('--client_cert', action='store_true', help='Client authentication enforced if present')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')    
    parser.add_argument('--ca_locations', type=str, help='List of ca-locations')
    return parser


if __name__ == '__main__':
    arg_parser = configure_arg_parser()
    run_server(arg_parser.parse_args())