from distutils.core import setup

setup(name='bankscrape',
    version='1.1',
    description="Web Scrapers for Financial Institutions",
    author="Ryan Nowakowski",
    author_email="tubaman@fattuba.com",
    packages=['bankscrape', 'bankscrape.banks'],
    scripts=['scripts/bankscrape'],
    install_requires=['BeautifulSoup>=4', 'requests'],
    )
