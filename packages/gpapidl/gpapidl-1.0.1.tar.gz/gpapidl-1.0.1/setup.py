from setuptools import setup

setup(name='gpapidl',
      version='1.0.1',
      description='Unofficial python api for google play',
      url='https://github.com/rehmatworks/googleplay-api',
      author='Rehmat Alam',
      author_email='contact@rehmat.works',
      license='GPL3',
      packages=['gpapidl'],
      package_data={'gpapidl': ['device.properties']},
      install_requires=['cryptography>=2.2',
                        'protobuf>=3.5.2',
                        'requests'])
