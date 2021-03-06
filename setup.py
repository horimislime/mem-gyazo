from setuptools import setup, find_packages
import os

name = "mem-gyazo"
version = "0.1"


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name=name,
    version=version,
    description="in-memory gyazo server",
    long_description=read('README.md'),
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    keywords="",
    author="",
    author_email='',
    url='',
    license='',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Flask',
        'python-memcached'
        ],
    entry_points="""
    [paste.app_factory]
    main = app.controller:make_app
    """,
    )
