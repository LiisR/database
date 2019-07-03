#!/usr/bin/env python3

'''Script to search from database. 
'''

import cgi, os.path   
import psycopg2
from psycopg2 import Error
import database as db

import re

DATABASE_NAME = "Proovitoo"
TABLE_NAME = "personal_data"
connection = psycopg2.connect(user = "postgres",
                                  password = "ProovitooSQL1",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = DATABASE_NAME) 

def main():
    form = cgi.FieldStorage()  
    search_id = form.getfirst('id_number', '')
    search_results = processDbData(search_id)

    contents = db.fileToStr('data_access.html')   # process input into a page

    print(contents)
    print(search_results)

def processDbData(search_id):
    """Opens connection with database, 
    data search from db, create html page 
    with retrieved results and 
    closes connection with db"""
    cur = db.openConnection(connection)
    col_names = db.getColNames(cur,TABLE_NAME)
    search_col = "id_code"
    if "isikukood" in col_names:
        search_col = "isikukood"

    records = getPartialSearchResults(cur,search_col,search_id)
    results_table = createHTMLTable(records,cur)
    db.closeConnection(cur,connection)
    return results_table

def createHTMLTable(records,cursor):
    """Create html table based on data search results"""
    col_names = db.getColNames(cursor,TABLE_NAME)
    html = "&nbsp;Leiti "+str(len(records))+""" kirjet!<br><table 
            style="width:100%"><tr>"""
    for col in col_names:
        html +="<th>"+col+"</th>"
    for data in records:
        html += "<tr>"
        for i in range(len(col_names)):
            html +="<td>"+data[i]+"</th>"
        html += "</tr>"
    html += "</table>" 
    return html

def getPartialSearchResults(cursor, col_name, search_criteria):
    """Search data from db table and return the results"""
    select_querys = "SELECT * FROM "+TABLE_NAME+ \
                    " WHERE "+col_name+" LIKE '"+search_criteria+"%';"
    cursor.execute(select_querys,)
    records = cursor.fetchall()
    return records

try:   # NEW
    print("Content-type: text/html\n\n")   # say generating html
    main() 
except:
    cgi.print_exception()                 # catch and print errors
