# Student Database FBLA Competition

This is my submission for the FBLA coding and programming competition. 

It consists of a webserver with Flask as a backend, and a SQL server as the database.

There will be a way to create admin accounts which can track data, including generating reports, picking the winners, and search the database

In the real world, a barcode scanner is used to scan the barcode on a student ID on the tracker page, and the site pops up a notification saying {Student} has been tracked! (Or something in that area. When it's scanned, the server looks up the ID and returns the name, and then adds the event to the student in the database.

To recognize student names, there with have to be a database with all of the student names correlated with their id numbers
