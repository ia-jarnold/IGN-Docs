########################san.conf example###########################
#[req]
#default_bits  = 2048
#distinguished_name = req_distinguished_name
#req_extensions = req_ext
#x509_extensions = v3_req
#prompt = no
#[req_distinguished_name]
#countryName = US 
#stateOrProvinceName = California 
#localityName = Folsom 
#organizationName = Inductive 
#commonName = Ignition OPC Ua V2 
#[req_ext]
#subjectAltName = @alt_names
#[v3_req]
#subjectAltName = @alt_names
#[alt_names]
#IP.1 = 127.0.0.1
#IP.2 = 192.168.153.156
#DNS.1 = DESKTOP-39PKKLT.localdomain
#
# Save above to san.conf for below
#
## Generate .PEM key and certs with san config.
openssl req -x509 -nodes -days 730 -newkey rsa:2048 -keyout key.pem -out cert.pem -config san.conf

# Print the cert
openssl x509 -in cert.pem -text -noout

# conver to der to match usually
openssl x509 -in cert.pem -out cert.der -outform DER
