import os
from typing import TypedDict, Optional
from agent.dashscope_api import generate_test_ideas, generate_test_code, generate_impl_code, summarize
from agent.utils import run_in_venv, ensure_app_dir, get_user_input, print_report
from langgraph.graph import StateGraph, END, START

def filter_markdown_codeblock(text):
    """Remove lines starting with markdown code block markers."""
    return '\n'.join(line for line in text.splitlines() if not line.strip().startswith('```'))

class StateSchema(TypedDict, total=False):
    user_requirement: Optional[str]
    test_ideas: Optional[str]
    test_code: Optional[str]
    impl_code: Optional[str]
    result: Optional[str]
    confirm_result: Optional[str]
    test_status: Optional[str]

# 节点函数全部用 StateSchema 作为 state

def node_user_input(state: StateSchema) -> StateSchema:
    if state.get("user_requirement") is None:
        state["user_requirement"] = get_user_input("请输入你的需求：")
    return state

def node_generate_test_ideas(state: StateSchema) -> StateSchema:
    state["test_ideas"] = generate_test_ideas(state["user_requirement"])
    return state

def node_user_confirm(state: StateSchema) -> StateSchema:
    print("\n【单元测试思路】\n" + state["test_ideas"])
    confirm = get_user_input("你是否确认这些测试点？(y/n): ")
    if confirm.lower() == 'y':
        state["confirm_result"] = "generate_test_code"
    else:
        state["confirm_result"] = "generate_test_ideas"
        # 允许用户补充需求
        state["user_requirement"] = get_user_input("请补充或修改你的需求：")
    return state

def node_generate_test_code(state: StateSchema) -> StateSchema:
    ensure_app_dir()
    test_code = generate_test_code(state["user_requirement"], state["test_ideas"])
    test_code = filter_markdown_codeblock(test_code)
    with open("app/test_main.py", "w") as f:
        f.write(test_code)
    state["test_code"] = test_code
    return state

def node_run_test(state: StateSchema) -> StateSchema:
    # 安装 pytest
    run_in_venv("pip install pytest", install_requirements=False)
    result = run_in_venv("pytest app/test_main.py", install_requirements=False)
    state["result"] = result
    return state

def node_generate_impl_code(state: StateSchema) -> StateSchema:
    impl_code = generate_impl_code(state["user_requirement"], state["test_ideas"])
    impl_code = filter_markdown_codeblock(impl_code)
    with open("app/main.py", "w") as f:
        f.write(impl_code)
    state["impl_code"] = impl_code
    return state

def node_run_test_with_impl(state: StateSchema) -> StateSchema:
    result = run_in_venv("pytest app/test_main.py", install_requirements=False)
    state["result"] = result
    return state

def node_check_test_result(state: StateSchema) -> StateSchema:
    # 简单判断所有 test 通过
    if "failed" not in state["result"]:
        state["test_status"] = "all_pass"
    else:
        state["test_status"] = "has_fail"
    return state

def node_summarize(state: StateSchema) -> StateSchema:
    report = summarize(state["user_requirement"], state["test_ideas"], state["impl_code"], state["result"])
    print_report(report)
    return state

def init_code_agent(user_requirement=None):
    """
    构建并运行 code agent workflow。user_requirement 可选，返回最终 state。
    """
    builder = StateGraph(StateSchema)
    builder.add_node("user_input", node_user_input)
    builder.add_node("generate_test_ideas", node_generate_test_ideas)
    builder.add_node("user_confirm", node_user_confirm)
    builder.add_node("generate_test_code", node_generate_test_code)
    builder.add_node("run_test", node_run_test)
    builder.add_node("generate_impl_code", node_generate_impl_code)
    builder.add_node("run_test_with_impl", node_run_test_with_impl)
    builder.add_node("check_test_result", node_check_test_result)
    builder.add_node("summarize", node_summarize)

    builder.set_entry_point("user_input")
    builder.add_edge("user_input", "generate_test_ideas")
    builder.add_edge("generate_test_ideas", "user_confirm")

    builder.add_conditional_edges(
        "user_confirm",
        lambda state: state["confirm_result"],
        {
            "generate_test_code": "generate_test_code",
            "generate_test_ideas": "generate_test_ideas"
        }
    )

    builder.add_edge("generate_test_code", "run_test")
    builder.add_edge("run_test", "generate_impl_code")
    builder.add_edge("generate_impl_code", "run_test_with_impl")
    builder.add_edge("run_test_with_impl", "check_test_result")

    builder.add_conditional_edges(
        "check_test_result",
        lambda state: "summarize" if state["test_status"] == "all_pass" else "generate_impl_code",
        {
            "summarize": "summarize",
            "generate_impl_code": "generate_impl_code"
        }
    )

    builder.add_edge("summarize", END)
    chain = builder.compile()
    # 打印mermaid格式的graph
    print("\n===== Mermaid 流程图 =====\n")
    print(chain.get_graph().draw_mermaid())
    print("========================\n")

    init_state: StateSchema = {
        "user_requirement": user_requirement,
        "test_ideas": None,
        "test_code": None,
        "impl_code": None,
        "result": None,
        "confirm_result": None,
        "test_status": None
    }
    return chain.invoke(init_state)

def main():
    init_code_agent()

if __name__ == "__main__":
    main() 