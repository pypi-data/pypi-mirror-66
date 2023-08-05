# -*- coding: utf-8 -*-

from nwae.utils.Log import Log
from inspect import currentframe, getframeinfo
from nwae.ml.ModelInterface import ModelInterface
from nwae.math.NumpyUtil import NumpyUtil
import nwae.utils.UnitTest as ut

try:
    from keras import models
    from keras import layers
    from keras.utils import to_categorical
    from keras.models import load_model
except Exception as ex_keras:
    Log.warning(
        str(__name__) + ' ' + str(getframeinfo(currentframe()).lineno)
        + ': Exception importing Keras modules: ' + str(ex_keras)
    )


class NnDenseModel(ModelInterface):

    MODEL_NAME = 'nn_dense'

    def __init__(
            self,
            # Unique identifier to identify this set of trained data+other files after training
            identifier_string,
            # Directory to keep all our model files
            dir_path_model,
            train_epochs        = 10,
            train_batch_size    = None,
            train_optimizer     = 'rmsprop',
            # 'sparse_categorical_crossentropy', etc.
            train_loss          = 'categorical_crossentropy',
            evaluate_metrics    = ('accuracy'),
            # Training data in TrainingDataModel class type
            training_data       = None,
            do_profiling        = False,
            # Train only by y/labels and store model files in separate y_id directories
            is_partial_training = False
    ):
        super().__init__(
            model_name          = NnDenseModel.MODEL_NAME,
            identifier_string   = identifier_string,
            dir_path_model      = dir_path_model,
            training_data       = training_data,
            is_partial_training = is_partial_training
        )

        self.identifier_string = identifier_string
        self.dir_path_model = dir_path_model
        self.train_epochs = train_epochs
        self.train_batch_size = train_batch_size
        self.train_optimizer = train_optimizer
        self.train_loss = train_loss
        self.evaluate_metrics = evaluate_metrics
        # Keras accepts only list/tuple type
        if type(self.evaluate_metrics) not in (list, tuple):
            self.evaluate_metrics = [self.evaluate_metrics]

        self.training_data = training_data
        if self.training_data is not None:
            self.check_training_data()
        self.is_partial_training = is_partial_training

        self.filepath_model = ModelInterface.get_model_file_prefix(
            dir_path_model      = self.dir_path_model,
            model_name          = self.model_name,
            identifier_string   = self.identifier_string,
            is_partial_training = self.is_partial_training
        )
        self.network = None
        self.model_loaded = False

        self.do_profiling = do_profiling
        return

    def is_model_ready(self):
        return self.model_loaded

    def set_training_data(
            self,
            td
    ):
        self.training_data = td
        self.check_training_data()

    def get_model_features(
            self
    ):
        return None
        #raise Exception('How to find the number of columns in the network?')

    def predict_class(
            self,
            # ndarray type of >= 2 dimensions, single point/row array
            x,
            top = 5
    ):
        self.wait_for_model()
        if top == 1:
            # This will only return the top match
            top_match = self.network.predict_classes(x=x)
            return NnDenseModel.predict_class_retclass(
                predicted_classes = top_match
            )
        else:
            # This will return the last layer NN output, thus we can rank them
            prob_distribution = self.network.predict(x=x)
            top_x_matches = NumpyUtil.get_top_indexes(
                data      = prob_distribution[0],
                ascending = False,
                top_x     = top
            )
            return NnDenseModel.predict_class_retclass(
                predicted_classes = top_x_matches
            )

    def predict_classes(
            self,
            # ndarray type of >= 2 dimensions
            x
    ):
        self.wait_for_model()
        p = self.network.predict_classes(x=x)
        return NnDenseModel.predict_class_retclass(
            predicted_classes = p
        )

    def train(
            self,
            write_model_to_storage = True,
            write_training_data_to_storage = False,
            model_params = None,
            # Option to train a single y ID/label
            y_id = None,
            # Transform train labels to categorical or not
            convert_train_labels_to_categorical = True
    ):
        Log.info(
            str(self.__class__) + str(getframeinfo(currentframe()).lineno)
            + ': Training for data, x shape '  + str(self.training_data.get_x().shape)
            + ', train labels with shape ' + str(self.training_data.get_y().shape)
        )

        x = self.training_data.get_x().copy()
        y = self.training_data.get_y().copy()
        # Convert labels to categorical one-hot encoding
        train_labels_categorical = to_categorical(y)

        n_labels = len(list(set(y.tolist())))
        Log.info(
            str(self.__class__) + str(getframeinfo(currentframe()).lineno)
            + ': Total unique labels = ' + str(n_labels) + '.'
        )

        network = models.Sequential()

        try:
            for i_layer in range(len(model_params)):
                ly = model_params[i_layer]
                layer_type = ly[ModelInterface.NN_LAYER_TYPE]
                if layer_type == ModelInterface.VALUE_NN_LAYER_TYPE_DENSE:
                    if i_layer == 0:
                        network.add(
                            layers.Dense(
                                units       = ly[ModelInterface.NN_LAYER_OUTPUT_UNITS],
                                activation  = ly[ModelInterface.NN_LAYER_ACTIVATION],
                                input_shape = ly[ModelInterface.NN_LAYER_INPUT_SHAPE]
                            )
                        )
                    else:
                        network.add(
                            layers.Dense(
                                units      = ly[ModelInterface.NN_LAYER_OUTPUT_UNITS],
                                activation = ly[ModelInterface.NN_LAYER_ACTIVATION]
                            )
                    )
                elif layer_type == ModelInterface.VALUE_NN_LAYER_TYPE_EMBEDDING:
                    # Embedding layers are not part of the NN optimization, its only function
                    # is to transform the input to a standard NN form
                    network.add(
                        # Embedding layers are usually for text data
                        layers.embeddings.Embedding(
                            # Must be at least the size of the unique vocabulary
                            input_dim    = ly[ModelInterface.NN_LAYER_INPUT_DIM],
                            # How many words, or length of word input vector
                            input_length = ly[ModelInterface.NN_LAYER_INPUT_LEN],
                            # Each word represented by a vector of dimension 8 (for example)
                            output_dim   = ly[ModelInterface.NN_LAYER_OUTPUT_DIM]
                        )
                    )
                elif layer_type == ModelInterface.VALUE_NN_LAYER_TYPE_FLATTEN:
                    # Usually comes after an embedding layer, does nothing but to convert
                    # a 2 dimensional input to a 1-dimensional output by the usual "flattening"
                    network.add(layers.Flatten())
                else:
                    raise Exception('Unrecognized layer type "' + str(layer_type) + '"')
        except Exception as ex_layers:
            errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                     + ': Error creating network layers for config: ' + str(model_params) \
                     +'. Exception: ' + str(ex_layers)
            Log.error(errmsg)
            raise Exception(errmsg)

        try:
            network.compile(
                optimizer = self.train_optimizer,
                loss      = self.train_loss,
                metrics   = self.evaluate_metrics
            )
        except Exception as ex_compile:
            errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                     + ': Error compiling network for config: ' + str(model_params) \
                     +'. Exception: ' + str(ex_compile)
            Log.error(errmsg)
            raise Exception(errmsg)

        # Log model summary
        network.summary(print_fn=Log.info)

        Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + 'Categorical Train label shape "' + str(train_labels_categorical.shape)
            + '":\n\r' + str(train_labels_categorical)
        )

        try:
            # print('***** x: ' + str(x))
            # print('***** y: ' + str(train_labels_categorical))
            train_labels = y
            if convert_train_labels_to_categorical:
                train_labels = train_labels_categorical
            if self.train_batch_size is not None:
                network.fit(
                    x,
                    train_labels,
                    epochs     = self.train_epochs,
                    batch_size = self.train_batch_size
                )
            else:
                network.fit(
                    x,
                    train_labels,
                    epochs    = self.train_epochs,
                )
        except Exception as ex_fit:
            errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno) \
                     + ': Error training/fitting network for config: ' + str(model_params) \
                     +'. Exception: ' + str(ex_fit)
            Log.error(errmsg)
            raise Exception(errmsg)

        self.network = network

        if write_model_to_storage:
            self.persist_model_to_storage(network=network)
        if write_training_data_to_storage:
            self.persist_training_data_to_storage(td=self.training_data)

        self.model_loaded = True
        return

    def evaluate(
            self,
            data,
            # If required, labels must be converted to_categorical() by caller,
            # as certain NN architecture that uses flatten layers won't require it
            # while others will need it
            labels
    ):
        return self.network.evaluate(data, labels)

    def load_model_parameters(
            self
    ):
        try:
            self.network = load_model(self.filepath_model)
            self.model_loaded = True
        except Exception as ex:
            errmsg = str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)\
                     + ': Model "' + str(self.identifier_string)\
                     + '" failed to load from file "' + str(self.filepath_model)\
                     + '". Got exception ' + str(ex) + '.'
            Log.error(errmsg)
            raise Exception(errmsg)

    def persist_model_to_storage(
            self,
            network = None
    ):
        self.network.save(self.filepath_model)
        Log.info(
            str(self.__class__) + ' ' + str(getframeinfo(currentframe()).lineno)
            + ': Saved network to file "' + self.filepath_model + '".'
        )
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

    from nwae.ml.nndense.NnDenseModelUnitTest import NnDenseModelUnitTest
    res_ut = NnDenseModelUnitTest(ut_params=ut_params).run_unit_test()
    exit(res_ut.count_fail)
