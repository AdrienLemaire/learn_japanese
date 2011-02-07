================
Learn a language
================

**After a request to extend this program to learn other languages such as
english, I'll do it in this branch**


Installation
------------

Make sure that you have a working Python_ 2.x >= 2.6, eg::

    $ sudo port install python26

Then download the project::

    $ git clone git@github.com:Fandekasp/learn_japanese.git
    $ cd learn_japanese
    $ pip install -r requirements.txt

.. _Python: http://python.org


for older users
~~~~~~~~~~~~~~~

If you already used this program before the tag v2, you will want to update your
user files to the new format. That can be done with::

    $ cd utils
    $ python migrate_v2.py

Bugs
----
First time you run the project, you will probably have an error, I'll fix it
later


How to use
----------
If you want to contribute to the project, fill the lang.txt in the vocabulary
directory. All files located in user_files are private for the user, containing
his own statistics, and are managed by the program.

When ready::

    $ ./main.py
