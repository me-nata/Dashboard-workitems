import urllib.request
import json

def GET(url, headers):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            status_code = response.status
            if status_code == 200:
                return json.loads(response.read().decode())
            else:
                return None
    except Exception as e:
        print(f"GET request failed: {e}")
        return None

def POST(url, json_data, headers):
    try:
        data = json.dumps(json_data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            status_code = response.status
            if status_code == 200:
                return json.loads(response.read().decode())
            else:
                return None
    except Exception as e:
        print(f"POST request failed: {e}")
        return None
