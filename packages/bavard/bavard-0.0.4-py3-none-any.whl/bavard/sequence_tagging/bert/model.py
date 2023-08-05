import os

import numpy as np
import tensorflow as tf
from official.nlp.bert.bert_models import get_transformer_encoder
from official.nlp.bert.configs import BertConfig
from tensorflow.python.keras.layers import Input, Dense, Multiply, TimeDistributed, Dropout
from tensorflow.python.keras.models import Model


def get_bert_encoder(max_seq_len, bert_dir='./uncased_L-12_H-768_A-12/'):
    bert_config = BertConfig.from_json_file(os.path.join(bert_dir, 'bert_config.json'))
    bert_encoder = get_transformer_encoder(bert_config, max_seq_len)
    return bert_encoder


class IntentClassifierAndSlotFiller:
    def __init__(self, max_seq_len, n_slots, n_intents, bert_dir):
        self.max_seq_len = max_seq_len
        self.n_slots = n_slots
        self.n_intents = n_intents
        self.bert_dir = bert_dir
        self.bert_encoder = get_bert_encoder(max_seq_len, bert_dir)
        self.model = None

    def build_model(self):
        in_id = Input(shape=(self.max_seq_len,), name='input_ids', dtype=tf.int32)
        in_mask = Input(shape=(self.max_seq_len,), name='input_masks', dtype=tf.int32)
        in_segment = Input(shape=(self.max_seq_len,), name='segment_ids', dtype=tf.int32)
        slots_mask = Input(shape=(self.max_seq_len, self.n_slots,), name='slots_mask', dtype=tf.float32)
        bert_inputs = [in_id, in_mask, in_segment]
        all_inputs = [in_id, in_mask, in_segment, slots_mask]

        # the output of trained Bert
        bert_sequence_output, bert_pooled_output = self.bert_encoder(bert_inputs)

        # add the additional layer for intent classification and slot filling
        intents_drop = Dropout(rate=0.1)(bert_pooled_output)
        intents_out = Dense(self.n_intents, activation='softmax', name='intent_classifier')(intents_drop)

        slots_drop = Dropout(rate=0.1)(bert_sequence_output)
        slots_out = TimeDistributed(Dense(self.n_slots, activation='softmax'))(slots_drop)
        slots_out = Multiply(name='slots_tagger')([slots_out, slots_mask])

        self.model = Model(inputs=all_inputs, outputs=[slots_out, intents_out])

    def compile_model(self):
        optimizer = tf.keras.optimizers.Adam(lr=5e-5)
        losses = {
            'slots_tagger': 'sparse_categorical_crossentropy',
            'intent_classifier': 'sparse_categorical_crossentropy'
        }
        loss_weights = {'slots_tagger': 3.0, 'intent_classifier': 1.0}
        metrics = {'intent_classifier': 'acc'}
        self.model.compile(optimizer=optimizer, loss=losses, loss_weights=loss_weights, metrics=metrics)
        self.model.summary()

    def fit(self, X, Y, validation_data=None, epochs=5, batch_size=32):
        X = (X[0], X[1], X[2], self.get_slots_output_mask(X[3]))
        if validation_data is not None:
            X_val, Y_val = validation_data
            validation_data = ((X_val[0], X_val[1], X_val[2], self.get_slots_output_mask(X_val[3])), Y_val)

        self.model.fit(X, Y, validation_data=validation_data, epochs=epochs, batch_size=batch_size)

    def get_slots_output_mask(self, slots_mask):
        slots_mask = np.expand_dims(slots_mask, axis=2)  # n x seq_len x 1
        slots_output_mask = np.tile(slots_mask, (1, 1, self.n_slots))  # n x seq_len x n_slots
        return slots_output_mask
