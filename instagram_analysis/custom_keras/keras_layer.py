import tensorflow as tf
import tensorflow.keras.backend as K
from collections import Counter


# Class representing AGDS
class SparseLayer(tf.keras.layers.Layer):
    def __init__(self, output_dim, **kwargs):
        super(SparseLayer, self).__init__(**kwargs)
        self.output_dim = output_dim
        

    def build(self, input_shape):
        self.kernel = self.add_weight(
            shape=(input_shape[0], self.output_dim), 
            initializer='random_normal',
            trainable=True)

    def call(self, input_data):
        multi_input = K.expand_dims(input_data, 0)
        multi_kernel = K.expand_dims(self.kernel, 0)
        coeffs = tf.keras.layers.Dot(axes=(1, 1))([multi_input, multi_kernel])
        return tf.keras.activations.softmax(coeffs)


# Class for AGDS Word2BoW processing
class AGDSVectorization(tf.keras.layers.Layer):
    def __init__(self, word_map, **kwargs):
        self.word_map = word_map
        super(AGDSVectorization, self).__init__(**kwargs)

    def call(self, input_data):
        post_vector = [0] * len(self.word_map)

        # Calculate word occurrences
        word_ctr = Counter(input_data)

        for word, freq in word_ctr.items():
            if word in self.word_map:
                post_vector[self.word_map.index(word)] = freq
        return post_vector

    def compute_output_shape(self, input_shape):
        return (input_shape[0], len(self.word_map))