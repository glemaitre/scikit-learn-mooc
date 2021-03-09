# %% [markdown]
# # 📃 Solution for Exercise 04
#
# The aim of this exercise is to:
#
# * verify if a GBDT tends to overfit if the number of estimators is not
#   appropriate as previously seen for AdaBoost;
# * use the early-stopping strategy to avoid adding unnecessary trees, to
#   get the best statistical performances.
#
# we will use the California housing dataset to conduct our experiments.

# %%
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

data, target = fetch_california_housing(return_X_y=True, as_frame=True)
target *= 100  # rescale the target in k$
data_train, data_test, target_train, target_test = train_test_split(
    data, target, random_state=0, test_size=0.5
)

# %% [markdown]
# Similarly to the previous exercise, create a gradient boosting decision tree
# and create a validation curve to assess the impact of the number of trees
# on the statistical performance of the model.

# %%
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import validation_curve

gbdt = GradientBoostingRegressor()
param_range = np.unique(np.logspace(0, 1.8, num=30).astype(int))
train_scores, test_scores = validation_curve(
    gbdt, data_train, target_train, param_name="n_estimators",
    param_range=param_range, n_jobs=-1)

# %%
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context("talk")

train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

plt.plot(param_range, train_scores_mean, label="Training score")
plt.plot(param_range, test_scores_mean, label="Cross-validation score")

plt.fill_between(param_range,
                 train_scores_mean - train_scores_std,
                 train_scores_mean + train_scores_std,
                 alpha=0.3)
plt.fill_between(param_range,
                 test_scores_mean - test_scores_std,
                 test_scores_mean + test_scores_std,
                 alpha=0.3)

plt.legend()
plt.ylabel("$R^2$ score")
plt.xlabel("# estimators")
_ = plt.title("Validation curve for GBDT regressor")

# %% [markdown]
# Unlike AdaBoost, the gradient boosting model will always improve when
# increasing the number of trees in the ensemble. However, it will reach a
# plateau where adding new trees will just make fitting and scoring slower.
#
# To avoid adding new unnecessary tree, gradient boosting offers an
# early-stopping option. Internally, the algorithm will use an out-of-sample
# set to compute the statistical performance of the model at each addition of a
# tree. Thus, if the statistical performance are not improving for several
# iterations, it will stop adding trees.
#
# Now, create a gradient-boosting model with `n_estimators=1000`. This number
# of trees will be too large. Change the parameter `n_iter_no_change` such
# that the gradient boosting fitting will stop after adding 5 trees that do not
# improve the overall statistical performance.

# %%
gbdt = GradientBoostingRegressor(n_estimators=1000, n_iter_no_change=5)
gbdt.fit(data_train, target_train)
gbdt.n_estimators_

# %% [markdown]
# We see that the number of trees used is far below 1000 with the current
# dataset. Training the GBDT with the entire 1000 trees would have been
# useless.
