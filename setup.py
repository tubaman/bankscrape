from distutils.core import setup

setup(name='bankscrape',
    version='1.0',
    description="Web Scrapers for Financial Institutions",
    author="Ryan Nowakowski",
    author_email="tubaman@fattuba.com",
    packages=['bankscrape', 'bankscrape.banks'],
    scripts=['scripts/bankscrape'],
    )
