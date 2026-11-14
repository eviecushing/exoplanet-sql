from pathlib import Path
import gzip
import io
import time
import urllib.parse

import pandas as pd
import requests

DATA = Path('data')
DATA.mkdir(exist_ok=True)

# confirmed planets from NASA Exoplanet Archive (one row per planet)
cols = ("pl_name,hostname,gaia_dr3_id,discoverymethod,disc_year,disc_facility,"
        "pl_orbper,pl_rade,pl_bmasse,pl_eqt,sy_pnum,sy_dist,st_teff") # same as in schema.sql

query = f'select {cols} from pscomppars'  # ? what is pscomppars - planetary systems composite paramters table.
url = ('https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query='
       + urllib.parse.quote(query) + '&format=csv')

planets = pd.read_csv(url)
planets.to_csv(DATA / 'planets.csv', index=False)
print(f'Planets: {len(planets)} rows')

# nearby stars: the Gaia Catalogue of Nearby Stars (GCNS, within 100 pc)
#    joined to Gaia DR3 for up-to-date astrometry and photometry

stars_file = DATA / "stars.csv"
if stars_file.exists():
    print("stars.csv already exists, skipping the Gaia download")
else:
    adql = """
    SELECT source_id, ra, dec, parallax,
           parallax / parallax_error AS parallax_over_error,
           pmra, pmdec, phot_g_mean_mag,
           phot_bp_mean_mag - phot_rp_mean_mag AS bp_rp
    FROM gcns.main
    """
    url = ("https://dc.zah.uni-heidelberg.de/tap/sync"
           "?REQUEST=doQuery&LANG=ADQL&FORMAT=csv&MAXREC=400000&QUERY="
           + urllib.parse.quote(adql))
    stars = pd.read_csv(url)
    stars.columns = stars.columns.str.lower()
    print(f"Duplicate source_ids: {stars['source_id'].duplicated().sum()}")
    stars.to_csv(stars_file, index=False)
    print(f"Stars: {len(stars)} rows")