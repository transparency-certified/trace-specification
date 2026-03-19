# TRO Declaration Format
<span style="display:inline-block; padding:2px 10px;  margin-bottom:16px; background:#f0ad4e; font-weight:bold; color:black; border-radius:4px; font-size:14px;">
  TROV 0.1 DRAFT</span>

*This document is a draft and subject to revision.
Please [submit feedback or report issues](https://github.com/transparency-certified/trace-specification/issues/new?title=tro-declaration-format.md:%20).*

A **TRO Declaration** is a JSON-LD document that describes a Transparent Research Object. It records which digital artifacts were involved in a computational workflow, how they were arranged at each stage, what performances (supervised computations) were conducted, and what transparency claims are warranted about the whole process.

| Document Section | Description |
|---------|-------------|
| [Overview](#overview) | What a TRO declaration contains at a high level |
| [Document Structure](#document-structure) | The `@context`, `@graph`, and namespace prefixes |
| [The TRO Object](#the-tro-object) | TRS, compositions, arrangements, artifacts, locations, performances |
| [The Warrant Chain](#the-warrant-chain) | How performance (TRP) attributes link back to TRS capabilities |
| [Identifier Conventions](#identifier-conventions) | `@id` patterns for TRS, performance, arrangement, and artifact nodes |
| [Signing and Timestamping](#signing-and-timestamping) | GPG and X.509/CMS signing, timestamp authorities |
| [Verification](#verification) | What verifying a TRO declaration may involve |
| [Complete Example](#complete-example) | A full annotated TRO declaration |
| [Notes](#notes) | JSON-LD conventions, design rationale, known limitations |

For definitions of the vocabulary terms used here, see the [TROV Vocabulary Reference](trov-vocabulary.md). For the conceptual background, see the [TRACE Conceptual Model](conceptual-model.md). For the design rationale behind the JSON-LD format, see [TRO Declaration Design](tro-declaration-design.md).

---

## Overview

A TRO declaration is a single JSON-LD file (conventionally `*.jsonld`) containing:

1. A **`@context`** block that maps short term names to full URIs.
2. A **`@graph`** array containing a single TRO object with all of its nested components. (See [Note 2](#notes) for why an array.)

The TRO object itself contains:

- **Identity and metadata** — who created it and when.
- **TRS description** — the Trusted Research System that assembled and signed the TRO, including the TRS's declared capabilities and signing identity.
- **Composition** — the complete set of research artifacts, each identified by a content hash. Includes a composition fingerprint for identifying equivalent compositions.
- **Arrangements** — named snapshots showing where artifacts were located at specific points in the workflow.
- **Performances** — records of supervised computations, each linking input arrangements to output arrangements, with transparency attributes warranted by TRS capabilities.
- **TRO attributes** — transparency claims about the TRO as a whole, warranted by performance (TRP) attributes.

Optionally, the TRO is accompanied by:

- A **detached signature** — a cryptographic signature over the declaration (e.g. GPG `.sig` or X.509/CMS `.p7s`).
- A **timestamp** — proof of when the signature was created (e.g. a separate RFC 3161 `.tsr` file, or embedded in the `.p7s`).

---

## Document Structure

### Top-Level Envelope

```json
{
    "@context": [ ... ],
    "@graph": [ { /* single TRO object */ } ]
}
```

The `@context` maps short property names (like `trov:hash`) to full URIs. In 0.1, the `@graph` array contains a single object — the TRO declaration itself (see [Note 2](#notes) for why it is an array).

### The `@context` Block

```json
"@context": [
    {
        "rdf":    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs":   "http://www.w3.org/2000/01/rdf-schema#",
        "trov":   "https://w3id.org/trace/trov/0.1#",
        "schema": "https://schema.org"
    }
]
```

The context defines four namespace prefixes:

| Prefix | Namespace | Purpose |
|--------|-----------|---------|
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | RDF type system |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | Labels and comments |
| `trov:` | `https://w3id.org/trace/trov/0.1#` | All TROV terms |
| `schema:` | `https://schema.org` | Standard metadata (name, description, dates) |

The mandatory parts of a TRO declaration depend only on TROV and the foundational `rdf:` and `rdfs:` namespaces. The `schema:` prefix is a convenience for common metadata — it may be omitted if no `schema:` properties are used, and no TRACE-compliant tool may reject a TRO declaration for missing `schema:` properties. Conversely, consumers of TROs — especially those curating triples extracted from TRO declarations — are free to discard non-TROV triples (e.g. `schema:` properties) to avoid undesired inferences that would result from importing large external ontologies.

> From the JSON perspective, the `@context` is boilerplate copied into every TRO declaration, and everything after the `@context` is ordinary JSON. See [TRO Declaration Design](tro-declaration-design.md) for background.

---

## The TRO Object

In 0.1, the single object in the `@graph` array is the TRO itself.

### Root Properties

Example root properties:

```json
{
    "@id": "tro",
    "@type": ["trov:TransparentResearchObject", "schema:CreativeWork"],
    "trov:vocabularyVersion": "0.1",
    "schema:creator":     "SIVACOR",
    "schema:name":        "Example TRO",
    "schema:description": "TRO produced by an example workflow",
    "schema:dateCreated": "2024-06-15T14:30:00",

    "trov:wasAssembledBy":  { ... },
    "trov:hasComposition":  { ... },
    "trov:hasArrangement":  [ ... ],
    "trov:hasPerformance":  [ ... ],
    "trov:hasAttribute":    [ ... ]
}
```

The `schema:` properties shown above are optional metadata. See [The `@context` Block](#the-context-block) for the dependency boundary.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Local identifier for the TRO within this document. Conventionally `"tro"`. |
| `@type` | string or array | **Yes** | Must include `"trov:TransparentResearchObject"`. May optionally include `"schema:CreativeWork"` to make the TRO discoverable by schema.org-aware tools (not required for using `schema:` properties). |
| `trov:vocabularyVersion` | string | **Yes** | The TROV vocabulary version this declaration conforms to, e.g. `"0.1"`. |
| `schema:creator` | string | no | Name of the agent or system that created this TRO declaration. |
| `schema:name` | string | no | Short title for the TRO. |
| `schema:description` | string | no | Human-readable description. |
| `schema:dateCreated` | string (ISO 8601) | no | When the TRO declaration was created. |
| `trov:wasAssembledBy` | object | **Yes** | The TRS that produced and signed this TRO. |
| `trov:hasComposition` | object | **Yes** | The artifact composition. |
| `trov:hasArrangement` | array | **Yes** | One or more artifact arrangements. |
| `trov:hasPerformance` | array | no | Zero or more performance records. |
| `trov:hasAttribute` | array | no | Zero or more TRO-level transparency attributes. |

---

### TRS Description (`trov:wasAssembledBy`)

The TRS block identifies the Trusted Research System that supervised the workflow and signed the TRO. It includes the TRS's declared capabilities and signing identity.

Example TRS description:

```json
"trov:wasAssembledBy": {
    "@id": "trs",
    "@type": ["trov:TrustedResearchSystem", "schema:Organization"],
    "schema:name":        "SIVACOR",
    "schema:description": "Secure Interactive Virtual Appliance ...",
    "trov:publicKey": "...",
    "trov:hasCapability": [
        {
            "@id": "trs/capability/0",
            "@type": "trov:CanProvideInternetIsolation"
        },
        {
            "@id": "trs/capability/1",
            "@type": "trov:CanRecordInternetAccess"
        }
    ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Local identifier. Conventionally `"trs"`. |
| `@type` | string or array | **Yes** | Must include `"trov:TrustedResearchSystem"`. |
| `trov:publicKey` | string | **Yes** | Signing identity of the TRS (e.g. GPG public key, X.509 certificate). Representation under review for 0.1. |
| `trov:hasCapability` | array | no | Zero or more capability declarations. |
| `schema:name` | string | no | Short name for the TRS. |
| `schema:description` | string | no | Human-readable description of the TRS. |

Each **capability** object declares that the TRS is able to enforce a specific transparency condition:

| Field | Type | Description |
|-------|------|-------------|
| `@id` | string | Local identifier, e.g. `"trs/capability/0"`. Referenced by performance attributes. |
| `@type` | string | A capability type from the TROV vocabulary, e.g. `"trov:CanProvideInternetIsolation"`. |

See [TROV Vocabulary Reference — TRS Capability Types](trov-vocabulary.md#named-individuals-trs-capability-types) for the full list of defined capability types.

---

### Timestamping Authority (`trov:wasTimestampedBy`)

If the TRS obtained an RFC 3161 timestamp for the TRO signature from a separate timestamping authority, the TSA is recorded as a property of the TRO root object (a sibling of `trov:wasAssembledBy`). Not all signing mechanisms require this — X.509/CMS signatures can embed the timestamp directly in the `.p7s` file, making a separate TSA block unnecessary.

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
| `@id` | string | **Yes** | Local identifier. Conventionally `"tsa"`. |
| `@type` | string | **Yes** | Must be `"trov:TimeStampingAuthority"`. |
| `trov:publicKey` | string | **Yes** | Public key of the timestamping authority. |

---

### Artifact Composition (`trov:hasComposition`)

The composition is the complete, deduplicated set of all artifacts described by the TRO. Each artifact is identified solely by its content hash, and artifact objects carry no resource path information. Paths are recorded separately in [artifact locations](#artifact-arrangements-trovhasarrangement). An artifact appearing at different paths — or across different workflow stages — is listed once in the composition and referenced by identity wherever it appears.

```json
"trov:hasComposition": {
    "@id": "composition/1",
    "@type": "trov:ArtifactComposition",
    "trov:hasFingerprint": {
        "@id": "fingerprint",
        "@type": "trov:CompositionFingerprint",
        "trov:hash": { "trov:hashAlgorithm": "sha256", "trov:hashValue": "218d9c33..." }
    },
    "trov:hasArtifact": [
        {
            "@id": "composition/1/artifact/0",
            "@type": "trov:ResearchArtifact",
            "trov:hash": { "trov:hashAlgorithm": "sha256", "trov:hashValue": "b5bb9d80..." },
            "trov:mimeType": "text/plain"
        },
        {
            "@id": "composition/1/artifact/1",
            "@type": "trov:ResearchArtifact",
            "trov:hash": { "trov:hashAlgorithm": "sha256", "trov:hashValue": "7d865e95..." },
            "trov:mimeType": "application/x-python"
        }
    ]
}
```

**Composition** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Local identifier. Conventionally `"composition/1"`. |
| `@type` | string | **Yes** | Must be `"trov:ArtifactComposition"`. |
| `trov:hasFingerprint` | object | **Yes** | The composition fingerprint (see below). |
| `trov:hasArtifact` | array | **Yes** | One or more artifact objects. |

**Fingerprint** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Local identifier. Conventionally `"fingerprint"`. |
| `@type` | string | **Yes** | Must be `"trov:CompositionFingerprint"`. |
| `trov:hash` | object | **Yes** | Hash computed over the sorted hash values of all artifacts (see below). Contains `trov:hashAlgorithm` and `trov:hashValue`. |

**Artifact** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Local identifier, e.g. `"composition/1/artifact/0"`. Referenced by artifact locations. |
| `@type` | string | **Yes** | Must be `"trov:ResearchArtifact"`. |
| `trov:hash` | object or array | **Yes** | One or more hashes of the artifact's content. Each object contains `trov:hashAlgorithm` (e.g. `"sha256"`) and `trov:hashValue`. |
| `trov:mimeType` | string | no | MIME type of the artifact (e.g. `"text/plain"`, `"application/pdf"`). |

#### Computing the Composition Fingerprint

The composition fingerprint allows two TROs that describe the same set of artifacts to be identified as equivalent, regardless of arrangement or metadata differences.

**Algorithm:**

1. Collect all `trov:hashValue` values from every `trov:hash` object on every artifact in the composition. If an artifact has multiple hashes, all of them are included.
2. Sort the hash values lexicographically.
3. Concatenate the sorted values into a single string (no separator).
4. Compute the hash of the concatenated string (UTF-8 encoded). The fingerprint's hash algorithm is independent of the algorithms used to hash individual artifacts.

**Example** (Python):

```python
import hashlib

def collect_hash_values(artifact):
    h = artifact["trov:hash"]
    if isinstance(h, list):
        return [entry["trov:hashValue"] for entry in h]
    return [h["trov:hashValue"]]

all_hashes = sorted(v for art in composition["trov:hasArtifact"] for v in collect_hash_values(art))
fingerprint = hashlib.sha256("".join(all_hashes).encode("utf-8")).hexdigest()
```

---

### Artifact Arrangements (`trov:hasArrangement`)

An arrangement captures where artifacts were located at a specific point in the workflow. A simple TRO might have just two arrangements — the artifacts present before and after a single computation — but multi-step workflows can have many, with intermediate arrangements shared between performances.

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
| `@id` | string | **Yes** | Local identifier, e.g. `"arrangement/0"`. Referenced by performances. |
| `@type` | string | **Yes** | Must be `"trov:ArtifactArrangement"`. |
| `rdfs:comment` | string | no | Human-readable description of what this arrangement represents. |
| `trov:hasArtifactLocation` | array | **Yes** | One or more artifact location objects. |

**Artifact location** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Local identifier, e.g. `"arrangement/0/location/0"`. |
| `@type` | string | **Yes** | Must be `"trov:ArtifactLocation"`. |
| `trov:artifact` | object | **Yes** | Reference to an artifact in the composition, e.g. `{ "@id": "composition/1/artifact/0" }`. |
| `trov:path` | string | **Yes** | The resource path (file path, URI, or other locator) for this artifact within this arrangement. |

> **Key concept:** The same artifact (same `@id` and content hash) can appear in multiple arrangements at different or identical paths. Conversely, different content at the same path across arrangements represents the file changing between workflow stages.

---

### Performances (`trov:hasPerformance`)

A performance records a supervised unit of work — typically a computation executed inside the TRS. Each performance links input arrangements to output arrangements and carries transparency attributes warranted by TRS capabilities.

```json
"trov:hasPerformance": [
    {
        "@id": "trp/0",
        "@type": "trov:TrustedResearchPerformance",
        "rdfs:comment": "Execution of analysis workflow",
        "trov:wasConductedBy": { "@id": "trs" },
        "trov:startedAtTime": "2024-06-15T14:00:00",
        "trov:endedAtTime":   "2024-06-15T14:25:00",
        "trov:accessedArrangement":       { "@id": "arrangement/0" },
        "trov:contributedToArrangement":  { "@id": "arrangement/1" },
        "trov:hasPerformanceAttribute": [
            {
                "@id": "trp/0/attribute/0",
                "@type": "trov:InternetIsolation",
                "trov:warrantedBy": { "@id": "trs/capability/0" }
            },
            {
                "@id": "trp/0/attribute/1",
                "@type": "trov:InternetAccessRecording",
                "trov:warrantedBy": { "@id": "trs/capability/1" }
            }
        ]
    }
]
```

**Performance** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Local identifier, e.g. `"trp/0"`. |
| `@type` | string | **Yes** | Must be `"trov:TrustedResearchPerformance"`. |
| `rdfs:comment` | string | no | Human-readable description. |
| `trov:wasConductedBy` | object | **Yes** | Reference to the TRS, e.g. `{ "@id": "trs" }`. |
| `trov:startedAtTime` | string (ISO 8601) | no | When the performance began. |
| `trov:endedAtTime` | string (ISO 8601) | no | When the performance ended. |
| `trov:accessedArrangement` | object or array | no | Reference(s) to input arrangement(s). A single arrangement may be a plain object reference; multiple arrangements use an array. |
| `trov:contributedToArrangement` | object or array | no | Reference(s) to output arrangement(s). A single arrangement may be a plain object reference; multiple arrangements use an array. |
| `trov:hasPerformanceAttribute` | array | no | Zero or more performance attribute objects. |

**Performance attribute** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | **Yes** | Local identifier, e.g. `"trp/0/attribute/0"`. |
| `@type` | string | **Yes** | A performance attribute type, e.g. `"trov:InternetIsolation"`. |
| `trov:warrantedBy` | object | **Yes** | Reference to the TRS capability that justifies this claim, e.g. `{ "@id": "trs/capability/0" }`. |

See [TROV Vocabulary Reference — TRP Attribute Types](trov-vocabulary.md#named-individuals-trp-attribute-types) for the defined attribute types and their required warranting capabilities.

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
| `@id` | string | **Yes** | Local identifier, e.g. `"tro/attribute/0"`. |
| `@type` | string | **Yes** | A TRO attribute type, e.g. `"trov:IncludesAllInputData"`. |
| `trov:warrantedBy` | object or array | **Yes** | Reference(s) to the performance attribute(s) that justify this claim. |

See [TROV Vocabulary Reference — TRO Attribute Types](trov-vocabulary.md#named-individuals-tro-attribute-types) for the defined attribute types.

---

## The Warrant Chain

The warrant chain is TROV's mechanism for accountability. TROV supports declaring part or all of the chain of warranting attributes and capabilities justifying a particular transparency claim. Downstream consumers — publishers, repositories, funding agencies — may impose their own requirements on the completeness of these chains.

```
TRO attribute    →  trov:warrantedBy  →  Performance attribute
                                           →  trov:warrantedBy  →  TRS capability
```

When the full chain is present, it works as follows in JSON terms:

1. A TRO attribute (in `trov:hasAttribute`) references a performance attribute by `@id`.
2. That performance attribute (in `trov:hasPerformanceAttribute`) references a TRS capability by `@id`.
3. That TRS capability (in `trov:hasCapability`) declares the TRS's ability to enforce the condition.

In this example, the TRO-level claim that all input data is included is warranted by a performance-level attribute asserting Internet isolation, which is in turn warranted by the TRS's declared capability to enforce it:

```json
"trov:hasCapability": [
    { "@id": "trs/capability/0", "@type": "trov:CanProvideInternetIsolation" }
],
...
"trov:hasPerformanceAttribute": [
    {
        "@id": "trp/0/attribute/0",
        "@type": "trov:InternetIsolation",
        "trov:warrantedBy": { "@id": "trs/capability/0" }
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

## Identifier Conventions

All `@id` values are local to the document. They are used for cross-referencing between objects within the same TRO declaration. The conventions used by tro-utils are:

| Object | Pattern | Examples |
|--------|---------|----------|
| TRO | `tro` | `"tro"` |
| TRS | `trs` | `"trs"` |
| TSA | `tsa` | `"tsa"` |
| Composition | `composition/{n}` | `"composition/1"` |
| Fingerprint | `fingerprint` | `"fingerprint"` |
| Artifact | `composition/{n}/artifact/{i}` | `"composition/1/artifact/0"` |
| Arrangement | `arrangement/{i}` | `"arrangement/0"` |
| Artifact location | `arrangement/{i}/location/{j}` | `"arrangement/0/location/0"` |
| TRS capability | `trs/capability/{i}` | `"trs/capability/0"` |
| Performance | `trp/{i}` | `"trp/0"` |
| Performance attribute | `trp/{i}/attribute/{j}` | `"trp/0/attribute/0"` |
| TRO attribute | `tro/attribute/{i}` | `"tro/attribute/0"` |

> **Note:** These identifier patterns are conventions, not requirements. The important thing is internal consistency: every `@id` referenced by another object must match a defined `@id` within the document. Tools should treat identifiers as opaque strings and rely on cross-references, not string parsing.

---

## Signing and Timestamping

A TRO package includes the declaration and one or more signing artifacts. The signing mechanism is not fixed — different TRS implementations use different approaches. What matters is that the signature can be verified against the public key or certificate recorded in the TRO declaration.

**Current implementations:**

| Signing mechanism | Package contents |
|-------------------|-----------------|
| GPG detached signature | `.jsonld` declaration, `.sig` signature, `.tsr` RFC 3161 timestamp |
| X.509/CMS (PKCS #7) | `.jsonld` declaration, `.p7s` signature (embeds certificate and timestamp) |

The signature covers the declaration file byte-for-byte. In the reference implementation (tro-utils), the declaration is serialized with `json.dumps(data, indent=2, sort_keys=True)` to ensure a deterministic byte sequence. The signature is a separate file, not embedded in the JSON.

---

## Verification

Verification of a TRO declaration may include:

1. Verifying that the signature on the declaration file matches the public key or certificate in the TRO declaration.
2. Optionally verifying that the timestamp proves the signature existed at the claimed time.
3. Recomputing the composition fingerprint from the listed artifact hashes and confirming it matches the declared fingerprint.
4. Confirming that every artifact referenced by an arrangement is present in the composition.
5. Tracing the warrant chain: confirming that each `trov:warrantedBy` reference resolves to an object of the expected type.

---

## Complete Example

The following is a minimal but complete TRO declaration describing a data file and a script, a computation that reads them and produces an output, and a claim of Internet isolation.

```json
{
    "@context": [
        {
            "rdf":    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs":   "http://www.w3.org/2000/01/rdf-schema#",
            "trov":   "https://w3id.org/trace/trov/0.1#",
            "schema": "https://schema.org"
        }
    ],
    "@graph": [
        {
            "@id": "tro",
            "@type": ["trov:TransparentResearchObject", "schema:CreativeWork"],
            "trov:vocabularyVersion": "0.1",
            "schema:name": "Example analysis TRO",
            "schema:description": "TRO from an analysis reading a data file and a script, producing one output",
            "schema:dateCreated": "2024-06-15T14:30:00",

            "trov:wasAssembledBy": {
                "@id": "trs",
                "@type": ["trov:TrustedResearchSystem", "schema:Organization"],
                "schema:name": "Example TRS",
                "schema:description": "A TRS that enforces Internet isolation",
                "trov:publicKey": "-----BEGIN PGP PUBLIC KEY BLOCK-----\n...\n-----END PGP PUBLIC KEY BLOCK-----\n",
                "trov:hasCapability": [
                    {
                        "@id": "trs/capability/0",
                        "@type": "trov:CanProvideInternetIsolation"
                    }
                ]
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
                    "trov:hash": { "trov:hashAlgorithm": "sha256", "trov:hashValue": "a1b2c3d4..." }
                },
                "trov:hasArtifact": [
                    {
                        "@id": "composition/1/artifact/0",
                        "@type": "trov:ResearchArtifact",
                        "trov:hash": { "trov:hashAlgorithm": "sha256", "trov:hashValue": "aaa1..." },
                        "trov:mimeType": "text/csv"
                    },
                    {
                        "@id": "composition/1/artifact/1",
                        "@type": "trov:ResearchArtifact",
                        "trov:hash": { "trov:hashAlgorithm": "sha256", "trov:hashValue": "bbb2..." },
                        "trov:mimeType": "application/x-python"
                    },
                    {
                        "@id": "composition/1/artifact/2",
                        "@type": "trov:ResearchArtifact",
                        "trov:hash": { "trov:hashAlgorithm": "sha256", "trov:hashValue": "ccc3..." },
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
                    "trov:wasConductedBy": { "@id": "trs" },
                    "trov:startedAtTime": "2024-06-15T14:00:00",
                    "trov:endedAtTime":   "2024-06-15T14:25:00",
                    "trov:accessedArrangement":      { "@id": "arrangement/0" },
                    "trov:contributedToArrangement": { "@id": "arrangement/1" },
                    "trov:hasPerformanceAttribute": [
                        {
                            "@id": "trp/0/attribute/0",
                            "@type": "trov:InternetIsolation",
                            "trov:warrantedBy": { "@id": "trs/capability/0" }
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

## Notes

**Note 1: JSON-LD as JSON.** A TRO declaration is valid JSON. Producers can build it with any JSON library, no RDF tooling required. The `@context`, `@id`, `@type`, and `@graph` keys are the only JSON-LD-specific syntax. Everything else is standard JSON objects, arrays, and strings.

**Note 2: Why `@graph` is an array.** In 0.1, the `@graph` array contains a single object, so the array wrapper may look redundant. It is kept for two reasons: it provides future flexibility for bundling additional top-level objects (e.g. supplementary hash/algorithm pairs for artifacts, or a standalone TRS profile) without changing the core JSON Schema for the TRO itself, and it matches the default output of common JSON-LD writer libraries.

**Note 3: Multiple performances.** A TRO may describe a multi-step workflow with multiple performances. Each performance links its own input and output arrangements. Arrangements may be shared: one performance's output arrangement can be another performance's input arrangement.

**Note 4: Arrangement ordering.** Arrangements are not explicitly ordered in the JSON array. The relationships between arrangements are expressed through the performances: `trov:accessedArrangement` identifies arrangements a performance read from, and `trov:contributedToArrangement` identifies arrangements it wrote to.
