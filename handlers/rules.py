RULES_SCHEMA = [
  {
    "rule_name": "rule_1",
    "collection_predicate": "any",
    "rules": [
      {
        "field_name": "sender",
        "predicate": "contains",
        "value": "vacancy@openings.shine.com"
      },
      {
        "field_name": "subject",
        "predicate": "equals",
        "value": "Urgent Hiring for Site Engineer at Nitcaa"
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
