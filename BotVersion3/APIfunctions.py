RECALL = {
            "type": "function",
            "function": {
                "name": "recall",
                "description": "Recall this fact.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fact": {
                            "type": "string",
                            "description": "A fact to recall.",
                        }
                    },
                },
            },
        }

DONT_RECALL = {
            "type": "function",
            "function": {
                "name": "dont_recall",
                "description": "Do not recall this memory",
                "parameters": {
                    "type": "object",
                    "properties": {},
                },
            },
        }

STORE_FACTS = {
            "type": "function",
            "function": {
                "name": "store_facts",
                "description": "store a relevant fact for later",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "facts": {
                            "type": "string",
                            "description": "A list of 1 sentence facts seperated by newline characters.",
                        },
                    },
                },
            },
        }

GENERATE_QUERIES = {
            "type": "function",
            "function": {
                "name": "generate_queries",
                "description": "generate queries for accessing the database.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "facts": {
                            "type": "string",
                            "description": "A list of 1 sentence queries seperated by newline characters.",
                        },
                    },
                },
            },
        }


#TODO - change this to take in all possible memories and recall based on those.