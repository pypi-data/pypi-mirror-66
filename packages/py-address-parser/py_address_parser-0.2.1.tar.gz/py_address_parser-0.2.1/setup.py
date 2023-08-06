from setuptools import setup

setup(
    name='py_address_parser',
    version='0.2.1',
    description='An address parsing library for Python based on usaddress.',
    url='https://github.com/R-Andrei/py_address_parser',
    author='Rares Andrei Faragau',
    author_email='faragau.rares@gmail.com',
    license='MIT',
    packages=['py_address_parser'],
    install_requires=[
          'usaddress',
      ],
    zip_safe=False
)
