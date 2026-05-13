
-- Appendix A: Database Schema Generation
-- Topic: Urban Transport Movement Tracking
-- DBMS: PostgreSQL

-- Drop tables in reverse dependency order (safe re-run)
DROP TABLE IF EXISTS TRIP CASCADE;
DROP TABLE IF EXISTS ROUTE_STOP CASCADE;
DROP TABLE IF EXISTS VEHICLE CASCADE;
DROP TABLE IF EXISTS TRANSPORT_TYPE CASCADE;
DROP TABLE IF EXISTS ENERGY_SOURCE CASCADE;
DROP TABLE IF EXISTS VEHICLE_MODEL CASCADE;
DROP TABLE IF EXISTS DRIVER CASCADE;
DROP TABLE IF EXISTS ROUTE CASCADE;
DROP TABLE IF EXISTS STOP CASCADE;


-- Level 1 tables (no foreign keys — filled first)
-- Table 1: ENERGY_SOURCE
-- Lookup table of energy types used by transport (3 records)
CREATE TABLE ENERGY_SOURCE (
    id_Energy_Source  SERIAL        PRIMARY KEY,
    Name              VARCHAR(50)   NOT NULL UNIQUE
);

-- Table 2: VEHICLE_MODEL
-- Lookup table of vehicle models (9 records)
CREATE TABLE VEHICLE_MODEL (
    id_Vehicle_Model  SERIAL        PRIMARY KEY,
    Name              VARCHAR(100)  NOT NULL
);

-- Table 3: TRANSPORT_TYPE
-- Classification of transport by technical characteristics (20 records)
CREATE TABLE TRANSPORT_TYPE (
    id_Transport_Type   SERIAL        PRIMARY KEY,
    Description         VARCHAR(200),
    Infrastructure_Type VARCHAR(100)  NOT NULL,
    id_Energy_Source    INT           NOT NULL REFERENCES ENERGY_SOURCE(id_Energy_Source),
    Capacity            INT           NOT NULL CHECK (Capacity > 0)
);

-- Table 4: DRIVER
-- Drivers who operate vehicles on routes (2000 records)
CREATE TABLE DRIVER (
    id_Driver          SERIAL        PRIMARY KEY,
    Last_Name          VARCHAR(100)  NOT NULL,
    First_Name         VARCHAR(100)  NOT NULL,
    Middle_Name        VARCHAR(100),
    License_Category   VARCHAR(10)   NOT NULL
);

-- Table 5: ROUTE
-- Fixed paths for vehicle movement (100 records)
CREATE TABLE ROUTE (
    id_Route     SERIAL           PRIMARY KEY,
    Route_Name   VARCHAR(100)     NOT NULL,
    Length_km    DECIMAL(6,2)     NOT NULL CHECK (Length_km > 0),
    Route_Type   VARCHAR(50)      NOT NULL,
    Status       VARCHAR(20)      NOT NULL DEFAULT 'Active'
);

-- Table 6: STOP
-- Fixed points where vehicles stop (200 records)
CREATE TABLE STOP (
    id_Stop       SERIAL        PRIMARY KEY,
    Stop_Name     VARCHAR(200)  NOT NULL,
    Stop_Address  VARCHAR(200),
    Stop_Type     VARCHAR(50)   NOT NULL,
    District      VARCHAR(100),
    Coordinates   VARCHAR(50)
);

-- Level 2 tables (depend on Level 1)
-- Table 7: VEHICLE
-- Physical transport units assigned to a type and model (2800 to 3200 vehicles per transport type)
CREATE TABLE VEHICLE (
    id_Vehicle          SERIAL        PRIMARY KEY,
    id_Vehicle_Model    INT           NOT NULL REFERENCES VEHICLE_MODEL(id_Vehicle_Model),
    Capacity            INT           NOT NULL CHECK (Capacity > 0),
    Inventory_Number    VARCHAR(20)   NOT NULL UNIQUE,
    Year_of_Manufacture INT           NOT NULL CHECK (Year_of_Manufacture BETWEEN 1990 AND 2026),
    id_Transport_Type   INT           NOT NULL REFERENCES TRANSPORT_TYPE(id_Transport_Type)
);

-- Table 8: ROUTE_STOP
-- Junction table: which stops belong to which route and in what order (5 to 20 stops per route)
CREATE TABLE ROUTE_STOP (
    id_Route_Stop         SERIAL          PRIMARY KEY,
    id_Route              INT             NOT NULL REFERENCES ROUTE(id_Route),
    id_Stop               INT             NOT NULL REFERENCES STOP(id_Stop),
    Stop_Order            INT             NOT NULL CHECK (Stop_Order > 0),
    Distance_From_Start   DECIMAL(6,2)    NOT NULL CHECK (Distance_From_Start >= 0),
    Arrival_Time          TIME,
    UNIQUE (id_Route, Stop_Order)
);

-- Level 3 table (depends on Level 2)
-- Table 9: TRIP
-- A route execution by a vehicle under a driver at a specific time
CREATE TABLE TRIP (
    id_Trip          SERIAL       PRIMARY KEY,
    Trip_Date        DATE         NOT NULL,
    Departure_Time   TIME         NOT NULL,
    Arrival_Time     TIME,
    Status           VARCHAR(20)  NOT NULL DEFAULT 'Completed',
    id_Vehicle       INT          NOT NULL REFERENCES VEHICLE(id_Vehicle),
    id_Driver        INT          NOT NULL REFERENCES DRIVER(id_Driver),
    id_Route         INT          NOT NULL REFERENCES ROUTE(id_Route)
);

-- Indexes for common query patterns
CREATE INDEX idx_trip_date       ON TRIP(Trip_Date);
CREATE INDEX idx_trip_route      ON TRIP(id_Route);
CREATE INDEX idx_trip_vehicle    ON TRIP(id_Vehicle);
CREATE INDEX idx_trip_driver     ON TRIP(id_Driver);
CREATE INDEX idx_route_stop_route ON ROUTE_STOP(id_Route);
CREATE INDEX idx_vehicle_type    ON VEHICLE(id_Transport_Type);
