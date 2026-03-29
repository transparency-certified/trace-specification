# TROV Vocabulary Reference
<span style="display:inline-block; padding:2px 10px;  margin-bottom:16px; background:#f0ad4e; font-weight:bold; color:black; border-radius:4px; font-size:14px;">
  TROV 0.1 DRAFT</span>

*This document is a draft and subject to revision.
Please [submit feedback or report issues](https://github.com/transparency-certified/trace-specification/issues/new?title=trov-vocabulary.md:%20).*

Term reference for the Transparent Research Object Vocabulary (TROV). Lists every class, property, and predefined value in the current draft, with descriptions and cardinality constraints.

| Document Section | Description |
|---------|-------------|
| [Vocabulary Metadata](#vocabulary-metadata) | Namespace, version, status, and license |
| [Classes](#classes) | Core entities: TRO, TRS, TRP, artifacts, compositions, arrangements |
| [Properties](#properties) | Relationships between entities: linking TROs to TRSs, TRPs, arrangements, etc. |
| [TRS Capability Types](#predefined-values-trs-capability-types) | What a TRS can do (e.g. provide internet isolation) |
| [TRP Attribute Types](#predefined-values-trp-attribute-types) | Transparency claims about a specific performance |
| [TRO Attribute Types](#predefined-values-tro-attribute-types) | Transparency claims about a TRO as a whole |
| [Cardinality Constraints](#cardinality-constraints) | Required vs optional properties and their multiplicities |
| [External Vocabularies](#external-vocabularies-used) | RDF, RDFS, and schema.org terms used alongside TROV |
| [Known Limitations](#known-limitations) | Scope boundaries and open questions for 0.1 |
| [Notes](#trov-vocab-notes) | JSON-LD context, design rationale, relationship to pre-release |

For the conceptual background motivating this vocabulary, see the [TRACE Conceptual Model](conceptual-model.md). For the JSON-LD format used to express TRO declarations, see [TRO Declaration Format](tro-declaration-format.md). For the design rationale behind the JSON-LD format, see [TRO Declaration Design](tro-declaration-design.md).

---

(vocabulary-metadata)=
## Vocabulary Metadata

| | |
|---|---|
| **Namespace** | `https://w3id.org/trace/trov/0.1#` |
| **Prefix** | `trov:` |
| **Version** | 0.1 (Draft) |
| **License** | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| **Publisher** | [TRACE Project](https://transparency-certified.github.io/) |
| **Status** | Namespace URI does not yet resolve — see [Versioning Strategy and Roadmap](trov-versioning-and-roadmap.md) for the resolution plan. |

---

(classes)=
## Classes

### Core Entities

| Class | Description |
|-------|-------------|
| `trov:TrustedResearchElement` | Common base class for TRSs, TRPs, and TROs. |
| `trov:TransparentResearchObject` | A set of research artifacts produced by one or more TRPs and signed by the assembling TRS. Subclass of `TrustedResearchElement`. |
| `trov:TrustedResearchSystem` | A system that performs TRPs and assembles TROs. Subclass of `TrustedResearchElement`. |
| `trov:TrustedResearchPerformance` | A supervised unit of work conducted by a TRS. The centerpiece of the TRACE conceptual model. Subclass of `TrustedResearchElement`. |
| `trov:TimeStampingAuthority` | An RFC 3161 timestamping authority trusted by a TRS. Subclass of `TrustedResearchElement`. |

### Artifacts and Compositions

| Class | Description |
|-------|-------------|
| `trov:ArtifactCollection` | Base class for collections of one or more artifacts. |
| `trov:ArtifactComposition` | The set of all digital artifacts described by a TRO, identified by a composition fingerprint. Subclass of `ArtifactCollection`. |
| `trov:ResearchArtifact` | A digital object (file, dataset, or bitstream) identified by a content hash. |
| `trov:CompositionFingerprint` | A hash computed over the sorted hashes of all artifacts in a composition. Enables identifying TROs that describe the same set of artifacts. |

### Arrangements and Locations

| Class | Description |
|-------|-------------|
| `trov:ArtifactArrangement` | A named collection of artifact locations. Arrangements are linked to performances as inputs or outputs. |
| `trov:ArtifactLocation` | The placement of a specific artifact within an arrangement. Links one artifact to one resource path. |

### The Warrant Chain: Attributes and Capabilities

The warrant chain is TROV's mechanism for accountability. When transparency claims are made about a TRO, the warrant chain records who is responsible for them.

```
TRO attribute
  ← warranted by → TRP attribute
    ← warranted by → TRS capability
```

| Class | Description |
|-------|-------------|
| `trov:TREAttribute` | Base class for attributes of a TRS, TRP, or TRO. |
| `trov:TRSAttribute` | An attribute of a TRS. Subclass of `TREAttribute`. |
| `trov:TRSCapability` | A declared ability of a TRS to enforce a specific transparency condition. Subclass of `TRSAttribute`. |
| `trov:TRSPolicy` | A TRS-level assertion about a capability. Subclass of `TRSCapability`. Under redesign — see Known Limitations. |
| `trov:TRPAttribute` | A transparency claim about the conditions under which a specific TRP was conducted. Subclass of `TREAttribute`. |
| `trov:TROAttribute` | A transparency claim about a TRO as a whole, warranted by attributes of its constituent TRPs. Subclass of `TREAttribute`. |

---

(properties)=
## Properties

### TRO Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:vocabularyVersion` | `TransparentResearchObject` | Literal (string) | The TROV vocabulary version this declaration conforms to (e.g. `"0.1"`). |
| `trov:wasAssembledBy` | `TransparentResearchObject` | `TrustedResearchSystem` | Links a TRO to the TRS that produced and signed it. |
| `trov:createdWith` | `TransparentResearchObject` | `schema:SoftwareApplication` | Software tool that generated this TRO declaration (optional). Value includes `schema:name` and `schema:softwareVersion`. |
| `trov:wasTimestampedBy` | `TransparentResearchObject` | `TimeStampingAuthority` | Links a TRO to a TSA that timestamped the TRS signature. |
| `trov:hasComposition` | `TransparentResearchObject` | `ArtifactComposition` | Links a TRO to the composition of artifacts it describes. |
| `trov:hasArrangement` | `TransparentResearchObject` | `ArtifactArrangement` | Links a TRO to an artifact arrangement it describes. |
| `trov:hasPerformance` | `TransparentResearchObject` | `TrustedResearchPerformance` | Links a TRO to a TRP it describes. |
| `trov:hasAttribute` | `TransparentResearchObject` | `TROAttribute` | Links a TRO to a transparency attribute asserted for it. |

### TRS Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:hasCapability` | `TrustedResearchSystem` | `TRSCapability` | Links a TRS to a capability it declares. |
| `trov:publicKey` | `TrustedResearchSystem` | Literal | The TRS's public key (optional). Required for GPG signing (binds the key to the signed declaration content). Not needed for X.509/CMS (the certificate chain is in the `.p7s` file). |
| `trov:customTerm` | `TrustedResearchSystem` | Resource | Declares a custom term that extends a TROV class. Each value is a resource with an `rdfs:subClassOf` triple connecting it to the TROV class it extends. See [TROV Extension Guide](trov-extension-guide.md#declaring-custom-types-in-the-declaration). |

### TRP Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:wasConductedBy` | `TrustedResearchPerformance` | `TrustedResearchSystem` | Links a TRP to the TRS that conducted it. |
| `trov:accessedArrangement` | `TrustedResearchPerformance` | `ArtifactArrangement` | Links a TRP to an arrangement it read from. |
| `trov:contributedToArrangement` | `TrustedResearchPerformance` | `ArtifactArrangement` | Links a TRP to an arrangement it wrote to. |
| `trov:hasPerformanceAttribute` | `TrustedResearchPerformance` | `TRPAttribute` | Links a TRP to a transparency attribute claimed for it. |
| `trov:startedAtTime` | `TrustedResearchPerformance` | Literal (ISO 8601 string) | When the performance began. |
| `trov:endedAtTime` | `TrustedResearchPerformance` | Literal (ISO 8601 string) | When the performance ended. |

### Composition and Artifact Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:hasArtifact` | `ArtifactComposition` | `ResearchArtifact` | Links a composition to an artifact it contains. |
| `trov:hasFingerprint` | `ArtifactComposition` | `CompositionFingerprint` | Links a composition to its fingerprint. |
| `trov:hash` | `ResearchArtifact` or `CompositionFingerprint` | Object or array of objects | One or more hashes of an artifact's contents or of a composition's sorted artifact hash values. Each object contains `trov:hashAlgorithm` and `trov:hashValue`. |
| `trov:hashAlgorithm` | (within `trov:hash` object) | Literal (string) | The algorithm used to compute the hash (e.g. `"sha256"`, `"hmac-sha256"`). |
| `trov:hashValue` | (within `trov:hash` object) | Literal (string) | The computed hash value. |
| `trov:mimeType` | `ResearchArtifact` | Literal (string) | The MIME type of an artifact. |

### Arrangement and Location Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:hasArtifactLocation` | `ArtifactArrangement` | `ArtifactLocation` | Links an arrangement to one of its artifact locations. |
| `trov:artifact` | `ArtifactLocation` | `ResearchArtifact` | Links a location to the artifact placed there. |
| `trov:path` | `ArtifactLocation` | Literal (string: file path, URI, or other locator) | The resource path for the artifact within this arrangement. |

### Warrant Chain Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:warrantedBy` | `TRPAttribute` | `TRSCapability` | Links a performance attribute to the TRS capability that justifies it. |
| `trov:warrantedBy` | `TROAttribute` | `TRPAttribute` | Links a TRO attribute to the performance attribute(s) that justify it. |

---

(predefined-values-trs-capability-types)=
## Predefined Values: TRS Capability Types

The following capability types are currently defined. This list is designed to grow as new transparency conditions are identified by the research community.

### Capabilities Implemented by tro-utils / SIVACOR

| Individual | Parent | Description |
|------------|--------|-------------|
| `trov:CanProvideInternetIsolation` | `TRSCapability` | The TRS can isolate computations from network access during a TRP. |
| `trov:CanRecordInternetAccess` | `TRSCapability` | The TRS can record all network accesses made during a TRP. |

### Additional Capabilities Under Discussion

| Individual | Parent | Description |
|------------|--------|-------------|
| `trov:CanIsolateEnvironment` | `TRSCapability` | The TRS can prevent access to the host environment during a TRP (e.g., sandbox or container execution). |
| `trov:CanPreventAuthorIntervention` | `TRSCapability` | The TRS can prevent author intervention during a TRP (e.g., fully automated execution). |
| `trov:CanExcludeInputs` | `TRSCapability` | The TRS can exclude input data from a TRO produced during a TRP. |
| `trov:CanExcludeOutputs` | `TRSCapability` | The TRS can exclude output data from a TRO produced during a TRP. |
| `trov:CanEnsureInputDataIncludedInTROPackage` | `TRSCapability` | The TRS can ensure all input data is included in the TRO package. |
| `trov:CanRequireInputDataExistsBeforeRun` | `TRSCapability` | The TRS can require all input data exists prior to a TRP. |
| `trov:CanRequireInputDataLocalBeforeRun` | `TRSCapability` | The TRS can require all input data is stored locally prior to a TRP. |
| `trov:CanEnsureInputDataPersistsAfterRun` | `TRSCapability` | The TRS can ensure all input data persists after a TRP. |
| `trov:CanEnsureOutputDataIncludedInTROPackage` | `TRSCapability` | The TRS can ensure all output data is included in the TRO package. |
| `trov:CanEnsureCodeIncludedInTROPackage` | `TRSCapability` | The TRS can ensure all custom code is included in the TRO package. |
| `trov:CanRecordSoftwareEnvironment` | `TRSCapability` | The TRS can record a full description of the software environment. |
| `trov:CanDetectInternetAccess` | `TRSCapability` | The TRS can detect Internet access during a TRP. |
| `trov:CanEnforceInternetIsolation` | `TRSCapability` | The TRS can enforce Internet isolation during a TRP. |
| `trov:CanPreventUserInteractionDuringRun` | `TRSCapability` | The TRS can prevent user interaction during a TRP. |
| `trov:CanEnforceCapabilitiesTechnically` | `TRSCapability` | The TRS can enforce all of its declared capabilities through technical means (as opposed to policy-based enforcement). |

---

(predefined-values-trp-attribute-types)=
## Predefined Values: TRP Attribute Types

| Individual | Parent | Warranted By | Description |
|------------|--------|-------------|-------------|
| `trov:InternetIsolation` | `TRPAttribute` | `trov:CanProvideInternetIsolation` | The TRP was conducted without network access. |
| `trov:InternetAccessRecording` | `TRPAttribute` | `trov:CanRecordInternetAccess` | All network accesses during the TRP were recorded. |

---

(predefined-values-tro-attribute-types)=
## Predefined Values: TRO Attribute Types

| Individual | Parent | Warranted By | Description |
|------------|--------|-------------|-------------|
| `trov:IncludesAllInputData` | `TROAttribute` | _(TRP attributes)_ | The TRO composition includes all input data employed in creating the TRO. |

---

(cardinality-constraints)=
## Cardinality Constraints

The following constraints are defined in SHACL shapes and enforced during validation.

| Shape | Property | Constraint |
|-------|----------|------------|
| TRO | `trov:vocabularyVersion` | Exactly 1 (string) |
| TRO | `trov:wasAssembledBy` | Exactly 1 TRS |
| TRO | `trov:wasTimestampedBy` | At most 1 TSA |
| TRO | `trov:createdWith` | At most 1 (object) |
| TRO | `trov:hasComposition` | Exactly 1 |
| TRO | `trov:hasArrangement` | At least 1 |
| TRS | `trov:publicKey` | At most 1 (string). Required for GPG signing. |
| TSA | `trov:publicKey` | At most 1 (string) |
| Composition | `trov:hasFingerprint` | Exactly 1 |
| Composition | `trov:hasArtifact` | At least 1 |
| Fingerprint | `trov:hash` | Exactly 1 (object) |
| Artifact | `trov:hash` | At least 1 (object or array) |
| Artifact | `trov:mimeType` | At most 1 (string) |
| Arrangement | `trov:hasArtifactLocation` | At least 1 |
| Location | `trov:artifact` | Exactly 1 |
| Location | `trov:path` | Exactly 1 (string) |

---

(external-vocabularies-used)=
## External Vocabularies Used

TROV uses terms from the following external vocabularies:

| Prefix | Namespace | Usage |
|--------|-----------|-------|
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | `rdf:type` |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | `rdfs:comment`, `rdfs:Class`, `rdfs:subClassOf` |
| `schema:` | `https://schema.org` | `schema:CreativeWork`, `schema:Organization`, `schema:creator`, `schema:name`, `schema:description`, `schema:dateCreated`. Optional — used in tro-utils for TRO and TRS metadata but not required for conformance. See [TRO Declaration Format — dependency boundary](tro-declaration-format.md#the-context-block). |

---

(known-limitations)=
## Known Limitations

| Limitation | Disposition |
|-----------|------------|
| Only two TRP attribute types defined (`InternetIsolation`, `InternetAccessRecording`) | Acceptable for 0.1 — new types can be added without breaking changes |
| Only one TRO attribute type defined (`IncludesAllInputData`) | Acceptable for 0.1 — same reasoning |
| `trov:publicKey` optional — required for GPG, not needed for X.509/CMS | Resolved: see [TRO Packages — Signing identity and trust](tro-packages.md#signing-identity-and-trust) |
| No `trov:signingMechanism` property to identify the signing approach | Resolve for 0.1 |
| `TRSPolicy` / `trov:hasPolicy` defined but not wired up | Deferred to 0.2 |
| `trov:TimeStampingAuthority` wraps an external concept (RFC 3161 TSA) | Acceptable for 0.1 — no standard RDF class exists; candidate for replacement if one emerges |

---

(trov-vocab-notes)=
## Notes

**Namespace.** The 0.1 namespace is `https://w3id.org/trace/trov/0.1#`; the pre-release namespace `https://w3id.org/trace/2023/05/trov#` is retired. See [Pre-Release Vocabulary Reference](trov-prerelease.md) for migration guidance.

**Extensibility.** The capability and attribute type lists are designed to be extended. New TRS capability types and corresponding performance/TRO attribute types can be added as new transparency conditions are identified. Existing TRS certificates and TRO declarations remain valid when new types are introduced.

**Signing mechanism.** TROV is agnostic to the specific signing technology. Current implementations use GPG and X.509/CMS. For GPG, `trov:publicKey` is required in the declaration to bind the key to the signed content. For X.509/CMS, the certificate chain in the `.p7s` file provides identity binding, so `trov:publicKey` is not needed. See [TRO Packages — Signing identity and trust](tro-packages.md#signing-identity-and-trust) for details. A proposed `trov:signingMechanism` property is under review for 0.1.

**Interoperability.** TROV aims to be interoperable with, rather than to replace, current and future Research Object standards (e.g., RO-Crate), archival formats (e.g., BagIt), and repository layouts. TROV complements the W3C PROV-O ontology for describing general provenance relationships.

**JSON-LD context.** TRO declarations use a `@context` block to map short-form term names to the URIs defined here. See [TRO Declaration Format](tro-declaration-format.md) for the structure and [TRO Declaration Design](tro-declaration-design.md) for the dual-audience rationale.
