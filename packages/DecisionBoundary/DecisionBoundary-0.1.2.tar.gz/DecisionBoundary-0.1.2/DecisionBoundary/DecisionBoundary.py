from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

class DecisionBoundary():
    """DecisionBoundary class for plotting the decision boundary of supervised
    classification model, such as neive_bayes, svm, decition tree etc.

    Attributes:
        clf (model) representing the fitted model object.
        X (features - numeric matrix) representing the features to predict the target.
        y (array) representing the target of the prediction.
    """

    def __init__(self, clf, X, y):
        self.clf = clf
        self.X = X
        self.y = y

    def get_pca(self):
        """Function to decrease the dimention of the features to 2d PCA for visulization.

        Args:
            None
        Returns: pc1 (primary) and pc2 (secondary)
        """
        self.X = preprocessing.StandardScaler().fit_transform(self.X)
        pca = PCA(n_components=2)
        components = pca.fit_transform(self.X)
        return components


    def DecisionBoundary(self, test_size=0.2, random_state=0):
        """Function to decrease the dimention of the features to 2d PCA for visulization.

        Args:
            test_size (float) between 0 and 1 indicating the test test_size
            random_state (int) representing the random seeds
        Returns: visulization of the decision boundary
        """
        data = self.get_pca()
        df = pd.DataFrame(data=data, columns=['pc1', 'pc2'])
        df['target'] = self.y
        X = df[['pc1', 'pc2']]
        y = df['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        # refit the model to pca
        pca_clf = self.clf.fit(X_train, y_train)
        
        h = .02  # step size in the mesh

        # Create color maps
        cmap_light = ListedColormap(['#FDAB9F', '#CFF4D2', '#AFAFC7'])
        cmap_bold = ListedColormap(['#FE7D6A', '#329D9C', '#5F7DAF'])

        #Plot the decision boundary. For that, we will assign a color to each
        # point in the mesh [x_min, x_max]x[y_min, y_max].
        x_min, x_max = X.iloc[:, 0].min() - 1, X.iloc[:, 0].max() + 1
        y_min, y_max = X.iloc[:, 1].min() - 1, X.iloc[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        Z = pca_clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        plt.figure(figsize=(8, 8))
        plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

        # Plot also the training points
        plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y, cmap=cmap_bold)
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        plt.show()