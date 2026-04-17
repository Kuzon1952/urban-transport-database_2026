# Urban Transport Database

## Description

This project is a relational database system developed for the subject area "urban public transport movement accounting".

The database is designed to store and manage information about vehicles, routes, drivers, stops, and trips, as well as to analyze transport activity within a city.

---

## Features

- Relational database design
- SQL implementation
- Transport movement tracking
- Route and stop management
- Trip recording and analysis
- Data integrity using primary and foreign keys

---

## Database Entities

- Transport_Type — classification of transport (bus, tram, trolleybus)
- Vehicle — transport unit
- Driver — person operating the vehicle
- Route — predefined path
- Stop — transport stop
- Trip — execution of a route
- Route_Stop — link between routes and stops

---

## Project Structure

urban-transport-database/
│
├── README.md
│
├── report/
│   └── Transport_Database_Report.pdf
│
└── project/
    └── src/
        ├── 01_create_tables.sql
        ├── 02_insert_reference_data.sql
        ├── 03_generate_data.sql
        ├── 04_queries.sql
        ├── 05_triggers.sql
        └── 06_procedures.sql

---

## SQL Files

- 01_create_tables.sql — create database schema
- 02_insert_reference_data.sql — insert base data
- 03_generate_data.sql — generate test data
- 04_queries.sql — SQL queries
- 05_triggers.sql — triggers
- 06_procedures.sql — stored procedures

---

## How to Run

1. Open your DBMS (MySQL or PostgreSQL)
2. Run scripts in order:
   - create tables
   - insert data
   - generate data
   - run queries
3. Check results

---

## Technologies

- SQL
- Relational Databases

---

## Author

Ovi Md Shamin Yasir  
SPbPU — Mathematics and Computer Science

---

## License

MIT
