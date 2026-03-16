import yaml

with open("C:/Python/wb-collector/docs/api/01-general.yaml", encoding="utf-8") as f:
    d = yaml.safe_load(f)

top_servers = [s["url"] for s in d.get("servers", [])]
print(f"Top-level servers: {top_servers}")

for path, methods in d["paths"].items():
    for method, spec in methods.items():
        if method not in ("get", "post", "put", "patch", "delete"):
            continue
        path_servers = [s["url"] for s in spec.get("servers", [])]
        host = path_servers[0] if path_servers else (top_servers[0] if top_servers else "common-api.wildberries.ru")
        print(f"{method.upper():<6} {host}{path}")
