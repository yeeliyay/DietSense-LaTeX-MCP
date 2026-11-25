"""Optional git bridge. Does not implement Overleaf private web APIs."""
import subprocess
import shutil
import re
import engine


def _git(*args: str) -> dict:
    if shutil.which('git') is None:
        return {'ok': False, 'error': 'Git not installed'}
    try:
        p=subprocess.run(['git','-C',str(engine.ROOT),*args],capture_output=True,text=True,
                         timeout=25,check=False,env=None)
        # Never leak credential-bearing remote URLs in output.
        output=((p.stdout or '')+'\n'+(p.stderr or ''))[-3500:]
        output=re.sub(r'https?://[^@\s]+@', 'https://[REDACTED]@',output)
        return {'ok':p.returncode==0,'output':output.strip(),'returncode':p.returncode}
    except subprocess.TimeoutExpired:
        return {'ok':False,'error':'git timed out'}


def git_status() -> dict:
    status=_git('status','--short','--branch')
    remotes=_git('remote')
    return {'status':status,'remote_names':remotes.get('output','').splitlines() if remotes.get('ok') else []}


def _remote_ok(remote: str) -> bool:
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9._-]{0,40}',remote):
        return False
    names=_git('remote')
    return names.get('ok',False) and remote in names.get('output','').splitlines()


def fetch(remote_name: str) -> dict:
    if not _remote_ok(remote_name):
        return {'ok':False,'error':'Unknown or invalid Git remote name'}
    return _git('-c','credential.interactive=never','fetch',remote_name)


def push(remote_name: str, approved: bool=False) -> dict:
    if not approved:
        return {'ok':False,'error':'Explicit user approval required: approved=True'}
    if not _remote_ok(remote_name):
        return {'ok':False,'error':'Unknown or invalid Git remote name'}
    if remote_name.lower()!='overleaf':
        return {'ok':False,'error':'Only remote named overleaf may be pushed by this tool'}
    status=_git('status','--porcelain')
    if not status.get('ok') or status.get('output'):
        return {'ok':False,'error':'Working tree must be clean; review and commit changes manually first'}
    return _git('-c','credential.interactive=never','push',remote_name,'HEAD')
