# TROV Pre-Release Vocabulary Reference
<span style="display:inline-block; padding:2px 10px;  margin-bottom:16px; background:#f0ad4e; font-weight:bold; color:black; border-radius:4px; font-size:14px;">
  DRAFT</span>

Frozen snapshot of the pre-release vocabulary used by early TRACE implementations. Lists only the terms actually produced by the pre-release implementations, with term changes and migration guidance for TROV 0.1.

| Document Section | Description |
|---------|-------------|
| [Vocabulary Metadata](#vocabulary-metadata) | Namespace, prefix, and status |
| [Scope](#scope) | What terms are included |
| [Classes](#classes) | Core entities, artifacts, arrangements, and locations |
| [Properties](#properties) | TRO, TRS, composition, arrangement, TRP, and warrant chain properties |
| [TRS Capabilities](#trs-capability-types) | Capability types produced by pre-release implementations |
| [TRP Attributes](#trp-attribute-types) | Attribute types and their warrant links |
| [External Vocabularies](#external-vocabularies-used) | RDF, RDFS, and schema.org terms used alongside TROV |
| [Term Changes in TROV 0.1](#term-changes-in-trov-01) | Term renames |
| [Migration](#migration-to-trov-01) | Steps to convert pre-release declarations to 0.1 |

## Vocabulary Metadata

- Namespace: `https://w3id.org/trace/2023/05/trov#`
- Prefix: `trov:`
- Status: **Retired.** This is a frozen snapshot of the pre-release vocabulary used by early TRACE implementations. It is superseded by [TROV 0.1](trov-vocabulary.md).

> **Migration notice.** The `2023/05` namespace was used during early development by pre-release TRACE implementations. TRO declarations created with this namespace remain valid documents but are not guaranteed to conform to TROV 0.1 without conversion. New implementations should use TROV 0.1 (`https://w3id.org/trace/trov/0.1#`). See the [Versioning Strategy and Roadmap](trov-versioning-and-roadmap.md) for details.

---

## Scope

This document records only the terms actually used by the pre-release implementations. Terms previously defined in the ontology file (`trov.ttl`) or in hand-written examples but not produced by early implementations are not listed here. For the full vocabulary including additional capability types and attribute types, see [TROV 0.1](trov-vocabulary.md).

---

## Classes

### Core Entities

| Class | Description |
|-------|-------------|
| `trov:TransparentResearchObject` | A set of research artifacts produced by one or more TRPs and signed by the assembling TRS. |
| `trov:TrustedResearchSystem` | A system that performs TRPs and assembles TROs. |
| `trov:TrustedResearchPerformance` | A supervised unit of work conducted by a TRS. |

### Artifacts and Compositions

| Class | Description |
|-------|-------------|
| `trov:ArtifactComposition` | The set of all digital artifacts described by a TRO. |
| `trov:ResearchArtifact` | A digital object identified by a content hash. |
| `trov:CompositionFingerprint` | A hash computed over the sorted hashes of all artifacts in a composition. |

### Arrangements and Loci

| Class | Description |
|-------|-------------|
| `trov:ArtifactArrangement` | A named collection of artifact locations capturing where artifacts were at a point in a workflow. |
| `trov:ArtifactLocus` | The location of a specific artifact within an arrangement. |

---

## Properties

### TRO Properties

| Property | Description |
|----------|-------------|
| `trov:wasAssembledBy` | Links a TRO to the TRS that produced it. |
| `trov:hasComposition` | Links a TRO to its artifact composition. |
| `trov:hasArrangement` | Links a TRO to an artifact arrangement. |
| `trov:hasPerformance` | Links a TRO to a TRP it describes. |
| `trov:hasAttribute` | Links a TRO to a transparency attribute. Present but empty in pre-release implementations. |

### TRS Properties

| Property | Description |
|----------|-------------|
| `trov:hasCapability` | Links a TRS to a capability it declares. |
| `trov:publicKey` | The public key associated with the TRS. ASCII-armored GPG key. |
| `trov:name` | Short name for the TRS. |
| `trov:owner` | Owner of the TRS. |
| `trov:description` | Description of the TRS. |
| `trov:contact` | Contact email for the TRS. |
| `trov:url` | URL for the TRS. |

### Composition and Artifact Properties

| Property | Description |
|----------|-------------|
| `trov:hasArtifact` | Links a composition or locus to an artifact. |
| `trov:hasFingerprint` | Links a composition to its fingerprint. |
| `trov:sha256` | SHA-256 digest of an artifact's contents or a composition's sorted artifact digests. |
| `trov:mimeType` | MIME type of an artifact. |

### Arrangement and Locus Properties

| Property | Description |
|----------|-------------|
| `trov:hasLocus` | Links an arrangement to one of its loci. |
| `trov:hasLocation` | Resource path for an artifact within an arrangement. |

### TRP Properties

| Property | Description |
|----------|-------------|
| `trov:wasConductedBy` | Links a TRP to the TRS that conducted it. |
| `trov:accessedArrangement` | Links a TRP to an arrangement it read from. |
| `trov:contributedToArrangement` | Links a TRP to an arrangement it wrote to. |
| `trov:hasPerformanceAttribute` | Links a TRP to a transparency attribute claimed for it. |
| `trov:startedAtTime` | When the performance began. |
| `trov:endedAtTime` | When the performance ended. |

### Warrant Chain Properties

| Property | Description |
|----------|-------------|
| `trov:warrantedBy` | Links a TRP attribute to the TRS capability that justifies it. |

---

## TRS Capability Types

| Type | Description |
|------|-------------|
| `trov:CanProvideInternetIsolation` | The TRS can isolate computations from network access during a TRP. |
| `trov:CanRecordInternetAccess` | The TRS can record all network accesses made during a TRP. |

---

## TRP Attribute Types

| Type | Warranted by | Description |
|------|-------------|-------------|
| `trov:InternetIsolation` | `trov:CanProvideInternetIsolation` | The TRP was conducted without network access. |
| `trov:InternetAccessRecording` | `trov:CanRecordInternetAccess` | All network accesses during the TRP were recorded. |

---

## External Vocabularies Used

Both implementations use the following external vocabularies alongside TROV:

| Prefix | Namespace | Terms used |
|--------|-----------|------------|
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | `rdf:type` (implicit via `@type`) |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | `rdfs:comment` |
| `schema:` | `https://schema.org` | `schema:CreativeWork`, `schema:Organization`, `schema:creator`, `schema:name`, `schema:description`, `schema:dateCreated` |

The `schema:` terms appear on the TRO root node and on the TRS node.

---

## Term Changes in TROV 0.1

| Pre-release | TROV 0.1 |
|-------------|----------|
| `trov:ArtifactLocus` | `trov:ArtifactLocation` |
| `trov:hasLocus` | `trov:hasArtifactLocation` |
| `trov:hasArtifact` (on locus) | `trov:artifact` |
| `trov:hasLocation` | `trov:path` |
| `trov:sha256` | `trov:hash` (object with `trov:hashAlgorithm` + `trov:hashValue`) |

---

## Migration to TROV 0.1

Based on the current 0.1 draft, updating a pre-release TRO declaration to conform to TROV 0.1 involves the following changes. These steps may be revised as 0.1 is finalized.

1. **Update the namespace URI** in the `@context` block from `https://w3id.org/trace/2023/05/trov#` to `https://w3id.org/trace/trov/0.1#`.
2. **Replace `trov:sha256`** with a `trov:hash` object containing `trov:hashAlgorithm` and `trov:hashValue`. For example, `"trov:sha256": "abc..."` becomes `"trov:hash": { "trov:hashAlgorithm": "sha256", "trov:hashValue": "abc..." }`.
3. **Add `trov:vocabularyVersion`** property to the TRO root object (value `"0.1"`).
4. **Rename artifact location terms.** `trov:ArtifactLocus` → `trov:ArtifactLocation`, `trov:hasLocus` → `trov:hasArtifactLocation`, `trov:hasArtifact` (on locations) → `trov:artifact`, `trov:hasLocation` → `trov:path`.
