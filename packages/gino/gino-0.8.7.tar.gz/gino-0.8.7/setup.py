#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst', encoding='utf-8') as history_file:
    history = history_file.read()


def req_file(filename):
    with open(filename) as f:
        content = f.readlines()
    return [x.strip() for x in content if x.strip()]


setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'pytest-asyncio',
    'pytest-mock',
    'psycopg2-binary',
]

setup(
    name='gino',
    version='0.8.7',
    description="GINO Is Not ORM - "
                "a Python asyncio ORM on SQLAlchemy core.",
    long_description=readme + '\n\n' + history,
    author="Fantix King",
    author_email='fantix.king@gmail.com',
    url='https://github.com/fantix/gino',
    packages=[p for p in find_packages() if p != 'tests'],
    include_package_data=True,
    install_requires=req_file('requirements.txt'),
    python_requires='>=3.5',
    entry_points="""
    [sqlalchemy.dialects]
    postgresql.asyncpg = gino.dialects.asyncpg:AsyncpgDialect
    asyncpg = gino.dialects.asyncpg:AsyncpgDialect
    """,
    license="BSD license",
    zip_safe=False,
    keywords='orm asyncio sqlalchemy asyncpg python3 sanic aiohttp tornado',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    project_urls={
        'Documentation': 'https://python-gino.readthedocs.io/',
        'Funding': 'https://www.patreon.com/fantixking',
        'Source': 'https://github.com/fantix/gino',
        'Tracker': 'https://github.com/fantix/gino/issues',
    },
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
