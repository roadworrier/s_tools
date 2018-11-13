#!/usr/bin/python
#
# This started out as the code from 
# https://pentesterscript.wordpress.com/2013/08/07/extract-contacts-call-log-message-from-skype-database/
# which required some indentation, and then some other snippets were added to make this do what I needed:
# List the date, time, duration of all skype calls, with the initator known.
#
# What does this do? Prints something like this:
#
#
#Timestamp: 2018-08-01 19:10:41 From live:someones_skypename :
#    <name>Someone's Actual Name</name>
#    <name>My Name</name>
#Timestamp: 2018-08-01 19:13:54 From my_skype_username :
#    <name>Someone's Actual Name</name>
#    <name>my_skype_username</name>
#Skype call duration: 0:03:13


import sqlite3
import optparse 
import os
import datetime
import xml.etree.cElementTree as et
import re
from HTMLParser import HTMLParser
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
from bs4 import BeautifulSoup


def printProfile(skypeDB):
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	c.execute("SELECT fullname, skypename, city, country, \
	datetime(profile_timestamp,'unixepoch') FROM Accounts;")

	for row in c:
		print '[*] - Found Account -'
		print '[+] User : '+str(row[0])
		print '[+] Skype Username : '+str(row[1])
		print '[+] Location : '+str(row[2])+','+str(row[3])
		print '[+] Profile Date : '+str(row[4])


def printContacts(skypeDB):
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	c.execute("SELECT displayname, skypename, city, country,\
	phone_mobile, birthday FROM Contacts;")

	for row in c:
		print '\n[*] - Found Contact -'
		try:
			print '[+] User : ' + str(row[0])
		except:
			pass
		print '[+] Skype Username : ' + str(row[1])

	if str(row[2]) !='' and str(row[2]) != 'None':
		print '[+] Location : ' + str(row[2]) + ',' + str(row[3])
		if str(row[4]) != 'None':
			print '[+] Mobile Number : ' + str(row[4])
		if str(row[5]) != 'None':
			print '[+] Birthday : ' + str(row[5])

def printCallLog(skypeDB):
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	c.execute("SELECT datetime(begin_timestamp,'unixepoch'), \
	identity FROM calls, conversations WHERE \
	calls.conv_dbid = conversations.id;"
	)
	print '\n[*] - Found Calls -'

	for row in c:
		print '[+] Time: '+str(row[0])+\
		' | Partner: '+ str(row[1])

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
    	if tag != 'duration':
    		return
        #print "Encountered a start tag:", tag
        #for name, value in attributes
    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag

    def handle_data(self, data):
        print "Encountered some data  :", data
    

def printMessages(skypeDB):
	conn = sqlite3.connect(skypeDB)
	c = conn.cursor()
	c.execute("SELECT datetime(timestamp,'unixepoch'), \
	dialog_partner, author, body_xml FROM Messages;")
	print '\n[*] - Found Messages -'
	
	time_text = "Timestamp: "
	time_int = 0
	prev_time_int = 0

	for row in c:
		try:
			if 'partlist' not in str(row[3]):
				if str(row[1]) != str(row[2]):
					msgDirection = 'To ' + str(row[1]) + ': '
			else:
				msgDirection = 'From ' + str(row[2]) + ' : '
			if str(row[3]).startswith('<partlist'):
				soup = BeautifulSoup(str(row[3]))
				call_length=soup.duration
				time_int=int(call_length.string)
				#print "call ln" + call_length.string
				print time_text + str(row[0]) + ' ' + msgDirection 
				cleaner_string = str(row[3])
				cleaner_string = re.sub('.*part.*\n', "", cleaner_string)
				cleaner_string = re.sub('.*part.*', "", cleaner_string)
				cleaner_string = re.sub('.*duration.*\n', "", cleaner_string)
				print cleaner_string.rstrip('\n')
				if prev_time_int == time_int:
					print "Skype call duration: " + str(datetime.timedelta(seconds=time_int)) + "\n"
				prev_time_int = time_int
			
		except:	
			pass

def main():
	parser = optparse.OptionParser("usage %prog "+\
	"-p " + """\nSpecify skype profile path after -p\n
The locations of the Skype database in different operating systems are\n
In windows C:\\Users\user_name\AppData\Roaming\Skype\skype_user_name\n
In mac Users/user_name/Library//Application/Support/Skype/skype_user_name\n
In Linux /root/.Skype/skype_user_name """)
	parser.add_option('-p', dest='pathName', type='string',\
	help='Specify Skype profile path')

	(options, args) = parser.parse_args()
	pathName = options.pathName
	if pathName == None:
		print parser.usage
		exit(0)
	elif os.path.isdir(pathName) == False:
		print '[!] Path Does Not Exist: ' + pathName
		exit(0)
	else:
		print "Running skyptool.py found here: https://github.com/roadworrier/s_tools"
		skypeDB = os.path.join(pathName, 'main.db')
	if os.path.isfile(skypeDB):
		printProfile(skypeDB)
		#printContacts(skypeDB)
		#printCallLog(skypeDB)
		printMessages(skypeDB)
	else:
		print '[!] Skype Database '+\
		'does not exist: ' + skpeDB

if __name__ == '__main__':
	main()