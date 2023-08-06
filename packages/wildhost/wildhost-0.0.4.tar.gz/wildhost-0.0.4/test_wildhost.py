from unittest import TestCase, mock

import wildhost


class TestWildhost(TestCase):
    'Tests the `wildhost` module. Some of the tests are functional tests and need to contact a DNS server.'

    def setUp(self):
        wildhost.ws.clear()

    def test_gen(self):
        got = list(wildhost.gen('foo.bar.spam.com'))
        expected = [
            'spam.com',
            'bar.spam.com',
            'foo.bar.spam.com',
        ]
        assert got == expected

    def test_resolves_valid(self):
        assert wildhost.resolves('google.com')

    def test_resolves_invalid(self):
        assert not wildhost.resolves('xxxx.google.com')

    def test_resolves_random(self):
        assert not wildhost.resolves_random('google.com')

    def test_check_fresh(self):
        assert not wildhost.check_fresh('mail.google.com')

    def test_check_cache(self):
        wildhost.ws.add('google.com')
        assert wildhost.check_cache('mail.google.com')
        assert not wildhost.check_cache('mail.yahoo.com')

    def test_not_wildcard(self):
        with mock.patch('wildhost.check_fresh') as check_fresh, mock.patch('wildhost.check_cache') as check_cache:
            check_cache.return_value = None
            check_fresh.return_value = None
            assert not wildhost.check('sub.domain.tld')
            assert check_cache.called
            assert check_fresh.called

    def test_wildcard_not_cached(self):
        with mock.patch('wildhost.check_fresh') as check_fresh, mock.patch('wildhost.check_cache') as check_cache:
            check_cache.return_value = None
            check_fresh.return_value = 'domain.tld'
            assert wildhost.check('sub.domain.tld')
            assert check_cache.called
            assert check_fresh.called

    def test_wildcard_cached(self):
        with mock.patch('wildhost.check_fresh') as check_fresh, mock.patch('wildhost.check_cache') as check_cache:
            check_cache.return_value = 'domain.tld'
            assert wildhost.check('sub.domain.tld')
            assert check_cache.called
            assert not check_fresh.called

    def test_wildcard_invalid(self):
        assert not wildhost.check('xxxx.google.com')
