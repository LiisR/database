#!/usr/bin/env python3

'''Script to process data upload. 
'''

import cgi, os.path   
import psycopg2
from psycopg2 import Error

import database as db

DATABASE_NAME = "Proovitoo"
TABLE_NAME = "personal_data"
connection = psycopg2.connect(user = "postgres",
                                  password = "ProovitooSQL1",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = DATABASE_NAME) 

def main():
    form = cgi.FieldStorage()  
    filename = form.getfirst('filename')

    processResults = processDbData(filename)
    contents = db.fileToStr('data_access.html')   # process input into a page
    print(contents)
    print(processResults)

def processDbData(file_name):
    """Opens connection with database, 
    creates table, fills with data and 
    closes connection with db"""
    # open database connection
    cur = db.openConnection(connection)  
    # read in the fail data
    done = readFile(file_name,cur)
    # close the database connection
    db.closeConnection(cur,connection) 
    return done

def readFile(name, cursor):

    f = open(name)
    idn_names = cleanTokens(f.readline())   # from first line get column names
    col_names = db.getColNames(cursor, TABLE_NAME) # from database get column names
    id_names = matchColNames(idn_names, col_names)  # compare db col names with the ones from file and match
    createNewTable(id_names,cursor) # create table

    # used to make parts of sql cmd
    data_types = ""
    data_names = ""
    for names in id_names:
        data_names += names+", " # before use remove last comma
        data_types += "%s,"

    # read lines from file and add the data to db
    line = f.readline()
    while line:
        data = cleanTokens(line) # split the line from ";" and remove linebreak       
        addData(data_names[:-2], data, data_types[:-1], cursor) #remove ", " and "," from end of the line
        line = f.readline()

    f.close()
    return "&nbsp;Fail laetud edukalt!<br>"

def matchColNames(id_names, col_names):
    """Matches and rearranges col names of table and file"""
    if len(col_names) != 0:
        result = []
        for id_n in id_names:
            for col_n in col_names:
                if id_n in ["id_code","isikukood"] and col_n in ["id_code","isikukood"]:
                    result.append(col_n)
                if "visit" in id_n and "visit" in col_n:
                    result.append(col_n)
                if  "last" in id_n and "last" in col_n:
                    result.append(col_n)
                if  "first" in id_n and "first" in col_n:
                    result.append(col_n)
                if  "dep" in id_n and "dep" in col_n:
                    result.append(col_n)
                if  "email" in id_n and "email" in col_n:
                    result.append(col_n)
                if  col_n != "id_code" and col_n == id_n and "code" in id_n:
                    result.append(col_n)
        return result
    else:
        return id_names
    
def cleanTokens(line):
    """Split from ";" and remove linebreak from last element"""
    tokens = line.split(";")
    tokens[len(tokens)-1] = tokens[len(tokens)-1][:-1]
    return tokens

def createNewTable(id_names, cursor):
    """Creates a new table with a name 
    TABLE_NAME if it does not exist"""

    new_table = "CREATE TABLE IF NOT EXISTS "+TABLE_NAME+" ("\
                +id_names[0]+" TEXT PRIMARY KEY,"   #ID INT PRIMARY KEY     NOT NULL
    for i in range(1,len(id_names)):
        new_table += " "+id_names[i]+ " TEXT NOT NULL,"
    new_table = new_table[:-1]
    new_table += ");"
    try:
        cursor.execute(new_table)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)

def addData(data_names, data, data_types,cursor):
    """Add new data to db, on conflict do nothing"""
    try:
        insert_query = " INSERT INTO "+TABLE_NAME+" ("+data_names+ \
                        ") VALUES ("+data_types+") ON CONFLICT DO NOTHING"
        cursor.execute(insert_query, data)
        connection.commit()
    except (Exception, psycopg2.Error) as error :
        print("Failed to insert record into table", error)

try:   
    print("Content-type: text/html\n\n")   
    main() 
except:
    cgi.print_exception()
