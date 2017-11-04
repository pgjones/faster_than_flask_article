Faster than Flask
=================

This is the code to accompany an `article
<https://medium.com/@pgjones/6x-faster-than-flask-8e89bfbe8e4f>`_.


Running
-------

Assuming you have at least Python 3.6, firstly to setup:

.. code-block::

    $ python -m venv venv
    $ source venv/bin/activate
    $ pip install -r app/requirements.txt
    $ cd app && gunicorn --config gunicorn.py 'run:create_app()'

Performance measurement
-----------------------

The commands used to measure the performance of the apps are,

.. code-block::

   $ wrk --connections 20 --duration 5m http://localhost:5000/films/
   $ wrk --connections 20 --duration 5m http://localhost:5000/films/995/
   $ wrk --connections 20 --duration 5m --script post.lua http://localhost:5000/reviews/

Database
--------

All of the above assumes you have the `Postgres sample database
<http://www.postgresqltutorial.com/postgresql-sample-database/>`_
running locally with the following addition made,

.. code-block:: sql

   CREATE TABLE review (
       film_id INTEGER REFERENCES film(film_id),
        rating INTEGER
   );

and a dvdrental user/role to access the database.
