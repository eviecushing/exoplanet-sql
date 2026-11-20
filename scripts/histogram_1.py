# plots histogram data from /queries/03_radius_valley.sql

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import numpy as np

df = pd.read_csv('data/selection_bias.csv')

main_methods = ["Transit", "Radial Velocity", "Microlensing", "Imaging"]
df = df[df["discoverymethod"].isin(main_methods)].set_index("discoverymethod")
df = df.loc[main_methods]   # fixed order on the x-axis
# Convert counts to percentages of each method's total
totals = df.sum(axis=1)
pct = df.div(totals, axis=0) * 100

# Readable column names for the legend
pct = pct.rename(columns={
    "earth_size": "Earth-size (< 1.25 R⊕)",
    "super_earth": "Super-Earth (1.25–2 R⊕)",
    "neptune_size": "Neptune-size (2–6 R⊕)",
    "giant": "Giant (> 6 R⊕)",
    "unknown": "No radius",
})

# One 100% stacked bar per method
pct.plot(kind="bar", stacked=True, figsize=(9, 6), width=0.7)

# Total number of planets above each bar
for i, n in enumerate(totals):
    plt.text(i, 101, f"n = {n}", ha="center", fontsize=10)

plt.ylim(0, 108)
plt.ylabel("Share of the method's planets (%)")
plt.xlabel("Detection method")
plt.xticks(rotation=0)
plt.title("Transits find mostly small planets; other methods mostly giants")
plt.legend(title="Planet size", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.figtext(0.01, 0.01,
            "Note: only transits measure radius directly; most radii for other "
            "methods are estimated by the archive from planet mass.",
            fontsize=8, style="italic")

plt.tight_layout(rect=(0, 0.04, 1, 1))
plt.savefig("charts/size_classes_by_method.png", dpi=150, bbox_inches="tight")
plt.show()
















Path("charts").mkdir(exist_ok=True)

df = pd.read_csv('data/valley.csv').sort_values("bin_lower_edge")
lower = df["bin_lower_edge"].to_numpy()
counts = df["n_planets"].to_numpy()

edges = np.append(lower, lower[-1] * lower[-1] / lower[-2])

plt.figure(figsize=(8, 5))
plt.stairs(counts, edges, color='maroon', fill=True, alpha=0.6, label="Confirmed planets")
plt.axvspan(1.5, 2.0, color="grey", alpha=0.2, label="Expected radius valley (1.5–2 R⊕)")

plt.xscale("log")
plt.xticks([1, 1.5, 2, 3, 4], ["1", "1.5", "2", "3", "4"])
plt.minorticks_off()
plt.xlabel("Planet radius (Earth radii)")
plt.ylabel("Number of planets per bin")
plt.title("Fewer planets between 1.5 and 2 Earth radii: the radius valley")
plt.legend()

plt.tight_layout()
plt.savefig("charts/radius_valley.png", dpi=150)
plt.show()
