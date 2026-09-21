import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python security/gitleaks_to_findings.py "
            "<gitleaks-report.json> <findings.json>"
        )
        sys.exit(2)

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])

    if not source.exists():
        print(f"ERROR: Gitleaks report not found: {source}")
        sys.exit(2)

    with source.open("r", encoding="utf-8") as file:
        gitleaks_findings = json.load(file)

    if not isinstance(gitleaks_findings, list):
        print("ERROR: Expected Gitleaks JSON report to contain an array.")
        sys.exit(2)

    findings = []

    for finding in gitleaks_findings:
        findings.append(
            {
                "id": finding.get("RuleID", "GITLEAKS-UNKNOWN"),
                "type": "secret",
                "severity": "HIGH",
                "exploitable": True,
                "source": "gitleaks",
                "file": finding.get("File"),
                "line": finding.get("StartLine"),
                "description": finding.get("Description"),
            }
        )

    with destination.open("w", encoding="utf-8") as file:
        json.dump(findings, file, indent=2)

    print(f"Normalized {len(findings)} Gitleaks finding(s).")


if __name__ == "__main__":
    main()