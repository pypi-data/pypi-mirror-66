#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools

    use_setuptools()
    from setuptools import setup

setup(
    install_requires=[
        "discord",
        "schema",
        "pyyaml",
        "pytest",
        "distro",
        "pip",
        "aiohttp",
        "colorama",
        "appdirs",
        "babel",
        "apsw",
        "fuzzywuzzy",
        "click",
        "packaging",
        "uvloop",
        "motor",
        "pymongo",
        "asyncpg",
        "lavalink",
        "tqdm",
        "yarl",
    ],
    # setup_cfg=True
)
# else:
#     # Metadata and options defined in setup.cfg
#     setup(install_requires=['discord', 'schema', 'pyyaml', 'pytest', 'distro', 'pip', 'aiohttp', 'colorama', 'appdirs',
#                             'babel', 'apsw', 'fuzzywuzzy', 'click', 'packaging', 'uvloop', 'motor', 'pymongo',
#                             'asyncpg', 'lavalink', 'tqdm', 'yarl'])
