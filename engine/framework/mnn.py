class MNN(object):
    name = "mnn"

    def detect(self, stream):
        if stream[-4:] == b'MNN\x00':
            return True
