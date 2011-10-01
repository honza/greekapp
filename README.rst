GreekApp
========

This is a reusable Django application that allows you to interact with the text of the
New Testament in its original language. This is intended for students of Koine
Greek.

Hovering over a Greek word will reveal its meaning and its grammatical
information (gender, tense, mood, person, etc.).

There's no accounts, nothing like that. It's using Redis as the backend because
it's blazing fast and very memory efficient.

All of the text, grammar, lexical data and so is in the public domain.

Installation
------------

1. ``$ pip install django-greekapp``
2. Add ``greekapp`` to ``INSTALLED_APPS``
3. Plug GreekApp to your project's ``urls.py``.
4. Make sure Redis is installed and running
5. Run the ``load`` management command to load data into Redis
6. Run the server.
7. Profit

License
-------

BSD, short and sweet.

.. image:: https://github.com/honza/greekapp/raw/master/screenshot.jpg
