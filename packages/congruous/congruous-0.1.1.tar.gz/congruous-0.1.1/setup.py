import os
from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements


README_PATH = 'README.md'
LONG_DESC = ''
# if os.path.exists(README_PATH):
#     with open(README_PATH) as readme:
#         LONG_DESC = readme.read()

INSTALL_REQUIRES = [
    'Click', 'matplotlib', 'fuzzywuzzy[speedup]', 'tabulate', 'reportlab', 'pytz']

setup(
    name='congruous',
    version='0.1.1',
    author='Mahesh Kumaran T',
    author_email='maheshtkumaran@gmail.com',
    description=(
        'A python command-line tool to compare and generate accuracy reports for custom built OCR models.'
    ),
    long_description=LONG_DESC,
    packages=find_packages(),
    py_modules=['congruous'],
    install_requires=INSTALL_REQUIRES,
    entry_points='''
        [console_scripts]
        congruous=congruous:cli
    ''',
)
