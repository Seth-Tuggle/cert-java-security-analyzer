# CERT Java Security Analyzer

My CS645 prototype uses CERT Java secure coding rules as context for AI-assisted
code review. I use the included Java examples to explore issues such as format
injection, hardcoded passwords, and resource handling.

## Setup

Install `requirements.txt`, then set your own `OPENAI_API_KEY` in the environment
or a local `.env` file.

```bash
python setup_rag_system.py
python analyze_java_code.py
```

The setup script fetches the referenced rules and builds a local knowledge base.
It needs network access and uses a paid embedding API. The second command starts
the interactive analyzer, which also uses your API account for code review.

I keep the generated knowledge base and indices out of version control.
`CodingRules.txt` contains the rule identifiers and source URLs.

## Current limitations

The setup script builds embeddings, but the analyzer currently supplies context
from the whole loaded knowledge base instead of retrieving the closest vector
matches. I treat its findings as suggestions to review, not proof that code is
secure or compliant.

The hardcoded password in the small vulnerability example is deliberately fake;
it isn't a working credential.

## Ownership

For details about my contributions and project attribution, see [CREDITS.md](CREDITS.md).
