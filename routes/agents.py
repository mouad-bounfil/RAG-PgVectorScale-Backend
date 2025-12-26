from flask import Blueprint
from controllers.agents import conversation_agent_controller

agents_bp = Blueprint("agents", __name__)


@agents_bp.route("/conversation", methods=["POST"])
def create_agent():
    return conversation_agent_controller()
