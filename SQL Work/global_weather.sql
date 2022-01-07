
-- Query 1
SELECT *
FROM city_list
WHERE city = ‘Atlanta’ AND country= ‘United States’;


-- Query 2
SELECT cd.year
	,cd.avg_temp AS city_avg_temp
    ,gd.avg_temp AS global_avg_temp
    ,AVG(cd.avg_temp) OVER(ORDER BY cd.year ROWS BETWEEN 10 PRECEDING AND CURRENT ROW) as city_decade_avg
    ,AVG(gd.avg_temp) OVER(ORDER BY cd.year ROWS BETWEEN 10 PRECEDING AND CURRENT ROW) as global_decade_avg
    ,AVG(cd.avg_temp) OVER(ORDER BY cd.year ROWS BETWEEN 25 PRECEDING AND CURRENT ROW) as city_qcent_avg
    ,AVG(gd.avg_temp) OVER(ORDER BY cd.year ROWS BETWEEN 25 PRECEDING AND CURRENT ROW) as global_qcent_avg
    ,AVG(cd.avg_temp) OVER(ORDER BY cd.year ROWS BETWEEN 50 PRECEDING AND CURRENT ROW) as city_hcent_avg
    ,AVG(gd.avg_temp) OVER(ORDER BY cd.year ROWS BETWEEN 50 PRECEDING AND CURRENT ROW) as global_hcent_avg
    ,AVG(cd.avg_temp) OVER(ORDER BY cd.year ROWS BETWEEN 100 PRECEDING AND CURRENT ROW) as city_cent_avg
    ,AVG(gd.avg_temp) OVER(ORDER BY cd.year ROWS BETWEEN 100 PRECEDING AND CURRENT ROW) as global_cent_avg
FROM city_data cd
JOIN global_data gd
ON cd.year= gd.year
WHERE cd.city = 'Atlanta';
