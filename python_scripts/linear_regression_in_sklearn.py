# %% [markdown]
# # Linear regression using scikit-learn
#
# In the previous notebook, we presented the parametrization of a linear model.
# During the exercise, you saw that varying parameters will give different
# that will fit better or worse the data. To evaluate quantitatively this
# goodness of fit, you implemented a so-called metric.
#
# When doing machine-learning, you are interested to select the model which
# will minimize the error on the data available. From the previous exercise,
# we could implement a brute-force approach, varying the weights and intercept
# and select the model with the lowest error.
#
# Hopefully, this problem of finding the best parameters values (i.e. that
# result in the lowest error) can be solved without the need to check every
# potential parameter combination. Indeed, this problem has a closed-form
# solution: the best parameter values can be found by solving an equation. This
# avoids the need for brute-force search. This strategy is implemented in
# scikit-learn.

# %%
import pandas as pd

data = pd.read_csv("../datasets/penguins.csv")
# select the features of interest
feature_names = "Flipper Length (mm)"
target_name = "Body Mass (g)"
X = data[[feature_names]].dropna()
y = data[target_name].dropna()


# %%
from sklearn.linear_model import LinearRegression

linear_regression = LinearRegression()
linear_regression.fit(X, y)

# %% [markdown]
# The instance `linear_regression` will store the parameter values in the
# attributes `coef_` and `intercept_`. We can check what the optimal model
# found is:

# %%
weight_flipper_length = linear_regression.coef_[0]
weight_flipper_length

# %%
intercept_body_mass = linear_regression.intercept_
intercept_body_mass

# %% [markdown]
# We will use the weight and intercept to plot the model found using the
# scikit-learn.
#
# First, we need to redefine the helper functions saw in the previous notebook.


# %%
def linear_model_flipper_mass(
    flipper_length, weight_flipper_length, intercept_body_mass
):
    """Linear model of the form y = a * x + b"""
    body_mass = weight_flipper_length * flipper_length + intercept_body_mass
    return body_mass


# %%
import seaborn as sns
import matplotlib.pyplot as plt


# %% [markdown]
# ### Data and model visualization


def plot_data_and_model(
    flipper_length_range, weight_flipper_length, intercept_body_mass,
    ax=None,
):
    """Compute and plot the prediction."""
    inferred_body_mass = linear_model_flipper_mass(
        flipper_length_range,
        weight_flipper_length=weight_flipper_length,
        intercept_body_mass=intercept_body_mass,
    )

    if ax is None:
        _, ax = plt.subplots()

    sns.scatterplot(data=data, x=feature_names, y=target_name, ax=ax)
    ax.plot(
        flipper_length_range,
        inferred_body_mass,
        linewidth=3,
        label=(
            f"{weight_flipper_length:.2f} (g / mm) * flipper length + "
            f"{intercept_body_mass:.2f} (g)"
        ),
    )
    plt.legend()

# %% [markdown]
# Now, we can use the weight and intercept of the scikit-learn model to make
# the plot.

# %%
import numpy as np
flipper_length_range = np.linspace(X.min(), X.max(), num=300)
plot_data_and_model(
    flipper_length_range, weight_flipper_length, intercept_body_mass
)

# %%
# In the solution of the previous exercise, we implemented a function to
# compute the error of the model. Instead of using it, we will import the
# metric directly from scikit-learn.

# %%
from sklearn.metrics import mean_squared_error

inferred_body_mass = linear_regression.predict(X)
model_error = mean_squared_error(y, inferred_body_mass)
print(f"The error of the optimal model is {model_error:.2f}")

# %% [markdown]
# In this notebook, you saw how to train a linear regression model using
# scikit-learn.
