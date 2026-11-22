# TRO Packages
<span class="draft-badge">
  TROV 0.1 DRAFT</span>

*This document is a draft and subject to revision.
Please [submit feedback or report issues](https://github.com/transparency-certified/trace-specification/issues/new?title=tro-packages.md:%20).*

How Transparent Research Objects are packaged for distribution. TRACE and TROV are generally agnostic to the packaging format. The TRO declaration is the authoritative record, and any container that preserves the declaration, its signature, and optionally the research artifacts is a valid package. This document describes the ZIP-based packaging approach used by current implementations.

| Section | Description |
|---------|-------------|
| [Overview](#tro-packages-overview) | What a TRO package contains |
| [Signature Files](#signature-files) | The files that accompany the declaration for each signing mechanism |
| [Directory Layout](#directory-layout) | How files are organized inside ZIP archives |
| [On-Demand Signing](#on-demand-signing) | Creating signed packages after execution |
| [Verification](#tro-packages-verification) | Package-level checks beyond declaration validation |

For the structure of the JSON-LD declaration itself, see [TRO Declaration Format](tro-declaration-format.md). For the vocabulary terms, see [TROV Vocabulary Reference](trov-vocabulary.md).

---

(tro-packages-overview)=
## Overview

A TRO package is a collection of files containing:

1. A **TRO declaration** — the JSON-LD file describing the artifacts, arrangements, performances, and warrant chains.
2. One or more **signature files**, which identify the key with which the declaration was signed, enable verification that that key was in fact employed, and support confirmation that the key is one that the organization certifying the TRO uses to sign TRO declarations.
3. Optionally, the **research artifacts** themselves (data files, code, outputs).

**Note:**  The word *package* typically suggests a single bundled archive containing a set of artifacts and descriptive metadata. TRO packages can be exactly that — which is why the ZIP-based formats are documented below — but they don't have to be. In TRACE, the declaration serves as a catalog of the artifacts and the conditions under which they were produced. The signature establishes that these records have not been altered. Everything else — how the artifacts are stored, whether they are bundled together, what archive format is used — is not constrained.

The following aspects of TRO packaging illustrate the flexibility this provides.

| Aspect | Explanation | Example |
|--------|-------------|---------|
| Artifacts are optional in the package | The declaration and its signature are the only required elements of a valid TRO package. The content hashes in the declaration allow artifacts to be verified wherever they are hosted. | A TRO describing a computation on restricted census data. The data and results cannot be distributed, but the declaration records what was computed and under what transparency constraints. Anyone who later gains authorized access to the data can verify it against the hashes in the declaration. |
| The package format itself is not prescribed | ZIP is used by current implementations, but any container that preserves the declaration and signature is acceptable. | An institutional repository that stores deposits as tarballs, or a data repository like Dataverse where the declaration and artifacts are individual file downloads rather than entries in an archive. |
| Existing package formats can become TROs | Adding a TRO declaration and signature to an existing Research Object package can make it TRACE-compliant without breaking its original format. | An institution that produces RO-Crate or BagIt packages can add the declaration and signature files to make them TROs while retaining full validity as RO-Crates or BagIt bags. |
| No literal packaging is required | The declaration, signature files, and artifacts do not need to be bundled into an archive at all. They can be individual files served from the same location. | A TRS publishes the declaration, its signature, and the research artifacts as files in a directory on a web server. A verifier downloads and checks them individually. |
| Two signing mechanisms are currently supported | GPG and X.509/CMS are both in use, and a TRS may use either. Other mechanisms may be added in future versions. | A central bank uses X.509 certificates from its existing PKI infrastructure. An academic research group uses GPG keys managed by its computing center. Both produce valid TRO packages. |
| Signing can happen after execution | A TRS may produce an unsigned package during execution and sign the declaration later on demand. | A TRS runs dozens of computations per week. Researchers select which results to publish, and only those declarations are signed, thereby avoiding the cost of signing infrastructure for exploratory runs. |

In short, the declaration is the authoritative record. The signature files prove it hasn't been tampered with, and that it was signed by the identified TRS. The research artifacts may be included in the package or hosted elsewhere; the declaration's content hashes allow each artifact to be positively verified against its declared hash regardless of where it resides.

---

(signature-files)=
## Signature Files

Every TRO package contains at minimum a declaration file and a signature. The specific signature files depend on the mechanism used:

### GPG signing

| File | Description |
|------|-------------|
| `{name}.jsonld` | The TRO declaration |
| `{name}.sig` | GPG detached signature over the declaration |
| `{name}.tsr` | RFC 3161 timestamp response from an external TSA (optional) |

The declaration carries the public key used to sign it, as `trov:publicKey`. The signature is verified with that key. If a timestamp is present, it is verified with the public key of the TSA.

### X.509/CMS signing

| File | Description |
|------|-------------|
| `{name}.jsonld` | The TRO declaration |
| `{name}.p7s` | CMS/PKCS #7 detached signature (DER-encoded) |

The `.p7s` file contains the signature and the X.509 certificate chain, and can also carry a timestamp countersignature, so no separate `.tsr` is needed. The certificate, and the timestamp if present, are taken from the `.p7s` for verification.

---

(directory-layout)=
## Directory Layout

TRACE places no requirements on the directory structure within a package. A flat archive with all files at the root is valid. So is any nested structure. A package that includes artifacts places them at the paths recorded in one of the declaration's arrangements.

The following examples illustrate two possible layouts inside a ZIP archive.

**GPG signing with separate artifact directory:**

```
archive.zip
├── tro/
│   ├── {name}.jsonld           declaration
│   ├── {name}.sig              GPG detached signature
│   └── {name}.tsr              RFC 3161 timestamp response (optional)
└── project/
    └── ...                     research artifacts (optional)
```

**X.509/CMS signing with flat layout:**

```
archive.zip
├── {name}.jsonld               declaration
├── {name}.p7s                  CMS signature, with optional embedded timestamp
└── ...                         research artifacts (optional)
```

In both cases, a verifier finds each artifact's file at the path recorded for it in the arrangement describing the package's layout, and confirms the file's content against the artifact's declared hash.

Repositories like Zenodo and Dataverse can display the file listing of a ZIP archive directly. Using a recognizable structure (e.g., a `tro/` directory for the declaration and signature files) may make the package easier to browse, but this is a usability choice.

---

(on-demand-signing)=
## On-Demand Signing

A TRS may produce unsigned packages during execution and sign them later on demand. This is valid as long as the declaration file is not modified between creation and signing.

1. The TRS executes the computation and produces a package with the declaration and artifacts.
2. At a later time, a researcher requests a signed version.
3. The TRS signs the original declaration, producing the signature artifacts.
4. The signed package is assembled with the declaration, signature, and artifacts.

A timestamp, if present, records when the declaration was signed, not when the computation ran. The declaration itself records when each performance started and ended, using the TRP properties `trov:startedAtTime` and `trov:endedAtTime`.

This allows TRS implementations to decouple signing from execution, which is useful when the signing infrastructure is external or intermittently available. For example, a TRS operating in an isolated environment without network access during execution can defer both signing and timestamping to a later stage when a timestamp authority is reachable.

The critical constraint is chain of custody: the TRS must sign the declaration it originally produced, not a copy provided by the researcher. The signature attests that the TRS stands behind the declaration.

---

(tro-packages-verification)=
## Verification

The [TRO Declaration Format](tro-declaration-format.md#tro-format-verification) describes what verifying a TRO declaration establishes. At the package level, verification also entails confirming:

1. **Signature validity**, i.e. that the signature on the declaration was made with the key the package identifies.
2. **Timestamp validity**, if a timestamp is present, i.e. that the declaration's signature was made no later than the time it shows.
3. **Artifact integrity**, if the package includes artifacts, i.e. that the file contents of each included artifact hash to the artifact's declared hash.

The signature covers the declaration file byte-for-byte. The declaration must not be modified, reformatted, or re-serialized between signing and verification.

### Signing identity and trust

The two signing mechanisms currently supported establish who signed the declaration in different ways, with different trust tradeoffs.

**GPG with `trov:publicKey`:** The declaration includes the public key used to sign it, and the TRS publishes the key's fingerprint, for example in its documentation or on a key server. Two routine checks together establish who signed: confirming that the declared key has the published fingerprint, and confirming that the signature was made with that key.

**X.509/CMS:** The `.p7s` file includes the signer's certificate, in which a certificate authority (CA) attests that the public key belongs to a named organization. Two straightforward checks together establish who signed the declaration: confirming that the certificate is valid and names the organization operating the TRS, and confirming that the signature was made with the certificate's key.

In both cases, the verifier consults a source beyond the TRO package to connect the key or certificate to the TRS named in the declaration, normally the TRS's published description, to which the URL identifying the TRS in the declaration ideally leads. The package alone cannot prove who signed it.

---

## History

| Date | Change |
|------|--------|
| 2026-11-18 | Rewrote the Verification section. |
| 2026-03-26 | Added isolated-environment timestamping scenario to on-demand signing section. |
| 2026-03-22 | Initial publication. |
