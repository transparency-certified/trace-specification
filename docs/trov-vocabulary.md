# TROV Vocabulary Reference

**Transparent Research Object Vocabulary (TROV)**

- Namespace: `https://w3id.org/trace/2023/05/trov#`
- Prefix: `trov:`
- Ontology IRI: `https://w3id.org/trace/trov/0.1/`
- Version: 0.1 (Draft)
- License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- Publisher: [TRACE Project](https://transparency-certified.github.io/)

TROV provides terms for describing Transparent Research Objects (TROs), the Transparent Research Systems (TRS) that produce them, and the Transparent Research Performances (TRPs) they record. For the conceptual background motivating this vocabulary, see the [TRACE Conceptual Model](conceptual-model.md). For the JSON-LD format used to express TRO declarations, see [TRO Declaration Format](tro-declaration-format.md).

---

## Classes

### Core Entities

| Class | Description |
|-------|-------------|
| `trov:TrustedResearchElement` | Common base class for TRSs, TRPs, and TROs. |
| `trov:TransparentResearchObject` | A set of research artifacts produced by one or more TRPs and signed by the performing TRS. Subclass of `TrustedResearchElement`. |
| `trov:TrustedResearchSystem` | A system certified to perform TRPs and assemble TROs. Subclass of `TrustedResearchElement`. |
| `trov:TrustedResearchPerformance` | A supervised unit of work conducted by a TRS. The centerpiece of the TRACE conceptual model. Subclass of `TrustedResearchElement`. |
| `trov:TimeStampingAuthority` | An RFC 3161 timestamping authority trusted by a TRS. Subclass of `TrustedResearchElement`. |

### Artifacts and Compositions

| Class | Description |
|-------|-------------|
| `trov:ArtifactCollection` | Base class for collections of one or more artifacts. |
| `trov:ArtifactComposition` | The set of all digital artifacts described by a TRO, identified by a composition fingerprint. Subclass of `ArtifactCollection`. |
| `trov:ResearchArtifact` | A digital object (file, dataset, or bitstream) identified by a content digest. |
| `trov:CompositionFingerprint` | A digest computed over the sorted digests of all artifacts in a composition. Enables identifying TROs that describe the same set of artifacts. |

### Arrangements and Loci

| Class | Description |
|-------|-------------|
| `trov:ArtifactArrangement` | A named collection of loci capturing the locations of artifacts at a specific point in a workflow. |
| `trov:ArtifactLocus` | The location of a specific artifact within an arrangement. Links an artifact to a resource path. Subclass of `ArtifactCollection`. |

### The Warrant Chain: Attributes and Capabilities

The warrant chain is the core trust mechanism of TRACE. No transparency claim about a TRO can be asserted without justification traceable to a declared TRS capability.

```
TRO attribute
  ← warranted by → TRP attribute
    ← warranted by → TRS capability
```

| Class | Description |
|-------|-------------|
| `trov:TREAttribute` | Base class for attributes of a TRS, TRP, or TRO. |
| `trov:TRSAttribute` | An attribute of a TRS. Subclass of `TREAttribute`. |
| `trov:TRSCapability` | A declared ability of a TRS to enforce a specific transparency condition. Subclass of `TRSAttribute`. The foundation of the warrant chain. |
| `trov:TRSPolicy` | A transparency condition always enforced by a particular TRS (as opposed to a capability that may be selectively applied). Subclass of `TRSCapability`. |
| `trov:TRPAttribute` | A transparency claim about the conditions under which a specific TRP was conducted. Subclass of `TREAttribute`. |
| `trov:TROAttribute` | A transparency claim about a TRO as a whole, warranted by attributes of its constituent TRPs. Subclass of `TREAttribute`. |

---

## Properties

### TRO Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:wasAssembledBy` | `TransparentResearchObject` | `TrustedResearchSystem` | Links a TRO to the TRS that produced and signed it. |
| `trov:wasTimestampedBy` | `TransparentResearchObject` | `TimeStampingAuthority` | Links a TRO to the TSA that timestamped the TRS signature. |
| `trov:hasComposition` | `TransparentResearchObject` | `ArtifactComposition` | Links a TRO to the composition of artifacts it describes. |
| `trov:hasArrangement` | `TransparentResearchObject` | `ArtifactArrangement` | Links a TRO to an artifact arrangement it describes. |
| `trov:hasPerformance` | `TransparentResearchObject` | `TrustedResearchPerformance` | Links a TRO to a TRP it describes. |
| `trov:hasAttribute` | `TransparentResearchObject` | `TROAttribute` | Links a TRO to a transparency attribute asserted for it. |

### TRS Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:hasCapability` | `TrustedResearchSystem` | `TRSCapability` | Links a TRS to a capability it declares. |
| `trov:publicKey` | `TrustedResearchSystem` | Literal | The public key (e.g., ASCII-armored GPG key) associated with the TRS. |

### TRP Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:wasConductedBy` | `TrustedResearchPerformance` | `TrustedResearchSystem` | Links a TRP to the TRS that conducted it. |
| `trov:accessedArrangement` | `TrustedResearchPerformance` | `ArtifactArrangement` | Links a TRP to an arrangement it read from. |
| `trov:contributedToArrangement` | `TrustedResearchPerformance` | `ArtifactArrangement` | Links a TRP to an arrangement it wrote to. |
| `trov:hasPerformanceAttribute` | `TrustedResearchPerformance` | `TRPAttribute` | Links a TRP to a transparency attribute claimed for it. |
| `trov:startedAtTime` | `TrustedResearchPerformance` | Literal (dateTime) | When the performance began. |
| `trov:endedAtTime` | `TrustedResearchPerformance` | Literal (dateTime) | When the performance ended. |

### Composition and Artifact Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:hasArtifact` | `ArtifactCollection` | `ResearchArtifact` | Links a collection to an artifact it contains. |
| `trov:hasFingerprint` | `ArtifactComposition` | `CompositionFingerprint` | Links a composition to its fingerprint. |
| `trov:sha256` | `ResearchArtifact` or `CompositionFingerprint` | Literal (string) | The SHA-256 digest of an artifact's contents or of a composition's sorted artifact digests. |
| `trov:mimeType` | `ResearchArtifact` | Literal (string) | The MIME type of an artifact. |

### Arrangement and Locus Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:hasLocus` | `ArtifactArrangement` | `ArtifactLocus` | Links an arrangement to one of its loci. |
| `trov:hasArtifact` | `ArtifactLocus` | `ResearchArtifact` | Links a locus to the artifact at that location. |
| `trov:hasLocation` | `ArtifactLocus` | Literal (string) | A resource path (file path, URI, or other locator) for the artifact within this arrangement. |

### Warrant Chain Properties

| Property | Domain | Range | Description |
|----------|--------|-------|-------------|
| `trov:warrantedBy` | `TRPAttribute` | `TRSCapability` | Links a performance attribute to the TRS capability that justifies it. |
| `trov:warrantedBy` | `TROAttribute` | `TRPAttribute` | Links a TRO attribute to the performance attribute(s) that justify it. |

---

## Named Individuals: TRS Capability Types

The following capability types are currently defined. This list is designed to grow as new transparency conditions are identified by the research community.

### Capabilities Implemented by tro-utils / SIVACOR

| Individual | Parent | Description |
|------------|--------|-------------|
| `trov:CanProvideInternetIsolation` | `TRSCapability` | The TRS can isolate computations from network access during a TRP. |
| `trov:CanRecordInternetAccess` | `TRSCapability` | The TRS can record all network accesses made during a TRP. |

### Additional Capabilities Defined in the Vocabulary

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

### TRS Policy Types

Policies are capabilities that a TRS always enforces (as opposed to capabilities it can selectively apply).

| Individual | Parent | Description |
|------------|--------|-------------|
| `trov:EnforcesInternetIsolation` | `TRSPolicy` | The TRS always prevents Internet access during TRPs. |
| `trov:EnforcesNoninteractiveExecution` | `TRSPolicy` | The TRS always executes TRPs in non-interactive mode. |
| `trov:EnforcesEnvironmentIsolation` | `TRSPolicy` | The TRS always isolates the host environment during TRPs. |

---

## Named Individuals: TRP Attribute Types

| Individual | Parent | Warranted By | Description |
|------------|--------|-------------|-------------|
| `trov:InternetIsolation` | `TRPAttribute` | `trov:CanProvideInternetIsolation` | The TRP was conducted without network access. |
| `trov:InternetAccessRecording` | `TRPAttribute` | `trov:CanRecordInternetAccess` | All network accesses during the TRP were recorded. |

---

## Named Individuals: TRO Attribute Types

| Individual | Parent | Warranted By | Description |
|------------|--------|-------------|-------------|
| `trov:IncludesAllInputData` | `TROAttribute` | _(TRP attributes)_ | The TRO composition includes all input data employed in creating the TRO. |

---

## Cardinality Constraints

The following constraints are defined in SHACL shapes and enforced during validation.

| Shape | Property | Constraint |
|-------|----------|------------|
| TRO | `trov:wasAssembledBy` | Exactly 1 TRS |
| TRO | `trov:wasTimestampedBy` | At most 1 TSA |
| TRO | `trov:hasComposition` | At least 1 |
| TRO | `trov:hasArrangement` | At least 1 |
| TRS | `trov:publicKey` | Exactly 1 (string) |
| TSA | `trov:publicKey` | Exactly 1 (string) |
| Composition | `trov:hasFingerprint` | Exactly 1 |
| Composition | `trov:hasArtifact` | At least 1 |
| Fingerprint | `trov:sha256` | Exactly 1 (string) |
| Artifact | `trov:sha256` | Exactly 1 (string) |
| Artifact | `trov:mimeType` | At most 1 (string) |
| Arrangement | `trov:hasLocus` | At least 1 |
| Locus | `trov:hasArtifact` | Exactly 1 |
| Locus | `trov:hasLocation` | Exactly 1 (string) |

---

## External Vocabularies Used

TROV uses terms from the following external vocabularies:

| Prefix | Namespace | Usage |
|--------|-----------|-------|
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | `rdf:type` |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | `rdfs:comment`, `rdfs:Class`, `rdfs:subClassOf` |
| `schema:` | `https://schema.org` | `schema:CreativeWork`, `schema:Organization`, `schema:creator`, `schema:name`, `schema:description`, `schema:dateCreated` (used in tro-utils for TRO and TRS metadata) |

---

## Notes

**Namespace.** The current namespace `https://w3id.org/trace/2023/05/trov#` reflects the May 2023 version. The w3id.org persistent URI `https://w3id.org/trace/trov/0.1/` resolves to the formal ontology definition.

**Extensibility.** The capability and attribute type lists are designed to be extended. New TRS capability types and corresponding performance/TRO attribute types can be added as new transparency conditions are identified. Existing TRS certificates and TRO declarations remain valid when new types are introduced.

**Signing mechanism.** TROV is agnostic to the specific signing technology. The `trov:publicKey` property reflects the current GPG-based implementation. X.509 support is planned.

**Interoperability.** TROV aims to be interoperable with, rather than to replace, current and future Research Object standards (e.g., RO-Crate), archival formats (e.g., BagIt), and repository layouts. TROV complements the W3C PROV-O ontology for describing general provenance relationships.

**JSON-LD context.** TRO declarations include a `@context` block that maps the short-form term names used in JSON to the full URIs defined here. Producers of TROs reference the context and write ordinary JSON; the context enables downstream RDF processing without requiring the producer to engage with RDF directly. See [TRO Declaration Design](tro-declaration-design.md) for the full rationale behind this dual-audience design.
