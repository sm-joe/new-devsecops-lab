import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python security/osv_to_findings.py "
            "<osv-report.json> <findings.json>"
        )
        sys.exit(2)

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])

    if not source.exists():
        print(f"ERROR: OSV report not found: {source}")
        sys.exit(2)

    with source.open("r", encoding="utf-8") as file:
        report = json.load(file)

    findings = []

    for result in report.get("results", []):
        package = result.get("package", {})

        for vulnerability in result.get("vulnerabilities", []):
            severity = "UNKNOWN"

            database_specific = vulnerability.get(
                "database_specific",
                {}
            )

            if database_specific.get("severity"):
                severity = database_specific["severity"].upper()

            findings.append(
                {
                    "id": vulnerability.get(
                        "id",
                        "OSV-UNKNOWN"
                    ),
                    "type": "vulnerability",
                    "severity": severity,
                    "exploitable": False,
                    "source": "osv-scanner",
                    "package": package.get("name"),
                    "version": package.get("version"),
                    "summary": vulnerability.get("summary"),
                }
            )

    with destination.open("w", encoding="utf-8") as file:
        json.dump(findings, file, indent=2)

    print(f"Normalized {len(findings)} OSV finding(s).")


if __name__ == "__main__":
    main()
