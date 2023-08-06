import unittest
from vetmanager.domain import DomainProd, DomainLocal, DomainTest


class TestDomain(unittest.TestCase):

    def test_prod_url(self):
        domain = DomainProd('tests')
        self.assertEqual(
            domain.url(),
            'https://tests.vetmanager.ru'
        )

    def test_test_url(self):
        domain = DomainTest('tests')
        self.assertEqual(
            domain.url(),
            'https://tests.tests.kube-dev.vetmanager.cloud'
        )

    def test_local_url(self):
        domain = DomainLocal('tests')
        self.assertEqual(domain.url(), 'http://tests.localhost:8080')


if __name__ == '__main__':
    unittest.main()
