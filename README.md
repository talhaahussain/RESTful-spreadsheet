# ECM3408-Assessment
Continuous Assessment for ECM3408 - Enterprise Computing, set by Prof. David Wakeling. Involves the use of a RESTful interface to implement a spreadsheet MVP as an SC microservice. This microservice was implemented in Flask and uses the repository design pattern, currently supporting 2 data sources, an SQL and a No-SQL database.

This work received a mark of 92/100, although this may be subject to increase in the future.

### Prerequisites

Python 3.6.8, the libraries *flask* and *requests*, as well as SQLite3.

### Usage

#### Starting Microservice

This submission includes this file and three other Python files. `sc.py` is the main program containing the Flask app.

The following instructions assume that you are trying to run the program on a Linux machine.

To run the program, please use either

```
python3 sc.py -r sqlite
```

or

```
python3 sc.py -r firebase
```

The option selected depends on whether you intend to have data stored in an SQLite database, or a Firebase Realtime Database. Please note that you must set up your own Firebase Realtime Database and obtain your own unique link to use the latter option. You will also need to ensure that you have a valid database name stored in an environment variable `FBASE`. This can be done using the following

```
export FBASE=<your database name here>
```

Please note that `sc.py` will not run unless the `-r` flag has been supplied, followed by one of the two above options provided.

`firebase_backend.py` can be run to clear any current data in a Firebase Realtime Database (assuming you've already exported the database name in this session). `sqlite_backend.py` can be run to test the database functions.

The microservice should listen on port 3000, once running.

#### Creating/Updating Cells

Cells can be created using the PUT method to */cells/id*, providing a JSON object that has an `id` property whose value is a string representing the cell identifier, and a `formula` property whose value is a string representing its formula. Please note that the `id` property must match the id specified in */cells/id*.

Cells are updated in the exact same manner, where the id in */cells/id* points to an existing cell.

When creating or updating a cell, if a mathematical formula is provided, or other cells are referenced (or both), the values of specified cells will be retrieved from storage and the given formula will be computed prior to storage. When this cell is read (see next section), the value will reflect the evaluated expression.

An example of cell creation (with id "B2" and formula "6") using cURL is specified below
```
curl -X PUT -H "Content-Type: application/json" -d "{\"id\":\"B2\",\"formula\":\"6\"}" localhost:3000/cells/B2
```

#### Reading Cells

Cells can be read from using the GET method to */cells/id*, where id corresponds to the desired cell.

An example of cell reading (with id "B2") using cURL is specified below
```
curl -X GET localhost:3000/cells/B2
```

#### Deleting Cells

Cells can be deleted using the DELETE method to */cells/id*.

An example of cell deletion (with id "B2") using cURL is specified below
```
curl -X DELETE localhost:3000/cells/B2
```

#### Listing Cells

A list of all cells can be obtained using the GET method to */cells*.

An example of listing all cells using cURL is specified below
```
curl -X GET localhost:3000/cells
```

### Limitations

The formula evaluation function does not check for cycles between cells. Division by zero is not supported, neither are imaginary numbers. Only the following operators are accepted: '+', '-', '*', '/' and unary '-'.

### Footnote

The `tests/` contains two bash scripts. `test10.sh` was provided to students to provide a benchmark for program functionality. `test50.sh` was the final script used to assess the project, run with both SQLite and Firebase.
