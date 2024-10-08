import os
import logging

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Suppress other warnings
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, SimpleRNN, Dense, Lambda
from tensorflow.keras.models import Model
import umap

# シード値の固定
SEED = 42
os.environ['PYTHONHASHSEED'] = str(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

def tf_build_simple_rnn_model(segments):
    num_segments, segment_length, input_dim = segments.shape
    rnn_units_factor = 1024

    rnn_units1 = input_dim * rnn_units_factor
    rnn_units2 = rnn_units1 // 2

    inputs = Input(shape=(segment_length, input_dim))
    x = SimpleRNN(rnn_units1, return_sequences=True)(inputs)
    rnn_output = SimpleRNN(rnn_units2, return_sequences=True)(x)
    model = Model(inputs=inputs, outputs=rnn_output)

    return model, rnn_output

def tf_build_attention_model(rnn_output):
    attention_units = 32

    attention = Dense(attention_units, activation='tanh')(rnn_output)
    attention = Dense(1, activation='softmax')(attention)

    context = Lambda(lambda x: tf.reduce_sum(x[0] * x[1], axis=1))([rnn_output, attention])
    attention_output = Dense(units=rnn_output.shape[-1], activation='tanh')(context)

    return attention_output

def reduce_dimensions_with_umap(models_output, n_components=3):
    SEED = 42
    reducer = umap.UMAP(n_components=n_components, random_state=SEED)
    reduced_vectors = reducer.fit_transform(models_output)
    
    return reduced_vectors

def run_models(segments):
    model, rnn_output = tf_build_simple_rnn_model(segments) # RNN層
    attention_output = tf_build_attention_model(rnn_output) # Attention層

    # Attentionモデルと統合した完全なモデル
    final_model = Model(inputs=model.input, outputs=attention_output)

    # モデル出力を取得
    models_output = final_model.predict(segments)
    print("models_output:", models_output.shape)

    # 次元削減
    feature_vectors = reduce_dimensions_with_umap(models_output, n_components=3)

    # RNN-Attention出力の取得
    return feature_vectors

