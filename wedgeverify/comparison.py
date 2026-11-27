"""Compare independently measured SU2 data to theory, without inventing runs."""
import argparse
import csv
from pathlib import Path
from .shock import solve_weak_shock

MEASURES = {"shock_angle_deg": "Shock angle (deg)",
            "p2_p1": "Pressure ratio", "rho2_rho1": "Density ratio",
            "mach_2": "Downstream Mach"}


def compare_rows(rows, mach=2.0, theta=10.0, gamma=1.4):
    truth = solve_weak_shock(mach, theta, gamma)
    out = []
    seen = set()
    for row in rows:
        level = row["mesh"].strip()
        if level in seen:
            raise ValueError(f"Repeated mesh name {level}")
        seen.add(level)
        record = {"mesh": level, "cells": int(row["cells"]), "h_m": float(row["h_m"])}
        if record["cells"] <= 0 or record["h_m"] <= 0:
            raise ValueError("cells and h_m must be positive")
        for q in MEASURES:
            raw = row.get(q, "").strip()
            if not raw:
                record[q] = "NOT_EXECUTED"
                record[f"{q}_abs_error"] = "NOT_EXECUTED"
                record[f"{q}_rel_error_pct"] = "NOT_EXECUTED"
            else:
                val = float(raw)
                if not (-1e6 < val < 1e6):
                    raise ValueError("Nonfinite or impossible input")
                exact = getattr(truth, q)
                record[q] = val
                record[f"{q}_abs_error"] = abs(val - exact)
                record[f"{q}_rel_error_pct"] = abs(val-exact)/abs(exact)*100
        out.append(record)
    return out


def main():
    parser = argparse.ArgumentParser(description="Compare user-measured CFD to theory")
    parser.add_argument("--input", required=True, help="CSV measurements; blank fields are NOT_EXECUTED")
    parser.add_argument("--output", default="results/mesh_errors.csv")
    args = parser.parse_args()
    with open(args.input, newline="", encoding="utf-8") as f:
        compared = compare_rows(csv.DictReader(f))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(compared[0]))
        writer.writeheader()
        writer.writerows(compared)
    print(f"Wrote {output}: {len(compared)} rows")

if __name__ == "__main__":
    main()
