import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="gospel",
    version="0.0.3",
    description="The Gospel of Jesus Christ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeForFaith/gospel",
    author="CodeForFaith",
    author_email="contact@codeforfaith.com",
    license="Unlicensed",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["gospel"],
    include_package_data=True,
    install_requires=["PyInquirer"],
    entry_points={
        "console_scripts": [
            "codeforfaith=gospel.__main__:main",
        ]
    },
)
