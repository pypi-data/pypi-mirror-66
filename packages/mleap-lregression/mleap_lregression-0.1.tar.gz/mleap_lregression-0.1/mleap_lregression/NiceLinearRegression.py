import numpy as np
import matplotlib.pyplot as plt


class NiceLinearRegression:

    def __init__(self, fit_intercept=True):
        """
        :param fit_intercept: Bool to indicate an inclusion of the intercept term in the model
        :rtype: None
        """
        self.coef_ = None
        self.intercept_ = None
        self._fit_intercept = fit_intercept
        self.is_fitted = False
        self.features_ = None
        self.target_ = None

    # Overrides builtin method returning the string object representation
    # Compare with __repr__ with extra details for developers to view
    def __str__(self):
        return "A nice linear regression model instance."

    def fit(self, X, y):
        """
        Estimate the model coefficients based on the data and target.

        :param X: 1D or 2D numpy array
        :param y: 1D numpy array
        """
        # Verify if X is 1D or 2D
        if len(X.shape) == 1:
            X = X.reshape(-1, 1)

        # features and data
        self.features_ = X
        self.target_ = y

        # Add column with a bias term if fit_intercept is True
        if self._fit_intercept:
            X_biased = np.c_[np.ones(X.shape[0]), X]  # c_ add along second (column) axis, before X
        else:
            X_biased = X

        # Coefficient estimation solution X'X**-1 * X'y
        xTx = np.dot(X_biased.T, X_biased)
        inv_xTx = np.linalg.inv(xTx)
        xTy = np.dot(X_biased.T, y)
        coef = np.dot(inv_xTx, xTy)

        # coefficients and intercept values
        if self._fit_intercept:
            self.intercept_ = coef[0]
            self.coef_ = coef[1:]
        else:
            self.intercept_ = 0
            self.coef_ = coef

        # Predict y based of the estimated coefficients
        self.fitted_ = np.dot(X, self.coef_) + self.intercept_

    def plot_fitted(self, line=True):
        """
        Plot fitted data against the true target
        :param line: Boolean to draw a 45 degree reference line
        :return: None
        """
        plt.title("True versus fitted values", fontsize=14)
        plt.scatter(self.target_, self.fitted_, s=100, alpha=0.75, color='red', edgecolor='k')
        if line:
            plt.plot(self.target_, self.target_, c='k', linestyle='dotted')
            plt.xlabel('True values')
            plt.ylabel('Predicted values')
            plt.grid(True)
            plt.show()

    def predict(self, X):
        """
        Predict y values for new data
        :param X: 1D or 2D numpy array
        :return: 1D numpy array
        """
        # Verify if X is 1D or 2D
        if len(X.shape) == 1:
            X = X.reshape(-1, 1)
        self.predicted_ = np.dot(X, self.coef_) + self.intercept_
        return self.predicted_


######### TESTING ########
#
# mle = NiceLinearRegression(fit_intercept=True)
# print(mle)
# print(mle.intercept_)
#
# # Generate random data for test
# # Set seed to have stable results
# X = 10 * np.random.random(size=(20, 2))  # Generate two features
# y = 3.5 * X.T[0] - 1.2 * X.T[1] + 2 * np.random.randn(20)  # Target based on feature 1 and 2 plus noise
#
# mle.fit(X, y)
# print("Regression coefficients {} and the intercept term {}".format(mle.coef_, mle.intercept_))
# mle.plot_fitted()
# y_pred = mle.predict((X))
