from adapters.google_adapter import mark_as_read, mark_as_unread
from schema.connection import get_connection

SQL_OPERATORS = {
    'contains': 'LIKE',
    'does_not_contain': 'NOT LIKE',
    'equals': '=',
    'does_not_equal': '!=',
    'less_than_days': '<',
    'greater_than_days': '>'
}


def load_collections():
    from handlers.rules import RULES_SCHEMA
    return RULES_SCHEMA


def is_valid_rule(rule):
    field_name = rule.get('field_name')
    predicate = rule.get('predicate')
    value = rule.get('value')

    if field_name == 'received_at':
        if predicate not in ['greater_than_days', 'less_than_days']:
            return False
        try:
            int(value)
        except ValueError:
            return False

    if field_name in ['sender', 'subject', 'message']:
        if predicate not in ['contains', 'does_not_contain', 'equals', 'does_not_equal']:
            return False

    return True


def generate_condition(field_name, sql_operator, value):
    if sql_operator in ["LIKE", "NOT LIKE"]:
        condition = f"{field_name} {sql_operator} '%{value}%'"

    elif sql_operator in ['>', '<'] and field_name == "received_at":
        condition = f"date({field_name}) {sql_operator} date('now', '-{value} days')"

    else:
        condition = f"{field_name} {sql_operator} '{value}'"

    return condition


def generate_sql_query_for_rules(collections):
    conditions = []
    sql_query = "SELECT message_id FROM emails WHERE "
    rules = collections.get('rules')
    collection_predicate = collections.get('collection_predicate')

    for rule in rules:
        if not is_valid_rule(rule):
            print(f"{rule} is not valid")
            continue

        field_name = rule.get('field_name')
        predicate = rule.get('predicate')
        value = rule.get('value')
        sql_operator = SQL_OPERATORS.get(predicate)
        if not sql_operator:
            continue

        condition = generate_condition(field_name, sql_operator, value)
        conditions.append(condition)

    if not conditions:
        return None

    if collection_predicate == 'all':
        sql_query += " AND ".join(conditions)
    elif collection_predicate == 'any':
        sql_query += " OR ".join(conditions)
    else:
        raise AssertionError("collection_predicate not implemented")

    return sql_query


def handle_action(action, service, message_id):
    if action == "mark_as_read":
        mark_as_read(service, message_id)

    if action == "mark_as_unread":
        mark_as_unread(service, message_id)

    if action == "move_to_inbox":
        mark_as_unread(service, message_id)


def rule_handler(service):
    conn = get_connection()
    c = conn.cursor()

    collections = load_collections()
    if not collections:
        print("No collections found")
        return

    for collection in collections:
        sql_query = generate_sql_query_for_rules(collection)
        if not sql_query:
            print("No SQL query found for the given collection")
            continue

        actions = collection.get('actions')
        if not actions:
            print("No actions found")
            continue

        c.execute(sql_query)

        messages = c.fetchall()
        if not messages:
            print("No data found in the database for the query")
            continue

        for message_id in messages:
            message_id = message_id[0]
            for action in actions:
                handle_action(action, service, message_id)
