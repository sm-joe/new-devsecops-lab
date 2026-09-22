# Security Decision: Remote Code Execution Risk

## Scenario

A dependency used by an internet-facing application is affected by a vulnerability that can result in remote code execution.

The vulnerability is classified as critical and has confirmed exploitability.

## Security Assessment

The risk is elevated because:

- The affected component is reachable by external users.
- Successful exploitation could allow arbitrary code execution.
- The vulnerability affects application runtime behavior.
- Exploitation could result in application or infrastructure compromise.

## Release Decision

A confirmed, exploitable critical RCE is treated as a release-blocking security finding.

The release should not proceed until the vulnerable dependency is:

- upgraded to a fixed version,
- replaced with a non-vulnerable implementation, or
- otherwise mitigated with a documented compensating control that reduces the exploitation path.

## Risk Trade-Off

Security enforcement must consider engineering and business impact, but an exception should not be used merely to avoid remediation work.

Where immediate remediation is technically unavailable, the exception process must document:

- exploitability
- exposure
- affected assets
- compensating controls
- accountable owner
- remediation plan
- expiration date

The maximum exception duration is 180 days.

## Example Compensating Controls

Depending on the architecture, temporary controls may include:

- removing or disabling the vulnerable functionality
- restricting network exposure
- applying an upstream mitigation
- adding targeted WAF protections
- isolating the affected workload
- increasing monitoring and detection

Compensating controls do not eliminate the underlying vulnerability and do not remove the requirement for permanent remediation.

## Decision Principle

The security decision is based on exploitability and exposure in addition to severity alone.

A critical vulnerability with a credible RCE path against an internet-facing component receives release-blocking treatment because the potential impact and attack surface materially increase the risk.