import os
from dotenv import load_dotenv
import dashscope

load_dotenv()
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
MODEL = os.getenv("DASHSCOPE_MODEL", "qwen-turbo")


def _call_dashscope(prompt):
    """Call dashscope with a prompt and return the response text."""
    if not DASHSCOPE_API_KEY:
        raise RuntimeError("DASHSCOPE_API_KEY not set in .env")
    response = dashscope.Generation.call(
        model=MODEL,
        api_key=DASHSCOPE_API_KEY,
        prompt=prompt,
        top_p=0.8,
        temperature=0.2,
    )
    return response['output']['text']


def generate_test_ideas(user_requirement):
    prompt = f"""
你是一个专业的Python开发者。用户需求如下：
{user_requirement}
请用中文列出2-5个关键的单元测试点，每个点用一句话描述。
"""
    return _call_dashscope(prompt)


def generate_test_code(user_requirement, test_ideas):
    prompt = f"""
你是一个专业的Python开发者。用户需求如下：
{user_requirement}
单元测试点如下：
{test_ideas}
请用pytest风格生成完整的测试代码，所有测试函数必须通过 from main import bubble_sort（或其它需要的函数）导入被测函数，不能直接写实现。所有注释都用英文，不要有任何说明、中文标点或markdown代码块，只输出纯pytest代码。
"""
    return _call_dashscope(prompt)


def generate_impl_code(user_requirement, test_ideas):
    prompt = f"""
你是一个专业的Python开发者。用户需求如下：
{user_requirement}
单元测试点如下：
{test_ideas}
请生成实现代码，所有注释都用英文，不要有任何说明、中文标点或markdown代码块，只输出纯Python代码，不要包含任何测试代码。
"""
    return _call_dashscope(prompt)


def generate_not_implemented_code(user_requirement, test_ideas):
    prompt = f"""
你是一个专业的Python开发者。用户需求如下：
{user_requirement}
单元测试点如下：
{test_ideas}
请生成一个完整的Python实现文件（main.py），包含所有通过测试所需的函数签名，但每个函数体只需 raise NotImplementedError。所有注释都用英文。不要输出任何说明、markdown代码块或非代码内容，只输出纯Python代码，不要包含任何测试代码。
"""
    return _call_dashscope(prompt)


def summarize(user_requirement, test_ideas, impl_code, result):
    prompt = f"""
你是一个专业的Python开发者。用户需求如下：
{user_requirement}
单元测试点如下：
{test_ideas}
实现代码如下：
{impl_code}
测试结果如下：
{result}
请用中文总结本次自动开发过程、实现思路、测试点和结果。
"""
    return _call_dashscope(prompt) 