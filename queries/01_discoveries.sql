-- how has the number of discoveries changed over time, and which detection methods drove it?

-- planets discovered per year and detection method
SELECT disc_year, discoverymethod, COUNT(*) AS n_planets
FROM planets
GROUP BY disc_year, discoverymethod
ORDER BY disc_year, n_planets DESC;

-- running total over the years
SELECT disc_year,COUNT(*) AS n_planets,
SUM(COUNT(*)) OVER (ORDER BY disc_year) AS running_total
FROM planets
GROUP BY disc_year
ORDER BY disc_year;

-- how many were discovered by transit method each year
SELECT disc_year, COUNT(*) AS n_planets,
COUNT(CASE WHEN discoverymethod = 'Transit' THEN 1 END) AS number_by_transit
FROM planets
GROUP BY disc_year
ORDER BY disc_year ASC;

-- why is there a peak in 2016?
SELECT disc_facility, COUNT(*) AS n_planets
FROM planets WHERE disc_year=2016
GROUP BY disc_facility
ORDER BY n_planets DESC;
