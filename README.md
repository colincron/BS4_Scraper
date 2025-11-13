BS4 Scraper

This is a web scraper that collects domain urls and saves them to a database. 
It also grabs x-frame-options data, server type, and webpage title.

It then initiates a port scan 
(credit to: https://github.com/ritvikb99/dark-fantasy-hack-tool) 
and outputs any open ports (from a subset of common ports)
to the screen. It does not log these to the database.

To install clone the repository 
Create a virtual python environment
Then run:
pip install requirements.txt 

run the program using:
python scraper.py

It will ask for an input, urls must begin with http or https
