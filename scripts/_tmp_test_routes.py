import urllib.request, json

routes = [
    ("GET", "http://localhost:8000/health"),
    ("GET", "http://localhost:8000/wb/general/ping/"),
    ("GET", "http://localhost:8000/db/general/news/"),
]

for method, url in routes:
    try:
        req = urllib.request.Request(url, method=method)
        with urllib.request.urlopen(req, timeout=5) as r:
            print(f"{r.status} {method} {url}")
    except Exception as e:
        print(f"ERR {method} {url} -> {e}")
