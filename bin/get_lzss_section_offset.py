#!/usr/bin/env python3

import sys
import struct


def main():
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: $0 <decrypted.kernelcache>"
        sys.exit(1)

    offset = 0
    with open(sys.argv[1], 'rb') as f:
        found = False
        while True:
            buf = f.read(16)
            if buf == "":
                break
            if len(buf) < 16:
                break
            for i in range(0, 16):
                if buf[i] == 0xff and i+4 < 16:
                    chunk = struct.unpack("<I", buf[i+1:i+5])[0]
                    if chunk == 0xfeedface or chunk == 0xfeedfacf:
                        found = True
                        print(offset+i)
                        break
            if found == True:
                break
            offset += 16


if __name__ == "__main__":
    sys.exit(main())
