# TRO Declaration Format
<span class="draft-badge">
  TROV 0.1 DRAFT</span>

*This document is a draft and subject to revision.
Please [submit feedback or report issues](https://github.com/transparency-certified/trace-specification/issues/new?title=tro-declaration-format.md:%20).*

A **TRO declaration** is a JSON-LD document that describes a Transparent Research Object. It records which digital artifacts were involved in a computational workflow, how they were arranged at each stage, which computations and other operations the TRS supervised, what transparency claims are made about those operations and about the TRO as a whole, and what capabilities of the TRS warrant those claims.

| Section | Description |
|---------|-------------|
| [Overview](#tro-format-overview) | The parts of a TRO declaration and their roles |
| [Declaration Envelope](#declaration-envelope) | The `@context` and `@graph` members of a TRO declaration |
| [TRO Elements](#tro-elements) | Each element of the TRO element graph, with its properties |
| [Warrant Chains](#the-warrant-chain) | How TRO and performance (TRP) attributes are supported by TRS capabilities |
| [Identifier Conventions](#identifier-conventions) | Recommended `@id` patterns for TRO elements |
| [Signing and Timestamping](#signing-and-timestamping) | Establishing trust with GPG and X.509/CMS signing |
| [Verification](#tro-format-verification) | What TRO verification establishes |
| [Complete Example](#complete-example) | A complete sample TRO declaration to use as a pattern |

For definitions of the vocabulary terms used here, see the [TROV Vocabulary Reference](trov-vocabulary.md). For the conceptual background, see the [TRACE Conceptual Model](conceptual-model.md). For the design rationale behind the JSON-LD format, see [TRO Declaration Design](tro-declaration-design.md).

---

(tro-format-overview)=
## Overview

A TRO declaration is a single JSON-LD file (conventionally `*.jsonld`) containing:

1. A **`@context`** block that maps short term names and element IDs to full URIs.
2. A **`@graph`** array describing the TRO as a graph of linked elements (see [Note 2](#tro-format-notes) for why it is an array).

The TRO element graph includes:

- **TRO properties** — the TRO's identity, TROV version and signing mechanism, and optionally who created it and when.
- **TRS declaration** — the Trusted Research System that assembled and signed the TRO; includes the TRS's declared capabilities and signing identity.
- **Composition** — the complete set of research artifacts referred to in the TRO declaration, each with the hash of its content; includes a composition fingerprint for identifying equivalent compositions.
- **Arrangements** — named snapshots showing where artifacts were located at specific points in the workflow.
- **Performances** — records of supervised computations, each linking input arrangements to output arrangements, with transparency attributes warranted by TRS capabilities.
- **TRO attributes** — transparency claims about the TRO as a whole, warranted by TRS capabilities directly or through the attributes of the performances.

The TRO declaration is accompanied by:

- A **detached signature** — a cryptographic signature over the declaration (e.g. GPG `.sig` or X.509/CMS `.p7s`).
- Optionally, a **timestamp** — proof of when the signature was created (e.g. a separate RFC 3161 `.tsr` file, or embedded in the `.p7s`).

---

(declaration-envelope)=
## Declaration Envelope

The top level of a TRO declaration has exactly two members:

- **`@context`** maps short term names and element IDs to full URIs; see [The `@context` Block](#the-context-block).
- **`@graph`** is an array whose contents describe the TRO; see [TRO Elements](#tro-elements) and, for why it is an array, [Note 2](#tro-format-notes).

```json
{
    "@context": { ... },
    "@graph": [ { /* description of the TRO */ } ]
}
```

(the-context-block)=
### The `@context` Block

The `@context` declares the namespace prefixes that the declaration's names use:

```json
"@context": {
    "rdf":    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs":   "http://www.w3.org/2000/01/rdf-schema#",
    "trov":   "https://w3id.org/trace/trov/0.1#",
    "schema": "https://schema.org/",
    .
    .
    .
}
```

All four prefixes above are usually present and represent the following vocabularies:

| Prefix | Namespace | Purpose |
|--------|-----------|---------|
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | RDF type system |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | Labels and comments |
| `trov:` | `https://w3id.org/trace/trov/0.1#` | All TROV terms |
| `schema:` | `https://schema.org/` | Standard metadata (name, description, dates) |

The mandatory parts of a TRO declaration depend only on TROV and the foundational `rdf:` and `rdfs:` namespaces. The `schema:` prefix is a convenience for common metadata; it may be omitted if no `schema:` properties are used, and no TRACE-compliant tool may reject a TRO declaration for missing `schema:` properties. Conversely, consumers of TROs are free to ignore properties and types from vocabularies other than TROV, `rdf:` and `rdfs:`, such as `schema:`.

The `@context` also generally carries an `@base`, a URL prefixed to every relative `@id` in the declaration; see [Identifier Conventions](#identifier-conventions).

```json
"@context": {
    .
    .
    .
    "@base":  "https://trs.example.org/tro/3f2a9c/"
}
```

---

(tro-elements)=
## TRO Elements

The `@graph` holds a root element describing the TRO, with the other elements nested within it under the properties shown below.

### TRO Properties

The TRO's properties identify it, record who created it and how it is signed, and link it to the other elements of the TRO element graph.

Example TRO properties:

```json
{
    "@id": "tro",
    "@type": "trov:TransparentResearchObject",

    "trov:vocabularyVersion": "0.1",
    "trov:signingMechanism": { "@id": "trov:GPGSigning" },

    "schema:creator":     { "@id": "https://trs.example.org/" },
    "schema:name":        "Example TRO",
    "schema:description": "TRO produced by an example workflow",
    "schema:dateCreated": "2024-06-15T14:30:00Z",

    "trov:wasAssembledBy":  { ... },
    "trov:wasTimestampedBy": { ... },
    "trov:createdWith":     { ... },
    "trov:hasComposition":  { ... },
    "trov:hasArrangement":  [ ... ],
    "trov:hasPerformance":  [ ... ],
    "trov:hasAttribute":    [ ... ]
}
```

The table below describes each property in the example above: the type of its value, whether it is required, and what it records. The `schema:` properties are optional metadata; where present, they take the values schema.org defines for them. See [The `@context` Block](#the-context-block) for how the `trov:` and `schema:` prefixes are defined.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Identifier for the TRO, conventionally the relative path `"tro"`. See [Identifier Conventions](#identifier-conventions). |
| `@type` | string or array | **Yes** | Must be (or include) `"trov:TransparentResearchObject"`. |
| `trov:vocabularyVersion` | string | **Yes** | The TROV vocabulary version this declaration conforms to, e.g. `"0.1"`, matching the version in the `trov` prefix. |
| `schema:creator` | object | no | The person or organization that created this TRO declaration, given as an object rather than a string. |
| `schema:name` | string or array | no | Short title for the TRO. |
| `schema:description` | string or array | no | Human-readable description of the TRO. |
| `schema:dateCreated` | string (ISO 8601) | no | When the TRO declaration was created: a date or a date-time. |
| `trov:signingMechanism` | object | **Yes** | A reference to the mechanism employed to sign the TRO declaration, currently either `trov:GPGSigning` or `trov:X509CMSSigning`. See [Signing and Timestamping](#signing-and-timestamping). |
| `trov:wasAssembledBy` | object | **Yes** | The TRS that produced and signed this TRO. |
| `trov:wasTimestampedBy` | object | no | The timestamping authority (TSA) that timestamped the signature on the TRO declaration. |
| `trov:createdWith` | object | no | The software that generated this TRO declaration. |
| `trov:hasComposition` | object | **Yes** | The complete set of artifacts described by the TRO with their hashes. |
| `trov:hasArrangement` | array | **Yes** | Snapshots of where the artifacts were located at points in the workflow. |
| `trov:hasPerformance` | array | no | The computations and other operations the TRS supervised. |
| `trov:hasAttribute` | array | no | Transparency claims about the TRO as a whole. |

---

### TRS Declaration (`trov:wasAssembledBy`)

The TRS declaration identifies the Trusted Research System that supervised the workflow and signed the TRO. It includes the TRS's declared capabilities and signing identity.

Example TRS declaration:

```json
"trov:wasAssembledBy": {
    "@id": "https://trs.example.org/",
    "@type": ["trov:TrustedResearchSystem", "schema:Organization"],
    "schema:name":        "Example TRS",
    "schema:description": "A TRS that enforces Internet isolation and records Internet access",
    "trov:publicKey": "...",
    "trov:hasCapability": [
        {
            "@id": "https://trs.example.org/capability/internet-isolation",
            "@type": "trov:CanProvideInternetIsolation"
        },
        {
            "@id": "https://trs.example.org/capability/internet-access-recording",
            "@type": "trov:CanRecordInternetAccess"
        }
    ],
    "trov:customTerm": [
        {
            "@id": "mytrs:CanProvideAuditLogging",
            "rdfs:subClassOf": { "@id": "trov:TRSCapabilityType" }
        }
    ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | A URL uniquely identifying the TRS, on a domain its operator controls, ideally one that leads to a description of the system. |
| `@type` | string or array | **Yes** | Must be (or include) `"trov:TrustedResearchSystem"`. |
| `trov:publicKey` | string | GPG: **Yes**; X.509/CMS: no | The TRS's public key. Required for GPG signing (binds key to signed content). Not needed for X.509/CMS (certificate is in the `.p7s` file). |
| `trov:hasCapability` | array | no | Zero or more capability declarations. |
| `trov:customTerm` | array | no | Declarations of custom terms that extend TROV classes. Each entry names the custom term and the TROV class it extends via `rdfs:subClassOf`. See [TROV Extension Guide](trov-extension-guide.md#declaring-custom-types-in-the-declaration). |
| `schema:name` | string | no | Short name for the TRS. |
| `schema:description` | string | no | Human-readable description of the TRS. |

Each **capability** object declares that the TRS is able to enforce a specific transparency condition:

| Field | Type | Description |
|-------|------|-------------|
| `@id` | string | A URL uniquely identifying the capability. Referenced by performance attributes. |
| `@type` | string | A capability type from the TROV vocabulary, e.g. `"trov:CanProvideInternetIsolation"`. |

See [TROV Vocabulary Reference — TRS Capability Types](trov-vocabulary.md#predefined-values-trs-capability-types) for the full list of defined capability types.

---

### Timestamping Authority (`trov:wasTimestampedBy`)

If the TRS obtained an RFC 3161 timestamp for the TRO signature from a separate timestamping authority, the TSA is recorded as a property of the TRO. Not all signing mechanisms require this. An X.509/CMS signature file (`.p7s`) can carry the timestamp itself, in which case no separate TSA block is needed.

```json
{
    "@id": "tro",
    "@type": "trov:TransparentResearchObject",
    "trov:wasAssembledBy": { ... },
    "trov:wasTimestampedBy": {
        "@id": "tsa",
        "@type": "trov:TimeStampingAuthority",
        "trov:publicKey": "..."
    },
    ...
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Identifier, conventionally the relative path `"tsa"`. |
| `@type` | string | **Yes** | Must be `"trov:TimeStampingAuthority"`. |
| `trov:publicKey` | string | no | Public key of the timestamping authority. Not needed when the timestamp is embedded in an X.509/CMS signature (`.p7s`). |

---

### Artifact Composition (`trov:hasComposition`)

The composition is the complete set of artifacts described by the TRO. Each artifact object records the hash of the artifact's content. No resource path information is included here; instead, paths to artifacts are recorded separately in [artifact locations](#artifact-arrangements-trovhasarrangement) associated with arrangements. An artifact appearing at different paths or across different workflow stages is listed once in the composition and referenced by identity wherever it appears.

```json
"trov:hasComposition": {
    "@id": "composition/1",
    "@type": "trov:ArtifactComposition",
    "trov:hasFingerprint": {
        "@id": "fingerprint",
        "@type": "trov:CompositionFingerprint",
        "trov:hash": {
            "trov:hashAlgorithm": "sha256",
            "trov:hashValue": "dd98ec1402795231d1ed39dc64336f9771411aaff6e916e3bd6f5107bf28d474"
        }
    },
    "trov:hasArtifact": [
        {
            "@id": "composition/1/artifact/0",
            "@type": "trov:ResearchArtifact",
            "trov:hash": {
                "trov:hashAlgorithm": "sha256",
                "trov:hashValue": "d0c804c3db78dbfa3d9a9206c5140f692c5f6735d2ed1f325d817a4e3bce713c"
            },
            "trov:mimeType": "text/csv"
        },
        {
            "@id": "composition/1/artifact/1",
            "@type": "trov:ResearchArtifact",
            "trov:hash": {
                "trov:hashAlgorithm": "sha256",
                "trov:hashValue": "068eeb145bad28caf162afe17344cbfa8d302036f9d275a3a10c36a49aca696a"
            },
            "trov:mimeType": "application/x-python"
        },
        {
            "@id": "composition/1/artifact/2",
            "@type": "trov:ResearchArtifact",
            "trov:hash": {
                "trov:hashAlgorithm": "sha256",
                "trov:hashValue": "fb986b83d00a50a45a52c8313d8e9f4b9963ca1cb979a18830bc8770c7106516"
            },
            "trov:mimeType": "text/csv"
        }
    ]
}
```

**Composition** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Identifier, conventionally a relative path like `"composition/1"`. |
| `@type` | string | **Yes** | Must be `"trov:ArtifactComposition"`. |
| `trov:hasFingerprint` | object | **Yes** | The composition fingerprint (see below). |
| `trov:hasArtifact` | array | **Yes** | One or more artifact objects. |

**Fingerprint** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Identifier, conventionally the relative path `"fingerprint"`. |
| `@type` | string | **Yes** | Must be `"trov:CompositionFingerprint"`. |
| `trov:hash` | object | **Yes** | Hash computed over the sorted hash values of all artifacts (see below). Contains `trov:hashAlgorithm` and `trov:hashValue`, with the algorithms and form permitted for artifacts. |

**Artifact** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Identifier, conventionally a relative path like `"composition/1/artifact/0"`. Referenced by artifact locations. |
| `@type` | string or array | **Yes** | Must be (or include) `"trov:ResearchArtifact"`. |
| `trov:hash` | object or array | **Yes** | One or more hashes of the artifact's content. Each object contains `trov:hashAlgorithm` (e.g. `"sha256"`) and `trov:hashValue`. The algorithms currently permitted are `"sha256"`, `"sha384"`, `"sha512"`, `"sha3-256"`, `"sha3-384"`, `"sha3-512"`, `"blake2b"`, `"blake2s"` and `"blake3"`. Hash values must be lowercase hexadecimal. |
| `trov:mimeType` | string | no | MIME type of the artifact, without parameters (e.g. `"text/plain"`, `"application/pdf"`, not `"text/plain; charset=utf-8"`). |

#### Computing the Composition Fingerprint

The composition fingerprint allows two TROs that describe the same set of artifacts to be identified as equivalent, regardless of arrangement or metadata differences.

**Algorithm defining the composition fingerprint:**

1. Collect all `trov:hashValue` values from every `trov:hash` object on every artifact in the composition. If an artifact has multiple hashes, all of them are included. If multiple artifacts share the same hash, it is included multiple times.
2. Sort the hash values lexicographically.
3. Concatenate the sorted values into a single string (no separator).
4. Compute the hash of the concatenated string (UTF-8 encoded). The fingerprint's hash algorithm is independent of the algorithms used to hash individual artifacts.

**Example** (Python), for a composition whose artifacts each have one or more hashes:

```python
import hashlib

def composition_fingerprint(composition):
    values = []
    for artifact in composition.artifacts:
        for artifact_hash in artifact.hashes:
            values.append(artifact_hash.value)
    joined = "".join(sorted(values))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()
```

---

(artifact-arrangements-trovhasarrangement)=
### Artifact Arrangements (`trov:hasArrangement`)

An arrangement captures where a set of artifacts were located at some point in the workflow. A simple TRO might have just two arrangements, the artifacts present before and after a single computation. In general, a performance may access several arrangements and contribute to several, and several performances may access or contribute to the same arrangement, so the arrangements of a TRO need not form a sequence.

Each arrangement contains **artifact locations** — records that place a specific artifact at a specific resource path.

```json
"trov:hasArrangement": [
    {
        "@id": "arrangement/0",
        "@type": "trov:ArtifactArrangement",
        "rdfs:comment": "Artifacts before execution",
        "trov:hasArtifactLocation": [
            {
                "@id": "arrangement/0/location/0",
                "@type": "trov:ArtifactLocation",
                "trov:artifact": { "@id": "composition/1/artifact/0" },
                "trov:path": "data/input.csv"
            },
            {
                "@id": "arrangement/0/location/1",
                "@type": "trov:ArtifactLocation",
                "trov:artifact": { "@id": "composition/1/artifact/1" },
                "trov:path": "scripts/analyze.py"
            }
        ]
    },
    {
        "@id": "arrangement/1",
        "@type": "trov:ArtifactArrangement",
        "rdfs:comment": "Artifacts after execution",
        "trov:hasArtifactLocation": [
            {
                "@id": "arrangement/1/location/0",
                "@type": "trov:ArtifactLocation",
                "trov:artifact": { "@id": "composition/1/artifact/0" },
                "trov:path": "data/input.csv"
            },
            {
                "@id": "arrangement/1/location/1",
                "@type": "trov:ArtifactLocation",
                "trov:artifact": { "@id": "composition/1/artifact/1" },
                "trov:path": "scripts/analyze.py"
            },
            {
                "@id": "arrangement/1/location/2",
                "@type": "trov:ArtifactLocation",
                "trov:artifact": { "@id": "composition/1/artifact/2" },
                "trov:path": "results/output.csv"
            }
        ]
    }
]
```

**Arrangement** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Identifier, conventionally a relative path like `"arrangement/0"`. Referenced by performances. |
| `@type` | string | **Yes** | Must be `"trov:ArtifactArrangement"`. |
| `rdfs:comment` | string | no | Human-readable description of what this arrangement represents. |
| `trov:hasArtifactLocation` | array | **Yes** | One or more artifact location objects. |

**Artifact location** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Identifier, conventionally a relative path like `"arrangement/0/location/0"`. |
| `@type` | string | **Yes** | Must be `"trov:ArtifactLocation"`. |
| `trov:artifact` | object | **Yes** | Reference to an artifact in the composition, e.g. `{ "@id": "composition/1/artifact/0" }`. |
| `trov:path` | string | **Yes** | The resource path (file path, URI, or other locator) for this artifact within this arrangement. |

> **Key concept:** The same artifact (same `@id` and content hash) can appear in multiple arrangements at different or identical paths. Conversely, when a file at a particular path has different content in different arrangements, each version is a distinct artifact in the composition.

---

### Performances (`trov:hasPerformance`)

A performance records a supervised unit of work, typically a computation executed inside the TRS. Each performance links input arrangements to output arrangements and carries transparency attributes warranted by TRS capabilities.

```json
"trov:hasPerformance": [
    {
        "@id": "trp/0",
        "@type": "trov:TrustedResearchPerformance",
        "rdfs:comment": "Execution of analysis workflow",
        "trov:wasConductedBy": { "@id": "https://trs.example.org/" },
        "trov:startedAtTime": "2024-06-15T14:00:00Z",
        "trov:endedAtTime":   "2024-06-15T14:25:00Z",
        "trov:accessedArrangement": {
            "@id": "trp/0/binding/0",
            "@type": "trov:ArrangementBinding",
            "trov:arrangement": { "@id": "arrangement/0" }
        },
        "trov:contributedToArrangement": {
            "@id": "trp/0/binding/1",
            "@type": "trov:ArrangementBinding",
            "trov:arrangement": { "@id": "arrangement/1" }
        },
        "trov:hasPerformanceAttribute": [
            {
                "@id": "trp/0/attribute/0",
                "@type": "trov:InternetIsolation",
                "trov:warrantedBy": { "@id": "https://trs.example.org/capability/internet-isolation" }
            },
            {
                "@id": "trp/0/attribute/1",
                "@type": "trov:InternetAccessRecording",
                "trov:warrantedBy": { "@id": "https://trs.example.org/capability/internet-access-recording" }
            }
        ]
    }
]
```

**Performance** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Identifier, conventionally a relative path like `"trp/0"`. |
| `@type` | string | **Yes** | Must be `"trov:TrustedResearchPerformance"`. |
| `rdfs:comment` | string | no | Human-readable description. |
| `trov:wasConductedBy` | object | **Yes** | Reference to the TRS, e.g. `{ "@id": "https://trs.example.org/" }`. |
| `trov:startedAtTime` | string (ISO 8601) | no | When the performance began, with its time zone (e.g. `Z` or `-08:00`). |
| `trov:endedAtTime` | string (ISO 8601) | no | When the performance ended, with its time zone. |
| `trov:accessedArrangement` | object or array | no | `ArrangementBinding`(s) for input arrangement(s). Each binding references an arrangement via `trov:arrangement` and optionally specifies a path via `trov:boundTo`. |
| `trov:contributedToArrangement` | object or array | no | `ArrangementBinding`(s) for output arrangement(s). Each binding references an arrangement via `trov:arrangement` and optionally specifies a path via `trov:boundTo`. |
| `trov:hasPerformanceAttribute` | array | no | Zero or more performance attribute objects. |

**Arrangement binding** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Identifier, conventionally a relative path like `"trp/0/binding/0"`. |
| `@type` | string | **Yes** | Must be `"trov:ArrangementBinding"`. |
| `trov:arrangement` | object | **Yes** | Reference to the arrangement, e.g. `{ "@id": "arrangement/0" }`. |
| `trov:boundTo` | string | no | Path where the arrangement was accessible to the TRP during execution. |

**Performance attribute** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Identifier, conventionally a relative path like `"trp/0/attribute/0"`. |
| `@type` | string | **Yes** | A performance attribute type, e.g. `"trov:InternetIsolation"`. |
| `trov:warrantedBy` | object | **Yes** | Reference to the TRS capability that justifies this claim, e.g. `{ "@id": "https://trs.example.org/capability/internet-isolation" }`. |

See [TROV Vocabulary Reference — TRP Attribute Types](trov-vocabulary.md#predefined-values-trp-attribute-types) for the defined attribute types and their required warranting capabilities.

> **Extension points:** TRS implementations can extend performances in two ways. Custom *properties* (operational metadata like architecture, resource usage, container image digests) use a TRS-specific namespace alongside the standard `trov:` properties. Custom *attribute and capability types* (new transparency claims specific to a TRS) also use the adopter's namespace and participate in the warrant chain through the standard `trov:warrantedBy` mechanism. Adopters who publish an RDF vocabulary for their custom types can declare subclass relationships to the core TROV types, enabling RDF consumers to discover them through inference. See [TROV Extension Guide](trov-extension-guide.md) for details.

---

### TRO Attributes (`trov:hasAttribute`)

TRO attributes are transparency claims about the TRO as a whole, warranted by attributes of its constituent performances.

```json
"trov:hasAttribute": [
    {
        "@id": "tro/attribute/0",
        "@type": "trov:IncludesAllInputData",
        "trov:warrantedBy": { "@id": "trp/0/attribute/0" }
    }
]
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Identifier, conventionally a relative path like `"tro/attribute/0"`. |
| `@type` | string | **Yes** | A TRO attribute type, e.g. `"trov:IncludesAllInputData"`. |
| `trov:warrantedBy` | object or array | **Yes** | Reference(s) to the TRS capability or performance attribute(s) that justify this claim. |

See [TROV Vocabulary Reference — TRO Attribute Types](trov-vocabulary.md#predefined-values-tro-attribute-types) for the defined attribute types.

---

(the-warrant-chain)=
## Warrant Chains

The warrant chain is TROV's mechanism for accountability. TROV supports declaring part or all of the chain of warranting attributes and capabilities justifying a particular transparency claim. Downstream consumers — publishers, repositories, funding agencies — may impose their own requirements on the completeness of these chains.

A TRP attribute is warranted by a TRS capability; a TRO attribute is warranted by a TRS capability, either directly or through TRP attributes. See [TROV Vocabulary Reference — The Warrant Chain](trov-vocabulary.md#the-warrant-chain-attributes-and-capabilities).

When the full chain is present, it works as follows in JSON terms:

1. A TRO attribute (in `trov:hasAttribute`) references a performance attribute by `@id`.
2. That performance attribute (in `trov:hasPerformanceAttribute`) references a TRS capability by `@id`.
3. That TRS capability (in `trov:hasCapability`) declares the TRS's ability to enforce the condition.

In this example, the TRO-level claim that all input data is included is warranted by a performance-level attribute asserting Internet isolation, which is in turn warranted by the TRS's declared capability to enforce it:

```json
"trov:hasCapability": [
    { "@id": "https://trs.example.org/capability/internet-isolation", "@type": "trov:CanProvideInternetIsolation" }
],
...
"trov:hasPerformanceAttribute": [
    {
        "@id": "trp/0/attribute/0",
        "@type": "trov:InternetIsolation",
        "trov:warrantedBy": { "@id": "https://trs.example.org/capability/internet-isolation" }
    }
],
...
"trov:hasAttribute": [
    {
        "@id": "tro/attribute/0",
        "@type": "trov:IncludesAllInputData",
        "trov:warrantedBy": { "@id": "trp/0/attribute/0" }
    }
]
```

---

(identifier-conventions)=
## Identifier Conventions

Every element of a TRO declaration that this page describes (the TRS and its capabilities, the TSA, the composition, its fingerprint and artifacts, the arrangements and their locations, the performances and their bindings, and the attributes) must be defined in the TRO declaration itself, and an `@id` referring to one must match an object defined there. Other `@id` values may name resources elsewhere.

Most `@id` values referring to other elements of the TRO can be written as relative paths, such as `"arrangement/0"`, to which the declaration's `@base` is prefixed. Without an `@base` such paths stay relative, and a consumer reading the declaration as linked data must supply a base. The TRS and its capabilities are shared across TROs, so their `@id`s are full URLs.

With an `@base` of `https://trs.example.org/tro/3f2a9c/`, the identifiers used in this page's examples become:

| Element | `@id` in the declaration | Full identifier |
|---------|--------------------------|-----------------|
| TRO | `tro` | `https://trs.example.org/tro/3f2a9c/tro` |
| Composition | `composition/1` | `https://trs.example.org/tro/3f2a9c/composition/1` |
| Artifact | `composition/1/artifact/0` | `https://trs.example.org/tro/3f2a9c/composition/1/artifact/0` |
| Arrangement | `arrangement/0` | `https://trs.example.org/tro/3f2a9c/arrangement/0` |
| Artifact location | `arrangement/0/location/0` | `https://trs.example.org/tro/3f2a9c/arrangement/0/location/0` |
| Performance | `trp/0` | `https://trs.example.org/tro/3f2a9c/trp/0` |
| Arrangement binding | `trp/0/binding/0` | `https://trs.example.org/tro/3f2a9c/trp/0/binding/0` |
| TRS | `https://trs.example.org/` | `https://trs.example.org/` (already full) |

This approach is an alternative to giving every element its own opaque identifier, such as a UUID. Uniqueness comes from one unique URI, the `@base`, together with a convention that yields suffixes unique within the declaration and easy to read. The convention is not a requirement, and tools should still treat identifiers as opaque strings, relying on cross-references rather than parsing.

---

(signing-and-timestamping)=
## Signing and Timestamping

A [TRO package](tro-packages.md) includes the declaration and one or more signing artifacts. The signing mechanism is not fixed; different TRS implementations use different approaches. What matters is that a verifier can confirm the declaration has not been altered since it was signed and, by checking the signing key or certificate against a source outside the package, that the TRS it names signed it. See [TRO Packages — Signing identity and trust](tro-packages.md#signing-identity-and-trust).

A TRO declaration states which mechanism signed it with `trov:signingMechanism`, whose value is the mechanism's TROV term, e.g. `"trov:signingMechanism": { "@id": "trov:GPGSigning" }`. The table lists the mechanisms in use today, with the TROV term for each and the files each puts in a TRO package:

| Signing mechanism | TROV term | Package contents |
|-------------------|-----------|-----------------|
| GPG detached signature | `trov:GPGSigning` | `.jsonld` declaration, `.sig` signature, `.tsr` RFC 3161 timestamp |
| X.509/CMS (PKCS #7) | `trov:X509CMSSigning` | `.jsonld` declaration, `.p7s` signature (embeds certificate and timestamp) |

---

(tro-format-verification)=
## Verification

Verifying a TRO declaration entails:

1. Using the signature to confirm that the declaration has not been altered since it was signed.
2. Confirming that the key or certificate used to sign the TRO belongs to the TRS the declaration names.
3. If the TRO was timestamped, using the timestamp to confirm that the signature existed at the claimed time.

Verification may also include:

4. Recomputing the composition fingerprint from the listed artifact hashes and confirming it matches the declared fingerprint.
5. Confirming that every artifact referenced by an arrangement is present in the composition.
6. Confirming that the capabilities of the TRS warrant the attributes declared for each TRP or the TRO.

---

(complete-example)=
## Complete Example

The following is a minimal but complete TRO declaration describing a data file and a script, a computation that reads them and produces an output, and a claim of Internet isolation.

```json
{
    "@context": {
        "rdf":    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs":   "http://www.w3.org/2000/01/rdf-schema#",
        "trov":   "https://w3id.org/trace/trov/0.1#",
        "schema": "https://schema.org/",
        "@base":  "https://trs.example.org/tro/3f2a9c/"
    },
    "@graph": [
        {
            "@id": "tro",
            "@type": "trov:TransparentResearchObject",

            "trov:vocabularyVersion": "0.1",
            "trov:signingMechanism": { "@id": "trov:GPGSigning" },

            "schema:name": "Example analysis TRO",
            "schema:description": "TRO from an analysis reading a data file and a script, producing one output",
            "schema:dateCreated": "2024-06-15T14:30:00Z",

            "trov:wasAssembledBy": {
                "@id": "https://trs.example.org/",
                "@type": ["trov:TrustedResearchSystem", "schema:Organization"],
                "schema:name": "Example TRS",
                "schema:description": "A TRS that enforces Internet isolation",
                "trov:publicKey": "-----BEGIN PGP PUBLIC KEY BLOCK-----\n...\n-----END PGP PUBLIC KEY BLOCK-----\n",
                "trov:hasCapability": [
                    {
                        "@id": "https://trs.example.org/capability/internet-isolation",
                        "@type": "trov:CanProvideInternetIsolation"
                    }
                ]
            },

            "trov:createdWith": {
                "@type": "schema:SoftwareApplication",
                "schema:name": "tro-utils",
                "schema:softwareVersion": "0.2.2"
            },

            "trov:wasTimestampedBy": {
                "@id": "tsa",
                "@type": "trov:TimeStampingAuthority",
                "trov:publicKey": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n"
            },

            "trov:hasComposition": {
                "@id": "composition/1",
                "@type": "trov:ArtifactComposition",
                "trov:hasFingerprint": {
                    "@id": "fingerprint",
                    "@type": "trov:CompositionFingerprint",
                    "trov:hash": {
                        "trov:hashAlgorithm": "sha256",
                        "trov:hashValue": "dd98ec1402795231d1ed39dc64336f9771411aaff6e916e3bd6f5107bf28d474"
                    }
                },
                "trov:hasArtifact": [
                    {
                        "@id": "composition/1/artifact/0",
                        "@type": "trov:ResearchArtifact",
                        "trov:hash": {
                            "trov:hashAlgorithm": "sha256",
                            "trov:hashValue": "d0c804c3db78dbfa3d9a9206c5140f692c5f6735d2ed1f325d817a4e3bce713c"
                        },
                        "trov:mimeType": "text/csv"
                    },
                    {
                        "@id": "composition/1/artifact/1",
                        "@type": "trov:ResearchArtifact",
                        "trov:hash": {
                            "trov:hashAlgorithm": "sha256",
                            "trov:hashValue": "068eeb145bad28caf162afe17344cbfa8d302036f9d275a3a10c36a49aca696a"
                        },
                        "trov:mimeType": "application/x-python"
                    },
                    {
                        "@id": "composition/1/artifact/2",
                        "@type": "trov:ResearchArtifact",
                        "trov:hash": {
                            "trov:hashAlgorithm": "sha256",
                            "trov:hashValue": "fb986b83d00a50a45a52c8313d8e9f4b9963ca1cb979a18830bc8770c7106516"
                        },
                        "trov:mimeType": "text/csv"
                    }
                ]
            },

            "trov:hasArrangement": [
                {
                    "@id": "arrangement/0",
                    "@type": "trov:ArtifactArrangement",
                    "rdfs:comment": "Artifacts before execution",
                    "trov:hasArtifactLocation": [
                        {
                            "@id": "arrangement/0/location/0",
                            "@type": "trov:ArtifactLocation",
                            "trov:artifact": { "@id": "composition/1/artifact/0" },
                            "trov:path": "data/input.csv"
                        },
                        {
                            "@id": "arrangement/0/location/1",
                            "@type": "trov:ArtifactLocation",
                            "trov:artifact": { "@id": "composition/1/artifact/1" },
                            "trov:path": "scripts/analyze.py"
                        }
                    ]
                },
                {
                    "@id": "arrangement/1",
                    "@type": "trov:ArtifactArrangement",
                    "rdfs:comment": "Artifacts after execution",
                    "trov:hasArtifactLocation": [
                        {
                            "@id": "arrangement/1/location/0",
                            "@type": "trov:ArtifactLocation",
                            "trov:artifact": { "@id": "composition/1/artifact/0" },
                            "trov:path": "data/input.csv"
                        },
                        {
                            "@id": "arrangement/1/location/1",
                            "@type": "trov:ArtifactLocation",
                            "trov:artifact": { "@id": "composition/1/artifact/1" },
                            "trov:path": "scripts/analyze.py"
                        },
                        {
                            "@id": "arrangement/1/location/2",
                            "@type": "trov:ArtifactLocation",
                            "trov:artifact": { "@id": "composition/1/artifact/2" },
                            "trov:path": "results/output.csv"
                        }
                    ]
                }
            ],

            "trov:hasPerformance": [
                {
                    "@id": "trp/0",
                    "@type": "trov:TrustedResearchPerformance",
                    "rdfs:comment": "Execution of analysis script",
                    "trov:wasConductedBy": { "@id": "https://trs.example.org/" },
                    "trov:startedAtTime": "2024-06-15T14:00:00Z",
                    "trov:endedAtTime":   "2024-06-15T14:25:00Z",
                    "trov:accessedArrangement": {
                        "@id": "trp/0/binding/0",
                        "@type": "trov:ArrangementBinding",
                        "trov:arrangement": { "@id": "arrangement/0" }
                    },
                    "trov:contributedToArrangement": {
                        "@id": "trp/0/binding/1",
                        "@type": "trov:ArrangementBinding",
                        "trov:arrangement": { "@id": "arrangement/1" }
                    },
                    "trov:hasPerformanceAttribute": [
                        {
                            "@id": "trp/0/attribute/0",
                            "@type": "trov:InternetIsolation",
                            "trov:warrantedBy": { "@id": "https://trs.example.org/capability/internet-isolation" }
                        }
                    ]
                }
            ],

            "trov:hasAttribute": [
                {
                    "@id": "tro/attribute/0",
                    "@type": "trov:IncludesAllInputData",
                    "trov:warrantedBy": { "@id": "trp/0/attribute/0" }
                }
            ]
        }
    ]
}
```

---

(tro-format-notes)=
## Notes

**Note 1: JSON-LD as JSON.** A TRO declaration is valid JSON. Producers can build it with any JSON library, no RDF tooling required. The `@context`, `@id`, `@type`, and `@graph` keys are the only JSON-LD-specific syntax. Everything else is standard JSON objects, arrays, and strings.

**Note 2: Why `@graph` is an array.** In 0.1, the `@graph` array contains a single object, so the array wrapper may look redundant. It is kept for two reasons: it provides future flexibility for bundling additional top-level objects (e.g. supplementary hash/algorithm pairs for artifacts, or a standalone TRS profile) without changing the core JSON Schema for the TRO itself, and it matches the default output of common JSON-LD writer libraries.

---

## History

| Date | Change |
|------|--------|
| (push date) | Aligned with tro-checks. Rewrote [Identifier Conventions](#identifier-conventions) and [Verification](#tro-format-verification) sections. |
| 2026-04-08 | Updated examples and field tables for ArrangementBinding. Fixed `schema:` prefix URI (trailing slash). |
| 2026-03-26 | Added `trov:customTerm` to TRS section with example. |
| 2026-03-22 | Made `trov:publicKey` optional for X.509/CMS signing. Added `trov:createdWith` to TRO root. |
| 2026-02-17 | Initial publication. |
