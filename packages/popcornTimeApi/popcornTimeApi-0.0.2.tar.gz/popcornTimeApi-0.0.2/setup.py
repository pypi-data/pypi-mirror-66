from setuptools import setup,setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='popcornTimeApi',
    version='0.0.2',
    description='Unofficial python Api wrapper for Popcorntime-Api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/DavidM42/popcornTimeApi',
    author='DavidM42',
    author_email='david@merz.dev',
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests'])