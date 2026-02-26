import json
import os
from urllib.request import urlopen
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

class Auth0Validator:
    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.audience = os.getenv("AUTH0_AUDIENCE")
        self.algorithms = ["RS256"]
        self.jwks_url = f"https://{self.domain}/.well-known/jwks.json"

    def __call__(self, auth: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        token = auth.credentials
        try:
            # 1. Obtener el kid del header
            header = jwt.get_unverified_header(token)
            kid = header.get("kid")

            # 2. Obtener las llaves de Auth0
            with urlopen(self.jwks_url) as response:
                jwks = json.loads(response.read())

            # 3. Buscar la llave y extraer el certificado x5c
            # Auth0 siempre envía el 'x5c' que es el certificado público.
            cert = None
            for key in jwks["keys"]:
                if key["kid"] == kid:
                    # El certificado viene en x5c como una lista de strings
                    cert = "-----BEGIN CERTIFICATE-----\n" + key["x5c"][0] + "\n-----END CERTIFICATE-----"
                    break

            if cert is None:
                raise Exception("No se encontró la llave pública para el 'kid' proporcionado.")

            # 4. Extraer la llave pública del certificado
            # Esto es mucho más seguro que armar la llave con 'n' y 'e'
            public_key = load_pem_x509_certificate(cert.encode(), default_backend()).public_key()

            # 5. Validar
            payload = jwt.decode(
                token,
                public_key, # Usamos el objeto de llave pública real
                algorithms=self.algorithms,
                audience=self.audience,
                issuer=f"https://{self.domain}/"
            )
            return payload

        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=f"Firma inválida o error de validación: {str(e)}"
            )
# Instanciamos el validador
auth_scheme = Auth0Validator()