CREATE TABLE flight (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source CHAR(5),
    destination CHAR(5),
    departuretimestamp DATETIME,
    arrivaltimestamp DATETIME,
    duration INTEGER,
    farebasis char(300),
    base_fare FLOAT,
    airline_taxes_amount FLOAT,
    total_amount FLOAT,
    number_of_tickets INTEGER
);

CREATE TABLE ticket (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    carrier char(30),
    flightnumber INTEGER,
    source CHAR(5),
    destination CHAR(5),
    departuretimestamp DATETIME,
    arrivaltimestamp DATETIME,
    class CHAR(2),
    numberofstops INTEGER,
    farebasis char(300),
    warningtext char(500),
    tickettype CHAR(2),

    FOREIGN KEY(farebasis) REFERENCES flight(farebasis)
);
