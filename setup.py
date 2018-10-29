from setuptools import setup, find_packages

setup(
    name='fiblockchain',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'requests'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
