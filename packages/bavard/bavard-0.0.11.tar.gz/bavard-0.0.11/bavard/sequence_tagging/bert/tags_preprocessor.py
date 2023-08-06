import numpy as np
from sklearn.preprocessing import LabelEncoder


class TagsPreprocessor:
    """Transforms sentence word tags into integer labels, taking into account that a
    word can produce multiple tokens."""

    def tokenize(self, tags_str_arr):
        return [s.split() for s in tags_str_arr]

    def fit(self, tags):
        self.label_encoder = LabelEncoder()

        tag_set = {'[CLS]', '[SEP]'}

        for sentence_tags in tags:
            for tag in sentence_tags.split():
                tag_set.add(tag)

        self.label_encoder.fit(list(tag_set))

    def transform(self, tags, word_masks):
        N, seq_len = word_masks.shape
        assert len(tags) == N

        encoded_tags = []
        for sentence_tags in tags:
            tags = sentence_tags.split()
            tags = ['[CLS]'] + tags + ['[SEP]']
            encoded = self.label_encoder.transform(tags).astype(np.int32)
            encoded_tags.append(encoded)

        output = np.zeros((N, seq_len), dtype=np.int32)

        for i in range(N):
            idx = 0
            for j in range(seq_len):
                if word_masks[i][j] == 1:
                    output[i][j] = encoded_tags[i][idx]
                    idx += 1
        return output

    def decode_tags(self, encoded_tags, word_masks):
        N, seq_length = word_masks.shape

        decoded = []
        for et in encoded_tags:
            decoded.append(self.label_encoder.inverse_transform(et))

        tags = []
        for i in range(N):
            sentence_tags = []
            for j in range(seq_length):
                if word_masks[i][j] == 1:
                    sentence_tags.append(str(decoded[i][j]))
            tags.append(sentence_tags)
        return np.array(tags)

    def inverse_transform(self, model_output, word_masks):
        # model_output = n x seq_len x n_tag_classes
        encoded_tags = np.argmax(model_output, axis=-1)
        return self.decode_tags(encoded_tags, word_masks)

    def load(self):
        pass

    def save(self):
        pass

