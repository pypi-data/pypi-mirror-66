from setuptools import setup
from pathlib import Path

setup(
    name="weighted_collection",
    packages={"weighted_collection"},
    version="1",
    license="MIT",
    description="A WeightedCollection assigns probability weights per elements and returns elements randomly using those weights.",
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Seth Alter",
    author_email="subalterngames@gmail.com",
    url="https://github.com/subalterngames/weighted_collection",
    download_url="https://github.com/subalterngames/weighted_collection/archive/v1.0.tar.gz",
    keywords=["collection", "random"],
    install_requires=["numpy"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)