revision_file = None
import os
for f in os.listdir('/app/src/migrations/versions'):
    if 'fix_dbw_orders_missing_fields' in f:
        revision_file = f'/app/src/migrations/versions/{f}'
        break

print(f"Found: {revision_file}")

migration_body = '''
def upgrade() -> None:
    op.execute("ALTER TABLE dbw_orders ADD COLUMN IF NOT EXISTS converted_currency_code INTEGER")
    op.execute("ALTER TABLE dbw_orders ADD COLUMN IF NOT EXISTS group_id VARCHAR(50)")
    op.execute("ALTER TABLE dbw_orders ADD COLUMN IF NOT EXISTS comment VARCHAR(500)")
    op.execute("ALTER TABLE dbw_orders ADD COLUMN IF NOT EXISTS options JSONB")
    # dbs_orders same set
    op.execute("ALTER TABLE dbs_orders ADD COLUMN IF NOT EXISTS converted_currency_code INTEGER")
    op.execute("ALTER TABLE dbs_orders ADD COLUMN IF NOT EXISTS group_id VARCHAR(50)")
    op.execute("ALTER TABLE dbs_orders ADD COLUMN IF NOT EXISTS comment VARCHAR(500)")
    op.execute("ALTER TABLE dbs_orders ADD COLUMN IF NOT EXISTS options JSONB")
    # pickup_orders
    op.execute("ALTER TABLE pickup_orders ADD COLUMN IF NOT EXISTS converted_currency_code INTEGER")
    op.execute("ALTER TABLE pickup_orders ADD COLUMN IF NOT EXISTS group_id VARCHAR(50)")
    op.execute("ALTER TABLE pickup_orders ADD COLUMN IF NOT EXISTS comment VARCHAR(500)")
    op.execute("ALTER TABLE pickup_orders ADD COLUMN IF NOT EXISTS options JSONB")


def downgrade() -> None:
    pass
'''

with open(revision_file) as f:
    content = f.read()

# Replace existing stub upgrade/downgrade
import re
content = re.sub(r'def upgrade\(\).*?def downgrade\(\).*?pass\s*$', '', content, flags=re.DOTALL)
content = content.rstrip() + '\n' + migration_body

with open(revision_file, 'w') as f:
    f.write(content)
print("Done")
