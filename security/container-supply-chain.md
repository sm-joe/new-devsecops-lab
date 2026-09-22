# Container Supply Chain Security

## 1. Purpose

Define the container build, scanning, SBOM, signing, attestation, and verification process used by the DevSecOps lab.

## 2. Build

Container images are built through GitHub Actions using Docker Buildx.

Pull requests build and scan the image but do not publish it.

Images are published only from the `main` branch.

## 3. Vulnerability Scanning

Trivy scans the built container image for CRITICAL and HIGH vulnerabilities.

A failing vulnerability scan prevents the image from progressing through the release workflow.

## 4. SBOM

Syft generates a CycloneDX SBOM for the container image.

The SBOM is retained as a GitHub Actions artifact for 30 days.

## 5. Image Signing

Images published to GHCR are signed using Cosign keyless signing.

Signing uses GitHub Actions OIDC rather than a stored private signing key.

## 6. Immutable Digest

After publication, the image digest is resolved from the registry.

Signing, signature verification, SBOM attestation, and attestation verification operate against the immutable image digest.

## 7. SBOM Attestation

The CycloneDX SBOM is attached to the image as a Cosign attestation.

The attestation is subsequently verified against the same immutable image digest.

## 8. Verification Chain

The release artifact must provide:

- Container image
- Immutable image digest
- Valid Cosign signature
- CycloneDX SBOM
- Valid SBOM attestation

## 9. Admission Control

Kubernetes admission enforcement is intentionally implemented in the separate Kubernetes security lab.

The future admission policy will require valid image signatures and the required SBOM attestation before workloads are admitted.

## 10. Keyless Signing Security Model

No long-lived Cosign private signing key is stored in GitHub repository secrets.

The signing identity is established through GitHub Actions OIDC and Sigstore.

## 11. Failure Conditions

Release progression must stop when:

- Container vulnerability scanning fails
- Image signing fails
- Signature verification fails
- SBOM generation fails
- SBOM attestation fails
- SBOM attestation verification fails

## 12. Verification Evidence

A successful release should provide evidence for:

1. Image scan
2. SBOM generation
3. Image digest
4. Cosign signature
5. Signature verification
6. SBOM attestation
7. Attestation verification
