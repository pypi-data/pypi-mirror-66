import os
os.system("rm -rf *.egg-info")

NAME_TO_RESERVE = "elasticsearch10-dsl"

from setuptools import setup

setup(
    name=NAME_TO_RESERVE,
    version="0",
    description="This is a reservation of the name '%s' for future use" % NAME_TO_RESERVE,
    author="Seth Michael Larson",
    author_email="seth.larson@elastic.co",
)

os.system("rm -rf *.egg-info")
