from abc import ABC, abstractmethod

from . import helpers

import dill

class ConfigurableAlgorithm(ABC):
    """
    This provides an abstract class that your classifier or regressor should extend.

    If you do this, it will be structured in a way that makes it easy to incorporate into
    cross-validation and grid-search experiments.
    """

    def __init__(self, config):
        """
        Initialize, with the given configuration.

        This configuration should include everything you can possibly configure about your algorithm,
        such as which feature groups to use (so you can easily do feature ablation),
        how you want features to be generated (e.g. unigrams vs ngrams vs skip grams vs embeddings)
        (so you can easily compare them).

        The configuration should also include a value for the key 'algorithm' which defines classification or
        regression algorithm to use (e.g. SVM, RandomForest, etc), and any hyperparameters needed to tune the
        it (so you can easily optimize these with a grid search).

        :param config: A dict of parameters used to configure and tune the algorithm.
        """

        # classifier hasn't been trained yet
        self.fitted = False

        # set up  config
        self.config = {}

        # copy default params
        for key, value in self.get_default_config().items():
            self.config[key] = value

        # then overwrite with those that are passed in
        for key, value in config.items():
            self.config[key] = value

        self.algorithm = None
        self.precomputed_feature_vectors = None

    @abstractmethod
    def get_default_config(self):

        pass

    @abstractmethod
    def get_custom_config_param_names(self):
        """
        Gets a list of all the custom parameter names that can be used in configurations.
        Everything left over must be specific to configuring the classification or regression algorithm.

        :return: a list of custom parameter names that can be used in configurations.
        """

        pass

    @abstractmethod
    def build_feature_vectors(items, labelsOrScores=None):
        """
        builds a 2d array of features (where each row represents an item, and each column is a feature).

        This is called during both training/fitting and testing/predicting. In training stage, you should
        specify the labels so you can fit normalizers, imputers, feature selectors, etc. These should be built as
        a side-effect of calling this method.

        In testing stage, you should not specify the labels or scores, so you can be sure there is no cross-contamination.


        :param items: an array of items, each of which will be used to generate features
        :param labelsOrScores: the (optional) ground truth labels or scores, to be used only during training/fitting
        :return: the built features.
        """

        pass

    def construct_pretraining_data(self, items, labelsOrScores=None):

        vectors = self.build_feature_vectors(items, labelsOrScores)

        data = self.prepare_saved_data()
        data['vectors'] = vectors

        return data

    def load_pretraining_data(self, data):

        self.handle_loaded_data(data)
        self.precomputed_feature_vectors = data['vectors']

    def fit(self, items, labelsOrScores, sample_weight=None):
        """
        fits (i.e. trains) your algorithm using the given labeled data.
        After this call you will be able to call pred to automatically label the unlabeled data.

        :param items: an array of items, each of which will be used to generate features
        :param labels: the ground truth labels
        :return:
        """

        assert self.fitted is False

        if self.precomputed_feature_vectors is not None:
            features = self.precomputed_feature_vectors
        else:
            features = self.build_feature_vectors(items, labelsOrScores)

        algorithm_name = self.config.get('algorithm', 'RandomForestClassifier')
        algorithm_conf = self.__get_algorithm_config()

        self.algorithm = helpers.initialize_algorithm(algorithm_name, algorithm_conf)
        self.algorithm.fit(features, labelsOrScores, sample_weight)

        self.fitted = True

    def predict(self, items):
        """
        uses the previously fitted algorithm to automatically infer labels (for classification) or scores (for regression)

        :param items: an array of items, each of which will be labeled or scored
        :return: an array of automatically generated labels or scores
        """

        assert self.fitted is True

        features = self.build_feature_vectors(items, None)

        return self.algorithm.predict(features)

    def predict_proba(self, items):
        """
        uses the previously fitted algorithm to automatically infer probabilities for labels. This will only work for classification.

        :param items: an array of items, each of which will be labeled
        :return: an array of automatically generated probabilities for labels
        """

        assert self.fitted is True

        features = self.build_feature_vectors(items, None)

        return self.algorithm.predict_proba(features)

    @abstractmethod
    def prepare_saved_data(self):

        pass

    @abstractmethod
    def handle_loaded_data(self, data):

        pass

    def save(self, path):

        assert self.fitted is True

        data = self.prepare_saved_data()

        data['_config'] = self.config
        data['_algorithm'] = self.algorithm

        dill.dump(data, open(path, "wb"))

    def load(self, path):

        data = dill.load(open(path, "rb"))

        self.config = data['_config']
        self.algorithm = data['_algorithm']

        self.fitted = True

        self.handle_loaded_data(data)

    def __get_algorithm_config(self):

        algorithm_conf = {}

        custom_param_names = self.get_custom_config_param_names()

        for key, value in self.config.items():

            if key in ['algorithm', 'id']:
                continue

            if key in custom_param_names:
                continue

            algorithm_conf[key] = value

        return algorithm_conf

