import phpserialize

def parse_session(data: bytes):
    result = {}
    i = 0
    length = len(data)
    while i < length:
        j = data.find(b"|", i)
        if j == -1:
            break
        key = data[i:j].decode("utf-8", errors="ignore")
        i = j + 1
        sub = data[i:]
        value = phpserialize.loads(sub, decode_strings=True)
        serialized = phpserialize.dumps(value, charset="utf-8")
        consumed = len(serialized)
        if sub[:consumed] != serialized:
            raise ValueError("Mismatch in serialization")
        result[key] = value
        i += consumed
    return result

sample = b'upload_progress_|a:0:{}logged_in|b:1;|a:6:{s:10:"start_time";i:0;s:15:"content_length";i:0;s:15:"bytes_processed";i:0;s:5:"files";a:0:{}s:4:"done";b:0;s:5:"value";s:4:"test";}'
print(parse_session(sample))
