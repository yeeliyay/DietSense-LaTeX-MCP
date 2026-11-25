# Development

## Tests

```bash
python -m unittest discover -s tests -v
python -m compileall -q server.py engine.py bridge.py
```

## Local build

```bash
cd project
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

`server.py` needs the `mcp` Python package; `engine.py` and `bridge.py` use the standard library.

## Future work
- Support `\input{}` trees and section-addressing across many files.
- Real PDF-page rendering with image analysis and diff-to-source mapping.
- `.bib` and figure modifications with the same preview/backup protection.
- Optional structured citations validation and reference integrity checks.
