from sklearn.datasets import load_boston
from sklearn.linear_model import Lasso
import matplotlib.pyplot as plt
import numpy as np
import sparsereg.preprocessing.symfeat as sf

from sparsereg.model import STRidge
from sparsereg.util.net import net

data = load_boston()
x, y = data.data, data.target
exponents = [1]
operators = {}
sym = sf.SymbolicFeatures(exponents=exponents, operators=operators)
features = sym.fit_transform(x)
ests = [Lasso, STRidge]
attrs = ["alpha", "threshold"]
names = ["Lasso", "STRidge"]
for est, attr, name in zip(ests, attrs, names):
    models = net(est, features, y, attr, filter=True, max_coarsity=5, r_max=1e5)
    m = sorted(models)
    scores = np.array([models[k].score(features, y) for k in m])
    plt.plot(m, scores, 'o--', label=name)
plt.legend()
plt.xlabel("# coefficient")
plt.ylabel(r"$R^2$")
plt.gca().invert_xaxis()
plt.show()
