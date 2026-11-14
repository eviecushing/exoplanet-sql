-- is there a shortage of planets between certain Earth radii in the archive?

SELECT width_bucket(pl_rade, 1, 4, 30) AS bin,
ROUND((1.0 + (width_bucket(pl_rade, 1, 4, 30) - 1) * 0.1)::numeric, 1)
AS bin_lower_edge, COUNT(*) AS n_planets
from planets
WHERE pl_rade >= 1 AND pl_rade < 4
GROUP BY bin
ORDER BY bin ASC;



-- clean sample and take logs (CTF splits up code so readable and reusable)
WITH clean AS (
    SELECT pl_rade FROM planets
    WHERE discoverymethod = 'Transit'
    AND pl_rade >= 1
    AND pl_rade < 4
)

SELECT width_bucket(LN(pl_rade), LN(1), LN(4), 20) AS bin,
ROUND(EXP(LN(1) + (width_bucket(LN(pl_rade), LN(1), LN(4), 20) - 1) * (LN(4) - LN(1)) / 20.0)::numeric, 3) AS bin_lower_edge,
COUNT(*) AS n_planets
FROM clean
GROUP BY bin
ORDER BY bin ASC;

-- planets in ranges of interest
SELECT 
    COUNT(CASE WHEN pl_rade >= 1.0 AND pl_rade < 1.5 THEN 1 END) AS range_1_0_to_1_5,
    COUNT(CASE WHEN pl_rade >= 1.5 AND pl_rade < 2.0 THEN 1 END) AS range_1_5_to_2_0,
    COUNT(CASE WHEN pl_rade >= 2.0 AND pl_rade <= 2.5 THEN 1 END) AS range_2_0_to_2_5
FROM planets;
