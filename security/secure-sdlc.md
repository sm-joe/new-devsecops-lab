# Secure Software Development Lifecycle

## 1. Purpose

Define the security controls applied throughout the software development lifecycle.

## 2. Developer Workflow

Developers receive security feedback before code reaches the main branch.

The developer-side controls include:

- Pre-commit Gitleaks secret scanning
- Local application tests
- Local security-tool execution where required

Secrets detected by Gitleaks prevent the commit from proceeding.

## 3. Pull Request Security

Pull requests run the fast security controls:

- Semgrep SAST
- Trivy SCA
- OSV-Scanner
- Trivy IaC scanning
- Checkov
- Container vulnerability scanning
- Container SBOM generation
- Gitleaks

These controls provide early security feedback before changes are merged.

## 4. Secondary Analysis

SonarQube provides additional code-quality and security analysis.

It operates separately from the fast blocking security checks.

## 5. Container Supply Chain

Container releases follow the container security process defined in:

`security/container-supply-chain.md`

The process includes:

- Vulnerability scanning
- SBOM generation
- Image publication
- Immutable digest resolution
- Keyless Cosign signing
- Signature verification
- SBOM attestation
- Attestation verification

## 6. Identity and Authentication

GitHub Actions uses OIDC federation where supported rather than long-lived static credentials.

Cosign keyless signing uses GitHub Actions OIDC with Sigstore.

## 7. Dependency Management

Dependabot monitors:

- npm dependencies
- Docker dependencies
- GitHub Actions

Dependency updates are reviewed through normal pull-request workflows.

## 8. Vulnerability Management

Security findings follow the vulnerability-management policy defined in:

`security/vulnerability-management.md`

Remediation targets are:

| Severity | SLA |
|----------|-----|
| Critical | 14 days |
| High | 30 days |
| Medium | 60 days |

Security exceptions must have an owner, justification, compensating controls, and an expiry date.

An exception may not exceed 180 days.

## 9. Security Governance

CODEOWNERS protects security-sensitive configuration and security-policy changes.

Security controls are maintained as code and executed through the CI/CD platform wherever practical.

## 10. Security Feedback Model

The overall model is:

Developer
→ Pre-commit security
→ Pull request security
→ Code review
→ Merge
→ Main-branch build
→ Container security
→ Signed and attested artifact

## 11. Design Principle

Security controls should provide early feedback while minimizing unnecessary engineering friction.

Controls should be automated where practical, measurable, and continuously improved based on observed findings and recurring failure patterns.