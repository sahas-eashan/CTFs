import struct
with open("remote_gameover.png","rb") as f:
    f.read(8)
    while True:
        chunk_len_bytes = f.read(4)
        if not chunk_len_bytes:
            break
        length = struct.unpack(">I", chunk_len_bytes)[0]
        chunk_type = f.read(4)
        data = f.read(length)
        crc = f.read(4)
        print(chunk_type.decode("ascii"), length)
