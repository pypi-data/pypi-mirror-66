from setuptools import setup
from distutils import dir_util

try:
    dir_util.remove_tree('dist')
except FileNotFoundError:
    pass

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name="mongo2json",
    version="1.0.0",
    author="drunckoder",
    author_email="drunckoder@gmail.com",
    description="Converts mongo shell JSON output to a valid JSON or a Python object",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/drunckoder/mongo2json",
    packages=["mongo2json"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "orjson"
    ],
    keywords="mongo mongodb shell export json",
    project_urls={
        "Repository": "https://github.com/drunckoder/mongo2json",
        "Bug Reports": "https://github.com/drunckoder/mongo2json/issues",
        # "Documentation": "https://mongo2json.readthedocs.io",
    },
)
