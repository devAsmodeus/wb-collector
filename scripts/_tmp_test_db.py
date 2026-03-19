import urllib.request

try:
    req = urllib.request.Request("http://localhost:8000/db/general/news/", method="GET")
    with urllib.request.urlopen(req, timeout=5) as r:
        print(r.status, r.read().decode())
except Exception as e:
    body = e.read().decode() if hasattr(e, 'read') else str(e)
    print("ERROR:", body)
