from tensorflow.keras import layers

from pau_keras.pade_keras_functions import *

init_w_numerator = [5.49891645e-02, 5.05004092e-01, 1.24178396e+00, 1.25790914e+00, 5.18128693e-01, 7.84309418e-02]
init_w_denominator = [1.76585345e-05, 2.49089658e+00, 8.24388417e-07, 1.55309717e-01]


class PAU(layers.Layer):
    def __init__(self, w_numerator=init_w_numerator, w_denominator=init_w_denominator, version="B", trainable=True):
        super(PAU, self).__init__()
        self.numerator = tf.Variable(initial_value=w_numerator, trainable=trainable)
        self.denominator = tf.Variable(initial_value=w_denominator, trainable=trainable)

        if version == "A":
            pau_func = PAU_PYTORCH_A_F
        elif version == "B":
            pau_func = PAU_PYTORCH_B_F
        elif version == "C":
            pau_func = PAU_PYTORCH_C_F
        elif version == "D":
            pau_func = PAU_PYTORCH_D_F
        else:
            raise ValueError("version %s not implemented" % version)

        self.pau_func = pau_func

    def build(self, input_shape):
        pass

    def call(self, input, training=True):
        return self.pau_func(input, self.numerator, self.denominator, training)
