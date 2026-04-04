with open('/app/src/services/fbw/sync/supplies.py') as f:
    content = f.read()

old = '''        result = await session.execute(select(FbwSupply.supply_id))
        supply_ids = [row[0] for row in result.fetchall()]'''

new = '''        result = await session.execute(select(FbwSupply.supply_id))
        supply_ids = list(result.scalars().all())
        await session.close()  # close before long HTTP loop'''

if old in content:
    content = content.replace(old, new)
    with open('/app/src/services/fbw/sync/supplies.py', 'w') as f:
        f.write(content)
    print("Fixed session management")
else:
    print("Not found")
