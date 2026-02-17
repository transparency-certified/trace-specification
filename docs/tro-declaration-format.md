# TRO Declaration Format

A **TRO Declaration** is a JSON-LD document that describes a Transparent Research Object. It records which digital artifacts were involved in a computational workflow, how they were arranged at each stage, what performances (supervised computations) were conducted, and what transparency claims are warranted about the whole process.

This document specifies the structure of a TRO declaration as JSON. For definitions of the vocabulary terms used here, see the [TROV Vocabulary Reference](trov-vocabulary.md). For the conceptual background, see the [TRACE Conceptual Model](conceptual-model.md).

---

## Overview

A TRO declaration is a single JSON file (conventionally `*.jsonld`) containing:

1. A **`@context`** block that maps short term names to full URIs.
2. A **`@graph`** array containing a single TRO object with all of its nested components.

The TRO object itself contains:

- **Identity and metadata** — who created it and when.
- **TRS reference** — the Trusted Research System that assembled and signed the TRO, including its declared capabilities and public key.
- **Composition** — the complete set of research artifacts, each identified by a SHA-256 content digest. Includes a composition fingerprint for identifying equivalent compositions.
- **Arrangements** — named snapshots showing where artifacts were located at specific points in the workflow.
- **Performances** — records of supervised computations, each linking an input arrangement to an output arrangement, with transparency attributes warranted by TRS capabilities.
- **TRO attributes** — transparency claims about the TRO as a whole, warranted by performance attributes.

Optionally, the TRO is accompanied by:

- A **detached signature** (`*.sig`) — a GPG signature over the declaration.
- A **timestamp response** (`*.tsr`) — an RFC 3161 timestamp proving when the signature was created.

---

## Document Structure

### Top-Level Envelope

```json
{
    "@context": [ ... ],
    "@graph": [ { /* single TRO object */ } ]
}
```

The `@context` maps short property names (like `trov:sha256`) to full URIs. The `@graph` array always contains exactly one object: the TRO.

### The `@context` Block

```json
"@context": [
    {
        "rdf":    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs":   "http://www.w3.org/2000/01/rdf-schema#",
        "trov":   "https://w3id.org/trace/2023/05/trov#",
        "schema": "https://schema.org"
    }
]
```

The context defines four namespace prefixes:

| Prefix | Namespace | Purpose |
|--------|-----------|---------|
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | RDF type system |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | Labels and comments |
| `trov:` | `https://w3id.org/trace/2023/05/trov#` | All TROV terms |
| `schema:` | `https://schema.org` | Standard metadata (name, description, dates) |

> **For JSON developers:** The `@context` is boilerplate. Copy it as-is into every TRO declaration. It exists so that downstream tools can interpret the document as linked data, but you never need to resolve or fetch it at runtime. Everything after the `@context` is ordinary JSON.

---

## The TRO Object

The single object in the `@graph` array is the TRO itself.

### Root Properties

```json
{
    "@id": "tro",
    "@type": ["trov:TransparentResearchObject", "schema:CreativeWork"],
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

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | Yes | Local identifier for the TRO within this document. Conventionally `"tro"`. |
| `@type` | string or array | Yes | Must include `"trov:TransparentResearchObject"`. May also include `"schema:CreativeWork"`. |
| `schema:creator` | string | No | Name of the agent or system that created this TRO declaration. |
| `schema:name` | string | No | Short title for the TRO. |
| `schema:description` | string | No | Human-readable description. |
| `schema:dateCreated` | string (ISO 8601) | No | When the TRO declaration was created. |
| `trov:wasAssembledBy` | object | Yes | The TRS that produced and signed this TRO. |
| `trov:hasComposition` | object | Yes | The artifact composition. |
| `trov:hasArrangement` | array | Yes | One or more artifact arrangements. |
| `trov:hasPerformance` | array | No | Zero or more performance records. |
| `trov:hasAttribute` | array | No | Zero or more TRO-level transparency attributes. |

---

### TRS Reference (`trov:wasAssembledBy`)

The TRS block identifies the Trusted Research System that supervised the workflow and signed the TRO. It includes the TRS's declared capabilities and public key.

```json
"trov:wasAssembledBy": {
    "@id": "trs",
    "@type": ["trov:TrustedResearchSystem", "schema:Organization"],
    "schema:name":        "SIVACOR",
    "schema:description": "Secure Interactive Virtual Appliance ...",
    "trov:publicKey": "-----BEGIN PGP PUBLIC KEY BLOCK-----\n...\n-----END PGP PUBLIC KEY BLOCK-----\n",
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
| `@id` | string | Yes | Local identifier. Conventionally `"trs"`. |
| `@type` | string or array | Yes | Must include `"trov:TrustedResearchSystem"`. |
| `trov:publicKey` | string | Yes | ASCII-armored GPG public key of the TRS signing key. |
| `trov:hasCapability` | array | No | Zero or more capability declarations. |
| `schema:name` | string | No | Short name for the TRS. |
| `schema:description` | string | No | Human-readable description of the TRS. |

Each **capability** object declares that the TRS is able to enforce a specific transparency condition:

| Field | Type | Description |
|-------|------|-------------|
| `@id` | string | Local identifier, e.g. `"trs/capability/0"`. Referenced by performance attributes. |
| `@type` | string | A capability type from the TROV vocabulary, e.g. `"trov:CanProvideInternetIsolation"`. |

See [TROV Vocabulary Reference — TRS Capability Types](trov-vocabulary.md#named-individuals-trs-capability-types) for the full list of defined capability types.

---

### Timestamping Authority (`trov:wasTimestampedBy`)

If the TRS obtained an RFC 3161 timestamp for the TRO signature, the TSA is recorded here.

```json
"trov:wasTimestampedBy": {
    "@id": "tsa",
    "@type": "trov:TimeStampingAuthority",
    "trov:publicKey": "-----BEGIN PGP PUBLIC KEY BLOCK-----\n...\n-----END PGP PUBLIC KEY BLOCK-----\n"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | Yes | Local identifier. Conventionally `"tsa"`. |
| `@type` | string | Yes | Must be `"trov:TimeStampingAuthority"`. |
| `trov:publicKey` | string | Yes | Public key of the timestamping authority. |

---

### Artifact Composition (`trov:hasComposition`)

The composition is the complete, deduplicated set of all artifacts described by the TRO. Each artifact is identified by its SHA-256 content digest, not by its file path. The same artifact appearing at different paths in different arrangements is listed once in the composition.

```json
"trov:hasComposition": {
    "@id": "composition/1",
    "@type": "trov:ArtifactComposition",
    "trov:hasFingerprint": {
        "@id": "fingerprint",
        "@type": "trov:CompositionFingerprint",
        "trov:sha256": "218d9c33959c89013ca3f0f9dfa9479e0df8d5e4a53bb319b5bfab87f506dadc"
    },
    "trov:hasArtifact": [
        {
            "@id": "composition/1/artifact/0",
            "@type": "trov:ResearchArtifact",
            "trov:sha256": "b5bb9d8014a0f9b1d61e21e796d78dccdf1352f23cd32812f4850b878ae4944c",
            "trov:mimeType": "text/plain"
        },
        {
            "@id": "composition/1/artifact/1",
            "@type": "trov:ResearchArtifact",
            "trov:sha256": "7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730",
            "trov:mimeType": "application/x-python"
        }
    ]
}
```

**Composition** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | Yes | Local identifier. Conventionally `"composition/1"`. |
| `@type` | string | Yes | Must be `"trov:ArtifactComposition"`. |
| `trov:hasFingerprint` | object | Yes | The composition fingerprint (see below). |
| `trov:hasArtifact` | array | Yes | One or more artifact objects. |

**Fingerprint** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | Yes | Local identifier. Conventionally `"fingerprint"`. |
| `@type` | string | Yes | Must be `"trov:CompositionFingerprint"`. |
| `trov:sha256` | string | Yes | SHA-256 digest computed over the sorted SHA-256 digests of all artifacts (see below). |

**Artifact** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | Yes | Local identifier, e.g. `"composition/1/artifact/0"`. Referenced by loci. |
| `@type` | string | Yes | Must be `"trov:ResearchArtifact"`. |
| `trov:sha256` | string | Yes | SHA-256 digest of the artifact's content. |
| `trov:mimeType` | string | No | MIME type of the artifact (e.g. `"text/plain"`, `"application/pdf"`). |

#### Computing the Composition Fingerprint

The composition fingerprint allows two TROs that describe the same set of artifacts to be identified as equivalent, regardless of arrangement or metadata differences.

**Algorithm:**

1. Collect the `trov:sha256` value of every artifact in the composition.
2. Sort the digests lexicographically.
3. Concatenate the sorted digests into a single string (no separator).
4. Compute the SHA-256 digest of that string (UTF-8 encoded).

**Example** (Python):

```python
import hashlib

artifact_hashes = [art["trov:sha256"] for art in composition["trov:hasArtifact"]]
fingerprint = hashlib.sha256(
    "".join(sorted(artifact_hashes)).encode("utf-8")
).hexdigest()
```

---

### Artifact Arrangements (`trov:hasArrangement`)

An arrangement captures where artifacts were located at a specific point in the workflow. A typical TRO has at least two arrangements: one for the inputs before a computation and one for the outputs after.

Each arrangement contains **loci** — records that place a specific artifact at a specific resource path.

```json
"trov:hasArrangement": [
    {
        "@id": "arrangement/0",
        "@type": "trov:ArtifactArrangement",
        "rdfs:comment": "Input files before execution",
        "trov:hasLocus": [
            {
                "@id": "arrangement/0/locus/0",
                "@type": "trov:ArtifactLocus",
                "trov:hasArtifact": { "@id": "composition/1/artifact/0" },
                "trov:hasLocation": "data/input.csv"
            },
            {
                "@id": "arrangement/0/locus/1",
                "@type": "trov:ArtifactLocus",
                "trov:hasArtifact": { "@id": "composition/1/artifact/1" },
                "trov:hasLocation": "scripts/analyze.py"
            }
        ]
    },
    {
        "@id": "arrangement/1",
        "@type": "trov:ArtifactArrangement",
        "rdfs:comment": "Output files after execution",
        "trov:hasLocus": [
            {
                "@id": "arrangement/1/locus/0",
                "@type": "trov:ArtifactLocus",
                "trov:hasArtifact": { "@id": "composition/1/artifact/0" },
                "trov:hasLocation": "data/input.csv"
            },
            {
                "@id": "arrangement/1/locus/1",
                "@type": "trov:ArtifactLocus",
                "trov:hasArtifact": { "@id": "composition/1/artifact/1" },
                "trov:hasLocation": "scripts/analyze.py"
            }
        ]
    }
]
```

**Arrangement** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | Yes | Local identifier, e.g. `"arrangement/0"`. Referenced by performances. |
| `@type` | string | Yes | Must be `"trov:ArtifactArrangement"`. |
| `rdfs:comment` | string | No | Human-readable description of what this arrangement represents. |
| `trov:hasLocus` | array | Yes | One or more locus objects. |

**Locus** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | Yes | Local identifier, e.g. `"arrangement/0/locus/0"`. |
| `@type` | string | Yes | Must be `"trov:ArtifactLocus"`. |
| `trov:hasArtifact` | object | Yes | Reference to an artifact in the composition, e.g. `{ "@id": "composition/1/artifact/0" }`. |
| `trov:hasLocation` | string | Yes | The resource path (file path, URI, or other locator) for this artifact within this arrangement. |

> **Key concept:** The same artifact (same `@id` and SHA-256 digest) can appear in multiple arrangements at different or identical paths. This is how TROV records that an input file was present before a computation and still present (unchanged) afterward.

---

### Performances (`trov:hasPerformance`)

A performance records a supervised unit of work — typically a computation executed inside the TRS. Each performance links an input arrangement to an output arrangement and carries transparency attributes warranted by TRS capabilities.

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
| `@id` | string | Yes | Local identifier, e.g. `"trp/0"`. |
| `@type` | string | Yes | Must be `"trov:TrustedResearchPerformance"`. |
| `rdfs:comment` | string | No | Human-readable description. |
| `trov:wasConductedBy` | object | Yes | Reference to the TRS, e.g. `{ "@id": "trs" }`. |
| `trov:startedAtTime` | string (ISO 8601) | No | When the performance began. |
| `trov:endedAtTime` | string (ISO 8601) | No | When the performance ended. |
| `trov:accessedArrangement` | object | No | Reference to the input arrangement. |
| `trov:contributedToArrangement` | object | No | Reference to the output arrangement. |
| `trov:hasPerformanceAttribute` | array | No | Zero or more performance attribute objects. |

**Performance attribute** fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `@id` | string | Yes | Local identifier, e.g. `"trp/0/attribute/0"`. |
| `@type` | string | Yes | A performance attribute type, e.g. `"trov:InternetIsolation"`. |
| `trov:warrantedBy` | object | Yes | Reference to the TRS capability that justifies this claim, e.g. `{ "@id": "trs/capability/0" }`. |

See [TROV Vocabulary Reference — TRP Attribute Types](trov-vocabulary.md#named-individuals-trp-attribute-types) for the defined attribute types and their required warranting capabilities.

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
| `@id` | string | Yes | Local identifier, e.g. `"tro/attribute/0"`. |
| `@type` | string | Yes | A TRO attribute type, e.g. `"trov:IncludesAllInputData"`. |
| `trov:warrantedBy` | object or array | Yes | Reference(s) to the performance attribute(s) that justify this claim. |

See [TROV Vocabulary Reference — TRO Attribute Types](trov-vocabulary.md#named-individuals-tro-attribute-types) for the defined attribute types.

---

## The Warrant Chain

The warrant chain is the core trust mechanism of TROV. Every transparency claim about a TRO traces back through a chain of justifications to a declared TRS capability.

```
TRO attribute    →  trov:warrantedBy  →  Performance attribute
                                           →  trov:warrantedBy  →  TRS capability
```

In JSON terms, this means:

1. A TRO attribute (in `trov:hasAttribute`) references a performance attribute by `@id`.
2. That performance attribute (in `trov:hasPerformanceAttribute`) references a TRS capability by `@id`.
3. That TRS capability (in `trov:hasCapability`) declares the TRS's ability to enforce the condition.

**No transparency claim can be asserted without this chain of justification.** A performance attribute for `trov:InternetIsolation` is only valid if the TRS declares `trov:CanProvideInternetIsolation` as a capability.

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
| Locus | `arrangement/{i}/locus/{j}` | `"arrangement/0/locus/0"` |
| TRS capability | `trs/capability/{i}` | `"trs/capability/0"` |
| Performance | `trp/{i}` | `"trp/0"` |
| Performance attribute | `trp/{i}/attribute/{j}` | `"trp/0/attribute/0"` |
| TRO attribute | `tro/attribute/{i}` | `"tro/attribute/0"` |

> **Note:** These identifier patterns are conventions, not requirements. The important thing is internal consistency: every `@id` referenced by another object must match a defined `@id` within the document. Tools should treat identifiers as opaque strings and rely on cross-references, not string parsing.

---

## Signing and Timestamping

A complete TRO package consists of three files:

| File | Extension | Description |
|------|-----------|-------------|
| TRO Declaration | `.jsonld` | The JSON-LD document described in this specification. |
| TRS Signature | `.sig` | Detached GPG signature over the declaration (signed with the key whose public half appears in `trov:publicKey`). |
| Timestamp Response | `.tsr` | RFC 3161 timestamp response from a Timestamping Authority, proving when the signature was created. |

The declaration is signed as-is (serialized with `json.dumps(data, indent=2, sort_keys=True)` in the reference implementation). The signature is detached: it is a separate file, not embedded in the JSON.

**Verification** requires:

1. Checking the GPG signature against the public key in the TRO declaration.
2. Optionally checking the RFC 3161 timestamp response.
3. Validating the composition fingerprint against the listed artifacts.
4. Validating that arrangements reference only artifacts present in the composition.
5. Validating the warrant chain: every performance attribute must reference a TRS capability of the correct type.

---

## Complete Example

The following is a minimal but complete TRO declaration describing two input files, a computation that reads them and produces an output, and a claim of Internet isolation.

```json
{
    "@context": [
        {
            "rdf":    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs":   "http://www.w3.org/2000/01/rdf-schema#",
            "trov":   "https://w3id.org/trace/2023/05/trov#",
            "schema": "https://schema.org"
        }
    ],
    "@graph": [
        {
            "@id": "tro",
            "@type": ["trov:TransparentResearchObject", "schema:CreativeWork"],
            "schema:name": "Example analysis TRO",
            "schema:description": "TRO from an analysis reading two inputs and producing one output",
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

            "trov:hasComposition": {
                "@id": "composition/1",
                "@type": "trov:ArtifactComposition",
                "trov:hasFingerprint": {
                    "@id": "fingerprint",
                    "@type": "trov:CompositionFingerprint",
                    "trov:sha256": "a1b2c3d4..."
                },
                "trov:hasArtifact": [
                    {
                        "@id": "composition/1/artifact/0",
                        "@type": "trov:ResearchArtifact",
                        "trov:sha256": "aaa111...",
                        "trov:mimeType": "text/csv"
                    },
                    {
                        "@id": "composition/1/artifact/1",
                        "@type": "trov:ResearchArtifact",
                        "trov:sha256": "bbb222...",
                        "trov:mimeType": "application/x-python"
                    },
                    {
                        "@id": "composition/1/artifact/2",
                        "@type": "trov:ResearchArtifact",
                        "trov:sha256": "ccc333...",
                        "trov:mimeType": "text/csv"
                    }
                ]
            },

            "trov:hasArrangement": [
                {
                    "@id": "arrangement/0",
                    "@type": "trov:ArtifactArrangement",
                    "rdfs:comment": "Inputs before execution",
                    "trov:hasLocus": [
                        {
                            "@id": "arrangement/0/locus/0",
                            "@type": "trov:ArtifactLocus",
                            "trov:hasArtifact": { "@id": "composition/1/artifact/0" },
                            "trov:hasLocation": "data/input.csv"
                        },
                        {
                            "@id": "arrangement/0/locus/1",
                            "@type": "trov:ArtifactLocus",
                            "trov:hasArtifact": { "@id": "composition/1/artifact/1" },
                            "trov:hasLocation": "scripts/analyze.py"
                        }
                    ]
                },
                {
                    "@id": "arrangement/1",
                    "@type": "trov:ArtifactArrangement",
                    "rdfs:comment": "Outputs after execution",
                    "trov:hasLocus": [
                        {
                            "@id": "arrangement/1/locus/0",
                            "@type": "trov:ArtifactLocus",
                            "trov:hasArtifact": { "@id": "composition/1/artifact/0" },
                            "trov:hasLocation": "data/input.csv"
                        },
                        {
                            "@id": "arrangement/1/locus/1",
                            "@type": "trov:ArtifactLocus",
                            "trov:hasArtifact": { "@id": "composition/1/artifact/1" },
                            "trov:hasLocation": "scripts/analyze.py"
                        },
                        {
                            "@id": "arrangement/1/locus/2",
                            "@type": "trov:ArtifactLocus",
                            "trov:hasArtifact": { "@id": "composition/1/artifact/2" },
                            "trov:hasLocation": "results/output.csv"
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

**JSON-LD as JSON.** A TRO declaration is valid JSON. Producers can build it with any JSON library — no RDF tooling is required. The `@context`, `@id`, `@type`, and `@graph` keys are the only JSON-LD-specific syntax. Everything else is standard JSON objects, arrays, and strings.

**Content-based identity.** Artifacts are identified by SHA-256 digest, not by file path. The same content at different paths is one artifact with multiple loci. Different content at the same path across arrangements represents the file changing between workflow stages.

**Single composition per TRO.** A TRO declaration contains exactly one `trov:hasComposition`. All artifacts from all arrangements are collected into this single composition.

**Arrangement ordering.** Arrangements are not explicitly ordered in the JSON array. The temporal relationship between arrangements is expressed through performances: a performance's `trov:accessedArrangement` is the "before" state and its `trov:contributedToArrangement` is the "after" state.

**Multiple performances.** A TRO may describe a multi-step workflow with multiple performances. Each performance links its own input and output arrangements. Arrangements may be shared: one performance's output arrangement can be another performance's input arrangement.
