# Install pyjwt if you have Python on your workstation
pip3 install pyjwt

# Generate a test token
python3 -c "
import jwt, base64, json, subprocess

# Get the secret from K8s
result = subprocess.run(
  ['kubectl', 'get', 'secret', 'jwt-secret', '-n', 'production',
   '-o', 'jsonpath={.data.jwksFile}'],
  capture_output=True, text=True
)
jwks = json.loads(base64.b64decode(result.stdout))
key = base64.urlsafe_b64decode(jwks['keys'][0]['k'] + '==')

token = jwt.encode({'sub': 'jeremy', 'role': 'admin'}, key, algorithm='HS256')
print(f'Token: {token}')
"