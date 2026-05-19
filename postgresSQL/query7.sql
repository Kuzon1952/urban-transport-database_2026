-- Query 7 / Запрос 7
-- RU: Найти водителей, которые никогда не проезжали остановку 'Stop 157'.
-- EN: Find drivers who never passed stop 'Stop 157'.
-- A = 'Stop 157' (stop name)

--I select all drivers for whom there does not exist any trip whose route contains stop 'Stop 157'.
--NOT EXISTS means the driver never passed this stop in any recorded trip.


SELECT
    d.id_driver,
    d.last_name,
    d.first_name,
    d.middle_name,
    d.license_category
FROM driver d
WHERE NOT EXISTS (
    SELECT 1
    FROM trip t
    JOIN route_stop rs
        ON rs.id_route = t.id_route
    JOIN stop s
        ON s.id_stop = rs.id_stop
    WHERE t.id_driver = d.id_driver
      AND s.stop_name = 'Stop 157'
)
ORDER BY
    d.last_name,
    d.first_name,
    d.id_driver;
