-- Query 3 / Запрос 3
-- RU: Для всех моделей ТС посчитать число транспортных средств и рейсов.
--     Построить две гистограммы.
-- EN: For all vehicle models, count vehicles and trips.
--     Build two histograms.
-- No A/B parameters in this task.But i group by vehicle model.

SELECT
    vm.id_vehicle_model,
    vm.name AS model_name,
    COUNT(DISTINCT v.id_vehicle) AS vehicle_count,
    COUNT(t.id_trip) AS trip_count
FROM vehicle_model vm
LEFT JOIN vehicle v
    ON v.id_vehicle_model = vm.id_vehicle_model
LEFT JOIN trip t
    ON t.id_vehicle = v.id_vehicle
GROUP BY
    vm.id_vehicle_model,
    vm.name
ORDER BY
    vm.name;
