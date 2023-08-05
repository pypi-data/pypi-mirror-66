from py.test import raises

from .models import Reporter
from ..registry import Registry
from ..types import PynamoObjectType


def test_should_raise_if_no_model():
    with raises(AssertionError) as excinfo:
        class Character1(PynamoObjectType):
            pass
    assert 'valid PynamoDB Model' in str(excinfo.value)


def test_should_raise_if_model_is_invalid():
    with raises(AssertionError) as excinfo:
        class Character2(PynamoObjectType):
            class Meta:
                model = 1
    assert 'valid PynamoDB Model' in str(excinfo.value)


def test_should_map_fields_correctly():
    class ReporterType2(PynamoObjectType):
        class Meta:
            model = Reporter
            registry = Registry()

    expected_keys = [
        'articles',
        'first_name',
        'last_name',
        'email',
        'pets',
        'id',
        'favorite_article',
        'custom_map',
        'awards']
    assert all(item in expected_keys for item in ReporterType2._meta.fields.keys())


def test_should_map_only_few_fields():
    class Reporter2(PynamoObjectType):
        class Meta:
            model = Reporter
            only_fields = ('id', 'email')

    assert list(Reporter2._meta.fields.keys()) == ['email', 'id']
