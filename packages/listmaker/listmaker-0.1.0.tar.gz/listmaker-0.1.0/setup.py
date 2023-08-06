from setuptools import setup, find_packages

setup(name='listmaker', 
      version='0.1.0', 
      author='Vinayak Suley',
      author_email='vinayaksuley@gmail.com',
      url='http://pypi.python.org/pypi/listmaker_v010/',
      description='A utility for managing hierarchical lists',
      long_description=open('README.txt').read(),
      license='LICENSE.txt',
      packages=find_packages(),
      install_requires=['anytree'],
      python_requires='>=3',
      )
