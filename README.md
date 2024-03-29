# ECM3408-Assessment
Continuous Assessment for ECM3408 - Enterprise Computing, set by Prof. David Wakeling. Involves the use of a RESTful interface to implement a spreadsheet MVP as an SC microservice. 

This work received a mark of 92/100, although this may be subject to increase in the future.

### Prerequisites

### Usage

This submission includes this file and three other Python files. `sc.py` is the main program containing the Flask app.

The following instructions assume that you are trying to run the program on a Linux machine, with Python 3.6.8, flask and requests libraries, as well as standard libraries.

To run the program, please use either

```
python3 sc.py -r sqlite
```

or

```
python3 sc.py -r firebase
```

The option selected depends on whether you intend to have data stored in an Sqlite database, or a Firebase Realtime Database. Please note that you must set up your own Firebase Realtime Database and obtain your own unique link to use the latter option. You will also need to ensure that you have a valid database name stored in an environment variable `FBASE`. This can be done using the following

```
export FBASE=<your database name here>
```

Please note that `sc.py` will not run unless the `-r` flag has been supplied, followed by one of the two above options provided.

`firebase_backend.py` can be run to clear any current data in a Firebase Realtime Database (assuming you've already exported the database name in this session). `sqlite_backend.py` can be run to test the database functions.
