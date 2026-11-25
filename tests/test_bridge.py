import unittest
import bridge

class GitBridgeTests(unittest.TestCase):
    def test_push_requires_approval(self):
        self.assertFalse(bridge.push('overleaf',False)['ok'])
    def test_bad_remote_rejected(self):
        self.assertFalse(bridge.fetch('--evil')['ok'])

if __name__ == '__main__':
    unittest.main()
