import ssl
import urllib.request

# Paths to the certificate and key files
CLIENT_CERT = 'client.pem'
CLIENT_KEY  = 'client.key'
SERVER_CERT = 'server.pem'
#CA_CERT = 'ca.pem'

def create_ssl_context():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    #context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    #context.load_verify_locations(cafile=SERVER_CERT)    
    #context.load_verify_locations(cafile=CA_CERT)
    context.load_verify_locations(cafile=SERVER_CERT)
    return context

def fetch_secure_url(url):
    context = create_ssl_context()
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request, context=context) as response:
        print(f"Response status: {response.status}")
        print(response.read().decode('utf-8'))

if __name__ == "__main__":
    url = "https://server.acme.com:4443"
    fetch_secure_url(url)
