import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv(override=True)  # reads .env file and loads each line such as urls. 
engine = create_engine(os.environ['DATABASE_URL'])

# recreate the tables (one statement at a time)
schema_sql = Path("sql/schema.sql").read_text() 
with engine.begin() as conn:         # opens a connection called conn and starts a transaction
    for statement in schema_sql.split(";"):  # transaction rolls back block is something fails
        if statement.strip():
            conn.execute(text(statement))
# stars: in right shape already
stars= pd.read_csv('data/stars.csv')
stars.to_sql('stars', engine, if_exists='append', index=False,
             chunksize=2_000, method='multi')

# planets: turn 'Gaia DR3 123456...' into the number 123456...
planets = pd.read_csv("data/planets.csv")
planets["gaia_source_id"] = (planets["gaia_dr3_id"]
                             .str.extract(r"(\d+)$", expand=False)
                             .astype("Int64"))
planets = planets.drop(columns="gaia_dr3_id")
# Insert planets directly with SQLAlchemy (missing values become NULL)
from sqlalchemy import MetaData, Table, insert

planets_table = Table("planets", MetaData(), autoload_with=engine)
records = (planets.astype(object)
                  .where(planets.notna(), None)
                  .to_dict("records"))

with engine.begin() as conn:
    conn.execute(insert(planets_table), records)

print(f"Loaded {len(stars)} stars and {len(planets)} planets")