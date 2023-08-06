import setuptools

with open("raveberry/README.md", "r") as f:
    long_description = f.read()

with open("raveberry/requirements/common.txt") as f:
    required_packages = f.read().splitlines()

setuptools.setup(
    name="raveberry",
    version="0.4.5",
    author="Jonathan Hacker",
    author_email="raveberry@jhacker.de",
    description="A multi-user music server with a focus on participation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raveberry/raveberry",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django :: 2.2",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3",
    ],
    packages=["raveberry"],
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=required_packages,
    scripts=["raveberry/bin/raveberry"],
)
