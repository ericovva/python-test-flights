import sqlite3
from datetime import datetime
from collections import OrderedDict

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#! TODO Async
def find_flight(source, dest):
    with sqlite3.connect('db.sqlite') as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        query = 'select t.*, f.base_fare, f.airline_taxes_amount, f.total_amount, duration from flight f join ticket t ON t.farebasis = f.farebasis where f.source = ? and f.destination = ? order by f.departuretimestamp, farebasis, t.departuretimestamp'
        cursor.execute(query, (source, dest))
        result = cursor.fetchall()
        clusters = OrderedDict()
        for item in result:
            tickets = clusters.setdefault(item['farebasis'], [])
            tickets.append(item)
        return list(clusters.values())

def filter_flight(source, dest, cond=''):
    with sqlite3.connect('db.sqlite') as conn:
        conn.row_factory = dict_factory
        cursor = conn.cursor()
        condition = ''
        if cond == 'cheap':
            condition = 'and f.total_amount = (select min(total_amount) from flight)'
        elif cond == 'expensive':
            condition = 'and f.total_amount = (select max(total_amount) from flight)'
        elif cond == 'long':
            condition = 'and duration = (select max(duration) from flight)'
        elif cond == 'fast':
            condition = 'and duration = (select min(duration) from flight)'

        query = 'select t.*, f.base_fare, f.airline_taxes_amount, f.total_amount, duration from flight f join ticket t ON t.farebasis = f.farebasis where f.source = ? and f.destination = ? {condition}'.format(condition=condition)
        cursor.execute(query, (source, dest))
        result = cursor.fetchall()
        return result
