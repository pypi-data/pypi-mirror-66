import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="LSHlink-ffghcv",
  version="0.1",
  author="Boyang Pan & Nancun Li",
  author_email="nancun.li@duke.edu",
  description="Base on Fast agglomerative hierarchical clustering algorithm using Locality-Sensitive Hashing,  we develop algorithm in Python.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ffghcv/663final_project",
  packages=['LSHlink'],
  install_requires=[
        'sklearn',
        'numpy',
        'matplotlib',
        'scipy',
        'numba<=0.49.0'
    ]
)