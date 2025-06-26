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
You are a professional Python developer. The user requirement is as follows:
{user_requirement}
The unit test ideas are:
{test_ideas}
Please output ONLY pure pytest code for test_main.py, with NO explanations, NO comments except for necessary English comments, NO Chinese punctuation, and NO extra text. The code must be ready to run directly.
"""
    return _call_dashscope(prompt)


def generate_impl_code(user_requirement, test_ideas):
    prompt = f"""
You are a professional Python developer. The user requirement is as follows:
{user_requirement}
The unit test ideas are:
{test_ideas}
Please output ONLY the implementation code for main.py, with all comments in English, NO explanations, NO Chinese punctuation, and NO extra text. The code must be ready to run directly.
"""
    return _call_dashscope(prompt)


def summarize(user_requirement, test_ideas, impl_code, result):
    prompt = f"""
你是一个专业的Python开发者。用户需求如下：
{user_requirement}
单元测试点如下：
{test_ideas}
最终实现代码如下：
{impl_code}
pytest运行结果如下：
{result}
请用中文总结本次自动开发的过程和结果。
"""
    return _call_dashscope(prompt) 