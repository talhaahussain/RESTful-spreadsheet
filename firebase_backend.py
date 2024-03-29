import os
import json
import requests
import ast

def eval_cformula(cformula, FBASE_URL):
    tree = ast.parse(cformula)
    ids = []
    values = []
    for node in ast.walk(tree):
        if type(node) == ast.Name:
            ids.append(node.__dict__["id"])

    for i in ids:
        if read(i, FBASE_URL) != None:
            values.append(read(i, FBASE_URL)["formula"])
        else:
            values.append(0)
    
    if len(ids) == len(values):
        for i in range(len(ids)):
            cformula = cformula.replace(str(ids[i]), str(values[i]))
    else:
        return None
    
    return eval(cformula)


def create(id, js, FBASE_URL):
    url = FBASE_URL + "/cells/" + id + ".json"
    r = requests.put(url, json=js)
    return r

def read(id, FBASE_URL):
    url = FBASE_URL + "/cells/" + id + ".json"
    r = requests.get(url)
    if r.content.decode("utf-8") == "null":
        return None
    read_cell = ast.literal_eval(ast.literal_eval(r.content.decode("utf-8")))
    cell = {"id": None, "formula": None}
    cell["id"] = read_cell["id"]
    cell["formula"] = read_cell["formula"]
    return cell

def delete(id, FBASE_URL):
    url = FBASE_URL + "/cells/" + id + ".json"
    r = requests.delete(url)
    return r

def list_all(FBASE_URL):
    url = FBASE_URL + "/cells.json"
    r = requests.get(url)
    ids = r.content.decode("utf-8")
    if ids == "null":
        return []
    ids_dict = json.loads(ids)
    ids_list = []
    for i in ids_dict:
        ids_list.append(i)

    return ids_list



if __name__ == "__main__":
    FBASE = os.environ["FBASE"]
    FBASE_URL = "https://" + FBASE + "-default-rtdb.europe-west1.firebasedatabase.app"
    print("Clearing associated Firebase Realtime Database...\n")
    
    for identity in list_all(FBASE_URL):
        delete(identity, FBASE_URL)

    print("Done.")
