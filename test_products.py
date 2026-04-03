import urllib.request, json, time

BASE = "http://localhost:8080"

tests = [
    # WB proxy
    ("POST", "/products/wb/cards/",          {"settings": {"cursor": {"limit": 5}}}),
    ("GET",  "/products/wb/cards/limits",     None),
    ("GET",  "/products/wb/cards/errors",     None),
    ("GET",  "/products/wb/offices/",         None),
    ("GET",  "/products/wb/warehouses/",      None),
    ("GET",  "/products/wb/prices/goods",     None),
    ("GET",  "/products/wb/directories/categories", None),
    ("GET",  "/products/wb/directories/subjects",   None),
    ("GET",  "/products/wb/tags/",            None),
    # Sync
    ("POST", "/products/sync/cards/full",     None),
    ("POST", "/products/sync/prices/full",    None),
    ("POST", "/products/sync/tags/full",      None),
    ("POST", "/products/sync/warehouses/full", None),
    # DB
    ("GET",  "/products/db/cards/",           None),
    ("GET",  "/products/db/prices/",          None),
    ("GET",  "/products/db/tags/",            None),
    ("GET",  "/products/db/warehouses/",      None),
    ("GET",  "/products/db/directories/categories", None),
    ("GET",  "/products/db/directories/subjects",   None),
]

for method, path, body in tests:
    try:
        url = BASE + path
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, method=method,
                                     headers={"Content-Type": "application/json"} if data else {})
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.loads(r.read())
            if isinstance(resp, dict):
                total = resp.get("total") or resp.get("synced") or len(resp.get("data", resp.get("cards", [])))
                print(f"OK  {method} {path} [total={total}]")
            else:
                print(f"OK  {method} {path} [{type(resp).__name__}]")
    except urllib.error.HTTPError as e:
        print(f"ERR {method} {path} [{e.code}]")
    except Exception as e:
        print(f"ERR {method} {path} [{e.__class__.__name__}: {str(e)[:50]}]")
