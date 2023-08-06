"""
Flask-Docs-Api
-------------

Creates docs for your api
"""
from setuptools import setup

with open("../README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Flask-Docs-Api',
    version='1.0.1',
    url='http://github.com/lwerner-lshigh/flask-api/',
    license='MIT',
    author='Lukas Werner',
    author_email='lwerner@lshigh.org',
    description='Easy Docs for flask',
    long_description=long_description,
    long_description_content_type="text/markdown",
    #py_modules=['flask_docs_api'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    packages=['flask_docs_api'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)