==============
Learn Japanese
==============


Goal
----

This project has multiples goals :

 - First project using Python 3
 - Discovering the PyGame framework
 - Learn Japanese faster with this QCM software.


Installation
------------

Make sure that you have a working Python_ 3.x >= 3.1.2, eg::

    $ sudo port install python31


The following part doesn't work quite well for me, you can skip it.

    | As the *except* method has changed in Python 3, and virtualenv, setuptools and
    | pip not yet updated, we have to grab the virtualenv3 fork::
    |
    |     $ hg clone http://bitbucket.org/brandon/virtualenv3
    |     $ cd virtualenv3
    |     $ sudo python3.1 setup.py install
    |     $ cd ~/Envs # Your virtualenv directory
    |     $ python3.1 PATH/TO/virtualenv3.py learn_japanese

Now you have to install Pygame_ 1.9.1. For Mac Users, please refer to the
following document : http://programming.itcarlow.ie/PyGameInstall.pdf

`Be careful to have previously installed the Java Developer Package required by
PORTMIDI, and to get the latest version of the SDL library !`

Then download the project::

    $ git clone git@github.com:Fandekasp/learn_japanese.git



.. _Python: http://python.org
.. _Pygame: http://www.pygame.org
