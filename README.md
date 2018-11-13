# s_tools
A collection of tools I wrote for myself, but they may be useful to you too.

skyptool.py is a modification of https://pentesterscript.wordpress.com/2013/08/07/extract-contacts-call-log-message-from-skype-database/

List the date, time, duration of all skype calls stored in the local computer's Skype database, with the initator known.

Tested only with Windows Skype 7.40 so far.

Fails on newer versions of Skype: Microsoft has changed the schema and put things in Microsoft/Skype for Desktop/main.db and these queries won't work there.

It logs Skype calls, for example:
<pre>
Timestamp: 2018-08-01 19:10:41 From live:someones_skypename :
    <name>Someone's Actual Name</name>
    <name>My Name</name>
Timestamp: 2018-08-01 19:13:54 From my_skype_username :
    <name>Someone's Actual Name</name>
    <name>my_skype_username</name>
Skype call duration: 0:03:13
</pre>
