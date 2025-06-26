import os
from typing import TypedDict, Optional
import sys
import shutil
from agent.dashscope_api import generate_test_ideas, generate_test_code, generate_impl_code, summarize, generate_not_implemented_code
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
    print("\n[步骤] 用户输入需求")
    if state.get("user_requirement") is None:
        state["user_requirement"] = get_user_input("请输入你的需求：")
    print(f"需求: {state['user_requirement']}")
    return state

def node_generate_test_ideas(state: StateSchema) -> StateSchema:
    print("\n[步骤] 生成单元测试思路")
    state["test_ideas"] = generate_test_ideas(state["user_requirement"])
    print(f"测试思路: {state['test_ideas']}")
    return state

def node_user_confirm(state: StateSchema) -> StateSchema:
    print("\n[步骤] 用户确认测试点")
    print("【单元测试思路】\n" + state["test_ideas"])
    confirm = get_user_input("你是否确认这些测试点？(y/n): ")
    if confirm.lower() == 'y':
        state["confirm_result"] = "generate_test_code"
        print("用户已确认测试点")
    else:
        state["confirm_result"] = "generate_test_ideas"
        new_input = get_user_input("请补充或修改你的需求：")
        # 合并原需求和新输入
        state["user_requirement"] = (state["user_requirement"] or "") + '\n' + new_input
        print("用户未确认，需求已合并并更新")
        # 删除旧的测试和实现文件
        for f in ["app/test_main.py", "app/main.py"]:
            if os.path.exists(f):
                os.remove(f)
                print(f"已删除旧文件: {f}")
    return state

def node_generate_test_code(state: StateSchema) -> StateSchema:
    print("\n[步骤] 生成单元测试代码")
    ensure_app_dir()
    test_code = generate_test_code(state["user_requirement"], state["test_ideas"])
    test_code = filter_markdown_codeblock(test_code)
    with open("app/test_main.py", "w") as f:
        f.write(test_code)
    state["test_code"] = test_code
    print("测试代码已生成并写入 app/test_main.py")

    # 如果 main.py 不存在，调用 LLM 生成所有函数都 raise NotImplementedError 的 main.py
    main_path = "app/main.py"
    if not os.path.exists(main_path):
        not_impl_code = generate_not_implemented_code(state["user_requirement"], state["test_ideas"])
        not_impl_code = filter_markdown_codeblock(not_impl_code)
        with open(main_path, "w") as mf:
            mf.write(not_impl_code)
        print("main.py (NotImplementedError 版本) 已自动生成")
    return state

def node_run_test(state: StateSchema) -> StateSchema:
    print("\n[步骤] 运行初始单元测试（实现代码未写）")
    run_in_venv("pip install pytest", install_requirements=False)
    result = run_in_venv("pytest app/test_main.py", install_requirements=False)
    state["result"] = result
    print("初始测试结果：")
    print(result)
    # 校验：所有测试必须 fail
    if "FAILED" in result and "passed" not in result:
        state["test_status"] = "all_fail"
    else:
        state["test_status"] = "unexpected_pass"
        print("[警告] 实现未写时，测试未全部失败，流程将回到测试代码生成环节。请检查测试代码与 NotImplementedError 版本 main.py 的接口一致性。")
    return state

def node_generate_impl_code(state: StateSchema) -> StateSchema:
    print("\n[步骤] 生成实现代码")
    impl_code = generate_impl_code(state["user_requirement"], state["test_ideas"])
    impl_code = filter_markdown_codeblock(impl_code)
    with open("app/main.py", "w") as f:
        f.write(impl_code)
    state["impl_code"] = impl_code
    print("实现代码已生成并写入 app/main.py")
    return state

def node_run_test_with_impl(state: StateSchema) -> StateSchema:
    print("\n[步骤] 运行实现后的单元测试")
    result = run_in_venv("pytest app/test_main.py", install_requirements=False)
    state["result"] = result
    print("实现后测试结果：")
    print(result)
    # 校验：所有测试必须 pass
    if "FAILED" not in result and "passed" in result:
        state["test_status"] = "all_pass"
    else:
        state["test_status"] = "unexpected_fail"
        print("[警告] 实现写好后，测试未全部通过，流程将回到实现代码生成环节。请检查实现代码和测试代码接口一致性。")
    return state

def node_check_test_result(state: StateSchema) -> StateSchema:
    print("\n[步骤] 检查测试结果")
    if state["test_status"] == "all_pass":
        print("所有测试通过")
    elif state["test_status"] == "all_fail":
        print("所有测试都失败，符合预期（NotImplementedError 阶段）")
    elif state["test_status"] == "unexpected_pass":
        print("[异常] 实现未写时，测试未全部失败，流程回退。请检查测试代码和 main.py 的接口一致性。")
    elif state["test_status"] == "unexpected_fail":
        print("[异常] 实现写好后，测试未全部通过，流程回退。请检查实现代码和测试代码的接口一致性。")
    else:
        print("[未知状态] test_status:", state["test_status"])
    return state

def node_summarize(state: StateSchema) -> StateSchema:
    print("\n[步骤] 总结与报告")
    report = summarize(state["user_requirement"], state["test_ideas"], state["impl_code"], state["result"])
    print_report(report)
    return state

def check_and_prepare_app_dir():
    """检查app目录是否存在，必要时询问用户并删除。"""
    if os.path.exists("app"):
        ans = input("[警告] app 目录已存在，是否自动删除？(y/n): ").strip().lower()
        if ans == 'y':
            shutil.rmtree("app")
            print("app 目录已删除。")
        else:
            print("请手动删除 app 目录后再运行本程序！")
            sys.exit(1)

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
    builder.add_conditional_edges(
        "run_test",
        lambda state: "generate_impl_code" if state["test_status"] == "all_fail" else "generate_test_code",
        {
            "generate_impl_code": "generate_impl_code",
            "generate_test_code": "generate_test_code"
        }
    )
    builder.add_edge("generate_impl_code", "run_test_with_impl")
    builder.add_conditional_edges(
        "run_test_with_impl",
        lambda state: "check_test_result" if state["test_status"] == "all_pass" else "generate_impl_code",
        {
            "check_test_result": "check_test_result",
            "generate_impl_code": "generate_impl_code"
        }
    )
    builder.add_conditional_edges(
        "check_test_result",
        lambda state: "summarize" if state["test_status"] == "all_pass" else ("generate_test_code" if state["test_status"] == "unexpected_pass" else "generate_impl_code"),
        {
            "summarize": "summarize",
            "generate_test_code": "generate_test_code",
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
    check_and_prepare_app_dir()
    init_code_agent()

if __name__ == "__main__":
    main() 