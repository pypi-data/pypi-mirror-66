# -*- coding: utf-8 -*-

from nwae.utils.Log import Log
from inspect import getframeinfo, currentframe
from nwae.lang.preprocessing.BasicPreprocessor import BasicPreprocessor

try:
    import keras.utils as kerasutils
    import keras.preprocessing as kerasprep
except Exception as ex_keras:
    Log.warning(
        str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
        + ': Exception importing Keras modules: ' + str(ex_keras)
    )


#
# Transform text to suitable math objects for neural networks
#
class TxtTransform:

    def __init__(
            self,
            # List of tuples (doc, label)
            docs_label,
    ):
        self.docs_label = docs_label
        return

    def create_padded_docs(
            self,
            # 'pre' or 'post'
            padding = 'pre'
    ):
        docs = [x[0].split(' ') for x in self.docs_label]
        docs = [BasicPreprocessor.clean_punctuations(sentence=sent) for sent in docs]
        labels = [x[1] for x in self.docs_label]
        # How many unique labels
        n_labels = len(list(set(labels)))
        # Convert labels to categorical one-hot encoding
        labels_categorical = kerasutils.to_categorical(labels, num_classes=n_labels)

        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Docs: ' + str(docs)
        )
        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Labels: ' + str(labels)
        )
        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Labels converted to categorical: ' + str(labels_categorical)
        )

        unique_words = list(set([w for sent in docs for w in sent]))
        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Unique words: ' + str(unique_words)
        )

        #
        # Create indexed dictionary
        #
        one_hot_dict = BasicPreprocessor.create_indexed_dictionary(
            sentences = docs
        )
        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': One Hot Dict: ' + str(one_hot_dict)
        )

        #
        # Process sentences into numbers, with padding
        # In real environments, we usually also replace unknown words, numbers, URI, etc.
        # with standard symbols, do word stemming, remove stopwords, etc.
        #
        # Vocabulary dimension
        vs = len(unique_words) + 10
        enc_docs = BasicPreprocessor.sentences_to_indexes(
            sentences    = docs,
            indexed_dict = one_hot_dict
        )
        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Encoded Sentences (' + str(len(enc_docs)) + '):'
        )
        Log.debug(enc_docs)

        # pad documents to a max length of 4 words
        max_length = 1
        for sent in enc_docs:
            max_length = max(len(sent), max_length)
        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Max Length = ' + str(max_length)
        )

        p_docs = kerasprep.sequence.pad_sequences(enc_docs, maxlen=max_length, padding=padding)
        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Padded Encoded Sentences (' + str(p_docs.shape) + ') type "' + str(type(p_docs)) + '":'
        )
        Log.debug(p_docs)

        class RetClass:
            def __init__(self, encoded_docs, padded_docs, list_labels, list_labels_categorical, vocabulary_dimension, input_dim_max_length):
                self.encoded_docs = encoded_docs
                self.padded_docs = padded_docs
                self.list_labels = list_labels
                self.list_labels_categorical = list_labels_categorical
                self.vocabulary_dimension = vocabulary_dimension
                self.input_dim_max_length = input_dim_max_length

        return RetClass(
            encoded_docs            = enc_docs,
            padded_docs             = p_docs,
            list_labels             = labels,
            list_labels_categorical = labels_categorical,
            vocabulary_dimension    = vs,
            input_dim_max_length    = max_length
        )


if __name__ == '__main__':
    Log.LOGLEVEL = Log.LOG_LEVEL_DEBUG_1

    # Training data or Documents
    docs_label = [
        ('잘 했어!', 1), ('잘 했어요!', 1), ('잘 한다!', 1),
        ('Молодец!', 1), ('Супер!', 1), ('Хорошо!', 1),
        ('Плохо!', 0), ('Дурак!', 0),
        ('나쁜!', 0), ('바보!', 0), ('백치!', 0), ('얼간이!', 0),
        ('미친놈', 0), ('씨발', 0), ('개', 0), ('개자식', 0),
        ('젠장', 0),
        ('ok', 2), ('fine', 2)
    ]

    res = TxtTransform(
        docs_label = docs_label
    ).create_padded_docs()

    exit(0)
