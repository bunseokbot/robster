import tensorflow as tf


class TensorflowLite(object):
    name = "tflite"

    def detect(self, stream):
        if stream[4:8] == b'TFL3' or stream[-8:] == b'\x06\x00\x00\x00\x00\x00\x00\x01':
            return True

        return False

    def extract(self, stream):
        interpreter = tf.lite.Interpreter(model_content=stream)
        interpreter.allocate_tensors()
        tensors = [
            {'name': tensor['name'], 'index': tensor['index']}
            for tensor in interpreter.get_tensor_details() if tensor['name']
        ]
        return tensors
