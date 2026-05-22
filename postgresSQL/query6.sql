-- Query 6 / Запрос 6
-- RU: Найти транспортные средства, которые выполнили меньше рейсов,
--     чем транспортное средство с id_vehicle 4.
-- EN: Find vehicles that performed fewer trips than vehicle 
-- A = 4 (vehicle inventory number)

SELECT 
    v.id_vehicle,
    v.inventory_number,
    vm.name            AS model_name,
    COUNT(t.id_trip)   AS trip_count
FROM vehicle v
JOIN vehicle_model vm ON v.id_vehicle_model = vm.id_vehicle_model
JOIN trip t            ON v.id_vehicle = t.id_vehicle
GROUP BY v.id_vehicle, v.inventory_number, vm.name
HAVING COUNT(t.id_trip) < (
    SELECT COUNT(*)
    FROM trip
    WHERE id_vehicle = 4
)
ORDER BY trip_count DESC;