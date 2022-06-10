import unittest
from datetime import date, datetime
from unittest import mock

from models.mail import fetchMails
class TestMail(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        
    def test_fetch_mails(self):
        self.assertGreaterEqual(len(fetchMails()),1)
    
    
            

    

if __name__ == '__main__':
    unittest.main()