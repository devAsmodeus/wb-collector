import traceback, logging, json
logging.disable(logging.CRITICAL)

from litestar import Litestar, Router
from litestar.openapi import OpenAPIConfig
from src.api.products.directories import DirectoriesController
from src.api.products.tags import TagsController

router = Router(path="/products", route_handlers=[DirectoriesController, TagsController])
app = Litestar(
    route_handlers=[router],
    openapi_config=OpenAPIConfig(title="T", version="0.1", path="/docs"),
)

schema = app.openapi_schema
print("Schema paths:", list(schema.paths.keys()))

# Пробуем сериализовать
try:
    schema_dict = schema.to_schema()
    serialized = json.dumps(schema_dict)
    print("JSON serialization OK, size:", len(serialized))
except Exception:
    print("Serialization ERROR:")
    traceback.print_exc()
