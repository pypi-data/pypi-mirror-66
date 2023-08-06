from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='logger_json',
    version='1.0.2',
    description='Tool to display logs in JSON format',
    long_description_content_type="text/markdown",
    long_description=long_description,
    license='MIT',
    packages=find_packages(),
    author='Gizem Kacmaz',
    author_email='gizemkmz@gmail.com',
    keywords=['Json', 'Logger'],
)