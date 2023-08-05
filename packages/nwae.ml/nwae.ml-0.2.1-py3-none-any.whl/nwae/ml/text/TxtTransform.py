# -*- coding: utf-8 -*-

from nwae.utils.Log import Log
from inspect import getframeinfo, currentframe
from nwae.lang.preprocessing.BasicPreprocessor import BasicPreprocessor
from nwae.lang.LangFeatures import LangFeatures

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
            # List of documents or sentences
            docs,
            # List of labels
            labels,
            # If None we use space as word splitter
            langs = None
    ):
        self.docs = docs
        self.labels = labels
        self.langs = langs
        if self.langs is None:
            # Assume all English
            self.langs = [LangFeatures.LANG_EN] * len(self.docs)
        if (len(self.docs) != len(self.labels)) or (len(self.docs) != len(self.langs)):
            raise Exception(
                str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Length of docs ' + str(len(self.docs))
                + ' must equal labels shape ' + str(len(self.labels))
                + ' and langs shape ' + str(len(langs))
            )
        self.lang_features = LangFeatures()

        # We need to split the docs/sentences into a list of words
        self.docs_split = None
        return

    def __preprocess(self):
        self.docs_split = []
        for i in range(0, len(self.docs), 1):
            wsep = BasicPreprocessor.get_word_separator(lang=self.langs[i])
            self.docs_split.append(
                self.docs[i].split(wsep)
            )
        self.docs_split = [BasicPreprocessor.clean_punctuations(sentence=sent) for sent in self.docs_split]

    def create_padded_docs(
            self,
            # 'pre' or 'post'
            padding = 'pre'
    ):
        self.__preprocess()

        # How many unique labels
        n_labels = len(list(set(self.labels)))
        # Convert labels to categorical one-hot encoding
        labels_categorical = kerasutils.to_categorical(
            self.labels,
            # In order to be able to represent in a binary array the largest number, must add 1
            num_classes = max(self.labels) + 1
        )

        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Docs split: ' + str(self.docs_split)
        )
        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Labels: ' + str(self.labels)
        )
        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Labels converted to categorical: ' + str(labels_categorical)
        )

        unique_words = list(set([w for sent in self.docs_split for w in sent]))
        Log.debug(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Unique words: ' + str(unique_words)
        )

        #
        # Create indexed dictionary
        #
        one_hot_dict = BasicPreprocessor.create_indexed_dictionary(
            sentences = self.docs_split
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
            sentences    = self.docs_split,
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
            def __init__(
                    self,
                    encoded_docs,
                    padded_docs,
                    list_labels,
                    list_labels_categorical,
                    vocabulary_dimension,
                    input_dim_max_length
            ):
                self.encoded_docs = encoded_docs
                self.padded_docs = padded_docs
                self.list_labels = list_labels
                self.list_labels_categorical = list_labels_categorical
                self.vocabulary_dimension = vocabulary_dimension
                self.input_dim_max_length = input_dim_max_length

        return RetClass(
            encoded_docs            = enc_docs,
            padded_docs             = p_docs,
            list_labels             = self.labels.copy(),
            list_labels_categorical = labels_categorical,
            vocabulary_dimension    = vs,
            input_dim_max_length    = max_length
        )


import nwae.utils.UnitTest as ut
import pandas as pd
from nwae.ml.text.preprocessing.TrDataSampleData import SampleTextClassificationData
from nwae.ml.text.preprocessing.TrDataPreprocessor import TrDataPreprocessor
from nwae.lang.nlp.daehua.DaehuaTrainDataModel import DaehuaTrainDataModel

class TxtTransformUnitTest:

    def __init__(self, ut_params):
        self.ut_params = ut_params

    def run_unit_test_sample(
            self,
            sample_training_data
    ):
        res_final = ut.ResultObj(count_ok=0, count_fail=0)

        lang_main = SampleTextClassificationData.get_lang_main(sample_training_data=sample_training_data)
        lang_additional = SampleTextClassificationData.get_lang_additional(sample_training_data=sample_training_data)
        sample_data = SampleTextClassificationData.get_text_classification_training_data(
            sample_training_data = sample_training_data,
            type_io = SampleTextClassificationData.TYPE_IO_IN
        )
        expected_output_data = SampleTextClassificationData.get_text_classification_training_data(
            sample_training_data = sample_training_data,
            type_io = SampleTextClassificationData.TYPE_IO_OUT
        )

        fake_training_data = pd.DataFrame({
            DaehuaTrainDataModel.COL_TDATA_INTENT_ID: sample_data[SampleTextClassificationData.COL_CLASS],
            DaehuaTrainDataModel.COL_TDATA_INTENT_NAME: sample_data[SampleTextClassificationData.COL_CLASS_NAME],
            DaehuaTrainDataModel.COL_TDATA_TEXT: sample_data[SampleTextClassificationData.COL_TEXT],
            DaehuaTrainDataModel.COL_TDATA_TRAINING_DATA_ID: sample_data[SampleTextClassificationData.COL_TEXT_ID],
            # Don't do any processing until later
            DaehuaTrainDataModel.COL_TDATA_TEXT_SEGMENTED: None,
            DaehuaTrainDataModel.COL_TDATA_TEXT_LANG: None
        })
        Log.debug('Fake Training Data:\n\r' + str(fake_training_data.values))
        Log.debug('Expected Output:\n\r' + str(expected_output_data))

        ctdata = TrDataPreprocessor(
            model_identifier     = str([lang_main] + lang_additional) + ' Test Training Data Text Processor',
            language_main        = lang_main,
            df_training_data     = fake_training_data,
            dirpath_wordlist     = self.ut_params.dirpath_wordlist,
            postfix_wordlist     = self.ut_params.postfix_wordlist,
            dirpath_app_wordlist = self.ut_params.dirpath_app_wordlist,
            postfix_app_wordlist = self.ut_params.postfix_app_wordlist,
            dirpath_synonymlist  = self.ut_params.dirpath_synonymlist,
            postfix_synonymlist  = self.ut_params.postfix_synonymlist,
            reprocess_all_text   = True,
            languages_additional = lang_additional
        )

        ctdata.go()

        Log.debug('*********** FINAL SEGMENTED DATA (' + str(ctdata.df_training_data.shape[0]) + ' sentences)')
        Log.debug(ctdata.df_training_data.columns)
        Log.debug(ctdata.df_training_data.values)

        res = TxtTransform(
            docs   = list( ctdata.df_training_data[DaehuaTrainDataModel.COL_TDATA_TEXT_SEGMENTED] ),
            labels = list( ctdata.df_training_data[DaehuaTrainDataModel.COL_TDATA_INTENT_ID] ),
            langs  = list( ctdata.df_training_data[DaehuaTrainDataModel.COL_TDATA_TEXT_LANG] )
        ).create_padded_docs()
        Log.debug(
            'Padded Docs: ' + str(res.padded_docs)
        )
        Log.debug(
            'Labels Categorical: ' + str(res.list_labels_categorical)
        )

        return res_final

    def run_unit_test(self):
        res_final = ut.ResultObj(count_ok=0, count_fail=0)

        for sample_training_data in SampleTextClassificationData.SAMPLE_TRAINING_DATA:
            #if not sample_training_data[SampleTextClassificationData.TYPE_LANG_ADDITIONAL]:
            #    continue
            res = self.run_unit_test_sample(sample_training_data = sample_training_data)
            res_final.update(other_res_obj=res)

        return res_final


if __name__ == '__main__':
    from nwae.ml.config.Config import Config
    config = Config.get_cmdline_params_and_init_config_singleton(
        Derived_Class       = Config,
        default_config_file = Config.CONFIG_FILE_DEFAULT
    )

    Log.LOGLEVEL = Log.LOG_LEVEL_DEBUG_1

    ut_params = ut.UnitTestParams(
        dirpath_wordlist     = config.get_config(param=Config.PARAM_NLP_DIR_WORDLIST),
        postfix_wordlist     = config.get_config(param=Config.PARAM_NLP_POSTFIX_WORDLIST),
        dirpath_app_wordlist = config.get_config(param=Config.PARAM_NLP_DIR_APP_WORDLIST),
        postfix_app_wordlist = config.get_config(param=Config.PARAM_NLP_POSTFIX_APP_WORDLIST),
        dirpath_synonymlist  = config.get_config(param=Config.PARAM_NLP_DIR_SYNONYMLIST),
        postfix_synonymlist  = config.get_config(param=Config.PARAM_NLP_POSTFIX_SYNONYMLIST)
    )
    res = TxtTransformUnitTest(ut_params=ut_params).run_unit_test()
    exit(res.count_fail)

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

    r = TxtTransform(
        docs   = [x[0] for x in docs_label],
        labels = [x[1] for x in docs_label]
    ).create_padded_docs()

    exit(0)
