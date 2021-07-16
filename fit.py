from extraction import create_table
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split as tts
import numpy as np
"""
get_svm is a simple support vector machine classifier that
uses a linear kernel to predict whether or not a given baseball
player will make the Hall of Fame

It takes the dataframe collected from the lahman databse created
from create_table
"""


def get_svm():
    df, df2, y = create_table()
    x = df[0:1000]
    y = y[0:1000]
    x_train, x_test, y_train, y_test = tts(x, y, test_size=0.25)
    clf = svm.SVC(kernel='linear', C=1.0)
    predictor = clf.fit(x_train, y_train)
    return predictor, x_test, y_test
