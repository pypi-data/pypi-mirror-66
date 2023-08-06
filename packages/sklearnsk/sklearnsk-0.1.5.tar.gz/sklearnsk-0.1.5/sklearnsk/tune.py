import os
import time
import pickle
import json
import tqdm
import math

import numpy as np

from sklearn import model_selection, metrics

from abc import ABC, abstractmethod

from . import helpers

class ParameterSearchRecord():
    """
    Saves the results of a parameter search to file, so it can be resumed
    """

    def __init__(self, path, direction=None):

        if direction is None:
            direction = 'max'

        self.path = path

        if os.path.isfile(path):
            with open(path, "rb") as f:
                data = pickle.load(f)

                self.allConfigsAndScores = data.get('allConfigsAndScores', [])
                self.randomSeed = data.get('randomSeed', int(time.time()))
                self.direction = data.get('direction', 'max')

            f.close()
        else:
            self.allConfigsAndScores = []
            self.randomSeed = int(time.time())
            self.direction = direction

        self.scoresByConfigKey = {}

        self.bestConfig = None
        self.bestScore = None

        for (config, score) in self.allConfigsAndScores:
            key = self.__get_config_key(config)

            self.scoresByConfigKey[key] = score

            if self.__is_best(score):
                self.bestConfig = config
                self.bestScore = score

        print(' - recovered {} previously searched parameter permutations'.format(len(self.allConfigsAndScores)))
        print(' - best score so far is {}'.format(self.bestScore))

    def __is_best(self, score):

        if self.bestScore is None:
            return True

        if self.direction == 'max':
            return score > self.bestScore
        else:
            return score < self.bestScore

    def __get_config_key(self, config):

        return json.dumps(config, sort_keys=True)

    def update(self, config, score):

        self.allConfigsAndScores.append((config, score))

        if self.__is_best(score):
            self.bestConfig = config
            self.bestScore = score

        with open(self.path, "wb") as f:
            pickle.dump(
                {
                    'allConfigsAndScores': self.allConfigsAndScores,
                    'randomSeed': self.randomSeed,
                    'direction': self.direction
                }
                , f)

        f.close()

    def getScore(self, config):
        key = self.__get_config_key(config)
        return self.scoresByConfigKey.get(key)


class GridParameterSearcher(ABC):
    """
    This provides a tool to exhaustively evaluate different combinations of parameters.
    """

    @abstractmethod
    def initialize_algorithm(self, config):
        """
        Initializes an algorithm (which must extend ConfigurableAlgorithm) with the given configuration

        :param config: a configuration for the algorithm
        :param runs: the number of seperate runs to perform
        :return the initialized, configured algorithm
        """

        pass

    def __init__(self, items, labels=None, scores=None, scorer=None, scorer_config=None):
        """
        Initializes the GridSearcher, with the given dataset of items and labels

        :param items: an array of items
        :param labels: an array of ground-truth labels, to be specified if you are performing classification
        :param scores: an array of ground-truth scores, to be specified if you are performing regression
        """

        self.dataset = helpers.Dataset(items, labels, scores)

        if scorer is None:
            if self.dataset.for_classification():
                self.scorer = 'f1_score'
            else:
                self.scorer = 'r2_score'
        else:
            self.scorer = scorer

        if scorer_config is None:
            if self.dataset.for_classification() and not self.dataset.is_binary():
                self.scorer_config = {'average': 'micro'}
            else:
                self.scorer_config = {}
        else:
            self.scorer_config = scorer_config

    def do_search(self, configs, record, n_runs=1, n_folds=5, on_fold_completed=None):

        grid = model_selection.ParameterGrid(configs)

        print("{} distinct configurations to test".format(len(grid)))

        with tqdm.tqdm(total=len(grid) * n_runs * n_folds) as progress:

            for config in grid:

                score = record.getScore(config)

                # skip this set of parameters if we already have a record of it
                if (score is not None):
                    progress.update(n_runs * n_folds)
                    continue

                scores = []

                for run in range(0, n_runs):

                    folds = self.dataset.build_folds(n_folds)

                    gold = []
                    pred = None

                    for train_index, test_index in folds:

                        X_train, X_test = self.dataset.items[train_index], self.dataset.items[test_index]

                        if self.dataset.type == 'c':
                            y_train, y_test = self.dataset.labels[train_index], self.dataset.labels[test_index]
                        else:
                            y_train, y_test = self.dataset.scores[train_index], self.dataset.scores[test_index]

                        gold = np.concatenate((gold, y_test))

                        alg = self.initialize_algorithm(config)
                        alg.fit(X_train, y_train)

                        if self.scorer == 'roc_auc_score':
                            fold_pred = alg.predict_proba(X_test)
                        else:
                            fold_pred = alg.predict(X_test)

                        if pred is None:
                            pred = fold_pred
                        else:
                            pred = np.concatenate((pred, fold_pred))

                        progress.update(1)

                        if on_fold_completed is not None:
                            on_fold_completed()

                    scores.append(helpers.get_score(gold, pred, self.scorer, self.scorer_config))

                record.update(config, np.mean(scores))

        return record.bestConfig, record.bestScore


class RandomParameterSearcher(ABC):
    """
    This provides a tool to randomly search for the best combinations of parameters.
    """

    @abstractmethod
    def initialize_algorithm(self, config):
        """
        Initializes an algorithm (which must extend ConfigurableAlgorithm) with the given configuration

        :param config: a configuration for the algorithm
        :return the initialized, configured algorithm
        """

        pass

    def __init__(self, items, labels=None, scores=None, scorer=None, scorer_config=None):
        """
        Initializes the GridSearcher, with the given dataset

        :param items: an array of items
        :param labels: an array of ground-truth labels, to be specified if you are performing classification
        :param scores: an array of ground-truth scores, to be specified if you are performing regression
        """

        self.dataset = helpers.Dataset(items, labels, scores)

        if scorer is None:
            if self.dataset.for_classification():
                self.scorer = 'f1_score'
            else:
                self.scorer = 'r2_score'
        else:
            self.scorer = scorer

        if scorer_config is None:
            if self.dataset.for_classification() and not self.dataset.is_binary():
                self.scorer_config = {'average': 'micro'}
            else:
                self.scorer_config = {}
        else:
            self.scorer_config = scorer_config

    def do_search(self, param_distributions, record, budget=100, n_runs=1, n_folds=5, verbose=False, on_fold_completed=None):

        with tqdm.tqdm(total=budget * n_runs * n_folds) as progress:

            configs = list(model_selection.ParameterSampler(param_distributions, budget, record.randomSeed))
            for c in configs:

                config = self.__get_rounded_config(c)

                score = record.getScore(config)

                # skip this set of parameters if we already have a record of it
                if (score is not None):
                    if verbose:
                        print(config, score)

                    progress.update(n_runs * n_folds)
                    continue

                scores = []

                for run in range(0, n_runs):

                    folds = self.dataset.build_folds(n_folds)

                    gold = []
                    pred = None

                    for train_index, test_index in folds:

                        X_train, X_test = self.dataset.items[train_index], self.dataset.items[test_index]

                        if self.dataset.type == 'c':
                            y_train, y_test = self.dataset.labels[train_index], self.dataset.labels[test_index]
                        else:
                            y_train, y_test = self.dataset.scores[train_index], self.dataset.scores[test_index]

                        gold = np.concatenate((gold, y_test))

                        alg = self.initialize_algorithm(config)
                        alg.fit(X_train, y_train)

                        if self.scorer == 'roc_auc_score':
                            fold_pred = alg.predict_proba(X_test)
                        else:
                            fold_pred = alg.predict(X_test)

                        if pred is None:
                            pred = fold_pred
                        else:
                            pred = np.concatenate((pred, fold_pred))

                        progress.update(1)

                        if on_fold_completed is not None:
                            on_fold_completed()

                    scores.append(helpers.get_score(gold, pred, self.scorer, self.scorer_config))

                score = np.mean(scores)
                record.update(config, score)

                if verbose:
                    print(config, score)

        return record.bestConfig, record.bestScore

    def do_search_with_testset(self, param_distributions, record, X_test, y_test, budget=100, verbose=False):

        with tqdm.tqdm(total=budget) as progress:

            configs = list(model_selection.ParameterSampler(param_distributions, budget, record.randomSeed))
            for c in configs:

                config = self.__get_rounded_config(c)

                score = record.getScore(config)

                # skip this set of parameters if we already have a record of it
                if (score is not None):
                    if verbose:
                        print(config, score)

                    progress.update(n_runs * n_folds)
                    continue

                scores = []


                X_train = self.dataset.items

                if self.dataset.type == 'c':
                    y_train = self.dataset.labels
                else:
                    y_train = self.dataset.scores,

                alg = self.initialize_algorithm(config)
                alg.fit(X_train, y_train)

                if self.scorer == 'roc_auc_score':
                    pred = alg.predict_proba(X_test)
                else:
                    pred = alg.predict(X_test)

                record.update(config, helpers.get_score(y_test, pred, self.scorer, self.scorer_config))

                progress.update(1)

                if verbose:
                    print(config, score)

        return record.bestConfig, record.bestScore

    def __get_rounded_config(self, config):

        rounded = {}
        for (key, value) in config.items():

            if isinstance(value, (float, complex)):
                rounded[key] = self.__round_to_n(value, 3)
            else:
                rounded[key] = value

        return rounded

    def __round_to_n(self, x, n):
        return round(x, -int(math.floor(math.log10(abs(x)))) + (n - 1))


