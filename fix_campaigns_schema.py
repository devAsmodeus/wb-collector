import re

path = r'C:\Python\wb-collector\src\schemas\promotion\campaigns.py'
content = open(path, encoding='utf-8').read()

# Find AdvertCountItem class and add fields before it
insert_before = 'class AdvertCountItem(BaseModel):'
new_class = '''class AdvertListItem(BaseModel):
    """Single campaign entry from advert_list."""
    advertId: int | None = Field(None)
    changeTime: str | None = Field(None)


'''

content = content.replace(insert_before, new_class + insert_before, 1)

# Add type and advert_list fields to AdvertCountItem
# Find the count field line and add after it
content = re.sub(
    r'(    count: int \| None = Field\(None[^\n]*\n)',
    r'\1    type: int | None = Field(None)\n    advert_list: list[AdvertListItem] | None = Field(None)\n',
    content,
    count=1
)

open(path, 'w', encoding='utf-8').write(content)
print('Done')
for i, line in enumerate(open(path, encoding='utf-8').readlines()[:25], 1):
    print(f"{i}: {line}", end='')
