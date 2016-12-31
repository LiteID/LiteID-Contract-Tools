from setuptools import setup

setup(name='LiteID Contract Tools',
    version='0.1',
    description='Tools to interact with the official LiteID contract',
    long_description='Tools to interact with the official LiteID contract fia a JSON RPC server exposed by geth or the like',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 2.7',
    ],
    keywords='LiteID ethereum',
    url='https://github.com/LiteID/LiteID-Contract-Tools',
    author='Ferret_guy',
    author_email='mark@markomo.me',
    license='MIT',
    packages=['LiteIDContractTools'],
    dependency_links=['https://github.com/LiteID/ethjsonrpc/tarball/master'],
    include_package_data=True,
    zip_safe=False)