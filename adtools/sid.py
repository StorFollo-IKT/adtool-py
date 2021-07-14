import struct


def format_sid(sid: bytes) -> str:
    parts = [struct.unpack('I', sid[1:5])[0],
             struct.unpack('I', sid[8:12])[0],
             struct.unpack('I', sid[12:16])[0],
             struct.unpack('I', sid[16:20])[0],
             struct.unpack('I', sid[20:24])[0],
             struct.unpack('I', sid[24:28])[0]
             ]

    return 'S-%d-%s' % (sid[0], '-'.join(map(str, parts)))


def parse_sid(sid: str) -> bytes:
    parts = b'\x01' + \
            struct.pack('I', int(sid[4])) + \
            b'\x00\x00\x05'

    sections = sid.split('-')
    for section in sections[3:]:
        parts += struct.pack('I', int(section))

    return parts
