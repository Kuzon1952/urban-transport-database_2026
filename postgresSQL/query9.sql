-- Query 9 / Запрос 9
-- RU: Для транспортного средства с инвентарным номером 'INV-08-989'
--     в рейсе 4432 поменять водителя 99 на водителя 1.
-- EN: For vehicle 'INV-08-989', in trip 4432, change driver 99 to driver 1.
-- Vehicle A = 'INV-08-989' (vehicle inventory number)
-- Trip A = 4432 (trip id)
-- Driver A = 99 (old driver id)
-- Driver B = 1 (new driver id)


UPDATE trip t
SET id_driver = 1
FROM vehicle v
WHERE t.id_vehicle = v.id_vehicle
  AND v.inventory_number = 'INV-08-989'
  AND t.id_trip = 4432
  AND t.id_driver = 99
RETURNING
    t.id_trip,
    v.inventory_number AS vehicle,
    99 AS old_driver_id,
    t.id_driver AS new_driver_id,
    t.id_route,
    t.trip_date,
    t.departure_time;
