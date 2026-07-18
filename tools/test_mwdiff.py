import unittest
from mwdiff import norm, fn_diff

class TestMwDiff(unittest.TestCase):
    def test_norm(self):
        # Test normalization patterns
        lines = [
            "/* 0x10 */ li r3, 0",
            ".L100: li r4, 1",
            "li r5, @123",
            "li r6, $456",
            "lis r7, ...rodata.0@h",
            "  addi r8, r8, 1  ", # whitespace
            ".section" # should be dropped
        ]
        # Expected:
        # li r3, 0
        # li r4, 1
        # li r5, @N
        # li r6, $N
        # lis r7, @N@h
        # addi r8, r8, 1
        expected = [
            "li r3, 0",
            "li r4, 1",
            "li r5, @N",
            "li r6, $N",
            "lis r7, @N@h",
            "addi r8, r8, 1"
        ]
        self.assertEqual(norm(lines), expected)

    def test_fn_diff(self):
        a = ["li r3, 0", "li r4, 1"]
        b = ["li r3, 0", "li r4, 2"]
        diff = fn_diff(a, b)
        # unified_diff produces lines like '- li r4, 1' and '+ li r4, 2'
        self.assertTrue(any("-li r4, 1" in line for line in diff), f"Missing -li r4, 1 in {diff}")
        self.assertTrue(any("+li r4, 2" in line for line in diff), f"Missing +li r4, 2 in {diff}")
        
        # Test identical
        self.assertEqual(fn_diff(a, a), [])

if __name__ == '__main__':
    unittest.main()
