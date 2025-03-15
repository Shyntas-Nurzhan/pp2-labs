import json

def format_interface_status(data):
    header = "Interface Status\n" + "=" * 80
    table_header = f"{'DN'.ljust(60)}{'Description'.ljust(20)}{'Speed'.ljust(10)}MTU"
    separator = "-" * 59 + " " + "-"*18+ " "*2 + "-" * 6 + " "*3 + "-"*6
    rows = []
    
    for item in data["imdata"][:3]:
        attributes = item["l1PhysIf"]["attributes"]
        dn = attributes["dn"].ljust(60)
        descr = attributes.get("descr", "").ljust(20)
        speed = attributes["speed"].ljust(10)
        mtu = attributes["mtu"]
        rows.append(f"{dn}{descr}{speed}{mtu}")
    
    return "\n".join([header, table_header, separator] + rows)

file_path = "C:\Study\pp2\Lab4(homework)\json\sample-data.json"
with open(file_path, "r") as file:
    data = json.load(file)

output = format_interface_status(data)
print(output)