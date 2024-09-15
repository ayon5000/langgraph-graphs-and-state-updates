import os
import sqlite3
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

# CHECKPOINT_TYPE = "memory"
CHECKPOINT_TYPE = "sqlite"


class State(TypedDict):
    input: str
    user_feedback: str


def step_1(state: State) -> None:
    print("---Step 1---")


def human_feedback(state: State) -> None:
    print("---human_feedback---")


def step_2(state: State) -> None:
    print("---Step 2---")


builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("human_feedback", human_feedback)
builder.add_node("step_2", step_2)

builder.add_edge(START, "step_1")
builder.add_edge("step_1", "human_feedback")
builder.add_edge("human_feedback", "step_2")
builder.add_edge("step_2", END)

memory = None
if CHECKPOINT_TYPE == "memory":
    memory = MemorySaver()
elif CHECKPOINT_TYPE == "sqlite":
    conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
    memory = SqliteSaver(conn)

graph = builder.compile(checkpointer=memory, interrupt_before=["human_feedback"])

graph.get_graph().draw_mermaid_png(output_file_path="./graph.png")

if __name__ == "__main__":

    _ = load_dotenv()

    print("1", os.getenv("LANGCHAIN_PROJECT"))

    thread = {"configurable": {"thread_id": "2"}}

    # inital_input = {"input": "hello world"}

    # for event in graph.stream(inital_input, thread, stream_mode="values"):
    #     print(event)

    # print(graph.get_state(thread).next)

    user_input = input("Tell me how you want to update the state: ")

    graph.update_state(
        thread, values={"user_feedback": user_input}, as_node="human_feedback"
    )

    print("1", os.getenv("LANGCHAIN_PROJECT"))

    print("--State after update--")
    print(graph.get_state(thread))

    for event in graph.stream(None, thread, stream_mode="values"):
        print(event)

    print("--End State--")
    print(graph.get_state(thread))

    pass
