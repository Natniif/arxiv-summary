from setuptools import setup, find_packages

setup(
    name='arxiv-summary',
	author='Fintan Hardy',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'bs4',
        'requests',
        'pytest',
        'pyinstaller',
    ],
)