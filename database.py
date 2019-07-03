#!/usr/bin/env python3

'''Script to search from database. 
'''

import cgi, os.path   
import psycopg2
from psycopg2 import Error


def openConnection(connection):
    """Open database connection"""
    try:
        cursor = connection.cursor()    #allows us to execute PostgreSQL command through Python source code
        return cursor
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

def closeConnection(cursor,connection):
    """closing database connection"""
    if(connection):
        cursor.close()
        connection.close()

def fileToStr(fileName): 
    """Return a string containing the contents of the named file."""
    fin = open(fileName) 
    contents = fin.read()  
    fin.close() 
    return contents

def getColNames(cursor, table_name):
    """Returns table column names from db"""
    cmd = "select column_name from information_schema.columns where table_name = '"+\
            table_name+"' "
    cursor.execute(cmd)
    cols = cursor.fetchall()
    # converts arrays inside arrays to just array
    result = []
    for col in cols:
        result.append(col[0])
    return result