"""Export seven transparent charts for dark slides: python scripts/plot_figures.py."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MaxNLocator


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "figures/presentation"
GREEN = "#75CB6D"
TEXT = "#F2F8F1"
MUTED = "#B8CCB8"


def configure(background="none"):
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 12,
        "axes.titlesize": 21,
        "axes.titleweight": "bold",
        "axes.titlepad": 18,
        "axes.labelpad": 12,
        "text.color": TEXT,
        "axes.labelcolor": MUTED,
        "axes.edgecolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.bottom": False,
        "figure.facecolor": background,
        "axes.facecolor": background,
        "savefig.facecolor": background,
        "savefig.transparent": background == "none",
        "savefig.dpi": 220,
    })


def style_axis(ax):
    ax.grid(axis="y", color=MUTED, alpha=0.15, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, pad=9)


def save(ax, name, title, xlabel, ylabel):
    ax.set_title(title, loc="left")
    ax.set(xlabel=xlabel, ylabel=ylabel)
    style_axis(ax)
    ax.figure.savefig(OUTPUT / f"{name}.png", bbox_inches="tight", pad_inches=0.25)
    plt.close(ax.figure)


def annual_chart(table, column, name, title, ylabel, *, integer=False):
    fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")
    ax.plot(
        table["year"], table[column],
        color=GREEN, linewidth=2.8,
        marker="o", markersize=7, markeredgewidth=0,
    )
    ax.set_xticks(table["year"])
    ax.margins(x=0.04, y=0.18)
    if integer:
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        note = "Recorded survey coverage in the supplied dataset"
    else:
        note = "Equal weight per contributing route; confidence intervals pending"
    fig.text(0.01, -0.025, note, color=MUTED, fontsize=10)
    save(ax, name, title, "Year", ylabel)


def main():
    configure()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    annual = pd.read_csv(ROOT / "results/annual_indicators.csv")
    effort = pd.read_csv(ROOT / "results/annual_sampling_effort.csv")
    points = pd.read_csv(ROOT / "data/processed/point_surveys.csv")

    indicators = [
        ("richness", "01_richness", "Species richness", "Species per point survey"),
        ("recorded_abundance", "02_abundance", "Recorded abundance", "Detections per point survey"),
        ("shannon", "03_shannon", "Shannon diversity", "Shannon index (nats)"),
    ]
    for column, name, title, ylabel in indicators:
        annual_chart(annual, column, name, title, ylabel)

    for column, name, title in [
        ("point_surveys", "04_surveys", "Recorded point surveys"),
        ("routes", "05_routes", "Surveyed routes"),
    ]:
        annual_chart(effort, column, name, title, "Count", integer=True)

    for column, name, title, xlabel in [
        ("richness", "06_richness_distribution", "Species richness distribution", "Species per point survey"),
        ("recorded_abundance", "07_abundance_distribution", "Recorded abundance distribution", "Detections per point survey"),
    ]:
        values = points[column].dropna()
        bins = 35
        if column == "richness":
            bins = [n - 0.5 for n in range(int(values.max()) + 2)]
        _, ax = plt.subplots(figsize=(10, 5), layout="constrained")
        ax.hist(values, bins=bins, color=GREEN, alpha=0.95, rwidth=0.9)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        save(ax, name, title, xlabel, "Point surveys with valid values")

    print(f"Saved seven charts to {OUTPUT}")


if __name__ == "__main__":
    main()
