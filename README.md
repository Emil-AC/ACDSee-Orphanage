# Introduction
Photographers shooting thousands of photos a year need a suitable DAM to manage their image library and ACDSee is a pretty well known app that provides such a DAM for Windows.

Every autumn ACDSystems publishes a new version of this app and new users often at first are happy with the speed of the program, but as soon the the underling database gets filled with lots of images the app sometimes dramatically slows down. 

Orphanage was created to help new users, who plan to use AC for next couple of years with lots of images, to test the app with lots of data without the need to catalogue thousands of images and then assign all the different tags AC does support. The app allows to facilely fill AC with tons of categories, keywords or collections and see what happens to AC.

# Motive
In Oct 2019, I wanted upgrade my good old ACDSee Pro 8 with ACDSee ULtimate 2020. But after converting my database, I found that switching from manage mode to view mode with a single image took more then 30 seconds in AC Ulti 2020 instead of less then 2 seconds with AC Pro 8. When monitoring the app with Sysinternals Process Monitor I recognized that the newer version was loading the whole master list of AC-keywords from the db everytime when switching from manage mode to view mode. So I decided to have a closer look.

# How does Orphanage work
ACDSee allows to import/export portions of the db in to text files. These text files may contain proprietary ACDSee meta data for images like categoreis, keywords, collections, rating, label ... The file also may contain the master lists of definded keywords and categories, but not collections. These text files also do not support any face recognition data.

Orphange creates such a text file with ajustable amounts of keywords, categories and items. Items also may be assigned to adjustable numers of keywords, categories and collections. Of course none of the items added to the database does realy exist; all items are orphanaed. Therefore the name of this script. 

# How to use
Be sure to have python installed, I used v3.7.2
* Edit the config.ini file and set the values you want to try, but start with small values. With high values AC can easily go to guru mode. 
* Run orphanage.py with a full qualified path of the text file you want to create.
* Start ACDSee, switch to a new empty db and catalouge a few existing image files, or just drag'drop an image onto your ACDSee icon o the desktop.
* Import the text file with Menu-Tools-Database-Import dialogue
* Play with AC using the existing items you've catalogued and see how it goes. Things to test my be startup time of AC, switching from one mode to another, searching for a keyword or category, assigning an item to a keyword category or collection . . . simply all database related functions. 

# What to do when finished 
Terminate ACDsee and delete the test database.

# Why python
* Policies don't allow to run user writebale ps, vbs, cmd or bat scripts on my systems.
* This script is addressed to experienced user, nothing to just double click and have fun.
* I like python :-)

# Disclamer
There's not guaranty for anything, you use it on your own risk!
You may do with this script whatever you like. 


Emil, 2019-10-10

