"""
Check the "machine learning map" for choosing the right algorithm:
https://scikit-learn.org/stable/tutorial/machine_learning_map/.

"""
import logging
from pprint import pprint

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        # logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

# classification metrics imports
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

DEFAULT_CLASSIFIERS = {
    "SVM": SVC(),
    "LogisticRegression": LogisticRegression(max_iter=100),
    "KNN": KNeighborsClassifier(),
    "RandomForest": RandomForestClassifier(max_depth=None, n_estimators=100),
    "AdaBoost": AdaBoostClassifier(),
    "NaiveBayes": GaussianNB()
}

_logger = logging.getLogger(name=__file__)


class SuperClassifier:
    def __init__(self, classifiers=None):
        if classifiers is None:
            self.classifiers = DEFAULT_CLASSIFIERS
        else:
            # check input params
            if not isinstance(classifiers, dict):
                raise ValueError(f"parameter classifiers is of type {type(classifiers)}, but dict is expected")
            self.classifiers = classifiers

    def predict(self, X):
        predictions = {}
        for name, clf in self.classifiers.items():
            _logger.debug(f"making predictions with model {name}")
            y_pred = clf.predict(X)
            predictions[name] = y_pred
        return predictions

    def fit(self, X, y):
        for name, clf in self.classifiers.items():
            _logger.debug(f"fitting model {name}")
            try:
                clf.fit(X, y)
            except Exception as e:
                print(e)

    def evaluate(self, X, y, print_report=False):
        evaluation_results = {}
        for name, clf in self.classifiers.items():
            _logger.debug(f"evaluating model {name}")
            y_pred = clf.predict(X)
            if print_report:
                res = classification_report(y_true=y, y_pred=y_pred, output_dict=False)
                print(f"{name} classification report: \n", res)
            else:
                res = classification_report(y_true=y, y_pred=y_pred, output_dict=True)
                evaluation_results[name] = res
        return evaluation_results
