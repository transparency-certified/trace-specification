# TROV Extension Guide

How to include institution-specific metadata in TRO declarations using your own namespace, so that custom terms coexist with TROV terms without conflict. Covers namespace setup, JSON Schema validation of extensions, and term mappings for future alignment.

| Document Section | Description |
|---------|-------------|
| [Overview](#overview) | The core principle and what this guide covers |
| [Step by Step](#step-by-step) | Choose a prefix, add to @context, use prefixed property names |
| [JSON Schema Validation](#how-json-schema-validation-handles-extensions) | How the schema validates TROV terms while supporting extensions |
| [Aligning with Future Versions](#aligning-custom-terms-with-future-trov-versions) | Alignment when a custom term is later standardized in TROV |
| [Custom Attribute and Capability Types](#custom-attribute-and-capability-types) | Extending the warrant chain with adopter-defined transparency claims |

---

## Overview

Use your own namespace for institution-specific terms. TROV uses the prefix `trov:` for its terms; your system defines its own prefix for terms specific to your implementation. Custom terms coexist with TROV terms in the same declaration without conflict. The JSON Schema validates TROV terms while allowing namespaced extensions through.

---

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
        "schema": "https://schema.org",
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

---

## How JSON Schema Validation Handles Extensions

The TROV JSON Schema is designed to validate the TROV core while supporting namespaced extensions:

- **Known `trov:` properties** are validated for presence, type, and structure. Missing required properties, wrong types, and invalid capability or attribute names are caught.
- **JSON-LD keywords** (`@type`, `@id`, `@context`, etc.) are always allowed.
- **Namespaced extension terms** with prefixes defined in the `@context` are allowed through without validation.
- **Bare unprefixed terms** that are not JSON-LD keywords or known TROV properties are flagged as non-conformant.

---

## Aligning Custom Terms with Future TROV Versions

If a concept you defined in your namespace is later standardized as a `trov:` term (for example, if TROV adds `trov:containerArchitecture` in a future minor version), consider using the standard term in new declarations. Existing TRO declarations remain valid.

### Optional: Declare a term mapping

To make existing declarations queryable using the new standard term via RDF tools, you can publish an RDF term mapping. This goes in a small vocabulary file at your namespace URI (not in the `@context` of individual TRO declarations).

For example, if your namespace is `https://example.org/mytrs#`, publish a file at that URL containing:

```turtle
@prefix mytrs: <https://example.org/mytrs#> .
@prefix trov:  <https://w3id.org/trace/trov/1#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .

mytrs:architecture rdfs:subPropertyOf trov:containerArchitecture .
```

This tells RDF tools that `mytrs:architecture` is a specific case of `trov:containerArchitecture`. A SPARQL query for the TROV term will also find your custom term. You do not need to modify any existing TRO declarations. Anyone who dereferences your namespace finds the mappings automatically.

If you don't have infrastructure to serve files at your namespace URI, the mapping file can also be distributed alongside your TRO packages or published in a repository.

---

## Custom Attribute and Capability Types

The TROV vocabulary defines a set of performance attribute types (e.g. `trov:InternetIsolation`) and TRS capability types (e.g. `trov:CanProvideInternetIsolation`). Adopters whose TRS enforces transparency conditions not yet covered by TROV can define custom types in their own namespace.

### Using custom types in a TRO declaration

Custom attribute and capability types work exactly like the standard ones — they participate in the warrant chain through the standard `trov:warrantedBy` mechanism:

```json
"@context": [
    {
        "trov": "https://w3id.org/trace/trov/0.1#",
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

JSON consumers that don't recognize `mytrs:AuditLogging` can safely ignore it — the standard TROV attributes are unaffected.

### Enabling RDF inference for custom types

RDF consumers who want custom types to appear alongside standard TROV types in queries can import the adopter's published vocabulary. The adopter declares the subclass relationship in a vocabulary file at their namespace URI:

```turtle
@prefix mytrs: <https://example.org/mytrs#> .
@prefix trov: <https://w3id.org/trace/trov/0.1#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

mytrs:AuditLogging      rdfs:subClassOf trov:TRPAttributeType .
mytrs:CanProvideAuditLogging rdfs:subClassOf trov:TRSCapabilityType .
```

With this declaration loaded, a SPARQL query for all `trov:TRPAttributeType` instances will also find `mytrs:AuditLogging`.

### Path to standardization

If a custom type proves broadly useful across multiple TRS implementations, it can be proposed for inclusion in a future TROV version — the same graduation path described in [Aligning Custom Terms with Future TROV Versions](#aligning-custom-terms-with-future-trov-versions).

