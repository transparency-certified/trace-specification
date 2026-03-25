# TRACE Specification

The [TRACE](https://transparency-certified.github.io/) (TRAnsparency CErtified) specification defines how Transparent Research Objects (TROs) are declared, signed, and packaged for distribution. It is the primary documentation home for the TRACE project, funded by the National Science Foundation (OAC-2209628, OAC-2209629, OAC-2209630).

The documents in this repository are assembled into a [Jupyter Book](https://jupyterbook.org/) and published at **https://transparency-certified.github.io/trace-specification/**.

## Key specification pages

| Document | Description |
|----------|-------------|
| [TROV Vocabulary Reference](https://transparency-certified.github.io/trace-specification/docs/trov-vocabulary.html) | Terms defined by the TROV vocabulary |
| [TRO Declaration Format](https://transparency-certified.github.io/trace-specification/docs/tro-declaration-format.html) | Structure and field reference for TRO declarations |
| [TRO Packages](https://transparency-certified.github.io/trace-specification/docs/tro-packages.html) | How TROs are packaged, signed, and distributed |
| [TRO Declaration Design](https://transparency-certified.github.io/trace-specification/docs/tro-declaration-design.html) | Why TRO declarations use JSON-LD |
| [TROV Extension Guide](https://transparency-certified.github.io/trace-specification/docs/trov-extension-guide.html) | How to include institution-specific metadata |
| [TROV Versioning and Roadmap](https://transparency-certified.github.io/trace-specification/docs/trov-versioning-and-roadmap.html) | Version policy, namespace scheme, and roadmap |

## Repository structure

```
trace-specification/
├── _config.yml                  Jupyter Book configuration
├── _toc.yml                     Jupyter Book table of contents and navigation
├── _static/
│   └── custom.css               Custom styles for the published site
├── docs/                        Specification and documentation source files
├── build/
│   ├── run_docker.sh            Runs Jupyter Book build in Docker
│   └── config.sh                Build configuration
├── .github/workflows/
│   └── deploy.yml               builds and deploys to GitHub Pages
├── references.bib               BibTeX references
├── requirements.txt             Python dependencies for Jupyter Book
├── Makefile                     Jupyter Book build targets
└── test.sh                      Build script for local testing
```

## Related repositories

| Repository | Description |
|------------|-------------|
| [trov](https://github.com/transparency-certified/trov) | TROV ontology files (Turtle, JSON-LD, SHACL) |
| [trace-vocabularies](https://github.com/transparency-certified/trace-vocabularies) | Vocabulary hub with w3id.org redirects and Widoco builds |
| [transparency-certified.github.io](https://github.com/transparency-certified/transparency-certified.github.io) | Project website |

## Building locally

Using the Docker-based build (same image as CI):

```bash
./build/run_docker.sh test.sh
```

Or with `jupyter-book` installed locally:

```bash
./test.sh
```

See [.github/workflows/deploy.yml](.github/workflows/deploy.yml) for the full build process.

## License

Content is licensed under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).
