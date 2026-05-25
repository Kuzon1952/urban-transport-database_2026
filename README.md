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

```
urban-transport-database/
│
├── README.md
│
├──postgreSQL
|   ├──queries.jpg
|   ├──schema.sql
|   ├──generated_data.sql
|   ├──query1.sql
|   ├──query2.sql
|   ├──query3.sql
|   ├──query4.sql
|   ├──query5.sql
|   ├──query6.sql
|   ├──query7.sql
|   ├──query8.sql
|   ├──query9.sql
│
├── report/
│   └── Transport_Database_Report.pdf 
│
└── python/
    ├── fill_database.py
```
## Python 
- 01. fill_database.py it generates "generated_data.sql"

## SQL Files 

- 01. schema.sql
- 02. generated_data.sql
- 03. query1.sql
- 04. query2.sql
- 05. query3.sql
- 06. query4.sql
- 07. query5.sql
- 08. query6.sql
- 09. query7.sql
- 10. query8.sql
- 11. query9.sql
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
