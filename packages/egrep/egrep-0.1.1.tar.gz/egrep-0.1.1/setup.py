import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='egrep',
    version='0.1.1',
    author='Roberto Himmelbauer',
    author_email='robertoh89@gmail.com',
    description='A simple library for exectuing egrep linux commando to files',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rhimmelbauer/egrep',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=python3.7',
)