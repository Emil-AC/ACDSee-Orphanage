# Introduction
Photographers shooting thousands of photos a year need a suitable DAM to manage their image library and ACDSee is a pretty well known app that provides such a DAM for Windows.

Every autumn ACDSystems publishes a new version of this app and new users often at first are happy with the speed of the program, but as soon the the underling database gets filled with lots of images the app sometimes dramatically slows down. 

Orphanage was created to help new users, who plan to use AC for next couple of years with lots of images, to test the app with lots of data without the need to catalogue thousands of images and then assign all the different tags AC does support. The app allows to facilely fill AC with tons of categories, keywords or collections and see what happens to AC.

# Motive
In Oct 2019, I wanted upgrade my good old ACDSee Pro 8 with ACDSee ULtimate 2020. But after converting my database, I found that switching from manage mode to view mode with a single image took more then 30 seconds in AC Ulti 2020 instead of less then 2 seconds with AC Pro 8. When monitoring the app with Sysinternals Process Monitor I recognized that the newer version was loading the whole master list of AC-keywords from the db everytime when switching from manage mode to view mode.

# How does Orphanage work
ACDSee allows to import/export portions of the db in to text files. These text files may contain proprietary ACDSee meta data for images like categoreis, keywords, collections, rating, label ... The file also may contain the master lists of definded keywords, categories. Afaik, these text files do not support any face recognition data.

Orphange creates such a text file with ajustable amounts of keywords, collections and item. Of course none of the items added to the database does realy exist; all items are orphanaed. 

# How to use
Be sure to have python installed, I used v3.7.2
Edit the ini file and set the values you plan to use, but start with small values.
Run orphanage with a full qualified path of the text file you want to create.
Start ACDSee, switch to a new empty db and catalouge a few existing image files.
Import the text file with Menu-Tools-Database-Import.
Play with AC usimg the existing items you've catalogued and see how it goes.

# Why python
Policies don't allow user to run ps, vbs, cmd or bat scripts with write access on my system
I like python :-)

# Disclamer
There's not guaranty for anything, you use it on your own risk!
You may do with it whatever you like. 


Emil, 2019-10-10

