import unittest
import textAnalyzer

class TestStringMethods(unittest.TestCase):
    def test1(self):
        text = 'Python programming — text and web mining\n\nFinn'
        counter = textAnalyzer.count_words(text)
        self.assertEqual(len(counter), 7)
        self.assertTrue(counter['python'] == 1)
        self.assertTrue(counter['programming'] == 1)
        self.assertTrue(counter['text'] == 1)
        self.assertTrue(counter['and'] == 1)
        self.assertTrue(counter['web'] == 1)
        self.assertTrue(counter['mining'] == 1)
        self.assertTrue(counter['finn'] == 1)
        self.assertTrue(counter['—']==0)

    def testPdfRead(self):
        file_path = 'test.pdf'
        (content, page_count) = textAnalyzer.get_pdf_file_content(file_path)
        self.assertEqual(page_count, 2)
        self.assertTrue(content and len(content) > 0)

if __name__ == '__main__':
    unittest.main()