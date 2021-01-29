class TensorflowLite(object):
    name = "tflite"

    def detect(self, stream):
        if stream[4:8] == b'TFL3' and stream[-8:] == b'\x06\x00\x00\x00\x00\x00\x00\x01':
            return True

        return False
