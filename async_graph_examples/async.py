from dotenv import load_dotenv

_ = load_dotenv()

import operator
from typing import Annotated, Any, TypedDict
from langgraph.graph import StateGraph, START, END


# Defining State
class State(TypedDict):
    aggregate: Annotated[list[str], operator.add]


# Defining a Node Class that prints it's name when called
class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self, state: State) -> Any:
        print(f'Adding {self._value} to {state["aggregate"]}')
        return {"aggregate": [self._value]}


builder = StateGraph(State)
builder.add_node("a", ReturnNodeValue("I am A"))
builder.add_node("b", ReturnNodeValue("I am B"))
builder.add_node("c", ReturnNodeValue("I am C"))
builder.add_node("d", ReturnNodeValue("I am D"))

builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("a", "c")
builder.add_edge("b", "d")
builder.add_edge("c", "d")
builder.add_edge("d", END)

graph = builder.compile()

graph.get_graph().draw_mermaid_png(
    output_file_path="./async_graph_examples/async_graph.png"
)


if __name__ == "__main__":
    print("Hello Async")
    graph.invoke(
        input={"aggregate": []},
        config={
            "configurable": {
                "thread": "foo",
            }
        },
    )
