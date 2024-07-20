

def generate_diff(first_file, second_file):

    def inner_(data1, data2):

        out_store = []

        add_keys = set(data2.keys()) - set(data1.keys())
        del_keys = set(data1.keys()) - set(data2.keys())

        for key in sorted(set(data1.keys()) | set(data2.keys())):
            # add
            if key in add_keys:
                out_store.append({
                    "type": "add",
                    "key": key,
                    "value": data2[key]
                })

            # delete
            elif key in del_keys:
                out_store.append({
                    "type": "del",
                    "key": key,
                    "value": data1[key]
                })

            # nested  (two dicts, call recursion)
            elif (isinstance(data1.get(key), dict)
                  and isinstance(data2.get(key), dict)):
                out_store.append({
                    "type": "nested",
                    "key": key,
                    "children": inner_(data1.get(key), data2.get(key))
                })

            elif data1.get(key) != data2.get(key):
                out_store.append({
                    "type": "changed",
                    "key": key,
                    "old_value": data1[key],
                    "new_value": data2[key]
                })

            else:
                out_store.append({
                    "type": "unchanged",
                    "key": key,
                    "value": data1[key]
                })

        return out_store

    return inner_(first_file, second_file)
