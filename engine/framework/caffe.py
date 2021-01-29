class Caffe(object):
    name = "caffe"

    def detect(self, stream):
        if stream[2:7] == b'LeNet':
            return True

        return False
