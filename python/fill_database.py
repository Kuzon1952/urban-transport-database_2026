"""
Generate and optionally load test data for the Urban Transport database.

Run after schema.sql has created the tables.

Default quantities:
- 3 energy sources 3
- 9 vehicle models 9
- 20 transport types 10
- 2000 drivers 500
- 100 routes 100
- 200 stops 200
- 5 to 20 stops per route [5 to 20]
- 2800 to 3200 vehicles per transport type [50 to 100]
- 43 to 47 trips per driver 
- total generated records: more than 150,000


The script uses only the Python standard library. It writes generated_data.sql
and can execute it with psql when --execute is provided.
"""

from __future__ import annotations

import argparse
import datetime as dt
import getpass
import os
import random
import shutil
import subprocess
from pathlib import Path


ENERGY_SOURCES = [
    "Diesel",
    "Electric overhead wire",
    "Electric rail current",
]

VEHICLE_MODELS = [
    "LiAZ-5292",
    "NefAZ-5299",
    "MAN Lion's City",
    "71-931M Vityaz",
    "71-153 LVS-2005",
    "71-412 Pchyolka",
    "VMZ-5298.01",
    "AKSM-321",
    "Trollza-5265",
]

TRANSPORT_TYPES = [
    ("Bus", "City bus operating on urban roads", "Road", 1, 90),
    ("Trolleybus", "Trolleybus using overhead electrical wire", "Road with wire", 2, 80),
    ("Tram", "Tram running on rail tracks", "Rail in road", 3, 120),
    ("Electric bus", "Battery electric city bus", "Road with charging stations", 2, 85),
    ("Minibus", "Small passenger bus for local routes", "Road", 1, 22),
    ("Express bus", "High-capacity bus for express routes", "Road", 1, 100),
    ("Metro feeder", "Vehicle serving routes to metro stations", "Road", 2, 75),
    ("Suburban tram", "Rail vehicle for longer city routes", "Rail", 3, 130),
    ("Shuttle", "Small shuttle transport for short routes", "Road", 1, 18),
    ("Night bus", "Night public transport route vehicle", "Road", 1, 70),
    ("Airport express", "Express transport route to airport terminals", "Road", 1, 95),
    ("River tram", "Passenger transport on city waterways", "Water", 1, 60),
    ("Cable car", "Cable transport for difficult terrain", "Cable", 2, 35),
    ("Rapid tram", "High-speed tram for main city corridors", "Rail", 3, 140),
    ("Articulated bus", "Long articulated bus for high demand routes", "Road", 1, 150),
    ("School bus", "Special bus route for educational districts", "Road", 1, 45),
    ("Tourist bus", "Passenger bus for tourist city routes", "Road", 1, 50),
    ("Eco shuttle", "Small electric shuttle for central districts", "Road", 2, 25),
    ("Regional bus", "Bus serving city and nearby settlements", "Road", 1, 90),
    ("Service tram", "Technical tram used for service movement", "Rail", 3, 40),
]

LAST_NAMES = [
    "Ivanov", "Petrov", "Sidorov", "Kuznetsov", "Popov",
    "Lebedev", "Kozlov", "Novikov", "Morozov", "Volkov",
    "Sokolov", "Mikhailov", "Fedorov", "Andreev", "Alekseev",
    "Smirnova", "Volkova", "Guseva", "Titova", "Orlova",
]

FIRST_NAMES = [
    "Alexander", "Dmitry", "Sergey", "Andrey", "Mikhail",
    "Ivan", "Nikolay", "Vladimir", "Alexey", "Pavel",
    "Natalia", "Elena", "Olga", "Irina", "Anna",
    "Tatiana", "Maria", "Svetlana", "Ekaterina", "Yulia",
]

MIDDLE_NAMES = [
    "Alexandrovich", "Dmitrievich", "Sergeevich", "Andreevich", "Mikhailovich",
    "Ivanovich", "Nikolaevich", "Vladimirovich", "Alexeevich", "Pavlovich",
    "Alexandrovna", "Dmitrievna", "Sergeevna", "Andreevna", "Mikhailovna",
    "Ivanovna", "Nikolaevna", "Vladimirovna", "Alexeevna", "Pavlovna",
]

DISTRICTS = [
    "Central", "North", "South", "East", "West",
    "Harbor", "University", "Industrial", "Park", "Airport",
]

DRIVER_COUNT = 2000
ROUTE_COUNT = 100
STOP_COUNT = 200
VEHICLES_PER_TYPE_MIN = 2800
VEHICLES_PER_TYPE_MAX = 3200
STOPS_PER_ROUTE_MIN = 5
STOPS_PER_ROUTE_MAX = 20
TRIPS_PER_DRIVER_MIN = 43
TRIPS_PER_DRIVER_MAX = 47


def sql_text(value: str | None) -> str:
    if value is None:
        return "NULL"
    return "'" + value.replace("'", "''") + "'"


def sql_date(value: dt.date) -> str:
    return sql_text(value.isoformat())


def sql_time(value: dt.time) -> str:
    return sql_text(value.strftime("%H:%M:%S"))


def chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[i:i + size] for i in range(0, len(values), size)]


def insert_many(table: str, columns: list[str], values: list[str], batch_size: int = 500) -> str:
    statements: list[str] = []
    column_sql = ", ".join(columns)
    for batch in chunks(values, batch_size):
        statements.append(
            f"INSERT INTO {table} ({column_sql}) VALUES\n"
            + ",\n".join(batch)
            + ";"
        )
    return "\n\n".join(statements)


def random_date(rng: random.Random, start: dt.date, end: dt.date) -> dt.date:
    days = (end - start).days
    return start + dt.timedelta(days=rng.randint(0, days))


def time_from_minutes(minutes: int) -> dt.time:
    minutes = minutes % (24 * 60)
    return dt.time(hour=minutes // 60, minute=minutes % 60)


def build_sql(seed: int, start_date: dt.date, end_date: dt.date) -> tuple[str, dict[str, int]]:
    rng = random.Random(seed)
    lines: list[str] = [
        "-- Generated by fill_database.py",
        "-- Run after schema.sql",
        "",
        "TRUNCATE TABLE",
        "    TRIP,",
        "    ROUTE_STOP,",
        "    VEHICLE,",
        "    TRANSPORT_TYPE,",
        "    ENERGY_SOURCE,",
        "    VEHICLE_MODEL,",
        "    DRIVER,",
        "    ROUTE,",
        "    STOP",
        "RESTART IDENTITY CASCADE;",
        "",
    ]

    energy_values = [f"({sql_text(name)})" for name in ENERGY_SOURCES]
    lines.append(insert_many("ENERGY_SOURCE", ["Name"], energy_values))

    model_values = [f"({sql_text(name)})" for name in VEHICLE_MODELS]
    lines.append(insert_many("VEHICLE_MODEL", ["Name"], model_values))

    type_values: list[str] = []
    for _, description, infrastructure, energy_id, capacity in TRANSPORT_TYPES:
        type_values.append(
            f"({sql_text(description)}, {sql_text(infrastructure)}, {energy_id}, {capacity})"
        )
    lines.append(
        insert_many(
            "TRANSPORT_TYPE",
            ["Description", "Infrastructure_Type", "id_Energy_Source", "Capacity"],
            type_values,
        )
    )

    driver_values: list[str] = []
    for i in range(DRIVER_COUNT):
        last_name = LAST_NAMES[i % len(LAST_NAMES)]
        first_name = FIRST_NAMES[i % len(FIRST_NAMES)]
        middle_name = MIDDLE_NAMES[i % len(MIDDLE_NAMES)]
        license_category = ["D", "D1", "D2"][i % 3]
        driver_values.append(
            f"({sql_text(last_name)}, {sql_text(first_name)}, "
            f"{sql_text(middle_name)}, {sql_text(license_category)})"
        )
    lines.append(
        insert_many(
            "DRIVER",
            ["Last_Name", "First_Name", "Middle_Name", "License_Category"],
            driver_values,
        )
    )

    route_values: list[str] = []
    route_type_by_id: dict[int, int] = {}
    for route_id in range(1, ROUTE_COUNT + 1):
        type_id = ((route_id - 1) % len(TRANSPORT_TYPES)) + 1
        route_type_by_id[route_id] = type_id
        route_type = TRANSPORT_TYPES[type_id - 1][0]
        length_km = round(rng.uniform(4.5, 38.0), 2)
        route_values.append(
            f"({sql_text('Route ' + str(route_id))}, {length_km:.2f}, "
            f"{sql_text(route_type)}, {sql_text('Active')})"
        )
    lines.append(
        insert_many("ROUTE", ["Route_Name", "Length_km", "Route_Type", "Status"], route_values)
    )

    stop_values: list[str] = []
    stop_types = ["Standard", "Terminal", "Transfer", "Express"]
    for stop_id in range(1, STOP_COUNT + 1):
        district = DISTRICTS[(stop_id - 1) % len(DISTRICTS)]
        coordinates = f"59.{90000 + stop_id * 7},30.{30000 + stop_id * 11}"
        stop_values.append(
            f"({sql_text('Stop ' + str(stop_id))}, "
            f"{sql_text('Street ' + str((stop_id % 60) + 1) + ', No. ' + str((stop_id % 25) + 1))}, "
            f"{sql_text(stop_types[stop_id % len(stop_types)])}, "
            f"{sql_text(district)}, {sql_text(coordinates)})"
        )
    lines.append(
        insert_many(
            "STOP",
            ["Stop_Name", "Stop_Address", "Stop_Type", "District", "Coordinates"],
            stop_values,
        )
    )

    vehicle_values: list[str] = []
    vehicles_by_type: dict[int, list[int]] = {}
    next_vehicle_id = 1
    for type_id, (_, _, _, _, type_capacity) in enumerate(TRANSPORT_TYPES, start=1):
        vehicle_count = rng.randint(VEHICLES_PER_TYPE_MIN, VEHICLES_PER_TYPE_MAX)
        vehicles_by_type[type_id] = []
        for item in range(1, vehicle_count + 1):
            model_id = ((type_id + item - 2) % len(VEHICLE_MODELS)) + 1
            capacity = max(10, type_capacity + rng.randint(-8, 8))
            inventory_number = f"INV-{type_id:02d}-{item:03d}"
            year = rng.randint(2000, 2026)
            vehicle_values.append(
                f"({model_id}, {capacity}, {sql_text(inventory_number)}, {year}, {type_id})"
            )
            vehicles_by_type[type_id].append(next_vehicle_id)
            next_vehicle_id += 1
    lines.append(
        insert_many(
            "VEHICLE",
            ["id_Vehicle_Model", "Capacity", "Inventory_Number", "Year_of_Manufacture", "id_Transport_Type"],
            vehicle_values,
        )
    )

    route_stop_values: list[str] = []
    for route_id in range(1, ROUTE_COUNT + 1):
        stop_count = rng.randint(STOPS_PER_ROUTE_MIN, STOPS_PER_ROUTE_MAX)
        selected_stops = rng.sample(range(1, STOP_COUNT + 1), stop_count)
        distance = 0.0
        for order, stop_id in enumerate(selected_stops, start=1):
            if order > 1:
                distance += rng.uniform(0.45, 1.8)
            arrival_minutes = 6 * 60 + (order - 1) * rng.randint(3, 6)
            route_stop_values.append(
                f"({route_id}, {stop_id}, {order}, {distance:.2f}, {sql_time(time_from_minutes(arrival_minutes))})"
            )
    lines.append(
        insert_many(
            "ROUTE_STOP",
            ["id_Route", "id_Stop", "Stop_Order", "Distance_From_Start", "Arrival_Time"],
            route_stop_values,
        )
    )

    trip_values: list[str] = []
    statuses = ["Completed"] * 85 + ["Delayed"] * 10 + ["Cancelled"] * 5
    for driver_id in range(1, DRIVER_COUNT + 1):
        trips_for_driver = rng.randint(TRIPS_PER_DRIVER_MIN, TRIPS_PER_DRIVER_MAX)
        for _ in range(trips_for_driver):
            route_id = rng.randint(1, ROUTE_COUNT)
            type_id = route_type_by_id[route_id]
            vehicle_id = rng.choice(vehicles_by_type[type_id])
            trip_date = random_date(rng, start_date, end_date)
            departure_minutes = rng.randint(5 * 60, 21 * 60)
            duration = rng.randint(45, 120)
            departure_time = time_from_minutes(departure_minutes)
            arrival_time = time_from_minutes(departure_minutes + duration)
            status = rng.choice(statuses)
            trip_values.append(
                f"({sql_date(trip_date)}, {sql_time(departure_time)}, {sql_time(arrival_time)}, "
                f"{sql_text(status)}, {vehicle_id}, {driver_id}, {route_id})"
            )
    lines.append(
        insert_many(
            "TRIP",
            ["Trip_Date", "Departure_Time", "Arrival_Time", "Status", "id_Vehicle", "id_Driver", "id_Route"],
            trip_values,
        )
    )

    lines.append(
        """
SELECT 'ENERGY_SOURCE' AS table_name, COUNT(*) AS records FROM ENERGY_SOURCE
UNION ALL
SELECT 'VEHICLE_MODEL', COUNT(*) FROM VEHICLE_MODEL
UNION ALL
SELECT 'TRANSPORT_TYPE', COUNT(*) FROM TRANSPORT_TYPE
UNION ALL
SELECT 'DRIVER', COUNT(*) FROM DRIVER
UNION ALL
SELECT 'ROUTE', COUNT(*) FROM ROUTE
UNION ALL
SELECT 'STOP', COUNT(*) FROM STOP
UNION ALL
SELECT 'VEHICLE', COUNT(*) FROM VEHICLE
UNION ALL
SELECT 'ROUTE_STOP', COUNT(*) FROM ROUTE_STOP
UNION ALL
SELECT 'TRIP', COUNT(*) FROM TRIP
UNION ALL
SELECT '--- TOTAL ---', (
    SELECT SUM(records) FROM (
        SELECT COUNT(*) AS records FROM ENERGY_SOURCE
        UNION ALL SELECT COUNT(*) FROM VEHICLE_MODEL
        UNION ALL SELECT COUNT(*) FROM TRANSPORT_TYPE
        UNION ALL SELECT COUNT(*) FROM DRIVER
        UNION ALL SELECT COUNT(*) FROM ROUTE
        UNION ALL SELECT COUNT(*) FROM STOP
        UNION ALL SELECT COUNT(*) FROM VEHICLE
        UNION ALL SELECT COUNT(*) FROM ROUTE_STOP
        UNION ALL SELECT COUNT(*) FROM TRIP
    ) s
)
ORDER BY records;
""".strip()
    )

    counts = {
        "ENERGY_SOURCE": len(ENERGY_SOURCES),
        "VEHICLE_MODEL": len(VEHICLE_MODELS),
        "TRANSPORT_TYPE": len(TRANSPORT_TYPES),
        "DRIVER": len(driver_values),
        "ROUTE": len(route_values),
        "STOP": len(stop_values),
        "VEHICLE": len(vehicle_values),
        "ROUTE_STOP": len(route_stop_values),
        "TRIP": len(trip_values),
    }
    counts["TOTAL"] = sum(counts.values())
    return "\n\n".join(lines) + "\n", counts


def run_psql(args: argparse.Namespace, sql_path: Path) -> None:
    psql_path = args.psql or shutil.which("psql")
    if not psql_path:
        raise SystemExit("psql was not found. Generate the SQL file and run it from DBeaver instead.")

    env = os.environ.copy()
    password = args.password or env.get("PGPASSWORD")
    if password is None:
        password = getpass.getpass("PostgreSQL password: ")
    if password:
        env["PGPASSWORD"] = password

    command = [
        psql_path,
        "-h", args.host,
        "-p", str(args.port),
        "-U", args.user,
        "-d", args.database,
        "-v", "ON_ERROR_STOP=1",
        "-f", str(sql_path),
    ]
    subprocess.run(command, check=True, env=env)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate and optionally load urban transport test data.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=5432, type=int)
    parser.add_argument("--database", default="urban_transport_db")
    parser.add_argument("--user", default="postgres")
    parser.add_argument("--password", default=None)
    parser.add_argument("--psql", default=None, help="Optional full path to psql.exe")
    parser.add_argument("--execute", action="store_true", help="Execute generated SQL with psql")
    parser.add_argument("--seed", default=20260512, type=int)
    parser.add_argument("--start-date", default="2024-01-01")
    parser.add_argument("--end-date", default="2026-05-12")
    parser.add_argument("--output", default="generated_data.sql")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    start_date = dt.date.fromisoformat(args.start_date)
    end_date = dt.date.fromisoformat(args.end_date)
    if end_date < start_date:
        raise SystemExit("--end-date must be after --start-date")

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = Path(__file__).resolve().parent / output_path

    sql, counts = build_sql(args.seed, start_date, end_date)
    output_path.write_text(sql, encoding="utf-8")

    print(f"Generated SQL: {output_path}")
    print("Planned record counts:")
    for table, count in counts.items():
        print(f"  {table}: {count}")

    if args.execute:
        run_psql(args, output_path)
        print("Data was loaded successfully.")
    else:
        print("SQL file was generated only. Run it in DBeaver or use --execute.")


if __name__ == "__main__":
    main()
