import unittest
from collections import defaultdict
from find_unused import get_all_unused_methods

# The program currently doesn't handle recursive functions, so if this fails it might be ok!
class TestFindUnused(unittest.TestCase):

    def test_example_app_py(self):
        self.assertDictEqual(get_all_unused_methods(["example/app.py"]), defaultdict(list, {'example/app.py': ['unused_func0']}))
    def test_example_demo_py(self):
        self.assertDictEqual(get_all_unused_methods(["example/demo.py"]), defaultdict(list, {'example/demo.py': ['unused_func1', 'used_func1']}))
    def test_example_demo2_py(self):
        self.assertDictEqual(get_all_unused_methods(["example/demo2.py"]), defaultdict(list, {'example/demo2.py': ['unused_func2', 'unused_func3', 'unused_func4', 'used_func4', 'used_func2']}))
    def test_example_all_py(self):
        self.assertDictEqual(get_all_unused_methods(["example/app.py", "example/demo.py", "example/demo2.py"]), defaultdict(list, {'example/app.py': ['unused_func0'], 'example/demo2.py': ['unused_func2', 'unused_func3', 'unused_func4'], 'example/demo.py': ['unused_func1']}))

unittest.main(verbosity=2)
