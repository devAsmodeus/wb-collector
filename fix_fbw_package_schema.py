with open('/app/src/schemas/fbw/supplies.py') as f:
    content = f.read()

old = '''class FBWPackageQR(BaseModel):
    """QR-код для упаковки поставки FBW."""
    file: str | None = Field(None, description="QR-код в формате base64")
    type: str | None = Field(None, description="Формат QR-кода: `svg` или `zplLabel`")'''

new = '''class FBWPackageQRItem(BaseModel):
    """Один QR-код в упаковке поставки FBW."""
    file: str | None = Field(None, description="QR-код в формате base64")
    type: str | None = Field(None, description="Формат QR-кода: svg или zplLabel")


class FBWPackageQR(BaseModel):
    """QR-коды для упаковки поставки FBW. WB возвращает массив или пустой список."""
    items: list[FBWPackageQRItem] = Field(default=[], description="Список QR-кодов")

    @classmethod
    def model_validate(cls, obj, **kwargs):
        # WB returns [] or [{file, type}, ...]
        if isinstance(obj, list):
            return cls(items=[FBWPackageQRItem(**i) if isinstance(i, dict) else i for i in obj])
        if isinstance(obj, dict):
            if "file" in obj or "type" in obj:
                return cls(items=[FBWPackageQRItem(**obj)])
        return super().model_validate(obj, **kwargs)'''

if old in content:
    content = content.replace(old, new)
    with open('/app/src/schemas/fbw/supplies.py', 'w') as f:
        f.write(content)
    print("Fixed FBWPackageQR schema")
else:
    print("Not found")
