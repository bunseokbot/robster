import zlib
import re


keywords = [
    b'spherical',
    b'linear',
    b'essential',
    b'circular',
    b'elliptical',
    b'ConvSeries',
    b'ConvNL',
    b'Maxpool',
]


class Tesseract(object):
    name = "tesseract"

    def detect(self, stream):
        if stream[0:2] == b'\x78\xDA':
            try:
                data = zlib.decompress(stream)
                for keyword in keywords:
                    if keyword in data:
                        return True
            except:
                return False

        return False
