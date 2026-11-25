"""Guarded LaTeX operations: project-local, back up changes, and compile safely."""
from __future__ import annotations
import difflib
import hashlib
import os
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("LATEX_PROJECT_ROOT", Path(__file__).parent / 'project')).expanduser().resolve()
MAIN = ROOT / 'main.tex'
BACKUPS = ROOT / '.mcp_backups'
SECTION_PATTERN = re.compile(r'(?m)^\\(section|subsection|subsubsection)\*?\{([^}\n]+)\}')
ABSTRACT_PATTERN = re.compile(r'(?s)(\\begin\{abstract\})(.*?)(\\end\{abstract\})')
KEYWORD_PATTERN = re.compile(r'(?s)(\\begin\{IEEEkeywords\})(.*?)(\\end\{IEEEkeywords\})')

def _read() -> str:
    if not MAIN.is_file():
        raise FileNotFoundError(f"Missing project main.tex: {MAIN}")
    return MAIN.read_text(encoding='utf-8')

def _safe_name(name: str) -> str:
    if name not in ('abstract', 'keywords') and not any(n == name for _, n in sections()):
        raise ValueError(f"Unknown section {name!r}. Call list_sections first.")
    return name

def sections() -> list[tuple[str,str]]:
    return [(m.group(1), m.group(2)) for m in SECTION_PATTERN.finditer(_read())]

def list_sections() -> list[dict]:
    return [{'level':level, 'title': title} for level,title in sections()]

def _scope(text: str, name: str) -> tuple[int,int]:
    if name in ('abstract','keywords'):
        m = (ABSTRACT_PATTERN if name == 'abstract' else KEYWORD_PATTERN).search(text)
        if not m: raise ValueError(f"No {name} environment in main.tex")
        return m.start(2),m.end(2)
    matches = list(SECTION_PATTERN.finditer(text))
    selected = next((i for i, m in enumerate(matches) if m.group(2) == name), None)
    if selected is None: raise ValueError(f"Unknown heading: {name}")
    start_match=matches[selected]
    rank={'section':1,'subsection':2,'subsubsection':3}
    current_rank=rank[start_match.group(1)]
    end=next((m.start() for m in matches[selected+1:] if rank[m.group(1)] <= current_rank), text.find('\\begin{thebibliography}',start_match.end()))
    if end == -1: end=len(text)
    return start_match.end(),end

def read_section(name: str) -> str:
    text=_read(); start,end=_scope(text,_safe_name(name)); return text[start:end].strip()

def preview_replacement(name: str, replacement: str) -> dict:
    text=_read(); start,end=_scope(text,_safe_name(name))
    if not replacement.strip(): raise ValueError('Empty replacement rejected')
    updated=text[:start]+'\n'+replacement.strip()+'\n'+text[end:]
    diff=''.join(difflib.unified_diff(text.splitlines(True),updated.splitlines(True),fromfile='current/main.tex',tofile='proposed/main.tex'))
    return {'section':name,'base_sha256':hashlib.sha256(text.encode()).hexdigest(),'diff':diff[:24000],'truncated':len(diff)>24000}

def apply_replacement(name: str,replacement: str,expected_sha256: str) -> dict:
    text=_read(); digest=hashlib.sha256(text.encode()).hexdigest()
    if digest != expected_sha256:
        raise ValueError('File changed since preview. Preview again before applying.')
    start,end=_scope(text,_safe_name(name))
    if not replacement.strip():raise ValueError('Empty replacement rejected')
    new=text[:start]+'\n'+replacement.strip()+'\n'+text[end:]
    BACKUPS.mkdir(parents=True,exist_ok=True)
    backup=BACKUPS/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.tex')
    backup.write_text(text,encoding='utf-8')
    tmp=MAIN.with_suffix('.tex.tmp');tmp.write_text(new,encoding='utf-8');tmp.replace(MAIN)
    return {'changed': True,'backup_id':backup.name,'new_sha256':hashlib.sha256(new.encode()).hexdigest()}

def rollback(backup_id: str) -> dict:
    if not re.fullmatch(r'\d{8}T\d{12}Z\.tex',backup_id): raise ValueError('Invalid backup ID')
    backup=BACKUPS/backup_id
    if not backup.is_file(): raise ValueError('Backup does not exist')
    current=_read(); name=BACKUPS/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.tex')
    name.write_text(current,encoding='utf-8')
    shutil.copyfile(backup,MAIN)
    return {'restored':backup_id,'previous_current_saved_as':name.name}

def compile_pdf() -> dict:
    _read()
    if not shutil.which('pdflatex'):
        return {'ok':False,'error':'pdflatex not found. Install TeX Live or MiKTeX.'}
    # No shell=True or -shell-escape. Prevent latexmkrc hooks by using pdflatex directly.
    build=ROOT/'.mcp_build'
    build.mkdir(parents=True,exist_ok=True)
    command=['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory='+str(build),'main.tex']
    try:
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=90,check=False,env={**os.environ,'openout_any':'p','shell_escape':'f'})
        if result.returncode == 0:
            result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=90,check=False,env={**os.environ,'openout_any':'p','shell_escape':'f'})
    except subprocess.TimeoutExpired:
        return {'ok':False,'error':'Compilation timed out (90 seconds)' }
    output=(result.stdout or '')+'\n'+(result.stderr or '')
    log=(build/'main.log').read_text(encoding='utf-8',errors='replace') if (build/'main.log').exists() else output
    signals=[ln.strip() for ln in log.splitlines() if re.search(r'(Overfull \\hbox|Underfull \\hbox|LaTeX Warning|Package .* Warning|^!|Undefined control sequence|Missing \$ inserted)',ln)]
    return {'ok':result.returncode==0,'pdf':str(build/'main.pdf') if (build/'main.pdf').exists() else None,'warnings':signals[:35], 'last_output':output[-3500:]}

def find_text(needle: str) -> dict:
    if not needle or len(needle)<2:raise ValueError('Provide at least 2 characters')
    text=_read(); matches=[i for i in range(len(text)) if text.startswith(needle,i)]
    return {'matches':len(matches),'contexts':[text[max(i-120,0):min(i+len(needle)+120,len(text))] for i in matches[:10]]}


_ALLOWED_READ_SUFFIXES={'.tex','.bib','.sty','.cls','.md','.txt'}

def _project_file(relative_path: str) -> Path:
    if not relative_path or '\x00' in relative_path:
        raise ValueError('Invalid path')
    path=(ROOT/relative_path).resolve()
    if not path.is_relative_to(ROOT) or path.suffix.lower() not in _ALLOWED_READ_SUFFIXES:
        raise ValueError('Only supported text files inside the LaTeX project can be read')
    if any(part.startswith('.') for part in path.relative_to(ROOT).parts):
        raise ValueError('Hidden files are not accessible')
    return path

def list_project_files() -> list[str]:
    result=[]
    for path in ROOT.rglob('*'):
        if path.is_file():
            try:
                _project_file(str(path.relative_to(ROOT)))
            except ValueError:
                continue
            result.append(path.relative_to(ROOT).as_posix())
    return sorted(result)[:300]

def read_project_file(relative_path: str) -> dict:
    path=_project_file(relative_path)
    if not path.is_file():
        raise FileNotFoundError(relative_path)
    if path.stat().st_size>1_000_000:
        raise ValueError('File too large for MCP read')
    text=path.read_text(encoding='utf-8')
    return {'path':relative_path, 'content':text, 'sha256':hashlib.sha256(text.encode()).hexdigest()}
