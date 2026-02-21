# TROV Extension Guide

**Adding custom terms to TRO declarations**

TRO declarations describe transparency properties using the TROV vocabulary. But every Transparent Research System has operational metadata that TROV does not cover — container runtime details, internal version numbers, resource utilization, institutional identifiers. This guide explains how to include that metadata cleanly, so that it coexists with TROV terms without conflict.

---

## The Rule

**Use your own namespace for institution-specific terms.**

TROV uses the prefix `trov:` for its terms. Your system should define its own prefix for terms specific to your implementation. This guarantees no collision with current or future TROV terms.

---

## Step by Step

### 1. Choose a namespace and prefix

Pick a namespace URI you control and a short prefix. The namespace should be a stable URL — it does not need to resolve to anything today, but it should be yours:

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

This is standard JSON-LD practice. Adding your own prefix does not affect TROV conformance.

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

The `trov:` properties are validated by the TROV JSON Schema. The `mytrs:` properties pass through — the schema recognizes them as namespaced extensions and does not flag them.

### 4. Do not use unprefixed custom terms

This is wrong:

```json
{
    "@id": "trs",
    "@type": "trov:TrustedResearchSystem",
    "trov:name": "My Research System",
    "version": "0.0.1",
    "architecture": "x86_64"
}
```

Unprefixed terms that are not part of the TROV vocabulary or JSON-LD keywords will be flagged as non-conformant by validators. They also create ambiguity — is `"version"` your system's version, or a future TROV term? A namespace prefix removes the ambiguity.

---

## How JSON Schema Validation Handles Extensions

The TROV JSON Schema is designed to validate the TROV core while tolerating namespaced extensions:

- **Known `trov:` properties** are validated for presence, type, and structure. Missing required properties, wrong types, and invalid capability or attribute names are caught.
- **JSON-LD keywords** (`@type`, `@id`, `@context`, etc.) are always allowed.
- **Namespaced extension terms** (any property matching a `prefix:name` pattern) are allowed through without validation. The schema does not know what `mytrs:version` should look like — that is your responsibility.
- **Bare unprefixed terms** that are not JSON-LD keywords or known TROV properties are flagged as non-conformant.

This means the schema enforces the "use your own namespace" rule automatically. You get structural validation of the TROV parts of your declaration and freedom to include whatever operational metadata your system needs.

---

## Aligning Custom Terms with Future TROV Versions

If a term you defined in your namespace is later standardized as a `trov:` term (for example, if TROV adds `trov:containerArchitecture` in a future minor version), you have two options:

### Option A: Update your declarations

Switch from `mytrs:architecture` to `trov:containerArchitecture` in new declarations. Old declarations remain valid — they just use your namespace for a concept that now has a standard name.

### Option B: Declare a term mapping

If you want old declarations to be queryable using the new standard term, you can publish an RDF term mapping. This goes in a small vocabulary file at your namespace URI — not in the `@context` of individual TRO declarations (the `@context` maps names to URIs but cannot express relationships between properties).

For example, if your namespace is `https://example.org/mytrs#`, publish a file at that URL containing:

```turtle
@prefix mytrs: <https://example.org/mytrs#> .
@prefix trov:  <https://w3id.org/trace/trov/1#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .

mytrs:architecture rdfs:subPropertyOf trov:containerArchitecture .
```

This tells RDF tools that `mytrs:architecture` is a specific case of `trov:containerArchitecture`. A SPARQL query for the TROV term will also find your custom term. You do not need to modify any existing TRO declarations — anyone who dereferences your namespace finds the mappings automatically.

If you don't have infrastructure to serve files at your namespace URI, the mapping file can also be distributed alongside your TRO packages or published in a repository. What matters is that consumers can find it.

> **Note.** Term mappings are only relevant if you or your consumers use RDF tooling. If you treat TRO declarations purely as JSON, Option A (updating new declarations) is simpler and sufficient.

---

## Summary

| Do | Don't |
|----|-------|
| Define your own namespace prefix | Use `trov:` for custom terms |
| Add your prefix to the `@context` | Leave custom terms unprefixed |
| Use `prefix:name` for all custom properties | Assume bare keys will be ignored |
| Let the JSON Schema validate TROV structure | Worry about custom terms failing validation |
| Publish term mappings if you want RDF queryability | Feel obligated to use RDF tooling |
