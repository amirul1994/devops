base64 encoding and decoding example

echo -n 'mysql' | base64

echo -n 'bXlzcWw=' | base64 --decode

all the credentials has been encoded into base64 

imperative way to create a secret

kubectl create secret generic my-db-secret --from-literal=DB_Host=mysql --from-literal=DB_User=root --from-literal=DB_Password=paswrd


the type field in a Secret resource specifies the type of the secret. The type helps Kubernetes understand how to interpret the data in the secret and can be used by applications or other Kubernetes components to handle the secret appropriately

Opaque: This is the most common type and is used for generic secrets. It allows you to store any key-value pairs, where the values are base64-encoded.

Other Types: Kubernetes supports other predefined secret types like, kubernetes.io/basic-auth for http basic authetication, kubernetes.io/tls for TLS certificates, kubernetes.io/dockerconfigjson for Docker registry credentials, and more. Each type has a specific structure and purpose.
