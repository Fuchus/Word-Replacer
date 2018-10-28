from setuptools import setup
from setuptools.command.install import install as _install

class Install(_install):
        def run(self):
         _install.do_egg_install(self)
         import nltk
         nltk.download("popular")
setup(
   name='Word replacer',
   version='1.0',
   description='A module that replaces certain words',
   author='Leonardo Martinho',
   author_email='leo@fuchus.de',
   install_requires=['requests', 'nltk', 'argparse', 'pathlib2']
)
