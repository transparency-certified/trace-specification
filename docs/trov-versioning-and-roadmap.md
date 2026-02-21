# TROV Versioning Strategy and Roadmap

This document describes the versioning policy for the Transparent Research Object Vocabulary (TROV), the current state of the vocabulary, and the roadmap from the current draft to TROV 1.0.

For the vocabulary terms themselves, see the [TROV Vocabulary Reference](trov-vocabulary.md). For the JSON-LD document format, see [TRO Declaration Format](tro-declaration-format.md).

---

## Guiding Principles

1. **Implementation drives the spec, not the reverse.** TROV exists to describe what Transparent Research Systems and consumers of TROs actually do.

2. **Stability for adopters.** Organizations building TRACE-compatible systems need confidence that the vocabulary will not change under them without warning. Every version must be identifiable, and breaking changes must be explicit and rare.

3. **Extensibility without conflict.** Adopters will need to include institution-specific metadata (container runtime details, internal system versions, etc.) in their TRO declarations. They can do this by using their own namespaces, rather than by requesting that terms specific to them be added to the `trov:` namespace. (See [Extensibility](#extensibility-adopter-specific-terms) for details.)

4. **Two perspectives, one vocabulary.** TROV data is simultaneously valid JSON and valid RDF. Producers and consumers alike may choose either perspective: some will treat TRO declarations as JSON documents validated against a schema; others will load them into a graph and query with SPARQL. Both perspectives must remain valid across versions. A version change that serves one perspective at the expense of the other is considered a design flaw.

5. **Minimal formalism.** The vocabulary governance should be as lightweight as possible while still preventing the problems that motivate it (term drift, silent incompatibilities, broken URIs). TROV is a practical vocabulary that any community producing computational research artifacts can adopt.

---

## Version Numbering

TROV uses **semantic versioning** adapted for a vocabulary, with different stability guarantees before and after 1.0.

### Pre-1.0 (Development)

Pre-1.0 versions (0.1, 0.2, etc.) are working drafts. Any 0.x release **may include breaking changes** — terms renamed, removed, or given incompatible semantics. This is the significance of pre-1.0 releases. Version 1.0 will be released when we can guarantee backwards compatibility for adopters going forward. Each 0.x version receives its own namespace URI.

When a 0.x version is superseded, its documentation is frozen into a snapshot page and the namespace URI resolves to that snapshot with migration guidance.

### Post-1.0 (Stable)

Once 1.0 is released, the standard semantic versioning rules apply:

- **MAJOR** (e.g. 1.0 → 2.0): Breaking changes — terms removed, renamed, or given incompatible semantics. Existing valid TRO declarations may no longer validate. New namespace URI.
- **MINOR** (e.g. 1.0 → 1.1): Add-only — new capability types, new attribute types, new optional properties. No terms removed, renamed, or redefined. Existing valid TRO declarations remain valid. Same namespace URI.
- **No patch versions.** Vocabulary terms are either defined or not. Typo fixes and clarifications to descriptions are editorial changes that do not change the version number.

Post-1.0, minor versions share a namespace and the living documentation is updated in place. Only a major version bump changes the namespace URI and triggers a frozen snapshot of the superseded version.

### Version Lifecycle

Each version passes through a simple lifecycle:

| Status | Meaning |
|--------|---------|
| **Draft** | Under active development. The namespace URI works and adopters can build against it, but terms may still change before release. |
| **Released** | Stable. The terms in this version will not change (though the version may eventually be superseded). |
| **Retired** | Superseded by a newer version. Documentation frozen into a snapshot page with migration guidance. Files remain available at their URIs indefinitely. |

The namespace URI stays the same across states — `trov/0.1#` is `trov/0.1#` whether the version is draft or released. Adopters do not need to change their `@context` on release day. The status is metadata about the version, not part of the identifier.

### Namespace URIs

Each version that may contain breaking changes relative to its predecessor receives its own namespace URI:

| Version | Namespace URI | Status |
|---------|--------------|--------|
| _(pre-release)_ | `https://w3id.org/trace/2023/05/trov#` | Retired. Frozen snapshot: [Pre-Release Reference](trov-prerelease.md). |
| 0.1 | `https://w3id.org/trace/trov/0.1#` | Draft. First documented and testable version. |
| 0.2, 0.3, ... | `https://w3id.org/trace/trov/0.2#`, ... | Future pre-1.0 versions, if needed. Each gets its own namespace. |
| 1.0 | `https://w3id.org/trace/trov/1#` | Planned. |
| 1.1, 1.2, ... | `https://w3id.org/trace/trov/1#` | Future minor versions share the major-version namespace. |

### Namespace History

The pre-release namespace `https://w3id.org/trace/2023/05/trov#` was minted in May 2023 using a date-based URI pattern. TROV now uses a version-based namespace pattern (`trace/trov/{version}#`). Pre-1.0, each version gets its own namespace because breaking changes are expected. Post-1.0, only major versions change the namespace.

The pre-release namespace is retired. TRO declarations created with the `2023/05` namespace remain valid documents but are not guaranteed to conform to TROV 0.1 without conversion. The `2023/05` URI resolves to the [Pre-Release Vocabulary Reference](trov-prerelease.md), which documents the terms used by pre-release implementations and provides migration guidance.

A one-time migration tool will convert pre-release TRO declarations to the 0.1 namespace.

### Documentation Lifecycle

The documentation strategy differs before and after 1.0:

**Pre-1.0:** Each 0.x version may include breaking changes. When a 0.x version is superseded, its documentation is frozen into a self-contained snapshot page (term inventory, known issues, migration steps). The living documentation (`trov-vocabulary.md`, `tro-declaration-format.md`, etc.) always describes the current version.

**Post-1.0:** Minor versions (1.1, 1.2, ...) are backwards-compatible. The living documentation is updated in place — new terms are added, the version number increments, but nothing is retired or frozen. Only a major version bump (2.0) freezes the previous major version's documentation.

```
2023/05/trov#   →  frozen snapshot (trov-prerelease.md)
trov/0.1#       →  living docs (current)
trov/0.2#       →  if needed: 0.1 frozen into trov-0.1.md, living docs updated
  ...
trov/1#         →  last 0.x frozen, living docs describe 1.0
                    1.1, 1.2 update living docs in place (same namespace)
trov/2#         →  1.x frozen, new namespace, living docs describe 2.0
```

---

## What Constitutes a Version

### TROV 0.1 (Current — Stabilization Target)

**Namespace:** `https://w3id.org/trace/trov/0.1#`

**Status:** First formally documented version. Based on pre-release implementations but cleaned up: property names reconciled, known bugs fixed, term list curated.

**Goal:** Produce a documented, testable baseline. Not aspirational — descriptive of deployed reality, with known issues resolved.

**Authoritative sources (in priority order):**

1. **tro-utils source code** — the reference implementation. What it produces is what 0.1 means.
2. **TROV term registry** (`schema/trov-terms.yaml`, not yet created) — the curated list of term names, descriptions, and warrant chain links. Generated artifacts (JSON Schema, documentation tables) will be derived from this file.
3. **TROV Vocabulary Reference** (`trov-vocabulary.md`) — the human-readable specification.
4. **trov.ttl** — the formal OWL ontology. Currently incomplete; will be updated to match the above.
5. **trov_shacl.ttl** — SHACL validation shapes. Currently partial; will be extended.

**What is in 0.1 (draft — under discussion and subject to change before release):**

- The classes, properties, and named individuals documented in the [TROV Vocabulary Reference](trov-vocabulary.md).
- The JSON-LD structure documented in the [TRO Declaration Format](tro-declaration-format.md).
- Two implemented TRS capabilities (`CanProvideInternetIsolation`, `CanRecordInternetAccess`) and their corresponding TRP attributes.
- Additional capability types defined in the vocabulary but not yet implemented in tro-utils.
- GPG-based signing as implemented. X.509/CMS signing as a documented alternative.

**What must happen before 0.1 is considered stable:**

- [ ] Reconcile property name divergences between tro-utils and hand-written examples (hasLocus vs hasArtifactLocation, etc.). Resolve in favor of tro-utils; update examples.
- [ ] Rename `"trov:Artifact Arrangement"` to `"trov:ArtifactArrangement"` in tro-utils (space in type name breaks RDF tooling and schema validation).
- [ ] Establish the YAML term registry as the single source of truth for term lists.
- [ ] Generate the JSON Schema from the term registry and validate it against existing TRO declarations from pre-release implementations.
- [ ] Update trov.ttl to include all properties and classes actually in use.
- [ ] Update trov_shacl.ttl to cover the full structure.
- [ ] Enable w3id.org namespace resolution.
- [ ] Design signing-identity representation that works across signing mechanisms (GPG, X.509/CMS, and others). Includes `trov:publicKey`, signing algorithm, and signature file references.
- [ ] Reconcile duplicate capability types (e.g. `CanPreventAuthorIntervention` vs `CanPreventUserInteractionDuringRun`).

### TROV 1.0 (Target — Guaranteed Stability)

**Goal:** A stable vocabulary with guaranteed backwards compatibility, full tooling support, and documentation sufficient for independent adoption without direct guidance from the TROV maintainers.

**Expected capabilities (may be introduced incrementally in 0.x releases):**

- Backwards compatibility guarantee. Minor versions add terms; nothing is removed or renamed.
- Complete warrant chain validation (TRO attributes → TRP attributes → TRS capabilities) implemented in tooling.
- Full set of SHACL shapes for validating TRO declarations and TRS certificates.
- Signing mechanism formally specified (algorithm-agnostic, supporting GPG and X.509/CMS at minimum).
- TRO package format specified (ZIP layout, relationship between declaration, signature, and payload).
- Published JSON-LD context file at a stable URI.
- Formal namespace resolution via w3id.org with content negotiation (HTML for browsers, Turtle/JSON-LD for RDF tools).
- trov-validate tool for compliance testing.
- trov-report tool for human-readable summaries.
- Peer-reviewed vocabulary description.

---

## Extensibility: Adopter-Specific Terms

Adopters will need to include metadata specific to their systems — container runtime details, internal system versions, resource utilization metrics, and similar operational data. This is expected and welcome.

**Rules for adopter extensions:**

1. **Use your own namespace** for institution-specific terms. For example, an adopter might use `mytrs:` for system-specific metadata. This guarantees no collision with future TROV terms.

2. **Unprefixed or `trov:`-prefixed terms not in the vocabulary are non-conformant.** A validator will flag them. This protects adopters from silently depending on terms that may change or conflict with future TROV additions.

3. **Propose new `trov:` terms through the normal process.** If an extension proves broadly useful (e.g., container runtime metadata), it can be proposed for inclusion in a future TROV minor version.

4. **The `@context` is extensible.** Adopters can add their own namespace prefixes to the `@context` block alongside the standard TROV prefixes. This is standard JSON-LD practice and does not affect TROV conformance.

**Example — adopter-specific metadata alongside TROV terms:**

```json
"@context": [
    {
        "rdf":  "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "trov": "https://w3id.org/trace/trov/0.1#",
        "schema": "https://schema.org",
        "mytrs": "https://example.org/mytrs#"
    }
],
...
"mytrs:version": "0.0.1",
"mytrs:architecture": "x86_64",
"mytrs:kernelVersion": "6.14.0-37-generic",
"mytrs:imageRepoDigests": ["dataeditors/stata18_5-mp@sha256:3699b018..."]
```

---

## Breaking vs Non-Breaking Changes

The following table describes how changes are classified **after 1.0**. Pre-1.0, any of these changes may occur in any 0.x release — the pre-1.0 period exists precisely to allow them.

| Change | Breaking? | Post-1.0 version bump |
|--------|-----------|----------------------|
| Add a new optional property | No | Minor |
| Add a new capability type | No | Minor |
| Add a new TRP or TRO attribute type | No | Minor |
| Change the description of an existing term | No | Editorial |
| Rename a property or class | **Yes** | Major |
| Remove a property or class | **Yes** | Major |
| Change a property from optional to required | **Yes** | Major |
| Change the semantics of an existing term | **Yes** | Major |
| Change the namespace URI | **Yes** | Major |
| Add a new required property | **Yes** | Major |

---

## Sources of Truth and Their Roles

The vocabulary is maintained through multiple artifacts that serve different audiences. They must stay in sync. The flow of authority is:

```
trace-specification/schema/
  trov-terms.yaml          (term registry — names, descriptions, warrant links)
      ↓ generates
trov/{version}/
  tro-schema.json          (JSON Schema — for TRO producers / JSON developers)
trace-specification/docs/
  trov-vocabulary.md        (reference tables — for all audiences)
      ↓ must be consistent with
trov/{version}/
  trov.ttl                  (OWL ontology — for RDF consumers)
  trov.jsonld               (OWL ontology — JSON-LD format)
  trov_shacl.ttl            (SHACL shapes — for RDF-based validation)
      ↓ must be implemented by
tro-utils                   (reference implementation — ground truth for behavior)
```

**Tagging strategy.** When a TROV version is released (or retired), the `trace-specification` repo is tagged `trov/0.1`, `trov/0.2`, etc. This makes it easy to retrieve the term registry and documentation for any version:

```
git show trov/0.1:schema/trov-terms.yaml
```

The `trov/` repo is tagged with the same labels. The frozen artifacts in each version directory are the generated outputs; the tag on `trace-specification` preserves the corresponding sources.

**When sources conflict:** tro-utils behavior is authoritative for 0.1. For 1.0, the term registry and specification documents become authoritative, and tro-utils is expected to conform.

This inversion — from "the code is the spec" to "the spec governs the code" — is the central transition from 0.1 to 1.0.

---

## Repository Structure and Namespace Resolution

### The trov/ repository

The [`trov/`](https://github.com/transparency-certified/trov) repository is the home for all machine-readable vocabulary artifacts. It contains one directory per version, and each directory holds every artifact a consumer needs for that version:

```
trov/
  README.md
  .github/workflows/deploy.yml      ← generates HTML docs, deploys to GitHub Pages
  prerelease/
    trov.ttl                         ← frozen OWL ontology (2023/05/trov# namespace)
  0.1/
    trov.ttl                         ← OWL ontology (Turtle)
    trov.jsonld                      ← OWL ontology (JSON-LD format)
    trov_shacl.ttl                   ← SHACL validation shapes
    tro-schema.json                  ← JSON Schema for TRO declaration validation
    trov.config                      ← WIDOCO configuration (generates HTML reference)
    sections/
      abstract-en.html               ← custom WIDOCO section (links to curated docs)
      introduction-en.html           ← custom WIDOCO section
```

The directory structure mirrors the namespace URI path: `trov/0.1/` corresponds to `https://w3id.org/trace/trov/0.1#`. Adding a new version means adding a directory.

**What goes in the trov/ repo:** machine-readable artifacts that consumers fetch programmatically — ontology files, validation schemas, SHACL shapes.

**What does NOT go in the trov/ repo:** human-readable documentation (that lives in `trace-specification/docs/`), the term registry and generation pipeline (that lives in `trace-specification/schema/`).

**HTML landing page.** When a browser dereferences the namespace URI, it receives an HTML page generated by [WIDOCO](https://github.com/dgarijo/Widoco) from `trov.ttl`. This is a standard LODE-style ontology reference page familiar to RDF practitioners. Custom `sections/` snippets add prominent links to the curated developer documentation in `trace-specification/` — the vocabulary reference, declaration format guide, and versioning roadmap — so that the auto-generated page serves as a recognizable landing page for ontology-oriented visitors and a quick gateway to the richer material for everyone else.

When a version is superseded, its directory is frozen in place. The files remain available at the same URIs indefinitely.

### The trace-specification/ repository

Human-readable documentation and the build pipeline live in `trace-specification/`:

```
trace-specification/
  docs/
    trov-vocabulary.md               ← living vocabulary reference (current version)
    tro-declaration-format.md        ← living declaration format guide (current version)
    trov-prerelease.md               ← frozen snapshot (retired pre-release)
    trov-versioning-and-roadmap.md   ← this document (version-independent)
  schema/
    trov-terms.yaml                  ← term registry (source of truth for term lists)
    tro-schema.json.j2               ← Jinja2 template for JSON Schema
    generate.py                      ← generates tro-schema.json and vocabulary tables
    requirements.txt                 ← Python dependencies (jinja2, pyyaml)
    Makefile                         ← sets up venv, runs generate.py
```

The generation pipeline in `schema/` produces artifacts that are committed to the `trov/` repo. The `docs/` directory always describes the current version; retired versions are frozen into snapshot pages.

### Namespace resolution via w3id.org

TROV namespace URIs are persistent URIs managed through [w3id.org](https://w3id.org/). The redirect rules live in a `.htaccess` file submitted via pull request to the [perma-id/w3id.org](https://github.com/perma-id/w3id.org) repository (under a `trace/` directory). Once merged, the w3id.org Apache server uses these rules to redirect requests to our GitHub Pages site. The wildcard design means this is a one-time PR — adding new TROV versions requires only adding a directory to the `trov/` repo, not updating the redirect rules.

```apache
RewriteEngine On

# Content negotiation for /trace/trov/{version}
RewriteCond %{HTTP_ACCEPT} text/turtle
RewriteRule ^trov/(.+?)/?$ https://transparency-certified.github.io/trov/$1/trov.ttl [R=303,L]

RewriteCond %{HTTP_ACCEPT} application/ld\+json
RewriteRule ^trov/(.+?)/?$ https://transparency-certified.github.io/trov/$1/trov.jsonld [R=303,L]

# Default (browser) → HTML documentation
RewriteRule ^trov/(.+?)/?$ https://transparency-certified.github.io/trov/$1/ [R=303,L]

# Pre-release namespace (different URL structure, one-time rule)
RewriteRule ^2023/05/trov/?$ https://transparency-certified.github.io/trov/prerelease/ [R=303,L]
```

The wildcard `(.+?)` captures the version from the URI path and maps it to the corresponding directory on GitHub Pages.

**Testing before the PR.** w3id.org has no staging environment, so we test the two sides independently:

1. **Verify GitHub Pages targets.** Confirm that `https://transparency-certified.github.io/trov/0.1/trov.ttl` (and `.jsonld`, and the HTML index) serve the correct content.
2. **Test rewrite rules locally.** Run Apache in Docker with our `.htaccess` and verify redirects with `curl -v -H "Accept: text/turtle" http://localhost/trace/trov/0.1` etc.
3. **Post-merge smoke test.** After the w3id.org PR is merged, verify the live URLs return the expected 303 redirects.

| Request | Accept header | Resolves to |
|---------|--------------|-------------|
| `https://w3id.org/trace/trov/0.1` | `text/turtle` | `trov/0.1/trov.ttl` |
| `https://w3id.org/trace/trov/0.1` | `application/ld+json` | `trov/0.1/trov.jsonld` |
| `https://w3id.org/trace/trov/0.1` | _(browser)_ | `trov/0.1/` (HTML, generated by WIDOCO) |
| `https://w3id.org/trace/2023/05/trov` | _(any)_ | `trov/prerelease/` |

---

## Roadmap

### Phase 1: Stabilize 0.1 (Now — June 2026)

Produce a documented, testable, internally consistent 0.1 that matches deployed reality.

- Establish YAML term registry and JSON Schema generation pipeline.
- Complete and publish the specification documents (vocabulary reference, declaration format, package format).
- Enable w3id.org namespace resolution.
- Fix known bugs and resolve vocabulary variations.
- Validate the JSON Schema against existing TRO declarations from pre-release implementations.
- Publish the vocabulary reference at the namespace URI.

### Phase 2: TROV 1.0 (July 2026 — June 2027)

Finalize the vocabulary, complete validation and reporting tooling, and release TROV 1.0 with guaranteed backwards compatibility.

- Finalize vocabulary and JSON-LD context (publish at stable URI).
- Complete SHACL shapes for validating TRO declarations and TRS certificates.
- Develop trov-validate tool for compliance testing.
- Develop trov-report tool for human-readable HTML and PDF summaries.
- Resolve open design questions (signing mechanism, package format, signing-identity representation).
- Update trov.ttl to full OWL coverage.
- Release TROV 1.0 with stable namespace URI, content negotiation, and full documentation.

### Phase 3: Adoption, Governance, and Publication (July 2027 — June 2029)

Support independent adoption, establish community governance, and publish the vocabulary description.

- Publish TRACE Adoption Guide for organizations building TRACE-compatible systems.
- Expand capability and attribute type catalog based on adopter feedback.
- Establish TROV Interest Group with charter and governance documents.
- Engage with relevant standards bodies and research data communities.
- Collect community feedback and incorporate into post-1.0 minor releases.
- Submit vocabulary description to a peer-reviewed journal.
- Improve adopter documentation based on deployment experience.

---

## Notes

**Why 0.1 and not 1.0?** Because 1.0 implies a stability commitment we cannot yet make. Calling the first documented version 0.1 gives adopters a clear baseline while leaving room for necessary changes.

**Why does each 0.x version get its own namespace?** Because pre-1.0 versions may include breaking changes. Giving each its own namespace makes this explicit. Post-1.0, minor versions share a namespace because backwards compatibility is guaranteed.

**Why a new namespace pattern?** The version-based pattern (`trace/trov/{version}#`) is more predictable than the pre-release date-based pattern. No pre-release TROs have been archived as permanent records, so the migration cost is bounded.

**The goal is to minimize 0.x releases.** Each pre-1.0 version bump creates migration work for adopters. The ideal path is 0.1 → 1.0 directly, but the versioning scheme supports intermediate versions if needed.
