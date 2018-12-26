import xml.etree.cElementTree as ET
#import aiosqlite
import sqlite3
from datetime import datetime
from collections import OrderedDict

def _insert_ticket(cursor, values):
        query = 'INSERT INTO ticket (carrier, flightnumber, source, destination, departuretimestamp, arrivaltimestamp, class, numberofstops, farebasis, warningtext, tickettype) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cursor.execute(query, (*values.values(),))


def _insert_flight(cursor, values):
    query = 'INSERT INTO flight (source, destination, departuretimestamp, arrivaltimestamp, duration, farebasis, base_fare, airline_taxes_amount, total_amount, number_of_tickets) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    cursor.execute(query, (*values.values(),))
    

def _parse_ticket(flight_xml):
    flight = {}
    for field in flight_xml:
        text = field.text 
        if field.tag == 'DepartureTimeStamp' or field.tag == 'ArrivalTimeStamp':
            text = datetime.strptime(text, "%Y-%m-%dT%H%M").strftime("%Y-%m-%dT%H:%M")
        flight[field.tag.lower()] = text.strip() if text else text
    return flight


if __name__ == "__main__":
    tree = ET.parse("RS_Via-3.xml")
    root = tree.getroot() 

    for priced_itineraries in root.iter('PricedItineraries'):
        with sqlite3.connect('db.sqlite') as conn:
            cursor = conn.cursor()
            for flights in priced_itineraries:
                # Onward flights
                tickets = []
                for flight_tag in flights[0].iter('Flight'):
                    tickets.append(_parse_ticket(flight_tag))
                first_ticket = tickets[0]
                last_ticket = tickets[-1]

                # Return flights
                for flight_tag in flights[1].iter('Flight'):
                    tickets.append(_parse_ticket(flight_tag))
                
                flight_prices = flights[2]
                flight = OrderedDict({
                    "source": first_ticket['source'],
                    "destination": last_ticket['destination'],
                    "departuretimestamp": first_ticket['departuretimestamp'],
                    "arrivaltimestamp": last_ticket['arrivaltimestamp'],
                    "duration": (datetime.strptime(tickets[-1]['arrivaltimestamp'], "%Y-%m-%dT%H:%M") - datetime.strptime(first_ticket['departuretimestamp'], "%Y-%m-%dT%H:%M")).seconds,
                    "farebasis": first_ticket['farebasis'],
                    "base_fare": flight_prices[0].text,
                    "airline_taxes_amount": flight_prices[1].text,
                    "total_amount": flight_prices[2].text,
                    "number_of_tickets": len(tickets),
                })

                _insert_flight(cursor, flight)
                # !TODO make one request
                for ticket in tickets:
                    _insert_ticket(cursor, ticket)

            conn.commit()
