import csv
import sqlite3
import click
from string import Template
from app.common import utils
from os.path import expanduser
import os


def create_connection():
    global con
    global cur
    try:
        home = expanduser("~")
        if os.path.exists(home + "/congruous/congruous.db"):
            pass
        else:
            os.makedirs(home + "/congruous/")
        con = sqlite3.connect(home + "/congruous/congruous.db")
        cur = con.cursor()
    except Exception as e:
        click.secho('congruous: ' + str(e), fg="red")


def setup_tables(table_name, drop=None):

    if table_name == 'pan':

        if drop != None:
            query = ''' DROP TABLE PAN '''
            resp = cur.execute(query)
            click.secho(
                'congruous: drop successful. store cleared for document type: ' + table_name, fg="green")

        query = ''' CREATE TABLE IF NOT EXISTS PAN (
            sno INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) ,
            father_name VARCHAR(255),
            pan_id  VARCHAR(10),
            `date` VARCHAR(2),
            month VARCHAR(2),
            `year` VARCHAR(4)
        );'''

        resp = cur.execute(query)
        con.commit()

        return True


def seed_database(table_name, file_contents):

    try:
        #  Insertion format for pan seed
        if table_name == 'pan':

            # validate before hand if the table exists and force seed
            pan_records = [tuple([index + 1, record['name'], record['father_name'], record['pan_id'],
                                  record['date'], record['month'], record['year']]) for index, record in enumerate(file_contents)]

            query = "INSERT INTO PAN VALUES(?,?,?,?,?,?,?);"
            cur.executemany(query, pan_records)
            click.secho('congruous: seed successful. number of records seeded: ' +
                        str(cur.rowcount), fg="green")

            # commit the changes to db
            con.commit()
            return

        if table_name == 'aadhar':
            return

    except Exception as e:
        click.secho('congruous: ' + str(e), fg="red")


def describe_records(document,  operation):

    if operation in ["head", "tail"]:

        if operation == "head":
            query = "SELECT * FROM PAN LIMIT 5;"
        else:
            query = "SELECT * FROM PAN ORDER BY sno DESC LIMIT 5"
        head_data = cur.execute(query)
        column_names = [description[0] for description in cur.description]
        utils.pretty_print_table(head_data, column_names)
        return

    if operation == "count":
        query = " SELECT COUNT(*) FROM PAN"
        number_of_records = cur.execute(query)
        number_of_records = number_of_records.fetchone()[0]
        click.secho(
            'congruous: count successful. number of records : ' + str(number_of_records), fg="green")
        return


def get_hcd_seed(document):

    query = 'SELECT  name, father_name, pan_id, `date`, month, `year` FROM ' + \
        document.upper() + ';'
    con.row_factory = sqlite3.Row
    seed_records = cur.execute(query)

    if document == 'pan':
        fields = ('name', 'father_name', 'pan_id', 'date', 'month', 'year')
        hcd_records = []
        seed_records = seed_records.fetchall()
        for record in seed_records:
            rec = {}
            for index, elem in enumerate(record):
                rec[fields[index]] = elem
            hcd_records.append(rec)
        return hcd_records


def update_store_reports(document, file_name, cong_report):

    query = '''
                CREATE TABLE IF NOT EXISTS REPORTS(
                    report_id INTEGER NOT NULL PRIMARY KEY ,
                    document VARCHAR,
                    ocrd_file VARCHAR,
                    total INTEGER,
                    correct INTEGER,
                    incorrect INTEGER,
                    accuracy INTEGER
                );
            '''
    cur.execute(query)

    insert_query = ' INSERT INTO REPORTS VALUES(?,?,?,?,?,?,?)'

    cur.execute(insert_query, (cong_report[document]['report_id'], document, file_name, cong_report['pan']['total_records']['total'],
                               cong_report['pan']['total_records']['correct'], cong_report['pan']['total_records']['incorrect'], cong_report['pan']['accuracy']))

    # commit the changes to db
    con.commit()
    return


def get_history(document):

    query = "SELECT * FROM REPORTS ORDER BY report_id DESC LIMIT 10"

    history_data = cur.execute(query)
    column_names = [description[0] for description in cur.description]
    utils.pretty_print_table(history_data, column_names)

    return
