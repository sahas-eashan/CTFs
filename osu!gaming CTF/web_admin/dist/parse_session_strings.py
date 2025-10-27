import phpserialize
from io import BytesIO

def parse_session(data_str):
    data = data_str.encode()
    idx = 0
    result = {}
    while idx < len(data):
        sep = data.find(b"|", idx)
        if sep == -1:
            break
        key = data[idx:sep].decode(errors="ignore")
        idx = sep + 1
        stream = BytesIO(data[idx:])
        value = phpserialize.load(stream, decode_strings=True)
        result[key] = value
        idx += stream.tell()
    return result

samples = [
    'upload_progress_|a:0:{}logged_in|b:1;|a:1:{s:1:"x";i:1;}'
]
for s in samples:
    print('Input:', s)
    try:
        print('Parsed:', parse_session(s))
    except Exception as e:
        print('Error:', e)
    print('-'*40)
