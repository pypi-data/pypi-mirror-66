import codecs
import os

from setuptools import find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def get_definitions(rel_path, *words):
    dwords = {word: None for word in words}
    for line in read(rel_path).splitlines():
        for word in words:
            if line.startswith(f"__{word}__"):
                delim = '"' if '"' in line else "'"
                dwords[word] = line.split(delim)[1]
                break

    return [dwords[word] for word in dwords]


long_description = read('README.md')
base_folder = 'base_model'

_version, _description, _author, _author_email = get_definitions(
    os.path.join(base_folder, '__init__.py'),
    'version',
    'description',
    'author',
    'author_email')

setup(
    name='base-model-guiosoft',
    version=_version,
    description=_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'python-dateutil',
        'orjson'
    ],
    url="https://github.com/guionardo/py-base-model",
    keywords='model',
    project_urls={
        "Documentation": "https://github.com/guionardo/py-base-model/wiki",
        "Source": "https://github.com/guionardo/py-base-model",
    },
    author=_author,
    author_email=_author_email,
    packages=find_packages(
        where=".",
        exclude=["tests"],
    ),
    zip_safe=True,
    python_requires='>=3.6.*'
)
