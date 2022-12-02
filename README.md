# Student Database FBLA Competition

This is my submission for the FBLA coding and programming competition. 

It consists of a webserver with Django as a backend, and a SQL server as the database.

There will be a way to create admin accounts which can track data, including generating reports, picking the winners, and search the database

Keeping with how it would work in the real world, to input data into the database, an admin can manually input it (as a way to fix errors) or an upload of a .csv file, which is compiled at the school event.

There will be a way to scan or input student id numbers at the event, which will go into the database, probably with a barcode scanner with a Google Sheet, which is exported to a csv file and emailed to the admin (not uploaded directly because computers at school events are often left unattended, and the possibility of being stolen makes it a risk to be logged in as an admin

To recognize student names, there with have to be a database with all of the student names correlated with their id numbers
