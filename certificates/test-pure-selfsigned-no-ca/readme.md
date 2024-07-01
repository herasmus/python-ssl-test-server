


# Certificate generation - selfsigned without CA
	
## 1) Creating test server key and certicate
#### Generate key and certificate

	# Generate a private key for the server
	openssl genpkey -algorithm RSA -out server.key

	# Create a server certificate
	openssl req -new -x509 -key server.key -out server.pem -days 365 -subj "/C=US/ST=California/L=San Francisco/O=MyCompany/OU=MyDepartment/CN=server.acme.com"

## 2) Creating a client key and certicate
#### Commands

	# Generate a private key for the client
	openssl genpkey -algorithm RSA -out client.key

	# Create a cleint certificate
	openssl req -new -x509 -key client.key -out client.pem -days 365 -subj "/C=US/ST=California/L=San Francisco/O=MyCompany/OU=MyDepartment/CN=client.acme.com

