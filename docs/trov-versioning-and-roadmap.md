# TROV Versioning Strategy and Roadmap
<span class="draft-badge">
  DRAFT</span>

*This document is a draft and subject to revision.
Please [submit feedback or report issues](https://github.com/transparency-certified/trace-specification/issues/new?title=trov-versioning-and-roadmap.md:%20).*

How TROV versions are numbered, what stability guarantees each version provides, and the roadmap from the current draft (0.1) to a stable 1.0 release. Covers namespace management, documentation lifecycle, repository structure, and resolution of URI-qualified terms.

| Document Section | Description |
|---------|-------------|
| [Design Goals](#design-goals) | Design goals governing TROV's evolution |
| [Version Numbering](#version-numbering) | Pre-1.0 vs post-1.0 stability and namespace URIs |
| [What Constitutes a Version](#what-constitutes-a-version) | What's in 0.1 (current draft) and what 1.0 requires |
| [Extensibility](#extensibility-adopter-specific-terms) | How adopters add institution-specific terms safely |
| [Breaking vs Non-Breaking Changes](#breaking-vs-non-breaking-changes) | Classification table for post-1.0 changes |
| [Repository Structure](#repository-structure-and-namespace-resolution) | trov and trace-specification layouts, URI resolution |
| [Roadmap](#roadmap) | Four phases: stabilize 0.1, evolve 0.x, release 1.0, governance/maintenance 1.x |

For the vocabulary terms themselves, see the [TROV Vocabulary Reference](trov-vocabulary.md). For the JSON-LD document format, see [TRO Declaration Format](tro-declaration-format.md). For adding institution-specific metadata to TRO declarations, see the [TROV Extension Guide](trov-extension-guide.md).

---

(design-goals)=
## Design Goals

1. **Grounded in practice.** TROV addresses transparency problems faced by real organizations, describes capabilities systems can feasibly implement, and answers verification questions reviewers commonly ask.

2. **Two perspectives, one vocabulary.** TRO declarations are simultaneously valid JSON and valid RDF. Both perspectives remain first-class across versions. (See [TRO Declaration Design](tro-declaration-design.md).)

3. **Stability for adopters.** Every version is identifiable. Breaking changes are explicit and rare.

4. **Extensibility without conflict.** Adopters include institution-specific metadata in TRO declarations using their own namespaces. Broadly applicable extensions may be standardized in future TROV versions. (See [Extensibility](#extensibility-adopter-specific-terms) for details.)

5. **Low barrier to adoption.** Any community producing computational research artifacts can benefit from TROV.

---

(version-numbering)=
## Version Numbering

TROV uses **semantic versioning** with different stability guarantees before and after 1.0.

### Pre-1.0 (Evolving)

Pre-1.0 versions (0.1, 0.2, etc.) are working drafts that **may include breaking changes** — terms renamed, removed, or given incompatible semantics. Each 0.x version receives its own namespace URI; when superseded, its documentation is frozen into a snapshot page with migration guidance.

### Post-1.0 (Stable)

Once 1.0 is released, the standard semantic versioning rules apply:

- **MAJOR** (e.g. 1.0 → 2.0): Breaking changes: terms removed, renamed, or given incompatible semantics. Existing valid TRO declarations may no longer validate against the latest version. New namespace URI.
- **MINOR** (e.g. 1.0 → 1.1): Add-only: new capability types, new attribute types, new optional properties. No terms removed, renamed, or redefined. Existing TRO declarations remain valid against the new version. Same namespace URI.
- **No patch versions.** Description clarifications and typo fixes in vocabulary files are editorial changes that can be made without changing the version number.

Minor versions share a namespace because they only add optional terms. The ontology file at the namespace URI is updated to include new terms, but existing declarations remain valid — the new terms are available, not required. Only a major version bump changes the namespace URI and triggers a frozen snapshot of the superseded version.

### Version Lifecycle

Each version passes through a simple lifecycle:

| Status | Meaning |
|--------|---------|
| **Draft** | Under active development. The namespace URI works and adopters can build against it, but terms may still change before release. |
| **Released** | Stable. The terms defined in this version will not be removed, renamed, or redefined. Future minor versions may add new terms at the same namespace URI. |
| **Retired** | Superseded by a newer version. Documentation frozen into a snapshot page with migration guidance. Files remain available at their URIs indefinitely. |

The namespace URI stays the same across states — `trov/0.1#` is `trov/0.1#` whether the version is draft or released. Adopters do not need to change their `@context` on release day.

When a version is released or retired, both `trace-specification` and `trov` repos are tagged `trov/0.1`, `trov/0.2`, etc. Each tagged release includes built documentation artifacts (Markdown source, per-page PDFs, and the whole-book PDF) as release assets, providing a permanent record of the specification as it stood at that version.

### Namespace URIs

Each version that may contain breaking changes relative to its predecessor receives its own namespace URI:

| Version | Namespace URI | Status |
|---------|--------------|--------|
| _(pre-release)_ | `https://w3id.org/trace/2023/05/trov#` | Retired. Frozen snapshot. Pre-Release Reference [coming soon]. |
| 0.1 | `https://w3id.org/trace/trov/0.1#` | Draft. Concrete target for implementers to converge on. |
| 0.2, 0.3, ... | `https://w3id.org/trace/trov/0.2#`, ... | Future pre-1.0 versions. Each gets its own namespace. |
| 1.0 | `https://w3id.org/trace/trov/1#` | Planned. |
| 1.1, 1.2, ... | `https://w3id.org/trace/trov/1#` | Future minor versions share the major-version namespace. |
| 2.0 | `https://w3id.org/trace/trov/2#` | No current plans. |

### Namespace History

The pre-release namespace `https://w3id.org/trace/2023/05/trov#` was minted in May 2023 using a date-based URI pattern. TROV now uses a version-based pattern (`trace/trov/{version}#`).

The pre-release namespace is retired. TRO declarations using the `2023/05` namespace require conversion for TROV 0.1 conformance. The `2023/05` URI will resolve to the Pre-Release Vocabulary Reference [coming soon], which documents the pre-release terms and provides migration guidance.

### Documentation Lifecycle

On `main`, `trov-vocabulary.md` always describes the latest released version (or the current draft if nothing has been released yet). Draft work for the next version happens on a branch (e.g. `0.2-draft`). When the new version is ready to release we:

1. Snapshot `trov-vocabulary.md` to a version-specific file (e.g. `trov-0.1.md`).
2. Merge the draft branch into `main`.

The snapshot is a self-contained page: term inventory, known issues, migration steps. Other documents (`tro-declaration-format.md`, `trov-extension-guide.md`, etc.) are updated on the draft branch as needed and merged along with the vocabulary reference.

**Post-1.0:** The same workflow continues. Minor versions are backwards-compatible (add-only), but `trov-vocabulary.md` is still snapshotted before each merge. This keeps every version visible side by side at the head of `main`, and lets someone receiving a TRO that references a specific TROV version look up what terms were available when that TRO was produced.

Snapshots and namespace URIs serve different purposes. Namespace URIs track compatibility — all 1.x versions share a namespace because they are backwards-compatible. Snapshots track what terms each version defined. TRO declarations post-0.1 include an explicit vocabulary version property so consumers can determine the specific minor version without parsing the namespace URI.

```
2023/05/trov#   →  frozen snapshot (trov-prerelease.md)
trov/0.1#       →  living docs on main (current)
trov/0.2#       →  trov-vocabulary.md snapshotted to trov-0.1.md, 0.2-draft branch merged
  ...
trov/1#         →  last 0.x frozen, living docs describe latest 1.x release
trov/1# (1.1)   →  trov-vocabulary.md snapshotted to trov-1.0.md, 1.1-draft branch merged
trov/1# (1.2)   →  trov-vocabulary.md snapshotted to trov-1.1.md, 1.2-draft branch merged
  ...
trov/2#         →  1.x frozen, new namespace, living docs describe latest 2.x release
```

---

(what-constitutes-a-version)=
## What Constitutes a Version

### TROV 0.1 (Current Draft — Stabilization Target)

**Namespace:** `https://w3id.org/trace/trov/0.1#`

**Status:** First formally documented version. Based on pre-release implementations: property names reconciled, known bugs fixed, term list curated.

**Goal:** Produce a documented, testable baseline. Descriptive of deployed reality, with known issues resolved.

**Authoritative sources (in priority order):**

1. **tro-utils source code** — the reference implementation. What it produces is what 0.1 means.
2. **trov.ttl** — the formal OWL ontology. Currently incomplete; will be updated to match the above.
3. **trov-shacl.ttl** — SHACL validation shapes. Currently partial; will be extended.
4. **TROV Vocabulary Reference** (`trov-vocabulary.md`) — the human-readable specification.

**What is in 0.1 (draft — under discussion and subject to change before release):**

- The classes, properties, and predefined values documented in the [TROV Vocabulary Reference](trov-vocabulary.md).
- The JSON-LD structure documented in the [TRO Declaration Format](tro-declaration-format.md).
- Support for GPG and X.509/CMS signing mechanisms.

**What must happen before 0.1 is considered stable:**

- [ ] Reconcile property name divergences between tro-utils and hand-written examples.
- [ ] Update trov.ttl to include all properties and classes actually in use.
- [ ] Enable w3id.org namespace resolution.
- [ ] Design signing-identity representation that works across signing mechanisms (GPG, X.509/CMS, and others).
- [ ] Reconcile duplicate capability types.
- [ ] Add `trov:vocabularyVersion` property for declaring the TROV vocabulary version used in a TRO declaration.

### TROV 1.0 (First Stable Release)

**Goal:** A stable vocabulary with guaranteed backwards compatibility, tooling for validation and reporting, and documentation sufficient for independent adoption without direct guidance from the TROV maintainers.

**Expected capabilities (introduced incrementally in 0.x releases):**

- Formal namespace resolution via w3id.org with content negotiation. HTML for browsers, Turtle and JSON-LD for RDF tools.
- Published `@context` file at a stable URI for reference. We recommend that TRO declarations embed the context inline so they remain self-contained.
- JSON Schema for basic validation of TRO declarations.
- Full set of SHACL shapes for validating TRO declarations and TRS certificates.
- Complete warrant chain validation (TRO attributes → TRP attributes → TRS capabilities) implemented in tooling.
- Signing mechanism formally specified (algorithm-agnostic, supporting GPG and X.509/CMS at minimum).
- At least one standard TRO package format specified (ZIP layout, relationship between declaration, signature, and payload).
- trov-validate tool for deep compliance testing (warrant chain completeness, cross-reference integrity).
- trov-report tool for human-readable summaries.

---

(extensibility-adopter-specific-terms)=
## Extensibility: Adopter-Specific Terms

Adopters will need to include metadata specific to their systems — container runtime details, internal system versions, resource utilization metrics, and similar operational data. For a step-by-step walkthrough, see the [TROV Extension Guide](trov-extension-guide.md).

**Rules for adopter extensions:**

1. **Use your own namespace** for institution-specific terms. For example, an adopter might use `mytrs:` for system-specific metadata (the prefix shorthand is local to each declaration; what matters is the URI it expands to). This guarantees no collision with future TROV terms.

2. **Unprefixed or `trov:`-prefixed terms not in the vocabulary are non-conformant.** A validator will flag them. This protects adopters from silently depending on terms that may change or conflict with future TROV additions.

3. **Propose new `trov:` terms.** If an extension proves broadly applicable, it can be proposed for inclusion in a future TROV minor version.

4. **The `@context` is extensible.** Adopters can add their own namespace prefixes to the `@context` block alongside the standard TROV prefixes.

**Example — adopter-specific metadata alongside TROV terms:**

```json
"@context": [
    {
        "rdf":  "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "trov": "https://w3id.org/trace/trov/0.1#",
        "schema": "https://schema.org/",
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

(breaking-vs-non-breaking-changes)=
## Breaking vs Non-Breaking Changes

The following table describes how changes are classified **after 1.0** (pre-1.0, any of these changes may occur in any 0.x release).

| Change | Breaking? | Post-1.0 version bump |
|--------|-----------|----------------------|
| Change the description of an existing term | No | None |
| Add a new optional property | No | Minor |
| Add a new capability type | No | Minor |
| Add a new TRP or TRO attribute type | No | Minor |
| Rename a property or class | **Yes** | Major |
| Remove a property or class | **Yes** | Major |
| Change a property from optional to required | **Yes** | Major |
| Change the semantics of an existing term | **Yes** | Major |
| Change the namespace URI | **Yes** | Major |
| Add a new required property | **Yes** | Major |

---

(repository-structure-and-namespace-resolution)=
## Repository Structure and Namespace Resolution

### The trov repository

The [`trov`](https://github.com/transparency-certified/trov) repository is the source for all machine-readable vocabulary files. It contains one directory per version, and the GitHub Actions workflow deploys these directories to GitHub Pages:

```
trov/
  README.md
  .github/workflows/deploy.yml      ← generates HTML docs, deploys to GitHub Pages
  0.1/
    context.jsonld                   ← JSON-LD context file (for reference)
    tro-schema.json                  ← JSON Schema for TRO declaration validation
    trov-shacl.ttl                   ← SHACL validation shapes
    trov.jsonld                      ← OWL ontology (JSON-LD format)
    trov.ttl                         ← OWL ontology (Turtle)
  prerelease/
    trov.ttl                         ← frozen OWL ontology (2023/05/trov# namespace)
```

**What goes in the trov repo:** master copies of the machine-readable artifacts that consumers fetch programmatically via GitHub Pages — ontology files, validation schemas, SHACL shapes.

**What does not go in the trov repo:** human-readable documentation (that lives in `trace-specification/docs/`).

When a version is superseded, its directory is frozen in place. The files remain available at the same URIs indefinitely.

### The trace-specification repository

Human-readable documentation lives in `trace-specification`:

```
trace-specification/
  docs/
    tro-declaration-format.md        ← living declaration format guide (current version)
    trov-0.1.md                      ← snapshot of trov-vocabulary.md when 0.1 is superseded
    trov-prerelease.md               ← frozen snapshot (retired pre-release)
    trov-versioning-and-roadmap.md   ← this document (version-independent)
    trov-vocabulary.md               ← living vocabulary reference (current version)
```

The `docs/` directory always describes the current version; retired versions are frozen into snapshot pages.

### Namespace resolution via w3id.org

TROV namespace URIs are persistent URIs managed through [w3id.org](https://w3id.org/). The redirect rules live in a `.htaccess` file submitted via pull request to the [perma-id/w3id.org](https://github.com/perma-id/w3id.org) repository (under a `trace/` directory). Once merged, the w3id.org Apache server uses these rules to redirect requests to our GitHub Pages site. The wildcard design means this is a one-time PR. For testing procedures, see [Documentation Infrastructure](documentation-infrastructure.md#testing-the-w3id-org-redirect-rules).

```apache
RewriteEngine On

# All redirects use 303 (See Other) per linked data best practice.
# The wildcard (.+?) captures the version (e.g. 0.1, 1) so new versions
# work without new rules.

# Direct access to the JSON-LD context file for a specific version
RewriteRule ^trov/(.+?)/context\.jsonld$ https://transparency-certified.github.io/trov/$1/context.jsonld [R=303,L]

# RDF tool requesting Turtle → serve the OWL ontology file
RewriteCond %{HTTP_ACCEPT} text/turtle
RewriteRule ^trov/(.+?)/?$ https://transparency-certified.github.io/trov/$1/trov.ttl [R=303,L]

# JSON-LD processor requesting JSON-LD → serve the ontology in JSON-LD format
RewriteCond %{HTTP_ACCEPT} application/ld\+json
RewriteRule ^trov/(.+?)/?$ https://transparency-certified.github.io/trov/$1/trov.jsonld [R=303,L]

# Browser or anything else → serve the HTML landing page for this version
RewriteRule ^trov/(.+?)/?$ https://transparency-certified.github.io/trov/$1/ [R=303,L]

# Special case: serve the HTML landing page for the pre-release version
RewriteRule ^2023/05/trov/?$ https://transparency-certified.github.io/trov/prerelease/ [R=303,L]
```

Examples of how namespace URIs resolve:

| Request | Accept header | Resolves to |
|---------|--------------|-------------|
| `https://w3id.org/trace/trov/0.1/context.jsonld` | _(any)_ | `https://transparency-certified.github.io/trov/0.1/context.jsonld` |
| `https://w3id.org/trace/trov/0.1` | `text/turtle` | `https://transparency-certified.github.io/trov/0.1/trov.ttl` |
| `https://w3id.org/trace/trov/0.1` | `application/ld+json` | `https://transparency-certified.github.io/trov/0.1/trov.jsonld` |
| `https://w3id.org/trace/trov/0.1` | _(any other)_ | `https://transparency-certified.github.io/trov/0.1/` (HTML landing page) |
| `https://w3id.org/trace/2023/05/trov` | _(any)_ | `https://transparency-certified.github.io/trov/prerelease/` |

**What gets served.** All content — including the Turtle and JSON-LD ontology files — is served from GitHub Pages, not from the `trov` repo directly. The repo is the source; the GitHub Actions workflow deploys its contents to GitHub Pages, which serves files with correct MIME types to confirm the format that w3id.org's content negotiation selected. See [Documentation Infrastructure](documentation-infrastructure.md#why-github-pages-not-raw-github-urls) for details.

The deployed site layout:

```
transparency-certified.github.io/trov/
  0.1/
    context.jsonld          ← JSON-LD context file (for reference)
    index.html              ← HTML landing page (generated)
    tro-schema.json         ← JSON Schema for TRO declaration validation
    trov-shacl.ttl          ← SHACL validation shapes
    trov.jsonld             ← OWL ontology (JSON-LD)
    trov.ttl                ← OWL ontology (Turtle)
  prerelease/
    index.html              ← HTML landing page (generated)
    trov.ttl                ← frozen OWL ontology
```

---

(roadmap)=
## Roadmap

### Phase 1: Stabilize 0.1 (Now — June 2026)

Produce a documented, testable, internally consistent 0.1 that matches deployed reality.

- Establish JSON Schema generation workflow.
- Complete and publish the specification documents (vocabulary reference, declaration format, package format).
- Enable w3id.org namespace resolution.
- Fix known bugs and resolve vocabulary variations.
- Test the JSON Schema against TRO declarations produced by pre-release implementations updated to target 0.1.
- Publish the vocabulary reference at the namespace URI.

### Phase 2: Evolve 0.x (July 2026 — June 2027)

Extend the vocabulary, complete validation and reporting tooling, and resolve open design questions.

- Release JSON Schema validator for basic structural validation of TRO declarations.
- Complete SHACL shapes for validating TRO declarations and TRS certificates.
- Develop trov-validate tool for deep compliance testing (SPARQL, SHACL).
- Develop trov-report tool for human-readable HTML and PDF summaries (SPARQL).
- Resolve open design questions (signing mechanisms, package formats, signing-identity representations).
- Update trov.ttl to full OWL coverage.
- Publish machine-readable vocabulary documents and JSON-LD context at namespace URIs.

### Phase 3: Release 1.0 (June 2027)

Release TROV 1.0 with guaranteed backwards compatibility, tooling for validation and reporting, and documentation sufficient for independent adoption.

- Stable namespace URI with content negotiation.
- Complete warrant chain validation implemented in tooling.
- At least one standard TRO package format specified.
- Full documentation set.

### Phase 4: Governance and Maintenance 1.x (July 2027 — June 2029)

Support independent adoption, establish community governance, and publish the vocabulary description.

- Publish TRACE Adoption Guide for organizations building TRACE-compatible systems.
- Expand capability and attribute type catalog based on adopter feedback.
- Establish TROV Interest Group with charter and governance documents.
- Engage with relevant standards bodies and research data communities.
- Collect community feedback and incorporate into post-1.0 minor releases.
- Submit description of vocabulary design and capabilities to a peer-reviewed journal.
- Improve adopter documentation based on deployment experience.

---

## History

| Date | Change |
|------|--------|
| 2026-03-26 | Updated terminology from "Named Individuals" to "Predefined Values". |
| 2026-02-19 | Initial publication. |

