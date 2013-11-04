#Welcome to alfred-pocket !

##What's this ?

It can bookmark to pocket from alfred easily.

ex. you type bookmark from alfred , your Safari's current tab's url will be
bookmarked.

##How to use

### STEP 0

Run this command.

    pip install -r requirements.txt

	python pocket.py

and open http://localhost:5000.



###STEP 1

Click this Authorize Pocket link.

###STEP 2

Write alfred's trigger like this.

/usr/bin/python alfred-pocket/pocket.py bookmark > /dev/null 2>&1 &
###STEP 3

You type bookmark command from alfred. Thats' all.




