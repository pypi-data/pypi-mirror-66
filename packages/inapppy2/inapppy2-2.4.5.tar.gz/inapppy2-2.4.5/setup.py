# encoding: UTF-8
from setuptools import setup


def get_description():
    with open("README.rst") as info:
        return info.read()


setup(
    name="inapppy2",
    version="2.4.5",
    packages=["inapppy", "inapppy.asyncio"],
    install_requires=["aiohttp", "rsa", "requests", "google-api-python-client"],
    description="In-app purchase validation library for Apple AppStore and GooglePlay.",
    keywords="in-app store purchase googleplay appstore validation",
    author="Lukas Šalkauskas",
    author_email="halfas.online@gmail.com",
    url="https://github.com/Nkhinatolla/InAppPy.git",
    long_description=get_description(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
