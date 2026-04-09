# TRO Packages
<span class="draft-badge">
  TROV 0.1 DRAFT</span>

*This document is a draft and subject to revision.
Please [submit feedback or report issues](https://github.com/transparency-certified/trace-specification/issues/new?title=tro-packages.md:%20).*

How Transparent Research Objects are packaged for distribution. TRACE and TROV are generally agnostic to the packaging format. The TRO declaration is the authoritative record, and any container that preserves the declaration, its signature, and optionally the research artifacts is a valid package. This document describes the ZIP-based packaging approach used by current implementations.

| Document Section | Description |
|---------|-------------|
| [Overview](#tro-packages-overview) | What a TRO package contains |
| [Package Contents](#package-contents) | Declaration, signing artifacts, and optional research artifacts for each signing mechanism |
| [Directory Layout](#directory-layout) | How files are organized inside ZIP archives |
| [On-Demand Signing](#on-demand-signing) | Creating signed packages after execution |
| [Verification](#tro-packages-verification) | Package-level checks beyond declaration validation |
| [Open Questions](#open-questions) | Design decisions not yet resolved for 0.1 |

For the structure of the JSON-LD declaration itself, see [TRO Declaration Format](tro-declaration-format.md). For the vocabulary terms, see [TROV Vocabulary Reference](trov-vocabulary.md).

---

(tro-packages-overview)=
## Overview

A TRO package is a collection of files containing:

1. A **TRO declaration** — the JSON-LD file describing the artifacts, arrangements, performances, and warrant chain.
2. One or more **signing artifacts** — files that allow a verifier to confirm the declaration's integrity and the identity of the assembling TRS.
3. Optionally, the **research artifacts** themselves (data files, code, outputs).

**Note:**  The word *package* typically suggests a single bundled archive containing a set of artifacts and descriptive metadata. TRO packages can be exactly that — which is why the ZIP-based formats are documented below — but they don't have to be. In TRACE, the declaration serves as a catalog of the artifacts and the conditions under which they were produced. The signature establishes that these records have not been altered. Everything else — how the artifacts are stored, whether they are bundled together, what archive format is used — is not constrained.

The following aspects of TRO packaging illustrate the flexibility this provides.

| Aspect | Explanation | Example |
|--------|-------------|---------|
| Artifacts are optional in the package | The declaration and its signature are the only required elements of a valid TRO package. The content hashes in the declaration allow artifacts to be verified wherever they are hosted. | A TRO describing a computation on restricted census data. The data and results cannot be distributed, but the declaration records what was computed and under what transparency constraints. Anyone who later gains authorized access to the data can verify it against the hashes in the declaration. |
| The package format itself is not prescribed | ZIP is used by current implementations, but any container that preserves the declaration and signature is acceptable. | An institutional repository that stores deposits as tarballs, or a data repository like Dataverse where the declaration and artifacts are individual file downloads rather than entries in an archive. |
| Existing package formats can become TROs | Adding a TRO declaration and signature to an existing Research Object package can make it TRACE-compliant without breaking its original format. | An institution that produces RO-Crate or BagIt packages can add the declaration and signing artifacts to make them TROs while retaining full validity as RO-Crates or BagIt bags. |
| No literal packaging is required | The declaration, signing files, and artifacts do not need to be bundled into an archive at all. They can be individual files served from the same location. | A TRS publishes the declaration, its signature, and the research artifacts as files in a directory on a web server. A verifier downloads and checks them individually. |
| The signing mechanism is not prescribed | TROV does not require a particular signing technology. GPG and X.509/CMS are both in use; other mechanisms are equally valid. | A central bank uses X.509 certificates from its existing PKI infrastructure. An academic research group uses GPG keys managed by its computing center. Both produce valid TRO packages. |
| Signing can happen after execution | A TRS may produce an unsigned package during execution and sign the declaration later on demand. | A TRS runs dozens of computations per week. Researchers select which results to publish, and only those declarations are signed, thereby avoiding the cost of signing infrastructure for exploratory runs. |

In short, the declaration is the authoritative record. The signing artifacts prove it hasn't been tampered with. The research artifacts may be included in the package or hosted elsewhere; the declaration's content hashes allow each artifact to be positively verified against its declared identity regardless of where it resides.

Critically, in TRACE an artifact's identity is its content hash, not its filename or path. Two files with different names but identical content are the same artifact. The same artifact can appear at different paths in different arrangements. This is why the package layout can be unconstrained.

---

(package-contents)=
## Package Contents

Every TRO package contains at minimum a declaration file and a signature. The specific signing artifacts depend on the mechanism used. TROV is agnostic to the signing mechanism; the two current implementations demonstrate different but equally valid approaches.

### GPG signing

| File | Description |
|------|-------------|
| `{name}.jsonld` | The TRO declaration |
| `{name}.sig` | GPG detached signature over the declaration |
| `{name}.tsr` | RFC 3161 timestamp response from an external TSA |

The GPG public key of the TRS is included in the declaration itself as `trov:publicKey`. Verification uses the public key from the declaration and the TSA's certificate.

### X.509/CMS signing

| File | Description |
|------|-------------|
| `{name}.jsonld` | The TRO declaration |
| `{name}.p7s` | CMS/PKCS #7 detached signature (DER-encoded) |

The `.p7s` file contains the signature, the X.509 certificate chain, and the timestamp countersignature in a single file. No separate `.tsr` is needed. Verification extracts the certificate and timestamp directly from the `.p7s`.

### Research artifacts

The package may include the research artifacts referenced by the declaration, organized in a directory alongside the declaration and signing files. Their content hashes in the declaration allow verification whether they are packaged or hosted externally.

---

(directory-layout)=
## Directory Layout

TRACE places no requirements on the directory structure within a package. A flat archive with all files at the root is valid. So is any nested structure. The declaration identifies artifacts by content hash, not by path.

The following examples illustrate two possible layouts inside a ZIP archive.

**GPG signing with separate artifact directory:**

```
archive.zip
├── tro/
│   ├── {name}.jsonld           declaration
│   ├── {name}.sig              GPG detached signature
│   └── {name}.tsr              RFC 3161 timestamp response
└── project/
    └── ...                     research artifacts (optional)
```

**X.509/CMS signing with flat layout:**

```
archive.zip
├── {name}.jsonld               declaration
├── {name}.p7s                  CMS signature with embedded timestamp
└── ...                         research artifacts (optional)
```

In both cases, the declaration's `trov:path` entries identify the location of each artifact included in the package. A verifier uses the content hashes in the declaration — not the directory structure or the file names — to confirm artifact integrity.

Repositories like Zenodo and Dataverse can display the file listing of a ZIP archive directly. Using a recognizable structure (e.g., a `tro/` directory for the declaration and signing files) may make the package easier to browse, but this is a usability choice.

---

(on-demand-signing)=
## On-Demand Signing

A TRS may produce unsigned packages during execution and sign them later on demand. This is valid as long as the declaration file is not modified between creation and signing.

1. The TRS executes the computation and produces a package with the declaration and artifacts.
2. At a later time, a researcher requests a signed version.
3. The TRS signs the original declaration, producing the signature artifacts.
4. The signed package is assembled with the declaration, signature, and artifacts.

The timestamp in the signature reflects when the signing occurred, not when the computation ran. Execution times are separately recorded in the declaration (`trov:startedAtTime`, `trov:endedAtTime`).

This allows TRS implementations to decouple signing from execution, which is useful when the signing infrastructure is external or intermittently available. For example, a TRS operating in an isolated environment without network access during execution can defer both signing and timestamping to a later stage when a timestamp authority is reachable.

The critical constraint is chain of custody: the TRS must sign the declaration it originally produced, not a copy provided by the researcher. The signature attests that the TRS stands behind the integrity of the package.

---

(tro-packages-verification)=
## Verification

The [TRO Declaration Format](tro-declaration-format.md#tro-format-verification) describes verification of the declaration's internal consistency (fingerprint, arrangement references, warrant chain). At the package level, a verifier additionally checks:

1. **Signature validity.** The signature on the declaration file matches the public key or certificate associated with the TRS. The key or certificate must be cryptographically bound to the signature — either by inclusion in the signed declaration itself (GPG: `trov:publicKey`) or by a certificate chain embedded in the signature file (X.509/CMS: `.p7s`). A public key provided separately from the signed content does not establish that the claimed TRS produced the signature.
2. **Timestamp validity.** The signed timestamp establishes that the declaration's signature was produced no later than the indicated time. For GPG, this is the `.tsr` file verified against the TSA's certificate. For X.509/CMS, the timestamp countersignature is embedded in the `.p7s`.
3. **Artifact integrity.** If research artifacts are included in the package, verify their content hashes match the values in the declaration.

The signature covers the declaration file byte-for-byte. The declaration must not be modified, reformatted, or re-serialized between signing and verification.

### Signing identity and trust

The two signing mechanisms currently in use bind the signer's identity to the signature in different ways, with different trust tradeoffs.

**GPG with `trov:publicKey`:** The TRS's public key is included in the declaration, which is the signed content. This creates a self-binding: a different signer cannot substitute their own key without modifying the declaration, which would invalidate the signature. The binding is strong — key and content are cryptographically inseparable. However, no third party vouches for who owns the key. The verifier must establish trust in the key through an independent channel (e.g., a key server, the TRS's published documentation, or out-of-band exchange).

**X.509/CMS:** The signer's certificate (containing their public key, organization name, and a chain to a trusted CA) is embedded in the `.p7s` file alongside the signature — not in the signed declaration itself. The CA vouches for the signer's identity, providing third-party trust. However, since the certificate is outside the signed content, a verifier must check that the certificate's identity matches the TRS named in the declaration. A valid signature from a valid certificate chain does not by itself prove the expected TRS signed the declaration, only that *some* entity with a CA-issued certificate did.

In both cases, a verifier must consult a trustworthy source beyond the TRO package itself to confirm that the key used to sign the declaration belongs to the TRS identified in the declaration. For GPG, this might be a key server or published key fingerprint. For X.509, the certificate authority serves this role. The mechanisms differ in where they place the key material and how identity is established, but neither is self-sufficient. The package alone cannot prove who signed it.

---

(open-questions)=
## Open Questions

The following design decisions are not yet resolved for 0.1:

| Question | Context |
|----------|---------|
| How does a verifier determine the signing mechanism? | (1) Require the mechanism to be decided at declaration time and include `trov:signingMechanism` as a mandatory property. (2) Make `trov:signingMechanism` optional, allowing validation rules when present (e.g. flagging a GPG-signed declaration that lacks `trov:publicKey`) and requiring the mechanism to be inferred from package contents when absent. (3) Omit the property entirely and always infer from the signing artifacts. |
| Should the declaration name the signing artifact files? | The declaration already names the TRS, the artifacts, and the warrant chain. Referencing the signature and timestamp files (e.g. `"trov:signatureFile": "tro.p7s"`) would make the declaration self-describing for verification — a verifier would know exactly what files to look for without inspecting the package. This would require committing to the signing mechanism and file names at declaration time, even for deferred signing. If adopted, `trov:signingMechanism` would effectively become mandatory. The two questions are coupled but separable: the mechanism could be declared without naming files, and files could be named without a formal mechanism property (the file names imply the mechanism). |
