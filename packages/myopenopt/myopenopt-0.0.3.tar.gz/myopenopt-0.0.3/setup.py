# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myopenopt']

package_data = \
{'': ['*']}

install_requires = \
['FuncDesigner>=0.5629,<0.5630', 'openopt>=0.5629,<0.5630']

setup_kwargs = {
    'name': 'myopenopt',
    'version': '0.0.3',
    'description': '`myopenopt` is a package for myopenopt.',
    'long_description': 'Myopenopt is a wrapper module for openopt. It supports to call openopt using the same functions and classes as in Gurobi, a commercial mixed integer optimization solver.\nFor more details, see the Gurobi HP http://www.gurobi.com/.\n::\n\n    from myopenopt import *\n    model = Model("sample", mtype=\'NLP\')\n    x1 = model.addVar(vtype="C", name="x1")\n    x2 = model.addVar(vtype="C", name="x2")\n    x3 = model.addVar(vtype="C", ub=10, name="x3")\n    model.update()\n    c1 = model.addConstr(x1**2 + 2*x2**2 <= x3**2, name="C1")\n    c2 = model.addConstr(x3 <= 30, name="C2")\n    c3 = model.addConstr(quicksum([x1, x2, x3]) <= 20, name="C3" )\n    model.setObjective(15*x1 + 18*x2 + 30*x3, GRB.MAXIMIZE)\n    print(model)\n    model.optimize(solver="ralg")\n    print("Result =", model.Status)\n    for v in model.getVars():\n        print(v.VarName, v.X)\n\nRequirements\n------------\n* Python 3.7 and openopt, FuncDesigner\n\nFeatures\n--------\n* nothing\n\nSetup\n-----\n::\n\n   Add compiler path(ex. C:\\Anaconda3\\MinGW\\bin)\n   $ pip install openopt\n   $ pip install FuncDesigner\n   $ pip install myopenopt\n\nHistory\n-------\n0.0.1 (2015-5-4)\n~~~~~~~~~~~~~~~~~~\n* first release\n',
    'author': 'Mikio Kubo',
    'author_email': 'kubomikio@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SaitoTsutomu/myopenopt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<3.8.0',
}


setup(**setup_kwargs)
