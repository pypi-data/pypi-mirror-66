#my third attempt at making a template pip package

create distribution archives:
*setuptools and wheel should be preinstalled*
python setup.py sdist bdist_wheel
*add .egg-info to .gitignore*

Upload:
pip install twine
twine upload dist/*
enter username: __token__
enter password: pypi-AgEIcHlwaS5vcmcCJDU0ZTIxMWRiLWNlMjYtNDM3ZS05YjJlLWYzYTk5NmE2NGJjMgACJXsicGVybWlzc2lvbnMiOiAidXNlciIsICJ2ZXJzaW9uIjogMX0AAAYgWzvnJ7sF-57Jw_YGg04aZTPCeuRpXrHBhAsPRfofZGc