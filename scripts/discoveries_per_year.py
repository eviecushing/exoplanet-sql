import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("data/discoveries_per_year.csv")

# one row per year, one column per method, counts in the cells
wide = df.pivot(index="disc_year", columns="discoverymethod",
                values="n_planets").fillna(0)

# Keep the four largest methods and add the rest together as "Other"
main_methods = ["Transit", "Radial Velocity", "Microlensing", "Imaging"]
other_methods = [m for m in wide.columns if m not in main_methods]
wide["Other"] = wide[other_methods].sum(axis=1)
wide = wide[main_methods + ["Other"]]

# One stacked bar per year
wide.plot(kind="bar", stacked=True, figsize=(12, 6), width=0.8)

plt.xlabel("Discovery year")
plt.ylabel("Number of planets discovered")
plt.title("Transits have dominated exoplanet discovery since the Kepler mission")
plt.legend(title="Detection method")

# Label every fifth year so the axis stays readable
years = wide.index.tolist()
plt.xticks(range(0, len(years), 5), years[::5], rotation=0)

plt.tight_layout()
plt.savefig("charts/discoveries_per_year.png", dpi=150, bbox_inches="tight")
plt.show()