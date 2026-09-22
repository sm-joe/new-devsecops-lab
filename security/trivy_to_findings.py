import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python security/trivy_to_findings.py "
            "<trivy-report.json> <findings.json>"
        )
        sys.exit(2)

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])

    if not source.exists():
        print(f"ERROR: Trivy report not found: {source}")
        sys.exit(2)

    with source.open("r", encoding="utf-8") as file:
        report = json.load(file)

    findings = []

    for result in report.get("Results", []):
        for vulnerability in result.get("Vulnerabilities") or []:
            severity = vulnerability.get("Severity", "UNKNOWN").upper()

            findings.append(
                {
                    "id": vulnerability.get(
                        "VulnerabilityID",
                        "TRIVY-UNKNOWN"
                    ),
                    "type": "vulnerability",
                    "severity": severity,
                    "exploitable": False,
                    "source": "trivy",
                    "package": vulnerability.get("PkgName"),
                    "installed_version": vulnerability.get(
                        "InstalledVersion"
                    ),
                    "fixed_version": vulnerability.get("FixedVersion"),
                    "title": vulnerability.get("Title"),
                }
            )

    with destination.open("w", encoding="utf-8") as file:
        json.dump(findings, file, indent=2)

    print(f"Normalized {len(findings)} Trivy finding(s).")


if __name__ == "__main__":
    main()
