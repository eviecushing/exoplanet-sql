-- planets with a matching star in the GCNS sample,
-- and the number of distinct host stars

SELECT COUNT(*) AS n_planets_matched, COUNT(DISTINCT p.hostname) AS n_host_stars
FROM stars s
JOIN planets p ON s.source_id = p.gaia_source_id;

--  For every star in stars, calculate its absolute magnitude, alongside source_id and bp_rp.
--  create a CTE
WITH flagged AS (
SELECT s.source_id, s.bp_rp, s.phot_g_mean_mag + 5 * LOG(s.parallax) - 10 AS absolute_magnitude, 
EXISTS (SELECT 1 FROM planets p WHERE p.gaia_source_id = s.source_id) AS is_host
FROM stars s
)

SELECT is_host, COUNT(*) as n_stars, 
ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY bp_rp)::numeric, 3) AS median_colour,
ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY absolute_magnitude)::numeric, 3) AS median_abs_mag
FROM flagged
GROUP BY is_host;

-- planets closer than 100 pc whose host star is NOT in the stars table
SELECT p.pl_name, p.hostname, p.sy_dist, p.gaia_source_id
FROM planets p
LEFT JOIN stars s ON s.source_id = p.gaia_source_id
WHERE p.sy_dist < 100
  AND s.source_id IS NULL
ORDER BY p.sy_dist;
 