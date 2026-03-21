"""
Проверка дрейфа схем: YAML → Pydantic → ORM (SQLAlchemy).

Логика:
  - Берём семантический снимок из manifest.json (поля схем)
  - Сканируем src/schemas/**/*.py — собираем Pydantic-поля
  - Сканируем src/models/**/*.py — собираем ORM-колонки
  - Выводим расхождения
"""
import ast
import json
from pathlib import Path

REPO_DIR      = Path(__file__).parent.parent.parent
MANIFEST_PATH = REPO_DIR / "docs" / "api" / "manifest.json"
SCHEMAS_DIR   = REPO_DIR / "src" / "schemas"
MODELS_DIR    = REPO_DIR / "src" / "models"


# ─── Чтение манифеста ────────────────────────────────────────────────────────

def load_yaml_fields() -> dict[str, set[str]]:
    """
    Возвращает {schema_name: {field1, field2, ...}} из manifest.json.
    Объединяет схемы со всех 13 файлов.
    """
    if not MANIFEST_PATH.exists():
        return {}
    raw   = json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))
    files = raw.get("files", [])
    if isinstance(files, dict):
        files = list(files.values())

    result: dict[str, set[str]] = {}
    for entry in files:
        for schema_name, fields in entry.get("semantics", {}).get("schemas", {}).items():
            # Нормализуем: models.Supply → Supply
            short_name = schema_name.split(".")[-1]
            result.setdefault(short_name, set()).update(fields)
    return result


# ─── Сканирование Pydantic схем ──────────────────────────────────────────────

def _parse_pydantic_class(node: ast.ClassDef) -> set[str]:
    """Извлекает имена полей из Pydantic BaseModel класса."""
    fields = set()
    for item in node.body:
        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
            fields.add(item.target.id)
    return fields


def load_pydantic_fields() -> dict[str, set[str]]:
    """
    Сканирует src/schemas/**/*.py.
    Возвращает {ClassName: {field1, field2, ...}}.
    """
    result: dict[str, set[str]] = {}
    for py_file in SCHEMAS_DIR.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                fields = _parse_pydantic_class(node)
                if fields:
                    result[node.name] = fields
    return result


# ─── Сканирование ORM моделей ─────────────────────────────────────────────────

def load_orm_fields() -> dict[str, set[str]]:
    """
    Сканирует src/models/**/*.py.
    Возвращает {TableName: {column1, column2, ...}}.
    """
    result: dict[str, set[str]] = {}
    for py_file in MODELS_DIR.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                fields = set()
                for item in node.body:
                    # Mapped[...] аннотации
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        name = item.target.id
                        # Пропускаем служебные: id, fetched_at, __tablename__
                        if not name.startswith("_"):
                            fields.add(name)
                if fields:
                    result[node.name] = fields
    return result


# ─── Сравнение ───────────────────────────────────────────────────────────────

def check_drift() -> dict:
    """
    Сравнивает три слоя. Возвращает отчёт о расхождениях.
    """
    yaml_schemas    = load_yaml_fields()
    pydantic_fields = load_pydantic_fields()
    orm_fields      = load_orm_fields()

    issues = []

    # YAML схемы с именами похожими на наши Pydantic классы
    for yaml_name, yaml_flds in yaml_schemas.items():
        # Ищем совпадение в Pydantic (по имени или частичному совпадению)
        pydantic_match = None
        for cls_name in pydantic_fields:
            if cls_name.lower() == yaml_name.lower() or yaml_name.lower() in cls_name.lower():
                pydantic_match = cls_name
                break

        if pydantic_match:
            pydantic_flds = pydantic_fields[pydantic_match]
            missing_in_pydantic = yaml_flds - pydantic_flds
            extra_in_pydantic   = pydantic_flds - yaml_flds
            if missing_in_pydantic or extra_in_pydantic:
                issues.append({
                    "layer":              "yaml→pydantic",
                    "yaml_schema":        yaml_name,
                    "pydantic_class":     pydantic_match,
                    "missing_in_code":    sorted(missing_in_pydantic),
                    "extra_in_code":      sorted(extra_in_pydantic),
                })

    # Pydantic vs ORM — для каждого ORM класса ищем Pydantic аналог
    for orm_name, orm_flds in orm_fields.items():
        pydantic_match = None
        for cls_name in pydantic_fields:
            # ORM: FbsOrder → Pydantic: Order, FBSOrder, etc.
            if cls_name.lower().replace("orm", "") == orm_name.lower().replace("orm", ""):
                pydantic_match = cls_name
                break

        if pydantic_match:
            pydantic_flds = pydantic_fields[pydantic_match]
            # Нормализуем ORM поля — убираем служебные
            skip = {"id", "fetched_at"}
            orm_clean      = {f for f in orm_flds if f not in skip}
            missing_in_orm = pydantic_flds - orm_clean - skip
            if missing_in_orm:
                issues.append({
                    "layer":          "pydantic→orm",
                    "pydantic_class": pydantic_match,
                    "orm_class":      orm_name,
                    "missing_in_orm": sorted(missing_in_orm),
                })

    return {
        "yaml_schemas":    len(yaml_schemas),
        "pydantic_classes": len(pydantic_fields),
        "orm_classes":     len(orm_fields),
        "issues":          issues,
        "issues_count":    len(issues),
    }
