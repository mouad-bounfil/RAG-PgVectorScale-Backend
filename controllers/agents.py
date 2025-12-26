from flask import request
from agents.index import conversation_agent as conversation_agent_response


def conversation_agent_controller():
    data = request.get_json()
    query = data.get("query")

    response = conversation_agent_response(query)
    return {
        "response": response,
        "status": "success",
        "code": 200,
    }
