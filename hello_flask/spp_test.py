import unittest
from app import app, my_autocorrect3

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_my_autocorrect3(self):
        sentence = 'iman'
        corrected_sentence = my_autocorrect3(sentence)
        self.assertEqual(corrected_sentence, 'imana')
        
        sentence = 'irem isi'
        corrected_sentence = my_autocorrect3(sentence)
        self.assertEqual(corrected_sentence, 'irema isi')
        
        sentence = 'umwam'
        corrected_sentence = my_autocorrect3(sentence)
        self.assertEqual(corrected_sentence, 'umwami')
        
        sentence = 'iman irem is'
        corrected_sentence = my_autocorrect3(sentence)
        self.assertEqual(corrected_sentence, 'imana irema isi')
        
    def test_home_post(self):
        response = self.client.post('/', data={'msg': 'iman irem is'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'imana irema isi', response.data)
        
        response = self.client.post('/', data={'msg': 'iman'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'imana', response.data)
        
        response = self.client.post('/', data={'msg': 'irem'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'irema', response.data)
        
        response = self.client.post('/', data={'msg': 'umwam'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'umwami', response.data)
        
if __name__ == '__main__':
    unittest.main()
