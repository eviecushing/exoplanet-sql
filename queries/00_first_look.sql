-- How many planets has each detection method found?
SELECT discoverymethod, COUNT(*) AS n_planets
FROM planets
GROUP BY discoverymethod
ORDER BY n_planets DESC;

-- Which year were the most planets discovered?
SELECT disc_year as year , count(*) as n_planets_discovered
FROM planets GROUP BY disc_year
ORDER BY n_planets_discovered DESC;

-- Which planet hosts (stars) are in the nearby Gaia sample, and how far away are they?
SELECT p.hostname, COUNT(*) AS n_planets,
ROUND((1000 / MIN(s.parallax))::numeric,1) AS distance_pc,
MIN(s.bp_rp) AS colour_bp_rp
FROM planets p 
JOIN stars s ON s.source_id = p.gaia_source_id
GROUP BY p.hostname
ORDER BY n_planets DESC, distance_pc
LIMIT 10;