-- do different detection methods find different kinds of planets?
SELECT discoverymethod, COUNT(*) as n_planets, 
ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pl_rade)::numeric, 3) AS median_radius,
ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pl_bmasse)::numeric, 3) AS median_mass,
ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY pl_orbper)::numeric, 3) AS median_orbital_period
FROM planets
GROUP BY discoverymethod
HAVING COUNT(*) >= 10
ORDER BY n_planets DESC;

-- how much data is known?
SELECT discoverymethod, COUNT(pl_rade) AS known_radii, 
COUNT(pl_bmasse) AS known_masses,
COUNT(pl_orbper) AS known_orbital_periods
FROM planets
GROUP BY discoverymethod
HAVING COUNT(*) >= 10
ORDER BY COUNT(*) DESC;

-- is there a selection bias?

SELECT discoverymethod, COUNT(CASE WHEN pl_rade < 1.25 THEN 1 END)  AS earth_size,
COUNT(CASE WHEN pl_rade >= 1.25 AND pl_rade < 2 THEN 1 END) AS super_earth,
COUNT(CASE WHEN pl_rade >= 2 AND pl_rade <= 6 THEN 1 END) AS neptune_size,
COUNT(CASE WHEN pl_rade > 6 THEN 1 END) AS giant,
COUNT(CASE WHEN pl_rade IS NULL THEN 1 END) AS unknown 
FROM planets
GROUP BY discoverymethod
ORDER BY COUNT(*) DESC;