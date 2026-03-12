ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "dish_name": {"type": "string", "minLength": 1, "maxLength": 128},
        "analysis_confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "items": {
            "type": "array",
            "minItems": 1,
            "maxItems": 32,
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "minLength": 1, "maxLength": 128},
                    "grams": {"type": "number", "minimum": 1, "maximum": 2500},
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
                },
                "required": ["name", "grams", "confidence"],
                "additionalProperties": False
            }
        }
    },
    "required": ["dish_name", "analysis_confidence", "items"],
    "additionalProperties": False
}

RECOMMENDATION_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string", "minLength": 1, "maxLength": 500},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1}
    },
    "required": ["summary", "confidence"],
    "additionalProperties": False
}
