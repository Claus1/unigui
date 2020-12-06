from setuptools import setup, find_packages
 
setup(name='unigui',
      version='0.1',
      url='',
      license='MIT',
      author='Georgii Dernovyi',
      author_email='g.dernovoy@gmail.com',
      description='Unigui - Universal app browser',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)