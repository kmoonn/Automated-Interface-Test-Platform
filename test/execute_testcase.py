import requests

case_data = {
    'method': 'GET',
    'protocol': 'http',
    'host': '127.0.0.1',
    'port': 5000,
    'path': 'api/case',
    'params': {
        'type': 'query_detail',
        'id': 3,
    },
    'headers': {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    },
    'body': None,
    'predict': ''
}

method = case_data['method']
protocol = case_data['protocol']
host = case_data['host']
port = case_data['port']
path = case_data['path']
params = case_data['params']
headers = case_data['headers']
payload = case_data['body']
predict = case_data['predict']

url = f'{protocol}://{host}:{port}/{path}'

response = requests.request(method=method, url=url, params=params, headers=headers, json=payload)

print(response.json())
