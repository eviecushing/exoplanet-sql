from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

Path("charts").mkdir(exist_ok=True)

# Load planets that have both a period and a radius
df = pd.read_csv("data/planets.csv")
df = df.dropna(subset=["pl_orbper", "pl_rade"])

# Group the methods: Transit, Radial Velocity, and everything else
df["method_group"] = df["discoverymethod"].where(
    df["discoverymethod"].isin(["Transit", "Radial Velocity"]), "Other")

plt.figure(figsize=(10, 7))

# Draw the groups in this order: Other first, Transit last
groups = [
    ("Other",           "#e011f3", "Other methods (radius mostly estimated)"),
    ("Radial Velocity", "#e07b39", "Radial velocity (radius estimated from mass)"),
    ("Transit",         "#0f12d3", "Transit (radius measured)"),
]
for group, colour, label in groups:
    subset = df[df["method_group"] == group]
    plt.scatter(subset["pl_orbper"], subset["pl_rade"],
                s=8, alpha=0.6, color=colour, edgecolors="none",
                label=f"{label}, n = {len(subset):,}")

# Reference lines for Earth, Neptune and Jupiter radii
for radius, name in [(1, "Earth"), (3.9, "Neptune"), (11.2, "Jupiter")]:
    plt.axhline(radius, color="black", linestyle=":", linewidth=0.8, alpha=0.6)
    plt.text(1.2e5, radius * 1.05, name, fontsize=9, alpha=0.7)

plt.xscale("log")
plt.yscale("log")
plt.xlim(0.1, 1e6)
plt.xlabel("Orbital period (days)")
plt.ylabel("Planet radius (Earth radii)")
plt.title("Transit planets cluster at short periods; most other radii are model estimates")
plt.legend(loc="lower right", markerscale=2, fontsize=9)
plt.grid(alpha=0.2, which="both")

plt.figtext(0.01, 0.01,
            "Source: NASA Exoplanet Archive (pscomppars). A few imaging planets "
            "with periods above 10^6 days are outside the plotted range.",
            fontsize=8, style="italic")

plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.savefig("charts/period_radius.png", dpi=150, bbox_inches="tight")
plt.show()