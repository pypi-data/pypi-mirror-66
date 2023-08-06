from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'hellocdw',
    version = '0.0.2',
    description = 'Some description here!',
    py_modules = ["hellocdw"],
    package_dir = {'':'src'},
    classifiers = ["Programming Language :: Python :: 3.6"], # Need to add license and operating systems
    long_description = long_description,
    long_description_content_type = "text/markdown"
    # you can now add also url, author, author_email
)