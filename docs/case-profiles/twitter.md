(caseprofile-twitter)=
# Twitter

Twitter provides access to data for [Academic
Research](https://developer.twitter.com/en/products/twitter-api/academic-research).
The Twitter [Developer Agreement and
Policy](https://developer.twitter.com/en/developer-terms/agreement-and-policy)
includes the following content redistribution policy:

> If you provide Twitter Content to third parties, including downloadable
  datasets or via an API, you may only distribute Tweet IDs, Direct Message IDs,
  and/or User IDs (except as described below). We also grant special permissions
  to academic researchers sharing Tweet IDs and User IDs for non-commercial
  research purposes.

Additionally:

> Academic researchers are permitted to distribute an unlimited number of Tweet
  IDs and/or User IDs if they are doing so on behalf of an academic institution
  and for the sole purpose of non-commercial research. For example, you are
  permitted to share an unlimited number of Tweet IDs for the purpose of
  enabling peer review or validation of your research. 

Finally:

> If Twitter Content is deleted, gains protected status, or is otherwise
> suspended, withheld, modified, or removed from the Twitter Applications
> (including removal of location information), you will make all reasonable
> efforts to delete or modify such Twitter Content (as applicable) as soon as
> possible

Since researchers are only able to redistribute Tweet IDs and content may be
deleted or modified, it is not possible to guarantee that the data used by the
original authors is available for research transparency and reproducibility.

Twitter does not advertise services to preserve datasets used in published
research.

## TRACE and Twitter 

### Retaining a private copy 

Because the policy applies to third-party redistribution, it is possible for the
researcher or research team to retain a copy of the original data, but it would
need to be treated as protected/confidential information. Using this approach, a
researcher could archive the original Twitter content used and only allow access
to approved researchers.

### Retaining information about the data

An alternative approach is to redistribute only the Tweet IDs, but provide
identifiable information about the full dataset used. This includes the filename
used in scripts along with metadata, such as a hash, that can be used determine
whether a "re-hydrated" dataset matches the original.

### Examples

See [Twitter](example-twitter) examples.
