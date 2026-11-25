"""Claude/Codex MCP server for safe editing of a local LaTeX project."""
from mcp.server.fastmcp import FastMCP
import engine
import bridge

mcp = FastMCP(
    "DietSense LaTeX Editor",
    instructions=(
        "Read the requested section or file, preview a minimal change, show the diff and "
        "ask the user for approval before applying. Compile and inspect warnings after editing. "
        "Do not push remote Git or Overleaf changes without explicit user approval. "
        "Never fabricate experimental results or references."
    ),
)

@mcp.tool()
def list_paper_sections() -> list[dict]:
    """List editable document sections, abstract and index terms."""
    return [{'level': 'environment', 'title': 'abstract'},
            {'level': 'environment', 'title': 'keywords'}] + engine.list_sections()

@mcp.tool()
def read_paper_section(section: str) -> str:
    """Read a section by exact title, or 'abstract' or 'keywords'."""
    return engine.read_section(section)

@mcp.tool()
def search_paper_text(phrase: str) -> dict:
    """Search in main.tex, returning a count and contexts."""
    return engine.find_text(phrase)

@mcp.tool()
def preview_section_edit(section: str, replacement_latex: str) -> dict:
    """Preview whole-section replacement. NEVER changes files."""
    return engine.preview_replacement(section, replacement_latex)

@mcp.tool()
def apply_section_edit(section: str, replacement_latex: str, preview_sha256: str) -> dict:
    """After user approval, apply the previewed section edit and save a backup."""
    return engine.apply_replacement(section, replacement_latex, preview_sha256)

@mcp.tool()
def compile_and_diagnose() -> dict:
    """Compile with pdflatex (no shell escape), inspect warnings and return PDF path."""
    return engine.compile_pdf()

@mcp.tool()
def restore_backup(backup_id: str) -> dict:
    """After approval, roll back main.tex to a saved backup."""
    return engine.rollback(backup_id)

@mcp.tool()
def list_project_files() -> list[str]:
    """List allowed project files without exposing credentials or backups."""
    return engine.list_project_files()

@mcp.tool()
def read_project_file(relative_path: str) -> dict:
    """Read a project-local .tex/.bib/.sty/.cls/.md/.txt file."""
    return engine.read_project_file(relative_path)

@mcp.tool()
def git_sync_status() -> dict:
    """Read-only Git status, current branch and remote names in the LaTeX project."""
    return bridge.git_status()

@mcp.tool()
def git_fetch_remote(remote_name: str = 'overleaf') -> dict:
    """Explicitly fetch a configured Git remote; does not merge, commit or push."""
    return bridge.fetch(remote_name)

@mcp.tool()
def git_push_to_overleaf(remote_name: str, approved: bool = False) -> dict:
    """Push to a configured Overleaf Git remote ONLY when approved=True; never commits."""
    return bridge.push(remote_name, approved)

if __name__ == '__main__':
    mcp.run(transport='stdio')
