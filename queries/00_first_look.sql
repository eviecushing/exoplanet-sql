-- how many planets has each detection method found?
SELECT discoverymethod, COUNT(*) AS n_planets
FROM planets
GROUP BY discoverymethod
ORDER BY n_planets DESC;
