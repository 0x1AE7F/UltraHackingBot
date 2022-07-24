# UltraHackingBot

This bot is made for the UltraHackingClub CTF team.

The bot acts as a remote shell giving the Team Members some useful tools on the fly.

Implemented Features:

ping,
traceroute,
cvelookup

CveLookup scrapes data from https://cve.mitre.org/
due to the webscraping the response usually takes around 20ms, which is quite high.
Ive implemented a caching system which stores all requests for 1 day before they get invalid.
This allows the user to get instant search results from already made search requests.

More commands will be added anytime soon!