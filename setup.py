from setuptools import find_packages, setup

setup(
    name='IG.Python.Api.Client',
    version=1.0,
    description='IG Markets Python igRestApiClient',
    url='https://github.com/oneangrytrader/IG.Python.Api.Client',
    author='One Angry Trader',
    packages=find_packages(),
    install_requires=[
      'requests~=2.24.0',
      'python-dateutil~=2.8.0'
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Natural Language :: English',
        ],
)
