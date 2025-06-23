jsonSchema ={
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "id": {
      "type": "string"
    },
    "kind": {
      "type": "string"
    },
    "document": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string"
        },
        "body": {
          "type": "string"
        },
        "highlight": {
          "type": "string"
        },
        "date": {
          "type": "string"
        }
      },
      "required": [
        "title",
        "body",
        "highlight",
        "date"
      ]
    },
    "metadata": {
      "type": "object",
      "properties": {
        "author": {
          "type": "object",
          "properties": {
            "id": {
              "type": "string"
            },
            "name": {
              "type": "string"
            },
            "username": {
              "type": "string"
            },
            "avatar": {
              "type": "string"
            }
          },
          "required": [
            "id",
            "name",
            "username",
            "avatar"
          ]
        },
        "legacy": {
          "type": "object",
          "properties": {
            "url": {
              "type": "string"
            }
          },
          "required": [
            "url"
          ]
        },
        "court": {
          "type": "string"
        },
        "jurisprudence_type": {
          "type": "string"
        },
        "degree": {
          "type": "string"
        },
        "party_names": {
          "type": "string"
        },
        "rapporteur_name": {
          "type": "string"
        },
        "summary_status": {},
        "guidance_status": {},
        "is_mandatory_precedent": {
          "type": "boolean"
        },
        "is_decision_merit": {
          "type": "boolean"
        },
        "is_decision_admissibility": {
          "type": "boolean"
        },
        "judging_organ": {
          "type": "string"
        },
        "thesis_type": {
          "type": "string"
        },
        "thesis": {
          "type": "string"
        },
        "theme_number": {
          "type": "string"
        },
        "theme": {
          "type": "string"
        },
        "has_gdpr_citation": {
          "type": "boolean"
        },
        "lawsuit_number": {
          "type": "string"
        },
        "related_judges": {
          "type": "string"
        },
        "document_entities": {
          "type": "string"
        },
        "document_citations": {
          "type": "string"
        },
        "addons": {
          "type": "object",
          "properties": {
            "key_value": {
              "type": "string"
            }
          },
          "required": [
            "key_value"
          ]
        }
      },
      "required": [
        "author",
        "legacy",
        "court",
        "jurisprudence_type",
        "degree",
        "party_names",
        "rapporteur_name",
        "summary_status",
        "guidance_status",
        "is_mandatory_precedent",
        "is_decision_merit",
        "is_decision_admissibility",
        "judging_organ",
        "thesis_type",
        "thesis",
        "theme_number",
        "theme",
        "has_gdpr_citation",
        "lawsuit_number",
        "related_judges",
        "document_entities",
        "document_citations",
        "addons"
      ]
    },
    "boosts": {
      "type": "object",
      "properties": {
        "recency": {
          "type": "number"
        },
        "authority": {
          "type": "number"
        },
        "overall": {
          "type": "number"
        },
        "experiments": {
          "type": "object",
          "properties": {
            "key_value": {
              "type": "string"
            }
          },
          "required": [
            "key_value"
          ]
        },
        "updated_at": {
          "type": "string"
        }
      },
      "required": [
        "recency",
        "authority",
        "overall",
        "experiments",
        "updated_at"
      ]
    },
    "features": {
      "type": "object",
      "properties": {
        "copies_lt": {
          "type": "number"
        },
        "copies_st": {
          "type": "number"
        },
        "impressions_lt": {
          "type": "number"
        },
        "impressions_st": {
          "type": "number"
        },
        "weighted_impressions_lt": {
          "type": "number"
        },
        "weighted_impressions_st": {
          "type": "number"
        },
        "authority_time_discounted": {
          "type": "number"
        },
        "copy_context": {
          "type": "string"
        },
        "click_context": {
          "type": "string"
        },
        "expanded_copy_context": {
          "type": "string"
        },
        "citation_context": {
          "type": "string"
        },
        "updated_at": {
          "type": "string"
        }
      },
      "required": [
        "copies_lt",
        "copies_st",
        "impressions_lt",
        "impressions_st",
        "weighted_impressions_lt",
        "weighted_impressions_st",
        "authority_time_discounted",
        "copy_context",
        "click_context",
        "expanded_copy_context",
        "citation_context",
        "updated_at"
      ]
    },
    "phrasal_terms": {
      "type": "object",
      "properties": {
        "entity_type": {
          "type": "string"
        },
        "title": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string"
            },
            "matches": {
              "type": "string"
            }
          },
          "required": [
            "entity_type",
            "matches"
          ]
        },
        "body": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string"
            },
            "matches": {
              "type": "string"
            }
          },
          "required": [
            "entity_type",
            "matches"
          ]
        },
        "highlight": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string"
            },
            "matches": {
              "type": "string"
            }
          },
          "required": [
            "entity_type",
            "matches"
          ]
        },
        "extensions": {
          "type": "object",
          "properties": {
            "key_value": {
              "type": "string"
            }
          },
          "required": [
            "key_value"
          ]
        },
        "updated_at": {
          "type": "string"
        }
      },
      "required": [
        "entity_type",
        "title",
        "body",
        "highlight",
        "extensions",
        "updated_at"
      ]
    },
    "date_times": {
      "type": "object",
      "properties": {
        "entity_type": {
          "type": "string"
        },
        "title": {},
        "body": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string"
            },
            "matches": {
              "type": "string"
            }
          },
          "required": [
            "entity_type",
            "matches"
          ]
        },
        "highlight": {},
        "extensions": {
          "type": "object",
          "properties": {
            "key_value": {
              "type": "string"
            }
          },
          "required": [
            "key_value"
          ]
        },
        "updated_at": {
          "type": "string"
        }
      },
      "required": [
        "entity_type",
        "title",
        "body",
        "highlight",
        "extensions",
        "updated_at"
      ]
    },
    "identities": {
      "type": "object",
      "properties": {
        "entity_type": {
          "type": "string"
        },
        "title": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string"
            },
            "matches": {
              "type": "string"
            }
          },
          "required": [
            "entity_type",
            "matches"
          ]
        },
        "body": {},
        "highlight": {},
        "extensions": {
          "type": "object",
          "properties": {
            "key_value": {
              "type": "string"
            }
          },
          "required": [
            "key_value"
          ]
        },
        "updated_at": {
          "type": "string"
        }
      },
      "required": [
        "entity_type",
        "title",
        "body",
        "highlight",
        "extensions",
        "updated_at"
      ]
    },
    "acronyms": {
      "type": "object",
      "properties": {
        "entity_type": {
          "type": "string"
        },
        "title": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string"
            },
            "matches": {
              "type": "string"
            }
          },
          "required": [
            "entity_type",
            "matches"
          ]
        },
        "body": {
          "type": "object",
          "properties": {
            "entity_type": {
              "type": "string"
            },
            "matches": {
              "type": "string"
            }
          },
          "required": [
            "entity_type",
            "matches"
          ]
        },
        "highlight": {},
        "extensions": {
          "type": "object",
          "properties": {
            "key_value": {
              "type": "string"
            }
          },
          "required": [
            "key_value"
          ]
        },
        "updated_at": {
          "type": "string"
        }
      },
      "required": [
        "entity_type",
        "title",
        "body",
        "highlight",
        "extensions",
        "updated_at"
      ]
    },
    "precedents": {
      "type": "object",
      "properties": {
        "entity_type": {
          "type": "string"
        },
        "title": {},
        "body": {},
        "highlight": {},
        "extensions": {
          "type": "object",
          "properties": {
            "key_value": {
              "type": "string"
            }
          },
          "required": [
            "key_value"
          ]
        },
        "updated_at": {
          "type": "string"
        }
      },
      "required": [
        "entity_type",
        "title",
        "body",
        "highlight",
        "extensions",
        "updated_at"
      ]
    },
    "themes": {
      "type": "object",
      "properties": {
        "entity_type": {
          "type": "string"
        },
        "title": {},
        "body": {},
        "highlight": {},
        "extensions": {
          "type": "object",
          "properties": {
            "key_value": {
              "type": "string"
            }
          },
          "required": [
            "key_value"
          ]
        },
        "updated_at": {
          "type": "string"
        }
      },
      "required": [
        "entity_type",
        "title",
        "body",
        "highlight",
        "extensions",
        "updated_at"
      ]
    },
    "merged_entities": {
      "type": "object",
      "properties": {
        "title": {
          "type": "object",
          "properties": {
            "matches": {
              "type": "string"
            }
          },
          "required": [
            "matches"
          ]
        },
        "body": {
          "type": "object",
          "properties": {
            "matches": {
              "type": "string"
            }
          },
          "required": [
            "matches"
          ]
        },
        "highlight": {
          "type": "object",
          "properties": {
            "matches": {
              "type": "string"
            }
          },
          "required": [
            "matches"
          ]
        },
        "extensions": {
          "type": "object",
          "properties": {
            "key_value": {
              "type": "string"
            }
          },
          "required": [
            "key_value"
          ]
        },
        "updated_at": {
          "type": "string"
        }
      },
      "required": [
        "title",
        "body",
        "highlight",
        "extensions",
        "updated_at"
      ]
    },
    "__key": {
      "type": "string"
    },
    "__value": {
      "type": "string"
    },
    "__offset": {
      "type": "number"
    },
    "__partition": {
      "type": "number"
    },
    "__timestamp": {
      "type": "string"
    }
  },
  "required": [
    "id",
    "kind",
    "document",
    "metadata",
    "boosts",
    "features",
    "phrasal_terms",
    "date_times",
    "identities",
    "acronyms",
    "precedents",
    "themes",
    "merged_entities",
    "__key",
    "__value",
    "__offset",
    "__partition",
    "__timestamp"
  ]
}