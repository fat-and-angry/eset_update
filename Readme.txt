###############################################################################

Tool for downloading Eset Antivirus updates

###############################################################################

Description:
This software is a free programm for downloading Eset Nos32 Antivirus updates.
It finds login and password for Eset update server and downloads updates on local computer.


Installation:
There are no special methods to installation this program. Just copy content of "src" folder to convenient place. 


Depends:
This softvare requires some other programs.

	rarfile - pyton module for manipulating RAR archives
		# yum install python-pip
		# pip-python install rarfile

	unrar - Utility for extracting, testing and viewing RAR archives
		# yum install unrar


Usage:
Run src/main.py script


Configuration:
Edit src/main.py for setting path for saving updates and setting logfile name

