import unittest
from extract import extract_title

class TestExtract(unittest.TestCase):
    def test_extract(self):
        md = """
## Countries

- Slovenia
- Croatia
- Serbia
- Montenegro
- Bosnia

# Song

1. here comes the
2. to the
3. to the
4. something something floor
"""
        extract = extract_title(md)
        self.assertEqual(extract, "Song")

    def test_extract_exception(self):
        md = """
## Countries

- Slovenia
- Croatia
- Serbia
- Montenegro
- Bosnia

### Song

1. here comes the
2. to the
3. to the
4. something something floor
"""
        with self.assertRaises(Exception) as context:
            extract = extract_title(md)
            self.assertEqual(str(context.exception), "no header!")
