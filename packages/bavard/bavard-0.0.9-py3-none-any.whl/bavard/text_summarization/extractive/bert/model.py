import os
from datetime import datetime

import tensorflow as tf
import tensorflow_hub as hub
from bert.tokenization.bert_tokenization import FullTokenizer
from tensorflow.keras.layers import Dense, TimeDistributed, Multiply
from tensorflow.keras.models import Model
from .decode_tf_record import decode_tf_record
from ..input_preprocessing import raw_input_to_features
from nltk.tokenize import sent_tokenize, word_tokenize


class ExtractiveSummarizer:
    def __init__(self,
                 tokenizer: FullTokenizer,
                 saved_model_dir: str,
                 max_seq_len=512,
                 max_sentences=20):
        self.tokenizer = tokenizer
        self.model = tf.keras.models.load_model(saved_model_dir)
        self.max_seq_len = max_seq_len
        self.max_sentences = max_sentences

    @staticmethod
    def build_model(input_len=512, n_sentences=20):
        input_ids = tf.keras.layers.Input(shape=(input_len,), dtype=tf.int32, name="input_ids")
        input_mask = tf.keras.layers.Input(shape=(input_len,), dtype=tf.int32, name="input_mask")
        segment_ids = tf.keras.layers.Input(shape=(input_len,), dtype=tf.int32, name="segment_ids")
        cls_indices = tf.keras.layers.Input(shape=(n_sentences,), dtype=tf.int32, name="cls_indices")
        cls_mask = tf.keras.layers.Input(shape=(n_sentences,), dtype=tf.int32, name="cls_mask")

        bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/1", trainable=True)
        bert_inputs = [input_ids, input_mask, segment_ids]
        bert_pooled_output, bert_sequence_output = bert_layer(bert_inputs)

        all_inputs = [*bert_inputs, cls_indices, cls_mask]

        batch_size = 1
        row_idx = tf.reshape(tf.range(batch_size), (batch_size, 1, 1))
        row_idx = tf.broadcast_to(row_idx, (batch_size, n_sentences, 1))
        cls_indices = tf.expand_dims(cls_indices, -1)
        cls_indices = tf.concat([row_idx, cls_indices], axis=-1)
        cls_out = tf.gather_nd(bert_sequence_output, indices=cls_indices)
        # cls_indices = tf.expand_dims(cls_indices, -1)
        # cls_out = tf.gather_nd(bert_sequence_output, indices=cls_indices, batch_dims=1)
        cls_outputs = TimeDistributed(Dense(1, activation='relu'))(cls_out)
        cls_outputs = tf.squeeze(cls_outputs, axis=-1)

        #tf.debugging.Assert(tf.shape(cls_outputs) == tf.shape(cls_mask), data=cls_mask)

        cls_outputs = Multiply(name='cls_outputs')([cls_outputs, tf.cast(cls_mask, tf.float32)])

        return Model(inputs=all_inputs, outputs=cls_outputs)

    @staticmethod
    def compile_model(model):
        optimizer = tf.optimizers.Adam(lr=5e-6)
        losses = {
            'cls_outputs': tf.losses.MeanSquaredError()
        }
        metrics = {'cls_outputs': 'accuracy'}
        model.compile(optimizer=optimizer, loss=losses, metrics=metrics)

    @staticmethod
    def train(model: Model,
              ds: tf.data.Dataset,
              batch_size: int,
              steps_per_epoch: int,
              epochs: int,
              saved_model_path: str):

        def split_x_y(item):
            x = {
                'input_ids': item['input_ids'],
                'input_mask': item['input_mask'],
                'segment_ids': item['segment_ids'],
                'cls_indices': item['cls_indices'],
                'cls_mask': item['cls_mask'],
            }
            y = {
                'cls_outputs': item['cls_outputs']
            }
            return x, y

        ds = ds.shuffle(buffer_size=100)\
            .map(map_func=lambda x: decode_tf_record(x, input_len=512, n_sentences=20, is_training=True)) \
            .map(split_x_y).batch(batch_size=batch_size).repeat()

        val_ds = ds.take(400)
        train_ds = ds.skip(400)

        # checkpoints

        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=saved_model_path,
                                                         save_best_only=True,
                                                         save_weights_only=False,
                                                         verbose=1)

        # tensorboard

        logdir = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        tb_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)

        # train

        model.fit(train_ds,
                  epochs=epochs,
                  steps_per_epoch=steps_per_epoch,
                  validation_data=val_ds,
                  callbacks=[cp_callback, tb_callback],
                  use_multiprocessing=True,
                  workers=4)

    def get_summary(self, text: str, max_words: int) -> str:
        input_features = raw_input_to_features(tokenizer=self.tokenizer,
                                               article=text,
                                               max_seq_len=self.max_seq_len,
                                               max_sentences=self.max_sentences,
                                               is_training=False)

        sentences = sent_tokenize(text)
        n_sent = min(len(sentences), self.max_sentences)

        x, _ = input_features.to_prediction_input()
        out = self.model.predict(x)
        out = out[:n_sent]

        sent_scores = []
        for i in range(n_sent):
            sent = sentences[i]
            score = out[0][i]
            sent_scores.append((sent, score, i))

        sent_scores = sorted(sent_scores, key=lambda x: x[1], reverse=True)

        total_words = 0

        summary_sentences = []
        for sent in sent_scores:
            if total_words >= max_words:
                break
            words = word_tokenize(sent[0])
            total_words += len(words)
            summary_sentences.append(sent)

        summary_sentences = sorted(summary_sentences, key=lambda x: x[2])

        result = " ".join([x[0] for x in summary_sentences])
        return result
