"""Scalar — современный рендерер OpenAPI-документации с тёмной темой."""

from __future__ import annotations

from typing import Any

from litestar import Request
from litestar.openapi.plugins import OpenAPIRenderPlugin
from litestar.serialization import encode_json

TAG_GROUPS = [
    {"name": "Система", "tags": ["System"]},
    {"name": "01. Общие", "tags": ["01. API Wildberries", "01. Синхронизация", "01. База данных"]},
    {"name": "02. Товары", "tags": ["02. API Wildberries", "02. Синхронизация", "02. База данных"]},
    {"name": "03. FBS", "tags": ["03. API Wildberries", "03. Синхронизация", "03. База данных"]},
    {"name": "04. DBW (Доставка на склад WB)", "tags": ["04. API Wildberries", "04. Синхронизация", "04. База данных"]},
    {"name": "05. DBS (Доставка силами продавца)", "tags": ["05. API Wildberries", "05. Синхронизация", "05. База данных"]},
    {"name": "06. Самовывоз", "tags": ["06. API Wildberries", "06. Синхронизация", "06. База данных"]},
    {"name": "07. FBW (Склады WB)", "tags": ["07. API Wildberries", "07. Синхронизация", "07. База данных"]},
    {"name": "08. Продвижение", "tags": ["08. API Wildberries", "08. Синхронизация", "08. База данных"]},
    {"name": "09. Коммуникации", "tags": ["09. API Wildberries", "09. Синхронизация", "09. База данных"]},
    {"name": "10. Тарифы", "tags": ["10. API Wildberries", "10. Синхронизация", "10. База данных"]},
    {"name": "11. Аналитика", "tags": ["11. API Wildberries", "11. Синхронизация", "11. База данных"]},
    {"name": "12. Отчёты", "tags": ["12. API Wildberries", "12. Синхронизация", "12. База данных"]},
    {"name": "13. Финансы", "tags": ["13. API Wildberries", "13. Синхронизация", "13. База данных"]},
]


class ScalarRenderPlugin(OpenAPIRenderPlugin):
    """Render plugin that serves Scalar API Reference instead of Swagger UI."""

    def __init__(self, *, path: str = "/docs") -> None:
        super().__init__(path=path)

    def render(self, request: Request, openapi_schema: dict[str, Any]) -> bytes:
        openapi_schema["x-tagGroups"] = TAG_GROUPS

        title = openapi_schema.get("info", {}).get("title", "API Reference")
        schema_json = self.render_json(request, openapi_schema)

        html = f"""\
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
    <style>
        body {{ margin: 0; padding: 0; }}
    </style>
</head>
<body>
    <script id="api-reference" type="application/json">{schema_json.decode()}</script>
    <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {{
            Scalar.createApiReference('#api-reference', {{
                darkMode: true,
                layout: 'modern',
                defaultOpenAllTags: false,
                defaultHttpClient: {{
                    targetKey: 'python',
                    clientKey: 'requests',
                }},
                hiddenClients: [],
                theme: 'kepler',
            }});
        }});

        /* ── Сворачиваем tag-группы в sidebar ── */
        (function () {{
            var attempts = 0;

            function collapseSidebar() {{
                var asides = document.querySelectorAll('aside');
                if (asides.length === 0) {{
                    if (++attempts < 60) setTimeout(collapseSidebar, 300);
                    return;
                }}

                /* Проверяем что Scalar отрендерил контент */
                var ready = false;
                asides.forEach(function (aside) {{
                    var ul = aside.querySelector('ul');
                    if (ul && ul.querySelectorAll(':scope > li').length > 2) ready = true;
                }});

                if (!ready) {{
                    if (++attempts < 60) setTimeout(collapseSidebar, 300);
                    return;
                }}

                asides.forEach(function (aside) {{
                    var topUL = aside.querySelector('ul');
                    if (!topUL) return;

                    var sections = topUL.querySelectorAll(':scope > li');

                    sections.forEach(function (section, idx) {{
                        /* System (idx=0) — не сворачиваем */
                        if (idx === 0) return;

                        var childUL = section.querySelector(':scope > ul');
                        if (!childUL) return;

                        /* Скрываем подтеги (WB / Sync / DB) */
                        childUL.style.setProperty('display', 'none', 'important');

                        /* Заголовок группы */
                        var header = section.querySelector(
                            ':scope > div[class*="group/button"]'
                        );
                        if (!header) return;

                        header.style.cursor = 'pointer';

                        /* SVG-шеврон — точная копия Scalar size-3 в size-4 обёртке */
                        if (!header.querySelector('.wb-chevron')) {{
                            var wrap = document.createElement('div');
                            wrap.className = 'wb-chevron size-4 flex items-center justify-center';
                            wrap.style.cssText =
                                'display:flex;align-items:center;justify-content:center;'
                                + 'width:16px;height:16px;margin-left:auto;'
                                + 'transition:transform 0.1s ease;transform:rotate(0deg);';
                            wrap.innerHTML =
                                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256"'
                                + ' fill="currentColor" width="1em" height="1em"'
                                + ' aria-hidden="true" role="presentation" class="size-3">'
                                + '<g><path d="M184.49,136.49l-80,80a12,12,0,0,1-17-17L159,128,'
                                + '87.51,56.49a12,12,0,1,1,17-17l80,80A12,12,0,0,1,184.49,136.49Z">'
                                + '</path></g></svg>';
                            header.appendChild(wrap);
                        }}

                        /* Переключение по клику */
                        header.addEventListener('click', function (e) {{
                            var hidden = childUL.style.display === 'none';
                            childUL.style.setProperty(
                                'display', hidden ? 'flex' : 'none', 'important'
                            );
                            var chev = header.querySelector('.wb-chevron');
                            if (chev) chev.style.transform =
                                hidden ? 'rotate(90deg)' : 'rotate(0deg)';
                            e.stopPropagation();
                            e.preventDefault();
                        }});
                    }});
                }});
            }}

            setTimeout(collapseSidebar, 1500);
        }})();
    </script>
</body>
</html>"""
        return html.encode()
