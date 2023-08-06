from os.path import dirname, join

import setuptools

with open(join(dirname(__file__), 'cambridict/VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cambridict",
    version=version,
    author="Duy Nguyen",
    author_email="tegieng7@gmail.com",
    license='MIT',
    description="Search the meaning of the word from Cambridge Dictionary online, and get the result in JSON format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tegieng7/cambridict",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'cssselect',
        'lxml',
        'requests',
        'pyyaml'
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['cambridge', 'dictionary']
)
