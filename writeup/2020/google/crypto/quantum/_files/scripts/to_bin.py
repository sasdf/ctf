import codecs


pub = "C4Bu/MBwugXDp2oQTUXOYg=="

with open('sigs.txt') as f, open('sigs.bin', 'wb') as out:
    for line in f:
        line = bytes.fromhex(line)
        assert len(line) == 160 * 8
        out.write(line)

with open('pub.bin', 'wb') as f:
    f.write(codecs.decode(pub.encode(), 'base64'))
