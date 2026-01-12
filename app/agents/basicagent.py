
#https://reference.langchain.com/python/langchain/models/?_gl=1*17bdmx4*_gcl_au*MTQ5MjM5NzIyNy4xNzYzMDA4NzMy*_ga*MTEzNjM2MzExMS4xNzYzMDA4NzMy*_ga_47WX3HKKY2*czE3NjgxNzU1NDUkbzYkZzAkdDE3NjgxNzU1NDUkajYwJGwwJGgw#langchain.chat_models.init_chat_model(model)
import os
from dataclasses import dataclass
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

from Prompts import SYSTEM_PROMPT
from tools import (
    Context,
    read_linux_documentation,
    read_systemd_documentation,
    read_generic_web_document,
    execute_command,   # dummy
)


os.environ["USER_AGENT"] = "linux-doc-agent/1.0"
groq_api_key = os.environ.get("GROQ_API_KEY")
print("GROQ_API_KEY:", bool(os.environ.get("GROQ_API_KEY")))

checkpointer = InMemorySaver()

model = init_chat_model(
    model="llama-3.1-8b-instant",
    model_provider="groq",
    temperature=0.5,
    timeout=10,
    max_tokens=1000,
    api_key=groq_api_key,
)


@dataclass
class ResponseFormat:
    """Structured response schema."""
    punny_response: str


agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[
         read_linux_documentation,
        read_systemd_documentation,
        read_generic_web_document,
        execute_command,   # dummy
    ],
    context_schema=Context,
    # response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer,
)

config = {"configurable": {"thread_id": "1"}}

print("\nType 'exit' or 'quit' to end the chat.\n")
while True:
    user_input = input("You: ").strip()

    if user_input.lower() in {"exit", "quit"}:
        print("Goodbye 👋")
        break

    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config,
        context=Context(user_id="1"),
    )

    final_message = response["messages"][-1]
    print("Agent:", final_message.content)