from dotenv import load_dotenv

_ = load_dotenv()

import operator
from typing import Annotated, Any, Sequence, TypedDict
from langgraph.graph import StateGraph, START, END


# Defining State
class State(TypedDict):
    aggregate: Annotated[list[str], operator.add]
    which: str


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
builder.add_node("e", ReturnNodeValue("I am E"))

builder.add_edge(START, "a")


def route_bc_or_cd(state: State) -> Sequence[str]:
    if state["which"] == "cd":
        return ["c", "d"]
    return ["b", "c"]


intermediates = ["b", "c", "d"]
builder.add_conditional_edges(
    "a",
    route_bc_or_cd,
    intermediates,
)
for node in intermediates:
    builder.add_edge(node, "e")

builder.add_edge("e", END)

graph = builder.compile()

graph.get_graph().draw_mermaid_png(
    output_file_path="./async_graph_examples/async_conditional_branch.png"
)


if __name__ == "__main__":
    print("Hello Async")
    graph.invoke(
        input={
            "aggregate": [],
            "which": "cd",
        },
        config={
            "configurable": {
                "thread": "foo",
            }
        },
    )
