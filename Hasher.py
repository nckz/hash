"""A class used to hash files.

Author: Nick Zwart
Date: 2020apr02
"""

import os
import time
import hashlib


class Hasher(object):
    """A file hashing class that tunes the read blocksize for fast execution.
    The hasher can also be used to hash multiple files together.
    """

    BMIN = 512  # minimum size
    BLOCKSIZE = BMIN * 128  # starting size
    BDEL = BMIN * 10  # delta increase
    BDELM = BMIN * 9  # delta decrease
    MAX_BLOCKSIZE = BLOCKSIZE * 1000  # max size

    def __init__(self):
        """Initialize the hasher."""
        self._hasher = hashlib.sha1()  # choose sha1 b/c its the fastest

    def hash(self, fname):
        """Return the hash value given a file path."""
        path = os.path.abspath(fname)
        assert os.path.isfile(path)  # must be a hashable file

        # initialize the starting blocksize
        blocksize = self.BLOCKSIZE

        # open the file for reading
        with open(path, 'rb') as afile:

            # run the first iteration before stepping into the loop
            st = time.time()
            buf = afile.read(blocksize)
            self._hasher.update(buf)
            last = time.time() - st

            # loop, if needed
            while len(buf) > 0:

                # read a block and time it
                st = time.time()
                buf = afile.read(blocksize)
                self._hasher.update(buf)
                dt = time.time() - st

                # If the time is longer than the last, back off and read fewer blocks
                # on the next round.  This assumes resource or IO limited.
                if dt > last:
                    # this round was slow, reduce block size
                    blocksize = max(blocksize - self.BDELM, self.BMIN)

                else:
                    # this round was fast, increase block size
                    blocksize = min(blocksize + self.BDEL, self.MAX_BLOCKSIZE)

                # save the time this round took
                last = dt

            return self.result()

    def result(self):
        """Return the current hash."""
        return self._hasher.hexdigest()


if __name__ == '__main__':

    import sys
    name = sys.argv[1]

    # get a hasher instance
    h = Hasher()

    # calc and show the sha1 sum
    print(h.hash(name))
