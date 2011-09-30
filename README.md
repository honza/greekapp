GreekApp
========

This is a Django application that allows you to interact with the text of the
New Testament in its original language. This is intended for students of Koine
Greek.

Hovering over a Greek word will reveal its meaning and its grammatical
information (gender, tense, mood, person, etc.).

There's no accounts, nothing like that. It's using Redis as the backend because
it's blazing fast and very memory efficient.

All of the text, grammar, lexical data and so is in the public domain.

Installation
------------

Clone the repo, install the requirements and start redis. Then run:

    $ python load.py

which will open the sqlite database and load all of the data contained therein
into redis. Once that's done, start your django server and you can visit the
site in your browser:

[http://localhost:8000/nt/](http://localhost:8000/nt/)

Type in a verse you'd like to study and enjoy.

License
-------

BSD, short and sweet.

https://github.com/honza/greekapp/raw/master/screenshow.jpg
