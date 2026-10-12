import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

if __package__:
    from .resilience_calculation import resilienceExtimator as estimator
else:
    from resilience_calculation import resilienceExtimator as estimator

from mygraphs import CVE_2014_0160_radar_entry_one_way as cve_graphs


def main():
    output_dir = Path(__file__).resolve().parents[1] / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    graph_output_dir = output_dir / "crss2_graphs"
    graph_output_dir.mkdir(parents=True, exist_ok=True)
    cve_graphs.OUTPUT_DIR = graph_output_dir
    cve = (7.5, "CVE-2014-0160")
    parameter_values = [step / 10 for step in range(1, 11)]
    military_resilience = np.empty((len(parameter_values), len(parameter_values)))
    (
        res_nodes,
        civilian_resilience,
        civ_layer_resilience,
        _,
        _,
    ) = estimator.resilienceCalculatorForCVE(
        cve,
        R0=1.0,
        mop=0,
        protection=0,
        MT=parameter_values[0],
        MO=parameter_values[0],
    )

    for mt_index, mt in enumerate(parameter_values):
        for mo_index, mo in enumerate(parameter_values):
            print(f"Evaluating military resilience for MT={mt}, MO={mo}...")
            (
                military_resilience[mt_index, mo_index],
                _,
                _,
            ) = estimator.calcMilitaryResilience(
                res_nodes,
                civilian_resilience,
                civ_layer_resilience,
                MT=mt,
                MO=mo,
            )

    mo_grid, mt_grid = np.meshgrid(parameter_values, parameter_values)
    figure = plt.figure(figsize=(10, 7))
    axes = figure.add_subplot(111, projection="3d")
    surface = axes.plot_surface(
        mo_grid,
        mt_grid,
        military_resilience,
        cmap="viridis",
        edgecolor="black",
        linewidth=0.25,
        antialiased=True,
    )
    axes.set_title("Military System Resilience: CVE-2014-0160 (Unprotected)")
    axes.set_xlabel("MO")
    axes.set_ylabel("MT")
    axes.set_zlabel("Military System Resilience")
    axes.set_xticks(parameter_values)
    axes.set_yticks(parameter_values)
    figure.colorbar(surface, ax=axes, label="Military System Resilience", shrink=0.65)
    figure.tight_layout()

    graph_path = output_dir / "CVE-2014-0160_unprotected_military_resilience_surface.png"
    figure.savefig(graph_path, dpi=200, bbox_inches="tight")
    plt.close(figure)

    data_path = output_dir / "CVE-2014-0160_unprotected_military_resilience.csv"
    with data_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(("MO", "MT", "military_resilience"))
        for mt_index, mt in enumerate(parameter_values):
            for mo_index, mo in enumerate(parameter_values):
                writer.writerow((mo, mt, military_resilience[mt_index, mo_index]))

    print(f"Evaluated {military_resilience.size} MO/MT combinations.")
    print(f"3D graph saved to {graph_path}")
    print(f"Values saved to {data_path}")


if __name__ == "__main__":
    main()
