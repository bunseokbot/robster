import re


class Ncnn(object):
    name = "ncnn"

    def detect(self, stream):
        if stream[0:8] == b'7767517\n':
            if re.match(r'[0-9]+ [0-9]+', stream.split(b'\n')[1].decode()):
                return True
