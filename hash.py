#!/usr/bin/env python3

import sys
import time
name = sys.argv[1]

import hashlib
# BLOCKSIZE = 65536
BMIN = 512
BLOCKSIZE = 512
BDEL = 512 * 4
BDELM = 128
MAX_BLOCKSIZE = 65536 * 10
hasher = hashlib.sha1()

# open the file for reading
with open(name, 'rb') as afile:

    # buf = afile.read(BLOCKSIZE)
    buf = b' '  # start
    last = 666666
    inc = True
    cnt = 0
    while len(buf) > 0:

        if inc:
            BLOCKSIZE = min(BLOCKSIZE+BDEL, MAX_BLOCKSIZE)
        else:
            BLOCKSIZE = max(BLOCKSIZE-BDELM, BMIN)

        st = time.time()
        buf = afile.read(BLOCKSIZE)
        hasher.update(buf)
        dt = time.time() - st

        if dt > last:
            inc = not inc

        last = dt
        cnt += 1
        print('cnt', cnt, inc, BLOCKSIZE)

print(hasher.hexdigest())
