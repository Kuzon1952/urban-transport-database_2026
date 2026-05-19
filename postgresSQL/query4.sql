-- Query 4 / Запрос 4
-- RU: Посчитать число водителей с равным числом рейсов.
--     Построить две гистограммы.
-- EN: Count how many drivers have the same number of trips.
--     Build histograms.
-- No A/B parameters in this task.

SELECT
    driver_trip_counts.trip_count,
    COUNT(*) AS driver_count
FROM (
    SELECT
        d.id_driver,
        COUNT(t.id_trip) AS trip_count
    FROM driver d
    LEFT JOIN trip t
        ON t.id_driver = d.id_driver
    GROUP BY
        d.id_driver
) AS driver_trip_counts
GROUP BY
    driver_trip_counts.trip_count
ORDER BY
    driver_trip_counts.trip_count;
