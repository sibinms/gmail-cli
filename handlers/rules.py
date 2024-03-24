RULES_SCHEMA = [
  {
    "rule_name": "rule_1",
    "collection_predicate": "any",
    "rules": [
      {
        "field_name": "sender",
        "predicate": "contains",
        "value": "Highire Manpower Services <vacancy@vacancies.shine.com>"
      },
      {
        "field_name": "subject",
        "predicate": "equals",
        "value": "Shop smarter, not harder; Beat online scammers"
      }
    ],
    "actions": [
      'mark_as_unread'
    ]
  },
  {
    "rule_name": "rule_2",
    "collection_predicate": "all",
    "rules": [
      {
        "field_name": "sender",
        "predicate": "contains",
        "value": "Highire Manpower Services <vacancy@vacancies.shine.com>"
      }
    ],
    "actions": [
      'mark_as_read'
    ]
  },
  {
    "rule_name": "rule_3",
    "collection_predicate": "all",
    "rules": [
      {
        "field_name": "received_at",
        "predicate": "less_than_days",
        "value": "2"
      }
    ],
    "actions": [
      'mark_as_read'
    ]
  }
]
