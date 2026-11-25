import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import engine

class TestEngine(unittest.TestCase):
 def test_safe_targeted_edit_and_restore(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)
   sample=r'''\documentclass{article}
\begin{document}
\begin{abstract}
Original summary.
\end{abstract}
\section{Introduction}
Before text.
\section{Methods}
Leave methods unchanged.
\end{document}
'''
   (root/'main.tex').write_text(sample,encoding='utf-8')
   with patch.object(engine,'ROOT',root),patch.object(engine,'MAIN',root/'main.tex'),patch.object(engine,'BACKUPS',root/'.mcp_backups'):
    self.assertIn('Before text.',engine.read_section('Introduction'))
    p=engine.preview_replacement('Introduction','New text.')
    self.assertIn('+New text.',p['diff'])
    saved=engine.apply_replacement('Introduction','New text.',p['base_sha256'])
    self.assertIn('Leave methods unchanged.',(root/'main.tex').read_text())
    with self.assertRaises(ValueError): engine.apply_replacement('Introduction','anything',p['base_sha256'])
    engine.rollback(saved['backup_id'])
    self.assertEqual((root/'main.tex').read_text(),sample)

 def test_path_traversal_rejected(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)
   with patch.object(engine,'ROOT',root):
    with self.assertRaises(ValueError):engine.read_project_file('../credentials.txt')

if __name__=='__main__':unittest.main()
