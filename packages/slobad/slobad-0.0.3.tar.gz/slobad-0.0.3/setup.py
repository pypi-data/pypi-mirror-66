import setuptools


version = '0.0.3'

# read the contents of README
with open("README.md") as f:
    long_description = f.read()


setuptools.setup(
    name='slobad',
    version=version,
    description='Caching of Pandas DataFrames',
    license='MIT',
    url='https://gitlab.com/slobad/slobad',
    maintainer='slobad developers',
    maintainer_email='slobadpy@gmail.com',
    packages=["slobad"],
    python_requires='>=3.6',
    install_requires=[
        "pandas>=0.19",
        "pyarrow",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
