import requests

try:
    res = requests.post('http://localhost:8000/api/v1/scan/url', json={'url': 'http://localhost:3005/'})
    print('STATUS:', res.status_code)
    print('RESPONSE:', res.text)
except Exception as e:
    print('ERROR:', str(e))
