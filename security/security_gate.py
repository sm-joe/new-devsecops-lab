import json
import sys
from pathlib import Path

import yaml


CONFIG_FILE = Path("security/security-gate.yml")


def load_config():
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def is_exploitable(finding):
    return finding.get("exploitable", False) is True


def evaluate_finding(finding, config):
    finding_type = finding.get("type", "")
    severity = finding.get("severity", "").upper()

    if finding_type == "secret":
        return {
            "decision": "BLOCK",
            "reason": "Secret detected"
        }

    if (
        finding_type == "vulnerability"
        and severity == "CRITICAL"
        and is_exploitable(finding)
    ):
        return {
            "decision": "BLOCK",
            "reason": "Critical exploitable vulnerability"
        }

    if finding_type == "data_exposure":
        return {
            "decision": "BLOCK",
            "reason": "Direct data exposure"
        }

    sla_days = config["remediation_sla_days"].get(severity)

    return {
        "decision": "SOFT_FAIL",
        "reason": f"{severity} finding requires remediation",
        "remediation_sla_days": sla_days
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python security/security_gate.py <findings.json>")
        sys.exit(2)

    findings_file = Path(sys.argv[1])

    with findings_file.open("r", encoding="utf-8") as file:
        findings = json.load(file)

    config = load_config()

    blocked = []
    soft_failures = []

    for finding in findings:
        result = evaluate_finding(finding, config)

        record = {
            **finding,
            **result
        }

        if result["decision"] == "BLOCK":
            blocked.append(record)
        else:
            soft_failures.append(record)

    print("Security Gate Results")
    print("=====================")

    if blocked:
        print(f"BLOCK: {len(blocked)} finding(s)")

        for finding in blocked:
            print(
                f"- [{finding.get('severity', 'N/A')}] "
                f"{finding.get('id', 'unknown')}: "
                f"{finding['reason']}"
            )

    if soft_failures:
        print(f"SOFT FAIL: {len(soft_failures)} finding(s)")

        for finding in soft_failures:
            print(
                f"- [{finding.get('severity', 'N/A')}] "
                f"{finding.get('id', 'unknown')}: "
                f"{finding['reason']} "
                f"(SLA: {finding.get('remediation_sla_days')} days)"
            )

    if not blocked:
        print("No hard-block conditions detected.")

    sys.exit(1 if blocked else 0)


if __name__ == "__main__":
    main()