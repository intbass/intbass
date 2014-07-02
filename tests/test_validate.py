from nose.tools import eq_, raises
import unittest
from app import validate


class TestEmail(unittest.TestCase):
    def test_valid(self):
        eq_(validate.email('example@example.com'), 'example@example.com')

    def test_validnumbers(self):
        eq_(validate.email('example123@example.com'), 'example123@example.com')

    def test_normalisedomain(self):
        eq_(validate.email('example@eXample.cOm'), 'example@example.com')

    def test_leavelocalpart(self):
        eq_(validate.email('eXample@eXample.cOm'), 'eXample@example.com')

    def test_punycode(self):
        eq_(validate.email('example@xn--bcher-kva.ch'),
            'example@xn--bcher-kva.ch')

    def test_shortdomain(self):
        eq_(validate.email('example@c.je'),
            'example@c.je')

    @raises(AssertionError)
    def test_invalid(self):
        validate.email('example')

    @raises(AssertionError)
    def test_nolocalpart(self):
        validate.email('@example.com')

    @raises(AssertionError)
    def test_nodomain(self):
        validate.email('example@')

#    @raises(AssertionError)
    def test_invaliddomain(self):
        validate.email('example@a')
