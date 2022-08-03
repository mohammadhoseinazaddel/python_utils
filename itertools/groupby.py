from itertools import groupby

data = [
    {"device_id": 1, "port_id": 1, "some_value": 1},
    {"device_id": 1, "port_id": 2, "some_value": 2},
    {"device_id": 1, "port_id": 2, "some_value": 3},
    {"device_id": 2, "port_id": 1, "some_value": 1},
    {"device_id": 2, "port_id": 1, "some_value": 2},
    {"device_id": 3, "port_id": 1, "some_value": 1},
]

grouped_data = groupby(data, key=lambda x: (x["device_id"], x["port_id"]))

for (device_id, port_id), group in grouped_data:
    print(f"device_id, port_id: {device_id}, {port_id}")
    print(f"  -> group: {list(group)}")
    
grouped_data2 = groupby(data, key=lambda x: x["device_id"])
for d, group in grouped_data2:
    print(list(group))
# https://stackoverflow.com/questions/51060140/itertools-group-by-multiple-keys
