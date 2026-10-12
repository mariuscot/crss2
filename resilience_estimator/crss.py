from dataclasses import replace
import math
from pathlib import Path

if __package__:
    from .resilience_calculation import resilienceExtimator as estimator
    from .resilience_calculation.saatyResilienceClassifier import SaatyResilienceClassifier
else:
    from resilience_calculation import resilienceExtimator as estimator
    from resilience_calculation.saatyResilienceClassifier import SaatyResilienceClassifier

def main():
    output_dir = Path(__file__).resolve().parents[1] / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "resilience_report.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    if report_path.exists():
        report_path.unlink()

    cve_scenarios = [
        ((7.5, "CVE-2014-0160"), "unprotected", 0),
        ((7.5, "CVE-2014-0160"), "protected", 1),
        ((8.8, "CVE-2017-0144"), "unprotected", 0),
        ((8.8, "CVE-2017-0144"), "protected", 1),
    ]
    classifier = SaatyResilienceClassifier()
    interval_lines = ["Resilience Classification Intervals:"]
    intervals = list(classifier.intervals.items())
    for index, (level, (lower, upper)) in enumerate(intervals):
        closing_bracket = "]" if index == len(intervals) - 1 else ")"
        interval_lines.append(f"  {level}: [{lower:.3f}, {upper:.3f}{closing_bracket}")
    interval_lines.append("")
    interval_lines.append(f"CR={classifier.consistency_ratio}")
    interval_lines.append("")
    report_path.write_text("\n".join(interval_lines), encoding="utf-8")

    for cve, protection_name, protection in cve_scenarios:
        (
            res_nodes,
            civilian_resilience,
            civ_layer_resilience,
            military_resilience,
            mil_layer_resilience,
        ) = estimator.resilienceCalculatorForCVE(
            cve, R0=1.0, mop=0, protection=protection, MT=0.1, MO=0.2
        )
        civ_layer_levels = {
            layer: classifier.classify(value)
            for layer, value in civ_layer_resilience.items()
        }
        mil_layer_levels = {
            layer: classifier.classify(value)
            for layer, value in mil_layer_resilience.items()
        }
        estimator.write_resilience_report(
            report_path,
            cve[1],
            protection_name,
            civilian_resilience,
            civ_layer_resilience,
            military_resilience,
            mil_layer_resilience,
            civ_layer_levels=civ_layer_levels,
            mil_layer_levels=mil_layer_levels,
        )

    print(f"Resilience report saved to {report_path}")
    


if __name__ == "__main__":
    main()
