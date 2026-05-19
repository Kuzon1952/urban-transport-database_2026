-- Query 6 / Запрос 6
-- RU: Найти транспортные средства, которые выполнили меньше рейсов,
--     чем транспортное средство с инвентарным номером 'INV-08-989'.
-- EN: Find vehicles that performed fewer trips than vehicle 'INV-08-989'.
-- A = 'INV-08-989' (vehicle inventory number)
-- Terminal note:
--   The full result can contain many rows, so this file shows the first
--   50 vehicles and also prints the total number in total_matching_vehicles.
--   Remove LIMIT 50 if the teacher asks to output the full list.

--I count trips for every vehicle.
--Then I compare each vehicle’s trip count with the trip count of vehicle 'INV-08-989'.
--The query returns vehicles whose number of trips is smaller.
--LIMIT 50 is only for terminal demonstration because the full result is large.

SELECT
    COUNT(*) OVER () AS total_matching_vehicles,
    v.id_vehicle,
    v.inventory_number,
    vm.name AS model_name,
    tt.description AS transport_type,
    COALESCE(tc.trip_count, 0) AS trip_count,
    vehicle_a.inventory_number AS compared_vehicle,
    COALESCE(tc_a.trip_count, 0) AS compared_vehicle_trip_count
FROM vehicle v
JOIN vehicle_model vm
    ON vm.id_vehicle_model = v.id_vehicle_model
JOIN transport_type tt
    ON tt.id_transport_type = v.id_transport_type
LEFT JOIN (
    SELECT
        id_vehicle,
        COUNT(*) AS trip_count
    FROM trip
    GROUP BY
        id_vehicle
) AS tc
    ON tc.id_vehicle = v.id_vehicle
JOIN vehicle vehicle_a
    ON TRUE
LEFT JOIN (
    SELECT
        id_vehicle,
        COUNT(*) AS trip_count
    FROM trip
    GROUP BY
        id_vehicle
) AS tc_a
    ON tc_a.id_vehicle = vehicle_a.id_vehicle
WHERE vehicle_a.inventory_number = 'INV-08-989'
  AND v.id_vehicle <> vehicle_a.id_vehicle
  AND COALESCE(tc.trip_count, 0) < COALESCE(tc_a.trip_count, 0)
ORDER BY
    trip_count DESC,
    v.inventory_number
LIMIT 50;
