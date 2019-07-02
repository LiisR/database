#!/usr/bin/env python3

'''Script to search from database. 
'''

import cgi, os.path   
import psycopg2
from psycopg2 import Error

import re

DATABASE_NAME = "DataCamp_Courses"
TABLE_NAME = "personal_data"
connection = psycopg2.connect(user = "postgres",
                                  password = "ProovitooSQL1",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = DATABASE_NAME) 

def main():
    form = cgi.FieldStorage()  
    search_id = form.getfirst('id_number', '')
    search_results = processDbData(search_id, "id_code")

    contents = processInput(search_id)   # process input into a page

    print(contents)
    print(search_results)

def processDbData(search_id, search_col):
    """Opens connection with database, 
    data search from db, create html page 
    with retrieved results and 
    closes connection with db"""
    cur = openConnection()
    records = getPartialSearchResults(cur,search_col,search_id)
    results_table = createHTMLTable(records,cur)
    closeConnection(cur)
    return results_table

def createHTMLTable(records,cursor):
    """Create html table based on data search results"""
    col_names = getColNames(cursor)
    html = "&nbsp;Leiti "+str(len(records))+""" kirjet!<br><table 
            style="width:100%"><tr>"""
    for col in col_names:
        html +="<th>"+col[0]+"</th>"
    for data in records:
        html += "<tr>"
        for i in range(len(col_names)):
            html +="<td>"+data[i]+"</th>"
        html += "</tr>"
    html += "</table>" 
    return html

def openConnection():
    """Open database connection"""
    try:
        cursor = connection.cursor()    #allows us to execute PostgreSQL command through Python source code
        return cursor
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

def closeConnection(cursor):
    """closing database connection"""
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

def processInput(numStr1):  
    '''Process input parameters and return the final page as a string.'''
    num1 = numStr1 # transform input to output data
    return fileToStr('data_access.html').format(**locals())

def fileToStr(fileName): 
    """Return a string containing the contents of the named file."""
    fin = open(fileName) 
    contents = fin.read() 
    fin.close() 
    return contents

def cleanTokens(line):
    "Split from ; and remove linebreak from last element"
    tokens = line.split(";")
    tokens[len(tokens)-1] = tokens[len(tokens)-1][:-1]
    return tokens

def getPartialSearchResults(cursor, col_name, search_criteria):
    """Search data from db table and return the results"""
    select_querys = "SELECT * FROM "+TABLE_NAME+ \
                    " WHERE "+col_name+" LIKE '"+search_criteria+"%';"
    cursor.execute(select_querys,)
    records = cursor.fetchall()
    return records

def getColNames(cursor):
    """Returns table column names from db"""
    cmd = "select column_name from information_schema.columns where table_name = '" \
        +TABLE_NAME+"' "
    cursor = connection.cursor()
    cursor.execute(cmd)
    cols = cursor.fetchall()
    return cols

try:   # NEW
    print("Content-type: text/html\n\n")   # say generating html
    main() 
except:
    cgi.print_exception()                 # catch and print errors
