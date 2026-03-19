# TRO Declaration Design: JSON and RDF
<span style="display:inline-block; padding:2px 10px;  margin-bottom:16px; background:#f0ad4e; font-weight:bold; color:black; border-radius:4px; font-size:14px;">
  TROV 0.1 DRAFT</span>

*This document is a draft and subject to revision.
Please [submit feedback or report issues](https://github.com/transparency-certified/trace-specification/issues/new?title=tro-declaration-design.md:%20).*

Why TRO declarations use JSON-LD, what each audience gets from the format, and how the JSON Schema constraint makes both JSON and RDF workflows possible from a single file.

| Document Section | Description |
|---------|-------------|
| [The Core Idea](#the-core-idea) | One file, two perspectives: valid JSON and valid RDF simultaneously |
| [What This Means in Practice](#what-this-means-in-practice) | What producers, JSON consumers, RDF consumers, and repositories each get |
| [The JSON Schema Constraint](#the-json-schema-constraint) | How the fixed document structure enables both audiences |
| [The @context Is the Bridge](#the-context-is-the-bridge) | How the JSON-LD context connects the JSON and RDF perspectives |
| [Summary](#summary) | Four-audience comparison table |

---

## The Core Idea

A TRO declaration — the document that describes a Transparent Research Object — is a JSON-LD document. This means it is simultaneously:

- **Valid JSON** — parseable by any JSON library, validatable against a JSON Schema, queryable with standard JSON tools (jq, JSONPath, any programming language's built-in JSON support).
- **Valid RDF** — loadable into a triplestore, queryable with SPARQL, validatable with SHACL shapes, combinable with other TROs and other linked data for cross-organization analysis.

This dual nature is the central architectural decision for TRO declarations: one file, two perspectives.

**Note:** *The [TRO Declaration Format](tro-declaration-format.md) defines where terms appear in the JSON-LD document tree. The [TROV vocabulary](trov-vocabulary.md) defines the RDF/OWL terms themselves. The TRACE specification encompasses the entire system.*

---

## What This Means in Practice

### For TRO producers

Trusted Research Systems isolate computational workflows from researcher interaction during execution, guaranteeing that results reflect the submitted code and data without modification. Some TRS implementations go further — operating inside air-gapped enclaves at institutions handling confidential data, where there is no network access, no large dependency trees, and no runtime resolution of remote resources.

A TRO producer writes JSON. It follows a schema. The `@context` block at the top is a fixed header that the producer copies from a template (e.g. one provided in [TRO Declaration Format](tro-declaration-format.md)). The rest of the document is a predictable tree of objects with known property names at known locations.

**What producers need:**
- A JSON Schema to validate against
- A field reference showing where each piece of information goes
- Example declarations to copy from

**What producers do not need:**
- An RDF library (rdflib, Jena, etc.)
- Network access to resolve the `@context` URI or namespace URIs
- A persistent triplestore

### For TRO consumers using JSON tools

A consumer who receives a TRO declaration can treat it as a JSON document. Because the TRO Declaration Format constrains the structure, information is in predictable locations in the document tree:

- The TRS is at a known path. Its capabilities are a list under a known property.
- Each TRP is at a known path. Its attributes, accessed arrangements, and contributed arrangements are under known properties.
- Artifacts, compositions, and arrangements follow the same pattern.

A consumer can extract information using standard JSON tools.

### For TRO consumers using RDF tools

The same document loaded into a triplestore (in memory or persistent) becomes a set of RDF triples.

**Cross-TRO querying.** A consumer who loads multiple TROs from different institutions into the same triplestore can query across them with SPARQL. For example, given an artifact's SHA-256 digest, a query can trace its production history across institutions — which TRP produced it, what input artifacts that TRP consumed, where each of those inputs came from (another TRP, or an original dataset), and so on transitively back through the full dependency chain, including what transparency attributes were in effect at each step.

These queries work without coordination between the institutions that produced the TROs. The `@context` maps JSON property names to globally unique URIs, so `trov:hasCapability` in one institution's TRO means the same thing as `trov:hasCapability` in another's.

**Warrant chain validation.** The TROV conceptual model defines a warrant chain: TRO attributes are warranted by TRP attributes, which are in turn warranted by TRS capabilities. When the full chain is present, it provides machine-verifiable justification for every transparency claim. In JSON, verifying this chain requires navigating the document tree and matching identifiers. In RDF, it is a graph traversal — SPARQL queries can walk the `trov:warrantedBy` links, and SHACL shapes can confirm that the chain is structurally complete.

**Reasoning over collections.** A triplestore holding TROs from many sources becomes a knowledge base. Consumers can ask questions that no single TRO can answer: What fraction of TROs were produced under conditions of internet isolation? Which artifacts have been independently produced by different TRSs? Are there TRPs that accessed the same input data but were conducted under different transparency attributes? Do all computations in the transitive provenance of a given set of artifacts meet a specified set of transparency requirements? These aggregate queries are the basis for meta-analyses of computational transparency.

**TROV tooling leverages RDF.** The trov-validate and trov-report tools we are developing use SPARQL and SHACL internally to validate warrant chains, check structural conformance, and generate human-readable summaries. The tools accept a TRO declaration as input and produce validation results or HTML/PDF reports as output.

### For data repositories and aggregators

A repository that archives TROs from multiple sources can implement each function using JSON tools, RDF tools, or a combination:

- **Ingest:** validate against the JSON Schema and store the file, or load directly into a triplestore, or both.
- **Query:** navigate individual declarations with JSON tools, or run SPARQL queries across the entire collection in a triplestore.
- **Display:** render human-readable summaries by walking the JSON document tree, or generate reports from SPARQL query results.
- **Serve:** expose the collection via a public SPARQL endpoint for programmatic access, serve the raw JSON files via API, or build web applications and dashboards that draw on either.

Both perspectives let repositories integrate TRO metadata with other vocabularies they already use — e.g. schema.org for describing datasets, W3C PROV for representing provenance, DataCite for facilitating citation — enabling queries that span transparency claims and existing metadata.

---

## The JSON Schema Constraint

The flexibility of RDF is powerful for interoperability but makes validation and tooling harder. If a TRO declaration were unconstrained RDF, a producer could express the same information in many structurally different ways, and consumers would need graph-pattern matching to find anything.

The TRO JSON Schema imposes a fixed document tree structure on top of the RDF vocabulary. This means:

- **Producers** know where to put each piece of information.
- **JSON consumers** know where to find each piece of information.
- **RDF consumers** still get valid triples, but in a predictable pattern.

The constraint is more restrictive than what RDF allows. You cannot rearrange the tree, nest things differently, or use blank nodes in creative ways in a TRO declaration. This restriction is what makes JSON Schema validation possible, what makes standard JSON tooling sufficient for most use cases, and what makes TRO declarations from different institutions structurally consistent.

---

## The `@context` Is the Bridge

The `@context` block is the mechanism that connects the two perspectives. For JSON producers, it is a fixed header that can be copied from the [TRO Declaration Format](tro-declaration-format.md) examples and modified only if adding a namespace prefix. For RDF consumers, it is the mapping that turns JSON property names into globally unique URIs.

A TRO producer who follows the JSON Schema and preserves the `@context` is producing valid linked data. The transparency claims in that TRO are machine-readable, globally identifiable, and combinable with any other TRO or linked dataset on the web.

---

## Summary

| Perspective | Tools | What you see | What you get |
|-------------|-------|-------------|---------------------|
| **JSON producer** | Any JSON library, JSON Schema validator | A JSON document with a fixed structure | Schema, field reference, examples |
| **JSON consumer** | jq, JSONPath, any language's JSON parser | A predictable tree you can navigate | Known paths to every piece of information |
| **RDF consumer** | Triplestore, SPARQL, SHACL | A graph of triples with standard vocabulary | Cross-TRO queries, linked data interoperability |
| **Repository** | JSON or RDF technologies | A collection of JSON documents or single graph of triples | Integration with existing metadata and standards |
