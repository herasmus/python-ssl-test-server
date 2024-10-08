import sys
import ssl
import urllib.request

# Paths to the certificate and key files
CLIENT_CERT = 'client.pem'
CLIENT_KEY  = 'client.key'
SERVER_CERT = 'server.pem'
#CA_CERT = 'ca.pem'

def create_ssl_context(mutual):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_verify_locations(cafile=SERVER_CERT)
    if(mutual == True):
        context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    #context.load_verify_locations(cafile=CA_CERT)
    return context

def fetch_secure_url(url, mutual):
    context = create_ssl_context(mutual)
    request = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(request, context=context) as response:
            print(f"Response status: {response.status}")
            print(response.read().decode('utf-8'))
    except ssl.SSLError as e:
        print(f"SSL Error: ({e})")
    except Exception as e:
        print(f"Unexpected Error: ({e})")

if __name__ == "__main__":
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

    url = "https://server.acme.com:4443"
    fetch_secure_url(url, mutual)