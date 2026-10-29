# CERT Java Security Analyzer

## Historical coursework

I'm preserving this older CS645 prototype to explain the project and keep its
main code available. I'm not maintaining it for standalone use. The original
class configuration, API access, and dependency versions may be needed, and
parts may now be outdated or deprecated.

## About the project

My prototype uses CERT Java secure coding rules as context for AI-assisted code
review. I use the included Java examples to explore format injection, hardcoded
passwords, and resource handling.

- `setup_rag_system.py`: downloads the referenced rule text and saves a local
  JSON knowledge base.
- `analyze_java_code.py`: sends Java source and rule context to the review API.
- `CodingRules.txt`: rule identifiers and source URLs.
- The small Java examples: deliberately vulnerable inputs for the exercise.

## Original environment and limitations

The project uses Python, network access to the rule sources, and an OpenAI API
account for code review. The saved knowledge base is generated locally and isn't
included in version control. The original setup also initializes an API client,
so it expects that configuration even though downloading the rules doesn't use
an embedding API.

The setup script does not build embeddings or a vector index. The analyzer
supplies context from the whole loaded knowledge base instead of retrieving
nearest vector matches. I treat its findings as suggestions, not proof that code
is secure or compliant. The password in the vulnerability example is intentionally
fake.

## Ownership

For details about my contributions and project attribution, see [CREDITS.md](CREDITS.md).
