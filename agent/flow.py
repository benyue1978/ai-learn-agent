import os
from agent.dashscope_api import generate_test_ideas, generate_test_code, generate_impl_code, summarize
from agent.utils import run_in_venv, ensure_app_dir, get_user_input, print_report

def filter_markdown_codeblock(text):
    """Remove lines starting with markdown code block markers."""
    return '\n'.join(line for line in text.splitlines() if not line.strip().startswith('```'))


def main():
    # 1. 用户输入需求
    user_requirement = get_user_input("请输入你的需求：")

    # 2. 生成单元测试思路
    while True:
        test_ideas = generate_test_ideas(user_requirement)
        print("\n【单元测试思路】\n" + test_ideas)
        confirm = get_user_input("你是否确认这些测试点？(y/n): ")
        if confirm.lower() == 'y':
            break
        user_requirement = get_user_input("请补充或修改你的需求：")

    # 3. 生成单元测试代码
    ensure_app_dir()
    test_code = generate_test_code(user_requirement, test_ideas)
    test_code = filter_markdown_codeblock(test_code)
    with open("app/test_main.py", "w") as f:
        f.write(test_code)

    # 4. venv 环境下运行测试（此时实现代码未写，测试应失败）
    run_in_venv("pytest app/test_main.py", install_requirements=True)

    # 5. 生成实现代码并循环测试
    while True:
        impl_code = generate_impl_code(user_requirement, test_ideas)
        impl_code = filter_markdown_codeblock(impl_code)
        with open("app/main.py", "w") as f:
            f.write(impl_code)
        result = run_in_venv("pytest app/test_main.py")
        print(result)
        if "failed" not in result.lower() and "error" not in result.lower():
            break
        print("有测试未通过，正在完善实现代码...")

    # 6. 总结与报告
    report = summarize(user_requirement, test_ideas, impl_code, result)
    print_report(report)

if __name__ == "__main__":
    main() 