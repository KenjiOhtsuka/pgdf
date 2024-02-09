import os
from codecs import open
from setuptools import setup, find_packages


root_dir = os.path.abspath(os.path.dirname(__file__))
# def _requirements():
#     requirements_file_path = os.path.join(root_dir, 'requirements.txt')
#     return [name.rstrip() for name in open(requirements_file_path).readlines()]
#     install_requires = _requirements()

# Get the long description from the README file
readme_file_path = os.path.join(root_dir, 'README.rst')
with open(readme_file_path, encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pgdf',
    packages=find_packages(),
    # package_dir={'': 'pgdf'},
    # packages=find_packages(where='pgdf'),
    version='0.0.1.0',
    py_modules=['pgdf', 'pgdf.main', 'pgdf.summary'],
    install_requires=[
        'xlsxwriter',
    ],
    entry_points={
        'console_scripts': ['pgdf=pgdf.main:main'],
    },
    license='MIT',
    author='Kenji Otsuka',
    author_email='kok.fdcm@gmail.com',
    description='Tool built with python to summarize git diff into an Excel file.',
    long_description=long_description,
    #url='https://github.com/KenjiOhtsuka/pgdf',
    include_package_data=True,
    # entry_points='''
    #     [console_scripts]
    #     myproject=myproject:cli
    # ''',
)

"""
# for development
python setup.py develop
# test
python -m doctest -v pgdf/summary.py
# for production
## build
python setup.py sdist bdist_wheel
## upload
twine upload -r testpypi dist/pgdf-{version}.tar.gz
twine upload -r pypi dist/pgdf-{version}.tar.gz
"""
