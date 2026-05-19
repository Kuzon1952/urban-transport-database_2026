-- Query 8 / Запрос 8
-- RU: Для каждого источника энергии и модели ТС посчитать число
--     транспортных средств и построить 3D-гистограмму.
-- EN: For each energy source and vehicle model, count vehicles and build
--     a 3D histogram.
-- No A/B parameters in this task.

--I take every combination of energy source and vehicle model.
--Then I count vehicles for each combination.
--The result can be used for a 3D histogram.

SELECT
    es.id_energy_source,
    es.name AS energy_source,
    vm.id_vehicle_model,
    vm.name AS model_name,
    COUNT(v.id_vehicle) AS vehicle_count
FROM energy_source es
CROSS JOIN vehicle_model vm
LEFT JOIN transport_type tt
    ON tt.id_energy_source = es.id_energy_source
LEFT JOIN vehicle v
    ON v.id_transport_type = tt.id_transport_type
   AND v.id_vehicle_model = vm.id_vehicle_model
GROUP BY
    es.id_energy_source,
    es.name,
    vm.id_vehicle_model,
    vm.name
ORDER BY
    es.name,
    vm.name;
