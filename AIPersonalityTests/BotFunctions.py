RECALL_MEMORIES = {
                    "name": "recall_memories",
                    "description": "Recall memories that are or could be relevant to the current conversation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "label": {
                                "type": "string",
                                "description": "A label for the most relevant memory",
                            },
                        },
                    },
                }


SAVE_EVENT = {
                    "name": "save_event",
                    "description": "Save or update an event that is mentioned in a conversation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "label": {
                                "type": "string",
                                "description": "A label for the most relevant memory",
                            },
                            "time": {
                                "type": "string",
                                "description": "The time the event will happen. Optional",
                            }
                        },
                    },
                }