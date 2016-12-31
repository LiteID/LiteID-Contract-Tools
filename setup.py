from setuptools import setup

setup(name='LiteID Contract Tools',
    version='0.1',
    description='Tools to interact with the official LiteID contract',
    long_description='Tools to interact with the official LiteID contract with a JSON RPC server exposed by geth',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 2.7',
    ],
    keywords='LiteID ethereum',
    url='https://github.com/LiteID/LiteID-Contract-Tools',
    author='ferret-guy',
    author_email='mark@markomo.me',
    license='MIT',
    packages=['LiteIDContractTools'],
    dependency_links=['https://github.com/LiteID/ethjsonrpc/tarball/master'],
    include_package_data=True,
    install_requires=[
          'pycryptodome>=3.3.1',
      ],
    zip_safe=False)
