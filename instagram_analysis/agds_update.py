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
            shape=(input_shape[1], self.output_dim), 
            initializer='random_normal',
            trainable=True)
        super(SparseLayer, self).build(input_shape)

    def call(self, input_data):
        multi_kernel = K.expand_dims(self.kernel, 0)
        coeffs = tf.keras.layers.Dot(axes=(1, 1))([input_data, multi_kernel])
        return tf.keras.activations.softmax(coeffs)
    
    def get_config(self):
        return {"output_dimension": self.output_dim}


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

# Associate words with archetypes/character traits as intermediate layer
# and with influencer as the "last" layer

# Dependencies
import pandas as pd
import numpy as np
from tqdm import tqdm
import copy
import os
import toml
import re
import itertools
from text_cleaner import *
import operator
from collections import Counter
import pickle
import sys

args = sys.argv
if not args[1]:
    print("No start index, exiting...")
    sys.exit(1)
if not args[2]:
    print("No ending index, exiting...")
    sys.exit(1)

start_idx = int(args[1])
end_idx = int(args[2])
print(f"Start index: {start_idx}, ending index: {end_idx}")

def extract_hashtags(post_text):
    HASH_RE = re.compile(r"\#\w+")
    out_list = re.findall(HASH_RE, post_text)
    return out_list

# Load the .csv with archetypes
arch_df = pd.read_csv('archetypes_pl_new.csv', index_col=0)

# Save the order of columns
trait_list = arch_df.columns.tolist()

# Load data
train_df = pd.read_csv("agds_structures/train_90.csv", index_col=0)
test_df = pd.read_csv("agds_structures/test_10.csv", index_col=0)

with open("agds_structures/vectorized_test_90.pickle", "rb") as f:
    test_vectorized = pickle.load(f)
    
with open("agds_structures/vectorized_train_90.pickle", "rb") as f:
    train_vectorized = pickle.load(f)
    
# Load structure
with open("agds_structures/finetuned_s90_10_word_trait_array.pickle", "rb") as f:
    softmax_word_df = pickle.load(f)

# Extract word map
softmax_word_map = softmax_word_df.columns.tolist()

# Prepare training data
X_train = np.array(train_vectorized)
print(len(X_train))

# Prepare validation/test dataset
X_val = np.array(test_vectorized)

# Create a model
def build_model():
    inputs = tf.keras.Input(shape=(len(softmax_word_map), ), name="input_layer")
    x = SparseLayer(5, name="AGDS_weight_layer")(inputs)
    outputs = tf.keras.activations.softmax(x)

    model = tf.keras.Model(
        inputs=inputs,
        outputs=[outputs]
    )
    return model

tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="./logs_agds_model")
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_accuracy', factor=0.2,
                              patience=5, min_lr=1e-7, verbose=1)
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_accuracy', min_delta=0, patience=20, verbose=1,
    mode='auto', baseline=None, restore_best_weights=True)

def trait_training_pipeline(trait_list):
    for trait in tqdm(trait_list):
        # Prepare labels
        y_train = tf.keras.utils.to_categorical(np.array(train_df[trait]), num_classes=5)
        y_val = tf.keras.utils.to_categorical(np.array(test_df[trait]), num_classes=5)

        # Create model
        test_model = build_model()

        # Set weights for a given trait
        test_model.get_layer("AGDS_weight_layer").set_weights([softmax_word_df.loc[trait].to_numpy().T])

        # Compile model
        test_model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=1e-2),
                       loss=tf.keras.losses.CategoricalCrossentropy(),
                       metrics=["accuracy"])

        # Set callbacks
        model_save_callback = tf.keras.callbacks.ModelCheckpoint("./agds_structures/weight_finetuning/"+trait+"-saved-model-{epoch:02d}-{val_accuracy:.2f}.hdf5", 
                                                              monitor='val_accuracy', 
                                                              verbose=1, save_best_only=True, save_weights_only=True, 
                                                              mode='max')
        

        # Train the model
        with tf.device("/GPU:0"):
            out = test_model.fit(X_train, 
                                 y_train,
                                 batch_size=10,
                                 validation_data=(X_val, y_val),
                                 epochs=100,
                                 callbacks=[model_save_callback, tensorboard_callback, reduce_lr, early_stop])

        weights_tmp = test_model.get_layer("AGDS_weight_layer").get_weights()[0]
        softmax_word_df.loc[trait] = weights_tmp.T


# 0 - 9
# 9 - 18
# 18 - 27
# 27 - 37
trait_training_pipeline(trait_list[start_idx:end_idx])

# Save new softmax structure
with open("agds_structures/finetuned_s90_10_word_trait_array.pickle", "wb") as f:
    pickle.dump(softmax_word_df, f)