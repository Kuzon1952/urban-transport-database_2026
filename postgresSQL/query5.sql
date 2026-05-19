-- Query 5 / Запрос 5
-- RU: Найти остановки с наибольшим и наименьшим числом маршрутов.
-- EN: Find stops having the largest and the smallest number of routes.
-- No A/B parameters in this task.

--For each stop, I count how many different routes include this stop.
--The first part finds stops where this count equals the maximum value.
--The second part finds stops where this count equals the minimum value.
--UNION ALL combines maximum and minimum results.


SELECT
    'maximum' AS result_type,
    s.id_stop,
    s.stop_name,
    s.stop_address,
    COUNT(DISTINCT rs.id_route) AS route_count
FROM stop s
LEFT JOIN route_stop rs
    ON rs.id_stop = s.id_stop
GROUP BY
    s.id_stop,
    s.stop_name,
    s.stop_address
HAVING COUNT(DISTINCT rs.id_route) = (
    SELECT MAX(stop_counts.route_count)
    FROM (
        SELECT COUNT(DISTINCT rs2.id_route) AS route_count
        FROM stop s2
        LEFT JOIN route_stop rs2
            ON rs2.id_stop = s2.id_stop
        GROUP BY
            s2.id_stop
    ) AS stop_counts
)

UNION ALL

SELECT
    'minimum' AS result_type,
    s.id_stop,
    s.stop_name,
    s.stop_address,
    COUNT(DISTINCT rs.id_route) AS route_count
FROM stop s
LEFT JOIN route_stop rs
    ON rs.id_stop = s.id_stop
GROUP BY
    s.id_stop,
    s.stop_name,
    s.stop_address
HAVING COUNT(DISTINCT rs.id_route) = (
    SELECT MIN(stop_counts.route_count)
    FROM (
        SELECT COUNT(DISTINCT rs2.id_route) AS route_count
        FROM stop s2
        LEFT JOIN route_stop rs2
            ON rs2.id_stop = s2.id_stop
        GROUP BY
            s2.id_stop
    ) AS stop_counts
)
ORDER BY
    result_type,
    stop_name;
