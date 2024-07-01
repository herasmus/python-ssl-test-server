


# Input used in certificate generation

## 1) Creating test test Certificate Authoriry
#### Generate key and certificate

    # Generate a private key for the CA
	openssl genpkey -algorithm RSA -out ca.key
	
	# Create a self-signed CA certificate
    openssl req -new -x509 -key ca.key -out ca.pem -days 365
	
#### Input
	Country Name (2 letter code) [AU]:DK
	State or Province Name (full name) [Some-State]:Denmark
	Locality Name (eg, city) []:Albertslund
	Organization Name (eg, company) [Internet Widgits Pty Ltd]:Acme Inc
	Organizational Unit Name (eg, section) []:Development
	Common Name (e.g. server FQDN or YOUR name) []:htrCA
	Email Address []:htr@acme.com
	
## 2) Creating test server key and certicate
#### Generate key and certificate

	# Generate a private key for the server
	openssl genpkey -algorithm RSA -out server.key

	# Create a certificate signing request (CSR)
	openssl req -new -key server.key -out server.csr
	

#### Input
	Country Name (2 letter code) [AU]:DK
	State or Province Name (full name) [Some-State]:Denmark
	Locality Name (eg, city) []:Albertslund
	Organization Name (eg, company) [Internet Widgits Pty Ltd]:Acme Inc
	Organizational Unit Name (eg, section) []:Development
	Common Name (e.g. server FQDN or YOUR name) []:htrServer
	Email Address []:htr@acme.com

	Please enter the following 'extra' attributes
	to be sent with your certificate request
	A challenge password []:hansemand
	An optional company name []:Acme Inc	
	
#### Sign the server CSR with the CA certificate:	
	openssl x509 -req -in server.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out server.pem -days 365

## 3) Creating a client key and certicate
#### Commands

	# Generate a private key for the client
	openssl genpkey -algorithm RSA -out client.key

	# Create a certificate signing request (CSR)
	openssl req -new -key client.key -out client.csr	

#### Input
	Country Name (2 letter code) [AU]:DK	
	State or Province Name (full name) [Some-State]:Denmark
	Locality Name (eg, city) []:Albertslund
	Organization Name (eg, company) [Internet Widgits Pty Ltd]:Acme Inc
	Organizational Unit Name (eg, section) []:Development
	Common Name (e.g. server FQDN or YOUR name) []:htrClient
	Email Address []:htr@acme.com

	Please enter the following 'extra' attributes
	to be sent with your certificate request
	A challenge password []:hansemand
	An optional company name []:Acme Inc


#### Sign the client CSR with the CA certificate:

