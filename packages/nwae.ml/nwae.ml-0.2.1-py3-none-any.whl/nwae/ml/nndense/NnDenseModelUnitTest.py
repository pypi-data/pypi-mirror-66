# -*- coding: utf-8 -*-

import nwae.ml.TrainingDataModel as tdm
from nwae.utils.Log import Log
from inspect import currentframe, getframeinfo
from nwae.ml.ModelInterface import ModelInterface
from nwae.ml.data.Mnist import MnistData
import numpy as np
import nwae.utils.UnitTest as ut
from nwae.ml.text.TxtTransform import TxtTransform
from nwae.ml.nndense.NnDenseModel import NnDenseModel

try:
    from keras.utils import to_categorical
except Exception as ex_keras:
    Log.warning(
        str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
        + ': Exception importing Keras modules: ' + str(ex_keras)
    )


class NnDenseModelUnitTest:

    THRESHOLD_PASS_PCT = 85.0
    THRESHOLD_PASS_PCT_LOW = 75.0

    def __init__(self, ut_params):
        self.ut_params = ut_params

    def run_unit_test(self):
        res_final = ut.ResultObj(count_ok=0, count_fail=0)
        # Demonstrating a network architecture requiring convertion to categorical the labels
        res_final.update(other_res_obj=self.test_math_function())
        # Demonstrating a network architecture with Flatten layer thus does not require categorical labels
        res_final.update(other_res_obj=self.test_text_classification())

        res_final.update(other_res_obj=self.test_text_classification_from_sample_data())
        return res_final

    def __check_result_of_test(
            self,
            # numpy ndarray type, input data
            data,
            labels,
            model_obj,
            res_obj,
            # Expected accuracy in %
            exp_acc
    ):
        n_rows = data.shape[0]
        # Predict all at once
        top_match_bulk = model_obj.predict_classes(x=data).predicted_classes

        # Compare some data, do it one by one
        count_correct_bulk = 0
        count_correct = 0
        for i in range(data.shape[0]):
            data_i = np.array([data[i]])
            label_i = labels[i]
            top_matches = model_obj.predict_class(x=data_i).predicted_classes
            top_match = top_matches[0]
            if top_match != label_i:
                Log.debug(
                    str(i) + '. ' + str(data_i) + ': Label=' + str(label_i)
                    + ', wrongly predicted=' + str(top_matches)
                )
            count_correct      += 1 * (top_match == label_i)
            count_correct_bulk += 1 * (top_match_bulk[i] == label_i)

        accuracy_manual_check      = round(100 * count_correct / data.shape[0], 2)
        accuracy_manual_check_bulk = round(100 * count_correct_bulk / data.shape[0], 2)
        Log.info(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Accuracy manual = ' + str(accuracy_manual_check) + '%.'
        )
        res_obj.update_bool(res_bool=ut.UnitTest.assert_true(
            observed = (accuracy_manual_check == exp_acc),
            expected = True,
            test_comment = ': Test manual predict accuracy: ' + str(accuracy_manual_check)
                           + ' on dataset with ' + str(n_rows) + ' rows data'
        ))
        res_obj.update_bool(res_bool=ut.UnitTest.assert_true(
            observed = (accuracy_manual_check == exp_acc),
            expected = True,
            test_comment = ': Test bulk predict accuracy: ' + str(accuracy_manual_check_bulk)
                           + ' on dataset with ' + str(n_rows) + ' rows data'
        ))
        return res_obj

    def test_math_function(self):
        res_final = ut.ResultObj(count_ok=0, count_fail=0)
        #
        # Prepare random data
        #
        n_rows = 1000
        input_dim = 5
        # Random vectors numpy ndarray type
        data = np.random.random((n_rows, input_dim))
        #
        # Design some pattern
        # Labels are sum of the rows, then floored to the integer
        # Sum >= 0, 1, 2, 3,...
        #
        row_sums = np.sum(data, axis=1)
        labels = np.array(np.round(row_sums - 0.5, 0), dtype=int)
        max_label_val = np.max(labels)

        model_obj = NnDenseModel(
            identifier_string = 'nwae_ml_unit_test_math_function',
            dir_path_model    = self.ut_params.dirpath_model,
            # Anything less than this will reduce the accuracy to < 90%
            train_epochs      = 20,
            train_batch_size  = 32
        )
        td = tdm.TrainingDataModel(
            x = data,
            y = labels,
            is_map_points_to_hypersphere = False
        )
        model_obj.set_training_data(td=td)

        #
        # Layers Design
        #
        labels_categorical = to_categorical(labels)
        nn_layers = [
            {
                ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_DENSE,
                ModelInterface.NN_LAYER_OUTPUT_UNITS: 512,
                # First layer just makes sure to output positive numbers with linear rectifier
                ModelInterface.NN_LAYER_ACTIVATION: 'relu',
                ModelInterface.NN_LAYER_INPUT_SHAPE: (td.get_x().shape[1],)
            },
            {
                ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_DENSE,
                ModelInterface.NN_LAYER_OUTPUT_UNITS: max_label_val+1,
                # Last layer uses a probability based output softmax
                ModelInterface.NN_LAYER_ACTIVATION: 'softmax'
            }
        ]

        model_obj.train(
            model_params = nn_layers
        )

        # Load back the model
        model_obj.load_model_parameters()

        loss, accuracy = model_obj.evaluate(
            data   = data,
            labels = labels_categorical
        )
        accuracy_pct = round(accuracy*100, 2)
        Log.info(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Train Accuracy: ' + str(accuracy_pct) + '% on dataset with ' + str(n_rows) + ' rows data'
        )
        res_final.update_bool(res_bool=ut.UnitTest.assert_true(
            # Lowest observed about 89.47%
            observed = (accuracy_pct > NnDenseModelUnitTest.THRESHOLD_PASS_PCT),
            expected = True,
            test_comment = ': Test train accuracy: ' + str(accuracy_pct)
                           + ' on dataset with ' + str(n_rows) + ' rows data'
        ))

        return self.__check_result_of_test(
            data      = data,
            labels    = labels,
            model_obj = model_obj,
            res_obj   = res_final,
            exp_acc   = accuracy_pct
        )

    def test_text_classification(self):
        res_final = ut.ResultObj(count_ok=0, count_fail=0)

        # Training data or Documents
        # Since our labels have a max value of 88, this means in the final layer of the NN,
        # we need 89 outputs, as the NN assumes a 0 index label ends at 88, thus 89 values.
        docs_label = [
            ('잘 했어!', 11), ('잘 했어요!', 11), ('잘 한다!', 11),
            ('Молодец!', 11), ('Супер!', 11), ('Хорошо!', 11),
            ('Плохо!', 50), ('Дурак!', 50),
            ('나쁜!', 50), ('바보!', 50), ('백치!', 50), ('얼간이!', 50),
            ('미친놈', 50), ('씨발', 50), ('개', 50), ('개자식', 50),
            ('젠장', 50),
            ('ok', 88), ('fine', 88)
        ]

        res = TxtTransform(
            docs   = [x[0] for x in docs_label],
            labels = [x[1] for x in docs_label]
        ).create_padded_docs()

        x = res.padded_docs
        y = np.array(res.list_labels)
        n_rows = len(res.padded_docs)
        #print('Padded docs: ' + str(res.padded_docs))
        #print('List labels: ' + str(res.list_labels))
        n_label_output = max(res.list_labels) + 1

        model_obj = NnDenseModel(
            identifier_string = 'nwae_ml_unit_test_text_classification',
            dir_path_model    = self.ut_params.dirpath_model,
            # Anything less than this will reduce the accuracy to < 90%
            train_epochs      = 150,
            train_loss        = 'sparse_categorical_crossentropy'
        )
        td = tdm.TrainingDataModel(
            x = x,
            y = y,
            is_map_points_to_hypersphere = False
        )
        model_obj.set_training_data(td=td)

        #
        # Layers Design
        #
        nn_layers = [
            {
                ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_EMBEDDING,
                ModelInterface.NN_LAYER_OUTPUT_DIM: 8,
                # Usually max sentence length
                ModelInterface.NN_LAYER_INPUT_LEN: res.input_dim_max_length,
                # Usually how many unique vocabulary words
                ModelInterface.NN_LAYER_INPUT_DIM: res.vocabulary_dimension
            },
            {
                ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_FLATTEN
            },
            {
                ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_DENSE,
                ModelInterface.NN_LAYER_OUTPUT_UNITS: n_label_output*5,
                # First layer just makes sure to output positive numbers with linear rectifier
                ModelInterface.NN_LAYER_ACTIVATION: 'relu',
            },
            {
                ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_DENSE,
                ModelInterface.NN_LAYER_OUTPUT_UNITS: n_label_output,
                # Last layer uses a probability based output softmax
                ModelInterface.NN_LAYER_ACTIVATION: 'softmax'
            }
        ]

        model_obj.train(
            model_params = nn_layers,
            convert_train_labels_to_categorical = False
        )

        # Load back the model
        model_obj.load_model_parameters()

        loss, accuracy = model_obj.evaluate(
            data   = res.padded_docs,
            labels = res.list_labels
        )
        accuracy_pct = round(accuracy*100, 2)
        Log.info(
            str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Train Accuracy: ' + str(accuracy_pct) + '% on dataset with '
            + str(n_rows) + ' rows data'
        )
        res_final.update_bool(res_bool=ut.UnitTest.assert_true(
            # Lowest is around 89.47%
            observed = (accuracy_pct > NnDenseModelUnitTest.THRESHOLD_PASS_PCT),
            expected = True,
            test_comment = ': Test train accuracy: ' + str(accuracy_pct)
                           + ' on dataset with ' + str(n_rows) + ' rows data'
        ))

        return self.__check_result_of_test(
            data      = x,
            labels    = y,
            model_obj = model_obj,
            res_obj   = res_final,
            exp_acc   = accuracy_pct
        )

    def test_text_classification_from_sample_data(self):
        from nwae.ml.text.preprocessing.TrDataSampleData import SampleTextClassificationData
        from nwae.ml.text.preprocessing.TrDataPreprocessor import TrDataPreprocessor
        from nwae.lang.nlp.daehua.DaehuaTrainDataModel import DaehuaTrainDataModel
        import pandas as pd

        res_final = ut.ResultObj(count_ok=0, count_fail=0)

        for sample_training_data in SampleTextClassificationData.SAMPLE_TRAINING_DATA:
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

            x = res.padded_docs
            y = np.array(res.list_labels)
            n_rows = len(res.padded_docs)
            # print('Padded docs: ' + str(res.padded_docs))
            # print('List labels: ' + str(res.list_labels))
            n_label_output = max(res.list_labels) + 1

            model_obj = NnDenseModel(
                identifier_string = 'nwae_ml_unit_test_text_classification',
                dir_path_model    = self.ut_params.dirpath_model,
                # Anything less than this will reduce the accuracy to < 90%
                train_epochs      = 100,
                train_loss        = 'sparse_categorical_crossentropy'
            )
            td = tdm.TrainingDataModel(
                x = x,
                y = y,
                is_map_points_to_hypersphere = False
            )
            model_obj.set_training_data(td=td)

            #
            # Layers Design
            #
            nn_layers = [
                {
                    ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_EMBEDDING,
                    ModelInterface.NN_LAYER_OUTPUT_DIM: 8,
                    # Usually max sentence length
                    ModelInterface.NN_LAYER_INPUT_LEN: res.input_dim_max_length,
                    # Usually how many unique vocabulary words
                    ModelInterface.NN_LAYER_INPUT_DIM: res.vocabulary_dimension
                },
                {
                    ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_FLATTEN
                },
                {
                    ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_DENSE,
                    ModelInterface.NN_LAYER_OUTPUT_UNITS: n_label_output * 5,
                    # First layer just makes sure to output positive numbers with linear rectifier
                    ModelInterface.NN_LAYER_ACTIVATION: 'relu',
                },
                {
                    ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_DENSE,
                    ModelInterface.NN_LAYER_OUTPUT_UNITS: n_label_output,
                    # Last layer uses a probability based output softmax
                    ModelInterface.NN_LAYER_ACTIVATION: 'softmax'
                }
            ]

            model_obj.train(
                model_params = nn_layers,
                convert_train_labels_to_categorical = False
            )

            # Load back the model
            model_obj.load_model_parameters()

            loss, accuracy = model_obj.evaluate(
                data   = x,
                labels = y
            )
            accuracy_pct = round(accuracy * 100, 2)
            Log.info(
                str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
                + ': Train Accuracy: ' + str(accuracy_pct) + '% on dataset with '
                + str(n_rows) + ' rows data'
            )
            res_final.update_bool(res_bool=ut.UnitTest.assert_true(
                # Lowest is around 89.47%
                observed=(accuracy_pct > NnDenseModelUnitTest.THRESHOLD_PASS_PCT_LOW),
                expected=True,
                test_comment=': Test train accuracy: ' + str(accuracy_pct)
                             + ' on dataset with ' + str(n_rows) + ' rows data'
            ))

        return res_final


def test_mnist_image_data(
        dirpath_model
):
    model_obj = NnDenseModel(
        identifier_string = 'keras_image_bw_example',
        dir_path_model    = dirpath_model,
        train_epochs      = 5,
        train_batch_size  = 128
    )
    # Disable SSL check to download the data, otherwise will fail SSL check
    from nwae.utils.networking.Ssl import Ssl
    Ssl.disable_ssl_check()

    (mnist_train_images_2d, mnist_train_labels), (mnist_test_images_2d, mnist_test_labels) = \
        MnistData.load_mnist_example_data()

    #np.savetxt("mnist_test_images_2d.csv", kr.mnist_test_images_2d, delimiter=",")
    #np.savetxt("mnist_train_labels.csv", kr.mnist_train_labels, delimiter=",")

    td = tdm.TrainingDataModel(
        x = mnist_train_images_2d,
        y = mnist_train_labels,
        is_map_points_to_hypersphere = False
    )
    model_obj.set_training_data(td = td)

    #
    # Layers Design
    #
    nn_layers = [
        {
            ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_DENSE,
            ModelInterface.NN_LAYER_OUTPUT_UNITS: 512,
            # First layer just makes sure to output positive numbers with linear rectifier
            ModelInterface.NN_LAYER_ACTIVATION:   'relu',
            ModelInterface.NN_LAYER_INPUT_SHAPE:  (td.get_x().shape[1],)
        },
        {
            ModelInterface.NN_LAYER_TYPE: ModelInterface.VALUE_NN_LAYER_TYPE_DENSE,
            ModelInterface.NN_LAYER_OUTPUT_UNITS: to_categorical(td.get_y()).shape[1],
            # Last layer uses a probability based output softmax
            ModelInterface.NN_LAYER_ACTIVATION:   'softmax'
        }
    ]

    print('Training started...')
    model_obj.train(
        model_params = nn_layers
    )
    print('Training done.')

    print('Loading model parameters...')
    model_obj.load_model_parameters()
    test_labels_cat = to_categorical(mnist_test_labels)

    test_loss, test_acc = model_obj.evaluate(mnist_test_images_2d, test_labels_cat)
    print('Test accuracy: ', test_acc)

    prd = model_obj.predict_classes(x=mnist_train_images_2d[0:10])
    print(prd.predicted_classes)

    # import matplotlib.pyplot as plt
    # for i in range(10):
    #     plt.imshow(mnist_train_images[i], cmap=plt.cm.binary)
    #     plt.show()
    return


if __name__ == '__main__':
    import nwae.ml.config.Config as cf
    config = cf.Config.get_cmdline_params_and_init_config_singleton(
        Derived_Class = cf.Config,
        default_config_file = cf.Config.CONFIG_FILE_DEFAULT
    )
    Log.LOGLEVEL = Log.LOG_LEVEL_INFO

    ut_params = ut.UnitTestParams(
        dirpath_wordlist     = config.get_config(param=cf.Config.PARAM_NLP_DIR_WORDLIST),
        postfix_wordlist     = config.get_config(param=cf.Config.PARAM_NLP_POSTFIX_WORDLIST),
        dirpath_app_wordlist = config.get_config(param=cf.Config.PARAM_NLP_DIR_APP_WORDLIST),
        postfix_app_wordlist = config.get_config(param=cf.Config.PARAM_NLP_POSTFIX_APP_WORDLIST),
        dirpath_synonymlist  = config.get_config(param=cf.Config.PARAM_NLP_DIR_SYNONYMLIST),
        postfix_synonymlist  = config.get_config(param=cf.Config.PARAM_NLP_POSTFIX_SYNONYMLIST),
        dirpath_model        = config.get_config(param=cf.Config.PARAM_MODEL_DIR)
    )
    Log.important('Unit Test Params: ' + str(ut_params.to_string()))

    res_ut = NnDenseModelUnitTest(ut_params=ut_params).run_unit_test()
    exit(res_ut.count_fail)
