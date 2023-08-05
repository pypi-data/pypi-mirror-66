import json

def is_number(x):
    try:
        float(x)
        return True
    except:
        return False

def print_fail(a, b, key):
    print(f"Failed on key: {key}")
    print(f"a: {json.dumps(a, indent=4)}")
    print(f"b: {json.dumps(b, indent=4)}")

def assert_close_enough(a, b):
    for key in a:
        if key in ['project', 'type', 'media_id', 'media_ids', 'id', 'meta', 'user']:
            continue
        if key not in b:
            print_fail(a, b, key)
        assert key in b
        if is_number(a[key]):
            diff = abs(a[key] - b[key])
            if diff > 0.0001:
                print_fail(a, b, key)
            assert diff < 0.0001
        else:
            assert a[key] == b[key]

