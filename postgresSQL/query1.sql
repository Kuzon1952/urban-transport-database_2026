-- Query 1 / Запрос 1
-- RU: Найти водителей, которые выполняли рейсы на транспортном средстве
--     с инвентарным номером 'INV-08-989' и проезжали остановку 'Stop 157'.
-- EN: Find drivers who performed trips on vehicle 'INV-08-989'
--     and passed stop 'Stop 157'.
-- A = 'INV-08-989' (vehicle inventory number)
-- B = 'Stop 157' (stop name)

SELECT DISTINCT
    d.id_driver,
    d.last_name,
    d.first_name,
    d.middle_name,
    d.license_category,
    v.inventory_number AS vehicle,
    s.stop_name AS stop
FROM vehicle v
JOIN trip t
    ON t.id_vehicle = v.id_vehicle
JOIN driver d
    ON d.id_driver = t.id_driver
JOIN route_stop rs
    ON rs.id_route = t.id_route
JOIN stop s
    ON s.id_stop = rs.id_stop
WHERE v.inventory_number = 'INV-08-989'
  AND s.stop_name = 'Stop 157'
ORDER BY
    d.last_name,
    d.first_name,
    d.id_driver;
