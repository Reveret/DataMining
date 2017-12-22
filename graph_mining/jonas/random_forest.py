from sklearn.ensemble import RandomForestClassifier


def run_random_forest(X_train, y_train, X_test, y_test):
    """
    Train a RandomForest and evaluate on the test set
    :param X_train: Training matrix
    :param y_train: Training ground-truth
    :param X_test: Testing matrix
    :param y_test: Testing ground-truth
    :return: Prediction score
    """
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(X=X_train, y=y_train)
    score = rf.score(X_test, y_test)
    return score

