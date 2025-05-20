**Week 10-13** As a test/demo of the my first blog entry for this site, a few
findings from the past few weeks and update on my current projects seemed
reasonable...

There are currently three major projects in the works:

- Metadata extraction and semantic search for criminal investigations (CCIQ)
- Unsupervised sentence summarization/compression
- Coreference resolution
  ([CorefUD 1.1](https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-5053))

And of course, this blog, along with a new birthday page for the institute:
<https://idi-birthday.web.app/> for the past two days.

Focus has primarily been on Project 1, CCIQ.

The core finding has been that Event Extraction (EE) and similar fields are
largely undefined and have little practical use in terms of criminal cases, as
there are _no ground truths_. When data is based on claimed facts, treating
these as events may not necessarily be correct, and thus needs to be accounted
for. The act of detecting them is interesting, but from previous police work, a
solid foundation for semantic search has seemed to be a better fit - as we can
then search for meanings behind a claimed fact.

[Maarten Grootendorst](https://www.maartengrootendorst.com/) has done
interesting work on the field, and is behind OSS like
[BERTopic](https://github.com/MaartenGr/BERTopic).

When investigating some use-cases for EE, before disregarding further
developments, the following papers were considered:

- [Beyond Bag-of-Concepts: Vectors of Locally
  Aggregated Concepts](https://arxiv.org/pdf/2205.01376v1.pdf)
- [A Survey on Deep Learning Event Extraction:
  Approaches and Applications](https://arxiv.org/pdf/2107.02126.pdf)
- [R2E: Rule-based Event Extractor](https://ceur-ws.org/Vol-1211/paper10.pdf)
- [Textual Entailment for Event Argument Extraction:
  Zero- and Few-Shot with Multi-Source Learning](https://arxiv.org/pdf/2205.01376v1.pdf) -
  Along with the github page: <https://github.com/osainz59/Ask2Transformers>
- [Towards High Performance Multilingual Event Extraction:
  Language Specific Issue and Feature Exploration](https://blender.cs.illinois.edu/paper/hlt09-event.pdf)
- [CLEVE: Contrastive Pre-training for Event Extraction](https://bakser.github.io/files/ACL21-CLEVE/CLEVE.pdf)
- [EventGraph: Event Extraction as Semantic Graph Parsing](https://arxiv.org/pdf/2210.08646.pdf) -
  **HIGHLY relevant**

![2023-03-31T22:20:36.728Z.png](https://firebasestorage.googleapis.com/v0/b/toffel.appspot.com/o/images%2F2023-03-31T22%3A20%3A36.728Z.png?alt=media&token=db48ffed-4c92-4bf9-8a17-40c574391756)
