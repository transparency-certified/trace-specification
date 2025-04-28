# TRACE Toolkit

The TRACE toolkit is a collection of Python libraries/packages that implements the TRACE
specification. 

## `tro-utils`

[tro-utils](https://github.com/transparency-certified/tro-utils)
is a Python package that provides utilities for working with
transparent Research Objects (TROs). It is designed to be used in conjunction with the
[TRO specification](./specifications/tro/0.1/index.md). The package includes following functions:
  

* `verify` - Verify the integrity of a TRO (i.e. it was signed and timestamped
  correctly).
* `arrangement` - Manages arrangements in the TRO. It has subcommands like `add`
  (adds a directory as a composition to the TRO) and `list` (lists available arrangements in the TRO).
* `composition` - Manages compositions in the TRO. It has subcommands like `info`
  that gets information about a current composition in the TRO.
* `performance` - Manages performance in the TRO. It has subcommands like `add`
  (adds a performance to the TRO).
* `sign` - Signs a TRO with a given key.
* `report` - Generates a report from a TRO.

## `trace-bdbag`

`trace-bdbag` package:
* Create and sign TRO

## `trace-prototype`

[trace-prototype](https://github.com/transparency-certified/trace-prototype) is a
an expansion of the proof-of-concept for containerized execution outside of [Whole Tale](https://wholetale.org).

It consists of a simple Docker-based job execution service utilizing REST API that's capable of

* Running jobs in a containerized environment.
* Generating compute environment using repo2docker.
* Configuring TRO claims.
* Generating TROs using BagIt and signing them with GPG.

and a command-line interface for uploading jobs and downloading TROs from the server.
