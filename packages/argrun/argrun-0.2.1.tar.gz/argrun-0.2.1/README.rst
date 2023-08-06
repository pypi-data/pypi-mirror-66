
argrun
======

a library that wraps argparse, mapping arguments to decorated functions

functions are only called if the associated command line argument is present/non-empty

Installation:
^^^^^^^^^^^^^

.. code-block:: sh

   $ pip install argrun

Usage:
^^^^^^

.. code-block::

   from functools import reduce
   import argrun 

   parser = argrun.ArgumentParser()

   @parser.parses('-m', '--multiply', help='multiplies numbers', nargs='*')
   def multiply(args):
       print(reduce(lambda x,y: x * y, map(int, args)))

   if __name__ == '__main__':
       parser.run()

Documentation:
--------------

argrun.argrun
=============

ArgumentRunner
--------------

.. code-block:: python

   ArgumentRunner(self)

ArgumentRunner offers a decorator, parses arguments, and allows decorated functions to be ran

parse_args
^^^^^^^^^^

.. code-block:: python

   ArgumentRunner.parse_args(*args, **kwargs)

Parses arguments and returns the result as a dictionary

parse
^^^^^

.. code-block:: python

   ArgumentRunner.parse(*args, **kwargs)

a decorator that defines the arguments to be parsed
and associates it with the decorated method

run
^^^

.. code-block:: python

   ArgumentRunner.run(*args, **kwargs)

Runs all decorated functions

add_argument
^^^^^^^^^^^^

.. code-block:: python

   ArgumentRunner.add_argument(*args, **kwargs)

adds an argument to be parsed without being run
