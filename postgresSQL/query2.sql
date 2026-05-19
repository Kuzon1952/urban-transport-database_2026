-- Query 2 / Запрос 2
-- RU: Посчитать число маршрутов, по которым выполняли рейсы транспортные
--     средства с источником энергии 'Diesel'.
-- EN: Count routes where vehicles using energy source 'Diesel' performed trips.
-- A = 'Diesel' (energy source name)

SELECT
    es.id_energy_source,
    es.name AS energy_source,
    COUNT(DISTINCT t.id_route) AS route_count
FROM energy_source es
JOIN transport_type tt
    ON tt.id_energy_source = es.id_energy_source
JOIN vehicle v
    ON v.id_transport_type = tt.id_transport_type
JOIN trip t
    ON t.id_vehicle = v.id_vehicle
WHERE es.name = 'Diesel'
GROUP BY
    es.id_energy_source,
    es.name;
