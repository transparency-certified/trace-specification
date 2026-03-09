# Documentation Infrastructure

How the TRACE project's documentation is built and deployed across three GitHub repositories, each with its own build pipeline, and how the results combine into a single public website.

| Document Section | Description |
|---------|-------------|
| [Repositories](#repositories) | The three repos that contribute to the public site |
| [How the Pieces Connect](#how-the-pieces-connect) | URL structure showing how the three repos map to the public site |
| [The Project Website](#the-project-website) | Jekyll site serving the landing page and top-level navigation |
| [The Specification Site](#the-specification-site) | Jupyter Book build and deploy pipeline |
| [The Vocabulary Reference](#the-vocabulary-reference) | Widoco-generated documentation from the TROV Turtle ontology |
| [Adding a Page to the Specification](#adding-a-page-to-the-specification) | Steps to create a new document and make it appear on the live site |

For the specification content itself, see [TRACE Specifications](specifications.md). For the TROV vocabulary terms, see [TROV Vocabulary](trov-vocabulary.md).

---

## Repositories

Three repositories under the [transparency-certified](https://github.com/transparency-certified) GitHub organization contribute to the public documentation:

| Repository | Contents | URL |
|------------|----------|-----|
| [transparency-certified.github.io](https://github.com/transparency-certified/transparency-certified.github.io) | Jekyll site — project landing page and navigation | Serves at root: [transparency-certified.github.io/](https://transparency-certified.github.io/) |
| [trace-specification](https://github.com/transparency-certified/trace-specification) | Jupyter Book source — specification documents, conceptual model, examples | Serves at: [transparency-certified.github.io/trace-specification/](https://transparency-certified.github.io/trace-specification/) |
| [trov](https://github.com/transparency-certified/trov) | TROV ontology in Turtle and JSON-LD, SHACL shapes, Widoco configuration | Serves at: [transparency-certified.github.io/trov/0.1/](https://transparency-certified.github.io/trov/0.1/) |

GitHub serves all three under the same domain: `transparency-certified.github.io` is the organization's GitHub Pages site, and the other two repos are project-level Pages sites that GitHub mounts at subpaths matching their repository names.

---

## How the Pieces Connect

The public site at `transparency-certified.github.io` is assembled by GitHub Pages from three independent deployments:

```
transparency-certified.github.io/
│
├── /                          ← Jekyll site (transparency-certified.github.io repo, main branch)
│   ├── index.html                Landing page
│   └── _config.yml               Menu links into /trace-specification/
│
├── /trace-specification/      ← Jupyter Book output (trace-specification repo, gh-pages branch)
│   ├── docs/specifications.html  Specification entry point
│   ├── docs/...                  Built documentation pages
│   └── _static/                  Sphinx theme assets
│
└── /trov/                     ← Widoco output (trov repo, gh-pages branch)
    └── 0.1/index.html            Vocabulary reference
```

Each component is built and deployed independently. The Jekyll site links into the specification via its menu configuration. The specification documents link to the vocabulary reference where relevant.

The `trace-specification` and `trov` repos each deploy to an orphan `gh-pages` branch containing only generated HTML and a `.nojekyll` file that tells GitHub Pages to serve files directly.

---

## The Project Website

The **[transparency-certified.github.io](https://github.com/transparency-certified/transparency-certified.github.io)** repository is a Jekyll site. GitHub Pages builds it automatically from the `main` branch. The site provides a landing page with project description and team information, and navigation that links into the specification and vocabulary sites.

---

## The Specification Site

The **[trace-specification](https://github.com/transparency-certified/trace-specification)** repository contains the specification documents as Markdown files in `docs/`. The build and deploy process works as follows:

### Source

The `main` branch contains:

- Markdown source files in `docs/`
- Jupyter Book configuration: `_config.yml` (book settings) and `_toc.yml` (table of contents structure)
- A GitHub Actions workflow: `.github/workflows/deploy.yml`

The `_toc.yml` file controls which documents appear in the built site and in what order. It organizes content into parts: TRACE Overview, TRACE Specifications, TRACE Infrastructure, and TRACE Development.

### Build

On every push to `main`, the GitHub Action:

1. Checks out the repository
2. Runs `jupyter-book build --all .` inside the `craigwillis/jupyter-book:latest` Docker image
3. Produces static HTML in `_build/html/`

### Deploy

The same GitHub Action uses `peaceiris/actions-gh-pages@v3.6.1` to push the built HTML to the `gh-pages` branch. Each deploy creates a commit with the message `deploy: <commit-hash>`, where the hash references the `main` branch commit that was built.

---

## The Vocabulary Reference

The **[trov](https://github.com/transparency-certified/trov)** repository contains the TROV ontology definition and uses a similar build and deploy pipeline.

### Source

The `0.1/` directory contains:

- `trov.ttl` — the ontology in Turtle (RDF) format
- `trov-shacl.ttl` — SHACL shape constraints for validation
- `trov.config` — configuration for the Widoco documentation generator

### Build

On pushes or pull requests to `main` (and on manual dispatch), the GitHub Action runs:

1. Checks out the repository
2. Runs [Widoco](https://github.com/dgarijo/Widoco) (`craigwillis/widoco:latest` Docker image) to generate HTML documentation from the Turtle ontology
3. Renames the output directory to `0.1/` and fixes the index filename (`index-en.html` to `index.html`)

### Deploy

The action uses `peaceiris/actions-gh-pages@v4` to push the Widoco output to an orphan `gh-pages` branch, following the same pattern as `trace-specification`. GitHub Pages serves the result at `transparency-certified.github.io/trov/`.

### Why GitHub Pages, not raw GitHub URLs

The w3id.org `.htaccess` rules redirect namespace URI requests to files on GitHub Pages. Content negotiation (Turtle vs JSON-LD vs HTML) happens at w3id.org, but GitHub Pages confirms the format by serving files with correct MIME types (`text/turtle`, `application/ld+json`, `text/html`). Raw GitHub URLs (`raw.githubusercontent.com`) serve everything as `text/plain`, which well-behaved RDF tools may reject. GitHub Pages is also required for the HTML landing page, which is served as `index.html` from a directory URL.

### Testing the w3id.org redirect rules

w3id.org has no staging environment, so we test independently before and after the PR:

1. **Verify GitHub Pages targets.** Confirm that `https://transparency-certified.github.io/trov/0.1/trov.ttl` (and `.jsonld`, and the HTML index) serve the correct content.
2. **Test rewrite rules locally.** Run Apache in Docker with our `.htaccess` and verify redirects with `curl -v -H "Accept: text/turtle" http://localhost/trace/trov/0.1` etc.
3. **Post-merge smoke test.** After the w3id.org PR is merged, verify the live URLs return the expected 303 redirects.

---

## Adding a Page to the Specification

To add a new document to the specification site:

1. **Create the Markdown file** in `docs/`. For example, `docs/my-new-page.md`.

2. **Register it in `_toc.yml`.** Add a `- file: docs/my-new-page` entry under the appropriate part and chapter list. Without this entry, Jupyter Book will not include the page in the build even though the file exists in the repository.

   For example, to add it under TRACE Specifications:

   ```yaml
   - caption: TRACE Specifications
     chapters:
     - file: docs/specifications
     - file: docs/questions
     - file: docs/my-new-page    # ← new entry
   ```

3. **Push to `main`.** The GitHub Action will build the site and deploy the result to `gh-pages`. The new page will appear at `transparency-certified.github.io/trace-specification/docs/my-new-page.html`.

The build runs automatically. If the build fails (e.g., due to a syntax error or a broken cross-reference), the `gh-pages` branch is not updated and the live site remains unchanged. Check the Actions tab on the repository to see build status.
