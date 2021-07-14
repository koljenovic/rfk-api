# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="RFK API Dokumentacija",
    author_email="malik@mekom.ba",
    url="",
    keywords=["Swagger", "RFK API Dokumentacija"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    **RFK RESTful API** omogućava jednostavan HTTP REST pristup lokalnim legacy DBF \\\&quot;*bazama podataka*\\\&quot; originalno korištenim u programskim jezicima Clipper i Visual FoxPro. Generički API podržava čitanje i izmjenu postojećih kao i dodavanje novih zapisa kroz emulaciju &#x60;SELECT&#x60;, &#x60;UPDATE&#x60; i &#x60;INSERT&#x60; SQL DML iskaza nad .DBF *tabelama* (datotekama) unutar &#x60;data&#x60; direktorija, brisanje nije podržano.  **Ne preporučuje se korištenje .DBF datoteka za trajno spremanje podataka u savremenim programskim rješenjima**, ovaj API prvenstveno služi za čitanje podataka zarobljenih u .DBF formatu, migraciju i privremena integracijska rješenja, ukoliko trebate savremeno, pouzdano i jednostavno rješenje za lokalnu pohranu i pristup razmotrite SQLite datotečnu bazu podataka sa punom SQL podrškom.  *Napomena:* API je namjenski pisan za RFK računovodstvenu aplikaciju izrađenu u Clipperu, te je na njoj i testiran, no trebao bi bez većih izmjena podržavati bilo koju vrstu Clipper ili VFP .DBF podatkovne datoteke.  Copyright 2021 MEKOM d.o.o. Visoko - MIT Licenca 
    """
)
