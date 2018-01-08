from setuptools import setup

setup(
   name='Word replacer',
   version='1.0',
   description='A module that replaces certain words',
   author='Leonardo Martinho',
   author_email='leo@fuchus.de',
   packages=['word_replacer, API'],  #same as name
   install_requires=['requests', 'nltk', 'argparse', 're', 'sys', 'pathlib2'], #external packages as dependencies
)