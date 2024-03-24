from unittest.mock import patch

import pytest

from handlers.rule_handler import load_collections, is_valid_rule, generate_condition, generate_sql_query_for_rules


class TestLoadCollections:
    @pytest.fixture
    def mock_rules_schema(self):
        return {'field': 'value'}

    def test_load_collections(self, mock_rules_schema):
        with patch('handlers.rules.RULES_SCHEMA', mock_rules_schema):
            collections = load_collections()
            assert collections == {'field': 'value'}


class TestIsValidRule:
    @pytest.mark.parametrize("rule, expected", [
        ({"field_name": "received_at", "predicate": "greater_than_days", "value": "2"}, True),
        ({"field_name": "received_at", "predicate": "less_than_days", "value": "3"}, True),
        ({"field_name": "received_at", "predicate": "equals", "value": "2024-03-21"}, False),
        ({"field_name": "received_at", "predicate": "greater_than_days", "value": "abc"}, False),
        ({"field_name": "sender", "predicate": "contains", "value": "example"}, True),
        ({"field_name": "sender", "predicate": "equals", "value": "example"}, True),
        ({"field_name": "sender", "predicate": "does_not_contain", "value": "example"}, True),
        ({"field_name": "sender", "predicate": "invalid_predicate", "value": "example"}, False),
    ])
    def test_is_valid_rule(self, rule, expected):
        assert is_valid_rule(rule) == expected


class TestGenerateCondition:
    @pytest.mark.parametrize("field_name, sql_operator, value, expected", [
        ("sender", "LIKE", "example", "sender LIKE '%example%'"),
        ("sender", "NOT LIKE", "example", "sender NOT LIKE '%example%'"),
        ("received_at", ">", "2", "date(received_at) > date('now', '-2 days')"),
        ("received_at", "<", "3", "date(received_at) < date('now', '-3 days')"),
        ("subject", "=", "Test Subject", "subject = 'Test Subject'"),
        ("message", "!=", "Test Message", "message != 'Test Message'"),
    ])
    def test_generate_condition(self, field_name, sql_operator, value, expected):
        assert generate_condition(field_name, sql_operator, value) == expected


class TestGenerateSQLQueryForRules:
    @pytest.mark.parametrize("collections, expected_query", [
        (
            {
                "collection_predicate": "all",
                "rules": [
                    {"field_name": "sender", "predicate": "contains", "value": "example"},
                    {"field_name": "received_at", "predicate": "greater_than_days", "value": "2"}
                ]
            },
            "SELECT message_id FROM emails WHERE sender LIKE '%example%' AND date(received_at) > date('now', '-2 days')"
        ),
        (
            {
                "collection_predicate": "any",
                "rules": [
                    {"field_name": "subject", "predicate": "equals", "value": "Test Subject"},
                    {"field_name": "message", "predicate": "does_not_contain", "value": "spam"}
                ]
            },
            "SELECT message_id FROM emails WHERE subject = 'Test Subject' OR message NOT LIKE '%spam%'"
        ),
    ])
    def test_generate_sql_query_for_rules(self, collections, expected_query):
        assert generate_sql_query_for_rules(collections) == expected_query

    def test_invalid_rules(self):
        # Test case for invalid rule (to ensure it's skipped)
        collections = {
            "collection_predicate": "all",
            "rules": [
                {"field_name": "invalid_field", "predicate": "invalid_predicate", "value": "value"}
            ]
        }
        assert generate_sql_query_for_rules(collections) is None

