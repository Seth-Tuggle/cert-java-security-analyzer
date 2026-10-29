# CERT Java Security Analyzer

A CS645 prototype that collects referenced CERT Java secure coding rules and
uses that knowledge as context for LLM-assisted review of Java source. Example
Java files illustrate format injection, hardcoded passwords, and resource handling.

## Setup

Install `requirements.txt`, then set your own `OPENAI_API_KEY` (or use a local
`.env` file). Run `python setup_rag_system.py` to fetch the referenced rules and
build the local knowledge base; this uses network access and a paid embedding API.
Then run `python analyze_java_code.py` for the interactive analyzer.

The retrieved standards and indices are generated locally and excluded from
version control. Rule identifiers and source URLs are retained in `CodingRules.txt`.
CERT standards belong to their respective authors; this repository does not
relicense them. No external API was called during recovery.

## Implementation scope

Although the setup script builds embeddings, the analyzer currently assembles
context from the whole loaded knowledge base rather than retrieving top-k vector
matches. It is a knowledge-grounded prototype, not a sound/static compliance
checker. Findings require human review. Any hardcoded password in the tiny
vulnerability example is deliberately a fake example, not a working credential.
