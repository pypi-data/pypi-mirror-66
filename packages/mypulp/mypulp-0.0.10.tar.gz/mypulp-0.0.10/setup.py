# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mypulp']

package_data = \
{'': ['*']}

install_requires = \
['pulp>=2.1,<3.0']

setup_kwargs = {
    'name': 'mypulp',
    'version': '0.0.10',
    'description': '`mypulp` is a package for mypulp.',
    'long_description': 'Mypulp is a wrapper module for PuLP. It supports to call PuLP using the same functions and classes as in Gurobi, a commercial mixed integer optimization solver.\nFor more details, see the Gurobi HP http://www.gurobi.com/.\n::\n\n    from mypulp import *\n    model = Model("lo1")\n    J, v = multidict({1:16, 2:19, 3:23, 4:28})\n    x1 = model.addVar(vtype=GRB.CONTINUOUS, name="x1")\n    x2 = model.addVar(vtype="C", name="x2")\n    x3 = model.addVar(lb=0, ub=30, vtype="C", name="x3")\n    model.update()\n    model.addSOS(2, [x1, x2, x3])\n    L1 = LinExpr([2, 1, 1], [x1, x2, x3])\n    model.addConstr(lhs=L1, sense="<=", rhs=60)\n    model.addConstr(x1 + 2*x2 + x3 <= 60)\n    model.setObjective(15*x1 + 18*x2 + 30*x3, GRB.MAXIMIZE)\n    model.write("mypulp1.mps")\n    model.write("mypulp1.lp")\n    model.optimize()\n    if model.Status == GRB.Status.OPTIMAL:\n        print("Opt. Value =", model.ObjVal)\n        for v in model.getVars():\n            print(v.VarName, v.X)\n        for c in model.getConstrs():\n            print(c.ConstrName, c.Pi)\n\nRequirements\n------------\n* Python 3.7, pulp\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   $ pip install pulp\n   $ pip install mypulp\n\nHistory\n-------\n* 0.0.1 (2015-05-04) first release\n* 0.0.8 (2016-02-03)\n',
    'author': 'Mikio Kubo',
    'author_email': 'kubomikio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/mypulp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<3.8.0',
}


setup(**setup_kwargs)
