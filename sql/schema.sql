DROP TABLE IF EXISTS planets; 
DROP TABLE IF EXISTS stars;  -- deletes tables if they already exist

CREATE TABLE stars (
    source_id            BIGINT PRIMARY KEY,   -- Gaia DR3 ID
    ra                   DOUBLE PRECISION,     -- deg  # double prec = data type(decimal with 15 sig dig)
    dec                  DOUBLE PRECISION,     -- deg
    parallax             DOUBLE PRECISION,     -- mas
    parallax_over_error  REAL,                
    pmra                 DOUBLE PRECISION,     -- mas/yr
    pmdec                DOUBLE PRECISION,     -- mas/yr
    phot_g_mean_mag      REAL,                 -- Gaia G magnitude
    bp_rp                REAL                  -- colour
);
CREATE TABLE planets (
    pl_name             TEXT PRIMARY KEY,
    hostname            TEXT NOT NULL,
    gaia_source_id      BIGINT,                 -- links to star.source_id
    discoverymethod     TEXT,
    disc_year           INTEGER,
    disc_facility       TEXT,
    pl_orbper           DOUBLE PRECISION,       -- orbital period, earth days
    pl_rade             DOUBLE PRECISION,       -- radius, earth radii
    pl_bmasse           DOUBLE PRECISION,       -- mass, earth masses
    pl_eqt              DOUBLE PRECISION,       -- equilibrium temp, K
    sy_pnum             INTEGER,                -- planets in the system
    sy_dist             DOUBLE PRECISION,       -- distance, pc
    st_eff              DOUBLE PRECISION       -- host star temp, K
);