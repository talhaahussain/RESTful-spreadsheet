import sqlite3
import ast

database = "database.db"

##################################
######## Database methods ########
##################################

class Cell:
    def __init__(self, cid, cformula):
        self.cid = cid
        self.cformula = cformula

def eval_cformula(cformula, cursor):
    tree = ast.parse(cformula)
    ids = []
    values = []
    for node in ast.walk(tree):
        if type(node) == ast.Name:
            ids.append(node.__dict__["id"])

    for i in ids:
        if read(i, cursor) != None:
            values.append(read(i, cursor).cformula)
        else:
            values.append(0)
    
    if len(ids) == len(values):
        for i in range(len(ids)):
            cformula = cformula.replace(str(ids[i]), str(values[i]))
    else:
        return None
    
    return eval(cformula)


def create(cid, cformula, cursor):
    cell = Cell(cid, cformula)
    with sqlite3.connect("database.db", check_same_thread=False) as connection:
        if cid not in list_all(cursor):
            cursor.execute(
                "INSERT INTO cells(cid,cformula) VALUES (?,?)",
                (cell.cid,cell.cformula)
            )
            connection.commit()
            return cell
        else:
            cursor.execute(
                "UPDATE cells SET cformula=? WHERE cid=?",
                (cell.cformula,cell.cid)
            )
            connection.commit()
            return cell


def read(cid, cursor):
    with sqlite3.connect("database.db") as connection:
        cursor.execute(
            "SELECT cid, cformula FROM cells WHERE cid=?", (cid,)
        )
        row = cursor.fetchone()
        if row:
            cell = Cell(row[0], row[1])
        else:
            cell = None

        return cell

def delete(cid, cursor):
    with sqlite3.connect("database.db") as connection:
        cursor.execute(
            "DELETE FROM cells WHERE cid=?", (cid,)
        )
        connection.commit()
        return True

def list_all(cursor):
    with sqlite3.connect("database.db") as connection:
        cursor.execute(
            "SELECT cid FROM cells"
        )
        row = cursor.fetchall()
        for i in range(len(row)):
            row[i] = row[i][0]
        return row


def create_table():
    with sqlite3.connect("database.db", check_same_thread=False) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS cells" +
            "(cid TEXT PRIMARY KEY, cformula TEXT)"
        )
        connection.commit()
        
        return cursor

def main():
    print("Testing Sqlite database...\n")
    cursor = create_table()
    list_all(cursor)
    create("B1", "B2 + B3", cursor)
    read("B1", cursor).cformula
    create("B2", "4", cursor)
    create("A7", "9", cursor)
    list_all(cursor)
    delete("A7", cursor)
    list_all(cursor)
    print("Done.")


if __name__ == "__main__":
    main()
