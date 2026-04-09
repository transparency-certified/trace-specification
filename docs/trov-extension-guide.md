# TROV Extension Guide
<span class="draft-badge">
  TROV 0.1 DRAFT</span>

*This document is a draft and subject to revision.
Please [submit feedback or report issues](https://github.com/transparency-certified/trace-specification/issues/new?title=trov-extension-guide.md:%20).*

How to extend the TRACE model with institution-specific terms in TRO declarations using your own namespace, so that custom terms coexist with TROV terms without conflict. Covers namespace setup, embedded declarations for custom types, JSON Schema validation of extensions, and term mappings for future alignment.

| Document Section | Description |
|---------|-------------|
| [Overview](#extension-guide-overview) | The core principle and what this guide covers |
| [Step by Step](#step-by-step) | Choose a prefix, add to `@context`, use prefixed property names |
| [JSON Schema Validation](#how-json-schema-validation-handles-extensions) | How the schema validates TROV terms while supporting extensions |
| [Extending TROV with Custom Types](#extending-trov-with-custom-types) | Defining custom capabilities, attributes, signing mechanisms, and other typed terms |
| [Aligning with Future Versions](#aligning-custom-terms-with-future-trov-versions) | Alignment when a custom term is later standardized in TROV |

---

(extension-guide-overview)=
## Overview

Use your own namespace for institution-specific terms. TROV uses the prefix `trov:` for its terms; your system may define its own prefix for terms specific to your implementation. Custom terms coexist with TROV terms in the same declaration without conflict. The JSON Schema validates TROV terms while allowing namespaced extensions through.

---

(step-by-step)=
## Step by Step

### 1. Choose a namespace and prefix

Pick a namespace URI under an Internet domain you own. The URI is the durable identifier for your terms. The prefix is just a shorthand used within a given TRO declaration:

```json
"mytrs": "https://example.org/mytrs#"
```

Use a prefix that is short, lowercase, and recognizable to your team.

### 2. Add the prefix to your `@context`

The `@context` block in a TRO declaration maps prefixes to namespace URIs. Add your prefix alongside the standard TROV prefixes:

```json
"@context": [
    {
        "rdf":  "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "trov": "https://w3id.org/trace/trov/0.1#",
        "schema": "https://schema.org/",
        "mytrs": "https://example.org/mytrs#"
    }
]
```

### 3. Use prefixed property names for your metadata

Wherever you add custom metadata, use your prefix:

```json
{
    "@id": "trs",
    "@type": "trov:TrustedResearchSystem",
    "trov:name": "My Research System",
    "trov:hasCapability": [ ... ],
    "mytrs:version": "0.0.1",
    "mytrs:architecture": "x86_64",
    "mytrs:kernelVersion": "6.14.0-37-generic",
    "mytrs:imageRepoDigests": ["dataeditors/stata18_5-mp@sha256:3699b018..."]
}
```

These steps are sufficient for plain data properties. If your custom terms extend TROV classes — for example, new capability types, attribute types, or signing mechanisms — they also need declarations so that validators can recognize them as described in step 4 below.

### 4. Declare custom types that extend TROV classes

If your TRS introduces custom capabilities, performance attributes, signing mechanisms, or other terms used as values for TROV properties, declare each one in a `trov:customTerm` array on the TRS node. This tells validators that the custom term is a legitimate value for the property and allows it to participate in the warrant chain:

```json
"trov:customTerm": [
    {
        "@id": "mytrs:CanProvideAuditLogging",
        "rdfs:subClassOf": { "@id": "trov:TRSCapabilityType" }
    }
]
```

See [Extending TROV with Custom Types](#extending-trov-with-custom-types) for a full example and details on which terms need declarations. For background on how the warrant chain works, see [The Warrant Chain](tro-declaration-format.md#the-warrant-chain).

---

(how-json-schema-validation-handles-extensions)=
## How JSON Schema Validation Handles Extensions

The TROV JSON Schema is designed to validate the TROV core while supporting namespaced extensions:

- **Known `trov:` properties** are validated for presence, type, and structure. Missing required properties, wrong types, and invalid capability or attribute names are caught.
- **JSON-LD keywords** (`@type`, `@id`, `@context`, etc.) are always allowed.
- **Namespaced extension terms** with prefixes defined in the `@context` are allowed through without validation.
- **Bare unprefixed terms** that are not JSON-LD keywords or known TROV properties are flagged as non-conformant.

---

(extending-trov-with-custom-types)=
## Extending TROV with Custom Types

The TROV vocabulary defines predefined values for capabilities, performance attributes, and other typed properties. Adopters whose TRS uses types not yet covered by TROV can define custom types in their own namespace.

### Which custom terms need declarations?

Custom terms that extend TROV classes such as new capability types, attribute types, or signing mechanisms need a declaration connecting them to the TROV class they extend. These are terms used as values for TROV properties like `trov:hasCapability`, `trov:hasPerformanceAttribute`, or `trov:signingMechanism`. Without these declarations, validators cannot confirm that the custom terms are legitimate values for those properties.

Custom terms that are plain data properties, additional metadata on a node, need no declaration at all. They are just extra properties that JSON consumers use directly and RDF consumers treat as ordinary triples. Prefixing such terms with the system-specific scheme (e.g. `sivacor:`) is sufficient.

For example, `mytrs:architecture` is a plain string property on the TRS node. It doesn't extend any TROV class and needs no declaration. But `mytrs:CanProvideAuditLogging`, used as a value for `trov:hasCapability`, needs to be declared as a kind of `trov:TRSCapabilityType` so that validators can recognize it.

### Declaring custom types in the declaration

To make a TRO declaration self-contained for validation, declare your custom types in a `trov:customTerm` array on the TRS node. Each entry states which TROV class your custom term extends:

```json
{
    "@id": "trs",
    "@type": "trov:TrustedResearchSystem",
    "trov:name": "My Research System",
    "trov:customTerm": [
        {
            "@id": "mytrs:CanProvideAuditLogging",
            "rdfs:subClassOf": { "@id": "trov:TRSCapabilityType" }
        },
        {
            "@id": "mytrs:AuditLogging",
            "rdfs:subClassOf": { "@id": "trov:TRPAttributeType" }
        }
    ],
    "trov:hasCapability": [ ... ]
}
```

One entry per custom type. List your custom terms and say what kind of TROV term each one is. That's all that's needed — not an entire ontology, just the bare minimum to connect your terms to the TROV type hierarchy.

Placing the declarations on the TRS node makes it clear which system introduces the custom terms. In the RDF graph, the `rdfs:subClassOf` triples are available for validation regardless of where they appear in the JSON structure. An RDF consumer loading this declaration can validate custom types against the TROV type hierarchy without fetching any external vocabulary. A SPARQL query for all `trov:TRPAttributeType` instances will also find `mytrs:AuditLogging`. JSON consumers can skip the `trov:customTerm` array entirely.

Adopters may also publish these declarations in a vocabulary file at their namespace URI, but embedding them in the declaration ensures validation works regardless of whether that external resource is reachable.

### Using custom types in a TRO declaration

With these custom terms declared, they work exactly like the standard ones. They participate in the warrant chain through the standard `trov:warrantedBy` mechanism:

```json
"@context": [
    {
        "trov": "https://w3id.org/trace/trov/0.1#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "mytrs": "https://example.org/mytrs#"
    }
],
...
"trov:hasCapability": [
    {
        "@id": "trs/capability/0",
        "@type": "trov:CanProvideInternetIsolation"
    },
    {
        "@id": "trs/capability/1",
        "@type": "mytrs:CanProvideAuditLogging"
    }
],
...
"trov:hasPerformanceAttribute": [
    {
        "@id": "trp/0/attribute/0",
        "@type": "trov:InternetIsolation",
        "trov:warrantedBy": { "@id": "trs/capability/0" }
    },
    {
        "@id": "trp/0/attribute/1",
        "@type": "mytrs:AuditLogging",
        "trov:warrantedBy": { "@id": "trs/capability/1" }
    }
]
```

JSON consumers that don't recognize `mytrs:AuditLogging` can safely ignore it. The standard TROV attributes are unaffected.

### Path to standardization

If a custom type proves broadly useful across multiple TRS implementations, it can be proposed for inclusion in a future TROV version via the graduation path described below.

---

(aligning-custom-terms-with-future-trov-versions)=
## Aligning Custom Terms with Future TROV Versions

If a concept you defined in your namespace is later standardized as a `trov:` term (for example, if a future version of TROV adds `trov:cpuArchitecture`, and this term fully captures the concept represented by your custom `mytrs:architecture` term), consider using the standard term in new declarations. Existing TRO declarations remain valid.

### Optional: Declare a term mapping

To make existing declarations queryable using the new standard term via RDF tools, you can publish an RDF term mapping. This goes in a small vocabulary file at your namespace URI (not in the `@context` of individual TRO declarations).

For example, if your namespace is `https://example.org/mytrs#`, publish a file at that URL containing:

```turtle
@prefix mytrs: <https://example.org/mytrs#> .
@prefix trov:  <https://w3id.org/trace/trov/1#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .

mytrs:architecture rdfs:subPropertyOf trov:cpuArchitecture .
```

This tells RDF tools that `mytrs:architecture` is a specific case of the new `trov:cpuArchitecture` term. A SPARQL query for the TROV term will also find your custom term. You do not need to modify any existing TRO declarations. Anyone who dereferences your namespace finds the mappings automatically.

If you don't have infrastructure to serve files at your namespace URI, the mapping file can also be distributed alongside your TRO packages or published in a repository.

---

## History

| Date | Change |
|------|--------|
| 2026-03-26 | Added `trov:customTerm` and embedded type declarations for custom capabilities, attributes, and signing mechanisms. |
| 2026-02-23 | Initial publication. |

