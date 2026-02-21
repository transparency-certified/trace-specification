# TRO Declaration Design: JSON and RDF

**How TRO declarations serve both JSON and RDF audiences**

---

## The Core Idea

A TRO declaration — the document that describes a Transparent Research Object — is a JSON-LD document. This means it is simultaneously:

- **Valid JSON** — parseable by any JSON library, validatable against a JSON Schema, queryable with standard JSON tools (jq, JSONPath, any programming language's built-in JSON support).
- **Valid RDF** — loadable into a triplestore, queryable with SPARQL, validatable with SHACL shapes, combinable with other TROs and other linked data for cross-organization analysis.

This is not a compromise or an accident. It is the central architectural decision for TRO declarations: one file, two perspectives, zero conversion.

**Note:** *The TRACE specification encompasses the entire system — TRS behavior, signing, validation, packaging, and more. Within it, the [TROV vocabulary](trov-vocabulary.md) defines the RDF/OWL terms (classes, properties, and named individuals) used to describe transparency properties. The [TRO Declaration Format](tro-declaration-format.md) defines the JSON-LD document format, including a JSON Schema that constrains the document structure. The vocabulary defines the terms; the declaration format defines where those terms appear in the document tree. Both are needed — and it is their combination that makes the dual JSON/RDF strategy work. See also the [TROV Extension Guide](trov-extension-guide.md) for adding institution-specific metadata and the [Versioning Strategy and Roadmap](trov-versioning-and-roadmap.md) for version policy.*

---

## What This Means in Practice

### For TRO producers (inside the vault)

We envision Transparent Research Systems operating inside controlled environments — air-gapped enclaves at institutions handling confidential data, where the constraints are severe: no network access, no large dependency trees, no runtime resolution of remote resources.

A TRO producer writes JSON. It follows a schema. The `@context` block at the top is a fixed header that the producer copies from a template. The rest of the document is a predictable tree of objects with known property names at known locations.

**What producers need:**
- A JSON Schema to validate against
- A field reference showing where each piece of information goes
- Example declarations to copy from

**What producers do NOT need:**
- Any understanding of RDF, triples, or graphs
- Any RDF library (rdflib, Jena, etc.)
- Network access to resolve the `@context` URI
- An ontology or a reasoner
- A persistent triplestore

### For TRO consumers using JSON tools

A consumer who receives a TRO declaration can treat it as a JSON document. Because the TRO Declaration Format constrains the structure (not just the vocabulary), information is in predictable locations in the document tree:

- The TRS is at a known path. Its capabilities are a list under a known property.
- Each TRP is at a known path. Its attributes, accessed arrangements, and contributed arrangements are under known properties.
- Artifacts, compositions, and arrangements follow the same pattern.

This predictability is a direct consequence of the JSON Schema constraint. A consumer can write a simple script using standard JSON tools to extract exactly what it needs.

### For TRO consumers using RDF tools

The same document, loaded into a triplestore, becomes a set of RDF triples. This is where the full power of the TROV vocabulary becomes available.

**Cross-TRO querying.** A consumer who loads multiple TROs from different institutions into the same triplestore can query across them with SPARQL:

- Which TRSs claim internet isolation capability?
- Which TRPs were conducted by a given TRS?
- Which artifacts appear in TROs from more than one institution?
- What transparency attributes are warranted across a collection of TROs?
- Trace the production history of a specific artifact (identified by its SHA-256 digest) across TROs from different institutions — where did it first appear, which TRPs consumed it, which produced it, and under what transparency attributes?

These queries work without any coordination between the institutions that produced the TROs. The `@context` — which the JSON producer treated as a fixed header — is what makes this possible. It maps the JSON property names to globally unique URIs, so `trov:hasCapability` in one institution's TRO means exactly the same thing as `trov:hasCapability` in another's.

**Warrant chain validation.** The TROV conceptual model defines a warrant chain: TRO attributes are warranted by TRP attributes, which are in turn warranted by TRS capabilities. When the full chain is present, it provides machine-verifiable justification for every transparency claim. In JSON, verifying this chain requires navigating the document tree and matching identifiers by hand. In RDF, it is a graph traversal — a SPARQL query or SHACL shape can walk the `trov:warrantedBy` links and confirm that every claimed attribute traces back to a declared capability. This is the kind of structural validation that RDF was designed for.

**Reasoning over collections.** A triplestore holding TROs from many sources becomes a knowledge base. Consumers can ask questions that no single TRO can answer: How many institutions have systems capable of internet isolation? Which artifacts have been independently produced by different TRSs? Are there TRPs that accessed the same input data but were conducted under different transparency attributes? These aggregate queries are the basis for meta-analyses of computational transparency across a research community.

**TROV tooling leverages RDF.** The trov-validate and trov-report tools we are developing use SPARQL and SHACL internally to validate warrant chains, check structural conformance, and generate human-readable summaries. Consumers who use these tools get the benefits of RDF reasoning through a simple interface — the tools accept a TRO declaration (a JSON file) as input and produce validation results or HTML/PDF reports as output. The RDF layer is an implementation detail hidden behind a simple command-line interface.

### For data repositories and aggregators

A repository that archives TROs from multiple sources can implement each function using JSON tools, RDF tools, or a combination:

- **Ingest:** validate against the JSON Schema and store the file, or load directly into a triplestore, or both.
- **Query:** navigate individual declarations with JSON tools, or run SPARQL queries across the entire collection in a triplestore.
- **Display:** render human-readable summaries by walking the JSON document tree, or generate reports from SPARQL query results.
- **Serve:** expose the collection via a public SPARQL endpoint for programmatic access, serve the raw JSON files via API, or build web applications and dashboards that draw on either.

A repository can start with JSON (simpler) and add RDF capabilities as the collection grows, or go RDF-native from the start. The format supports both paths.

---

## The Constraint That Liberates

RDF is inherently flexible — a graph can have any shape. This flexibility is powerful for interoperability but makes validation and tooling harder. If a TRO declaration were unconstrained RDF, a producer could express the same information in many structurally different ways, and consumers would need graph-pattern matching to find anything.

The TRO Declaration Format constrains this. The JSON Schema imposes a fixed document tree structure on top of the RDF vocabulary. This means:

- **Producers** know exactly where to put each piece of information.
- **JSON consumers** know exactly where to find each piece of information.
- **RDF consumers** still get valid triples — the tree structure maps cleanly to a graph — but the triples come in a predictable pattern.

The constraint is more restrictive than what RDF allows. You cannot rearrange the tree, nest things differently, or use blank nodes in creative ways. But this restriction is what makes JSON Schema validation possible, what makes simple JSON tooling sufficient for most use cases, and what makes TRO declarations from different institutions structurally consistent.

In short: the TRO Declaration Format trades RDF's structural flexibility for predictability, and both audiences benefit.

---

## The `@context` Is the Bridge

The `@context` block is the mechanism that connects the two perspectives. For JSON producers, it is a fixed header — copy it from the template, do not modify it unless adding your own namespace prefix. For RDF consumers, it is the mapping that turns JSON property names into globally unique URIs.

A TRO producer who follows the JSON Schema and preserves the `@context` is producing valid linked data. The transparency claims in that TRO are machine-readable, globally identifiable, and combinable with any other TRO or linked dataset on the web.

---

## Summary

| Perspective | Tools | What you see | What you get |
|-------------|-------|-------------|---------------------|
| **JSON producer** | Any JSON library, JSON Schema validator | A JSON document with a fixed structure | Schema, field reference, examples |
| **JSON consumer** | jq, JSONPath, any language's JSON parser | A predictable tree you can navigate | Known paths to every piece of information |
| **RDF consumer** | Triplestore, SPARQL, SHACL | A graph of triples with standard vocabulary | Cross-TRO queries, linked data interoperability |
| **Repository** | Both | JSON for ingest and display, RDF for query | Start simple, add power as the collection grows |
