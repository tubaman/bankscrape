==========
bankscrape
==========

I got tired of logging in to my bank's website to see my latest
transactions.  Bankscrape is a command line program that dumps your latest
transactions as CSV.  From there, you can import them into spreadsheet,
database, whatever.  Each financial institution has it's own plug-in to
tell bankscrape how to grab the transactions.  Currently there are plug-ins
for WellsFargo_ and Citicards_.  Anyone else want to contribute more?

.. _WellsFargo: https://github.com/tubaman/bankscrape/blob/master/bankscrape/banks/wellsfargo.py
.. _Citicards: https://github.com/tubaman/bankscrape/blob/master/bankscrape/banks/citicards.py
