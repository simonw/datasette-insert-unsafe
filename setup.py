from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-insert-unsafe",
    description="Unsafe permissions for datasette-insert - allows all actions without authentication",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-insert-unsafe",
    project_urls={
        "Issues": "https://github.com/simonw/datasette-insert-unsafe/issues",
        "CI": "https://github.com/simonw/datasette-insert-unsafe/actions",
        "Changelog": "https://github.com/simonw/datasette-insert-unsafe/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_insert_unsafe"],
    entry_points={"datasette": ["insert_unsafe = datasette_insert_unsafe"]},
    install_requires=["datasette", "datasette-insert>=0.6"],
    extras_require={"test": ["pytest", "pytest-asyncio", "httpx", "sqlite-utils"]},
    tests_require=["datasette-insert-unsafe[test]"],
)
