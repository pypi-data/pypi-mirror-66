import setuptools
import re

with open("README.md", "r") as fh:
  long_description = fh.read()

VERSIONFILE = "_version.py"
verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass # Okay, there is no version file.
else:
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        print("unable to find version in " + VERSIONFILE)
        raise RuntimeError("if _version.py exists, it is required to be well-formed")

setuptools.setup(
  name='matreplab',  
  version=verstr,
  scripts=['matREPLab'] ,
  author="Robin Tournemenne",
  author_email="rtournem@lavabit.com",
  description="A better matlab -nodesktop",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/RobinTournemenne/matREPLab",
  packages=setuptools.find_packages(),
  install_requires=[
      'pexpect',
      'pygments',
      'prompt_toolkit',
      'pathlib'
  ],
  classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
  ],
 )