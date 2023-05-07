from setuptools import setup, find_packages
 
setup(name='unigui',
      version='1.4.3',      
      license='MIT',
      author='Georgii Dernovyi',
      author_email='g.dernovoy@gmail.com',
      description='Unigui - Universal app browser',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      url="https://github.com/Claus1/unigui" ,      
      include_package_data=True,
      install_requires=[
          'websockets','jsonpickle', 'aiohttp'
      ],
      zip_safe=False)
