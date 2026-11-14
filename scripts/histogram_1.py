# plots histogram data from /queries/03_radius_valley.sql

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import numpy as np

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
