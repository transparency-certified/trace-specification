# Documentation Infrastructure

How the TRACE project's documentation is built and deployed across GitHub repositories, each with its own build pipeline, and how the results combine into a single public website.

| Document Section | Description |
|---------|-------------|
| [Repositories](#repositories) | The repos that contribute to the public site |
| [How the Pieces Connect](#how-the-pieces-connect) | URL structure showing how the repos map to the public site |
| [The Project Website](#the-project-website) | Jekyll site serving the landing page and top-level navigation |
| [The Specification Site](#the-specification-site) | Jupyter Book build stack, deploy pipeline, and downloads |
| [The Vocabulary Reference](#the-vocabulary-reference) | Widoco-generated documentation from the TROV Turtle ontology |
| [Updating After Vocabulary Changes](#updating-after-vocabulary-changes) | How vocabulary submodules work and how to trigger a rebuild |
| [Adding a Page to the Specification](#adding-a-page-to-the-specification) | Steps to create a new document and make it appear on the live site |

For the specification content itself, see [TRACE Specifications](specifications.md). For the TROV vocabulary terms, see [TROV Vocabulary](trov-vocabulary.md).

---

## Repositories

Four repositories under the [transparency-certified](https://github.com/transparency-certified) GitHub organization contribute to the public documentation:

| Repository | Contents | URL |
|------------|----------|-----|
| [transparency-certified.github.io](https://github.com/transparency-certified/transparency-certified.github.io) | Project landing page and navigation | Served as Jekyll site at: [transparency-certified.github.io/](https://transparency-certified.github.io/) |
| [trace-specification](https://github.com/transparency-certified/trace-specification) | Specification documents, conceptual model, examples | Served as Jupyter Book at: [transparency-certified.github.io/trace-specification/](https://transparency-certified.github.io/trace-specification/) |
| [trace-vocabularies](https://github.com/transparency-certified/trace-vocabularies) | Build hub — aggregates vocabulary repos as submodules, holds w3id.org redirect config and tests | Served as GitHub Pages at: [transparency-certified.github.io/trace-vocabularies/](https://transparency-certified.github.io/trace-vocabularies/) |
| [trov](https://github.com/transparency-certified/trov) | TROV ontology source files — Turtle, SHACL shapes, Widoco config. Submodule of trace-vocabularies. | Served via trace-vocabularies Pages site |

GitHub serves all of these independently under the same domain via its CDN: `transparency-certified.github.io` is the organization's GitHub Pages site, and repos with Pages enabled are mounted at subpaths matching their repository names.

---

## How the Pieces Connect

The public site at `transparency-certified.github.io` is assembled by GitHub Pages from independent deployments:

```
transparency-certified.github.io/
│
├── /                              ← Jekyll site (transparency-certified.github.io repo, main branch)
│   ├── index.html                    Landing page
│   └── _config.yml                   Menu links into /trace-specification/
│
├── /trace-specification/          ← Jupyter Book output (trace-specification repo, gh-pages branch)
│   ├── docs/specifications.html      Specification entry point
│   ├── docs/...                      Built documentation pages
│   └── _static/                      Sphinx theme assets
│
└── /trace-vocabularies/           ← Widoco output (trace-vocabularies repo, gh-pages branch)
    ├── index.html                    Vocabulary index page
    ├── trov/0.1/                     TROV 0.1 vocabulary reference
    └── trov/prerelease/              TROV pre-release vocabulary reference
```

Each component is built and deployed independently. The Jekyll site links into the specification via its menu configuration. The specification documents link to the vocabulary reference where relevant.

The `trace-specification` and `trace-vocabularies` repos each deploy to an orphan `gh-pages` branch containing only generated HTML and a `.nojekyll` file that tells GitHub Pages to serve files directly.

---

## The Project Website

The **[transparency-certified.github.io](https://github.com/transparency-certified/transparency-certified.github.io)** repository is a standard [Jekyll](https://jekyllrb.com/) site. GitHub Pages builds it automatically from the `main` branch using its built-in Jekyll support — no GitHub Action or Docker image is needed.

The site provides a landing page with project description and team information, and navigation that links into the specification and vocabulary sites. Jekyll configuration is in `_config.yml`, and the site layout is controlled by standard Jekyll conventions (`_layouts/`, `_includes/`, etc.).

---

## The Specification Site

The **[trace-specification](https://github.com/transparency-certified/trace-specification)** repository contains the specification documents as Markdown files in `docs/`. The build and deploy process works as follows:

### Source

The `main` branch contains:

- Markdown source files in `docs/`
- Jupyter Book configuration: `_config.yml` (book settings) and `_toc.yml` (table of contents structure)
- A GitHub Actions workflow: `.github/workflows/deploy.yml`

The `_toc.yml` file controls which documents appear in the built site and in what order. It organizes content into parts: TRACE Overview, TRACE Specifications, TRACE Infrastructure, and TRACE Development. Short sidebar labels can be set with `title:` entries in the TOC without changing the document headings. Only files listed in `_toc.yml` are built (`only_build_toc_files: true` in `_config.yml`) — Markdown files not registered in the TOC are ignored by the build even though they exist in the repository.

All new documents are written in plain GitHub-Flavored Markdown (GFM). Jupyter Book also supports MyST Markdown (a superset of GFM with Sphinx-specific directives), but MyST syntax renders as raw text when viewed on GitHub. Since the source files are frequently read directly on GitHub, GFM ensures they look correct everywhere — on GitHub, in the Jupyter Book site, in VS Code, and in Pandoc-generated PDFs. A few older documents use MyST features (cross-references, admonitions, glossary); these will be converted to GFM equivalents over time.

### Build Stack

The specification site is built by a pipeline of tools, each handling a different layer:

| Layer | Tool | Role |
|-------|------|------|
| Source | GitHub-Flavored Markdown | Document content — what authors write |
| Book engine | [Jupyter Book](https://jupyterbook.org/) | Reads `_config.yml` and `_toc.yml`, assembles pages into a navigable book |
| Doc generator | [Sphinx](https://www.sphinx-doc.org/) | Underlying engine that Jupyter Book delegates to — resolves cross-references, builds the search index, generates HTML |
| Theme | [sphinx-book-theme](https://sphinx-book-theme.readthedocs.io/) | Controls layout, sidebar navigation, dark mode, and toolbar (download, fullscreen, search) |
| Styling | `_static/custom.css` | Project-specific CSS overrides (table hover color, print layout adjustments) |

Authors interact only with the top layer (Markdown files and the TOC). The lower layers are configured once and rarely need attention.

### Build

On every push to `main`, the GitHub Action:

1. Checks out the repository
2. Runs `jupyter-book build --all .` inside the `craigwillis/jupyter-book:latest` Docker image
3. Produces static HTML in `_build/html/`

### Deploy

The same GitHub Action uses `peaceiris/actions-gh-pages@v3.6.1` to push the built HTML to the `gh-pages` branch. Each deploy creates a commit with the message `deploy: <commit-hash>`, where the hash references the `main` branch commit that was built.

### Downloads

Each page on the built site offers Markdown and PDF downloads via the toolbar. The Markdown download is the original source file. The PDF is generated by the browser's print rendering, with project-specific print styles in `_static/custom.css` that hide the auto-generated table of contents and adjust page margins.

---

## The Vocabulary Reference

The **[trace-vocabularies](https://github.com/transparency-certified/trace-vocabularies)** repository is a build hub that aggregates vocabulary source repos as git submodules. It runs Widoco to generate HTML documentation and serialization files, then deploys everything to GitHub Pages.

### Source

The **[trov](https://github.com/transparency-certified/trov)** repository is a submodule of trace-vocabularies. It contains the ontology source files:

- `0.1/trov.ttl` — the TROV 0.1 ontology in Turtle format
- `0.1/trov-shacl.ttl` — SHACL shape constraints for validation
- `0.1/trov.config` — Widoco configuration
- `prerelease/trov.ttl` — frozen pre-release ontology (`2023/05/trov#` namespace)
- `prerelease/trov.config` — Widoco configuration for the pre-release

Future satellite vocabularies will be separate repos added as additional submodules.

### Build

On pushes to `main` (and on manual dispatch), the trace-vocabularies GitHub Action:

1. Checks out the repository with submodules
2. Runs Widoco for each vocabulary version (currently TROV 0.1 and TROV pre-release)
3. Organizes output under `trov/{version}/` to match the GitHub Pages URL structure
4. Renames Widoco's default output files (`ontology.*`) to vocabulary-specific names (`trov.*`) so the w3id.org content negotiation rules can find them
5. Verifies all expected files exist before deploying

### Deploy

The action uses `peaceiris/actions-gh-pages@v4` to push the built output to an orphan `gh-pages` branch. GitHub Pages serves the result at `transparency-certified.github.io/trace-vocabularies/`. Only pushes to `main` trigger deployment — pull requests build but do not deploy.

A [vocabulary index page](https://transparency-certified.github.io/trace-vocabularies/) (`index.html` in the repo root) is copied into the build output during each deploy. It lists all published vocabularies and versions, and serves as the default landing page for unversioned requests via w3id.org.

### Updating After Vocabulary Changes

Pushing changes to a vocabulary repo (e.g. trov) does not automatically rebuild the site. The trace-vocabularies repo uses git submodules — each submodule records a specific commit from the vocabulary repo. To pick up new vocabulary content, you advance the submodule pointer and push to trace-vocabularies, which triggers the build workflow.

The submodule pointer is a deliberate decision, not an automatic sync. This means the published documentation always corresponds to a known vocabulary commit, and vocabulary authors can push work-in-progress without affecting the live site.

For the specific git commands to advance submodule pointers, pin to a tagged release, or check submodule status, see the [trace-vocabularies README](https://github.com/transparency-certified/trace-vocabularies#updating-vocabulary-documentation).

### w3id.org Namespace Resolution

TROV namespace URIs (e.g. `https://w3id.org/trace/trov/0.1#ArtifactComposition`) resolve via redirect rules in a `.htaccess` file registered at [w3id.org](https://w3id.org/). The rules perform content negotiation: RDF tools requesting Turtle get `trov.ttl`, JSON-LD processors get `trov.jsonld`, and browsers get the HTML documentation page. The redirect targets are the GitHub Pages URLs served by trace-vocabularies.

The `.htaccess` source of truth and a Mocha test suite (27 tests, covering all redirect rules in both local Docker and live remote modes) are in `trace-vocabularies/w3id/`.

### Why GitHub Pages, not raw GitHub URLs

The w3id.org `.htaccess` rules redirect namespace URI requests to files on GitHub Pages. Content negotiation (Turtle vs JSON-LD vs HTML) happens at w3id.org, but GitHub Pages confirms the format by serving files with correct MIME types (`text/turtle`, `application/ld+json`, `text/html`). Raw GitHub URLs (`raw.githubusercontent.com`) serve everything as `text/plain`, which well-behaved RDF tools may reject. GitHub Pages is also required for the HTML landing page, which is served as `index.html` from a directory URL.

---

## Adding a Page to the Specification

To add a new document to the specification site:

1. **Create the Markdown file** in `docs/`. For example, `docs/my-new-page.md`.

2. **Register it in `_toc.yml`.** Add a `- file: docs/my-new-page` entry under the appropriate part and chapter list. Without this entry, Jupyter Book will not include the page in the build even though the file exists in the repository. Optionally add a `title:` for a shorter sidebar label.

   For example, to add it under TRACE Specifications:

   ```yaml
   - caption: TRACE Specifications
     chapters:
     - file: docs/specifications
     - file: docs/questions
     - file: docs/my-new-page    # ← new entry
       title: My New Page        # ← optional short sidebar label
   ```

3. **Push to `main`.** The GitHub Action will build the site and deploy the result to `gh-pages`. The new page will appear at `transparency-certified.github.io/trace-specification/docs/my-new-page.html`.

The build runs automatically. If the build fails (e.g., due to a syntax error or a broken cross-reference), the `gh-pages` branch is not updated and the live site remains unchanged. Check the Actions tab on the repository to see build status.
