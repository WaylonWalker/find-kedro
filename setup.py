from pathlib import Path

from setuptools import find_packages, setup

NAME = "find-kedro"

README = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name=NAME,
    version="0.1.1",
    url="https://github.com/WaylonWalker/find-kedro.git",
    author="Waylon Walker",
    author_email="waylon@waylonwalker.com",
    description="finds nodes for your kedro pipeline",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    license="MIT",
    install_requires=["kedro", "click", "colorama", "pygments"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    # package_data={"public": ['**/public/**/*']},
    entry_points={
        # "kedro.global_commands": ["find-kedro = find_kedro.cli:cli"],
        "console_scripts": ["find-kedro = find_kedro.cli:cli"],
    },
)
