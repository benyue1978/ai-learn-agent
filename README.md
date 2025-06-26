# AI Learn Agent

本项目是一个基于 langgraph 和 dashscope 的 Python 代码自动生成 Agent。

## 功能简介
- 根据用户需求自动生成单元测试思路
- 生成单元测试代码
- 自动实现功能代码
- 在 venv 隔离环境下运行测试，直至全部通过
- 生成 app 目录，输出最终代码

## 依赖
- langgraph
- python-dotenv
- dashscope
- pytest

## 使用方法
1. 安装依赖：`pip install -r requirements.txt`
2. 配置 .env 文件，填写 dashscope 相关变量
3. 运行主程序：`python -m agent.flow`

## 主要流程
1. 用户输入需求
2. Agent 生成并与用户确认测试思路
3. 自动生成测试代码
4. venv 环境下运行测试
5. 自动实现功能代码并循环测试
6. 全部通过后输出总结报告

## 目录结构
- agent/ 代理主逻辑
- app/   生成的代码和测试 

## 示例

```text
[警告] app 目录已存在，是否自动删除？(y/n): y
app 目录已删除。

===== Mermaid 流程图 =====

---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        user_input(user_input)
        generate_test_ideas(generate_test_ideas)
        user_confirm(user_confirm)
        generate_test_code(generate_test_code)
        run_test(run_test)
        generate_impl_code(generate_impl_code)
        run_test_with_impl(run_test_with_impl)
        check_test_result(check_test_result)
        summarize(summarize)
        __end__([<p>__end__</p>]):::last
        __start__ --> user_input;
        check_test_result -.-> generate_impl_code;
        check_test_result -.-> generate_test_code;
        check_test_result -.-> summarize;
        generate_impl_code --> run_test_with_impl;
        generate_test_code --> run_test;
        generate_test_ideas --> user_confirm;
        run_test -.-> generate_impl_code;
        run_test -.-> generate_test_code;
        run_test_with_impl -.-> check_test_result;
        run_test_with_impl -.-> generate_impl_code;
        user_confirm -.-> generate_test_code;
        user_confirm -.-> generate_test_ideas;
        user_input --> generate_test_ideas;
        summarize --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc

========================


[步骤] 用户输入需求
请输入你的需求：斐波那契数列
需求: 斐波那契数列

[步骤] 生成单元测试思路
测试思路: 1. 测试输入为2时，返回斐波那契数列的前两项 [0, 1]。  
2. 测试输入为5时，返回前五项 [0, 1, 1, 2, 3]。  
3. 测试输入为0或负数时，抛出异常或返回空列表。  
4. 测试输入为1时，返回第一项 [0]。  
5. 测试生成的数列是否符合斐波那契定义，即每一项等于前两项之和。

[步骤] 用户确认测试点
【单元测试思路】
1. 测试输入为2时，返回斐波那契数列的前两项 [0, 1]。  
2. 测试输入为5时，返回前五项 [0, 1, 1, 2, 3]。  
3. 测试输入为0或负数时，抛出异常或返回空列表。  
4. 测试输入为1时，返回第一项 [0]。  
5. 测试生成的数列是否符合斐波那契定义，即每一项等于前两项之和。
你是否确认这些测试点？(y/n): y
用户已确认测试点

[步骤] 生成单元测试代码
测试代码已生成并写入 app/test_main.py
main.py (NotImplementedError 版本) 已自动生成

[步骤] 运行初始单元测试（实现代码未写）
初始测试结果：
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-8.4.1, pluggy-1.6.0
rootdir: /Users/song.yue/git/ai-learn-agent
collected 5 items

app/test_main.py FFFFF                                                   [100%]

=================================== FAILURES ===================================
___________________ test_fibonacci_input_2_returns_first_two ___________________

    def test_fibonacci_input_2_returns_first_two():
>       assert fibonacci(2) == [0, 1]
               ^^^^^^^^^^^^

app/test_main.py:5: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

n = 2

    def fibonacci(n):
        """Generate the first n numbers in the Fibonacci sequence.
    
        Args:
            n (int): The number of elements to generate.
    
        Returns:
            list: A list containing the first n Fibonacci numbers.
    
        Raises:
            ValueError: If n is less than or equal to 0.
        """
>       raise NotImplementedError
E       NotImplementedError

app/main.py:13: NotImplementedError
__________________ test_fibonacci_input_5_returns_first_five ___________________

    def test_fibonacci_input_5_returns_first_five():
>       assert fibonacci(5) == [0, 1, 1, 2, 3]
               ^^^^^^^^^^^^

app/test_main.py:8: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

n = 5

    def fibonacci(n):
        """Generate the first n numbers in the Fibonacci sequence.
    
        Args:
            n (int): The number of elements to generate.
    
        Returns:
            list: A list containing the first n Fibonacci numbers.
    
        Raises:
            ValueError: If n is less than or equal to 0.
        """
>       raise NotImplementedError
E       NotImplementedError

app/main.py:13: NotImplementedError
____________ test_fibonacci_input_0_or_negative_returns_empty_list _____________

    def test_fibonacci_input_0_or_negative_returns_empty_list():
>       assert fibonacci(0) == []
               ^^^^^^^^^^^^

app/test_main.py:11: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

n = 0

    def fibonacci(n):
        """Generate the first n numbers in the Fibonacci sequence.
    
        Args:
            n (int): The number of elements to generate.
    
        Returns:
            list: A list containing the first n Fibonacci numbers.
    
        Raises:
            ValueError: If n is less than or equal to 0.
        """
>       raise NotImplementedError
E       NotImplementedError

app/main.py:13: NotImplementedError
__________________ test_fibonacci_input_1_returns_first_item ___________________

    def test_fibonacci_input_1_returns_first_item():
>       assert fibonacci(1) == [0]
               ^^^^^^^^^^^^

app/test_main.py:15: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

n = 1

    def fibonacci(n):
        """Generate the first n numbers in the Fibonacci sequence.
    
        Args:
            n (int): The number of elements to generate.
    
        Returns:
            list: A list containing the first n Fibonacci numbers.
    
        Raises:
            ValueError: If n is less than or equal to 0.
        """
>       raise NotImplementedError
E       NotImplementedError

app/main.py:13: NotImplementedError
__________________ test_fibonacci_sequence_follows_definition __________________

    def test_fibonacci_sequence_follows_definition():
>       sequence = fibonacci(6)
                   ^^^^^^^^^^^^

app/test_main.py:18: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

n = 6

    def fibonacci(n):
        """Generate the first n numbers in the Fibonacci sequence.
    
        Args:
            n (int): The number of elements to generate.
    
        Returns:
            list: A list containing the first n Fibonacci numbers.
    
        Raises:
            ValueError: If n is less than or equal to 0.
        """
>       raise NotImplementedError
E       NotImplementedError

app/main.py:13: NotImplementedError
=========================== short test summary info ============================
FAILED app/test_main.py::test_fibonacci_input_2_returns_first_two - NotImplem...
FAILED app/test_main.py::test_fibonacci_input_5_returns_first_five - NotImple...
FAILED app/test_main.py::test_fibonacci_input_0_or_negative_returns_empty_list
FAILED app/test_main.py::test_fibonacci_input_1_returns_first_item - NotImple...
FAILED app/test_main.py::test_fibonacci_sequence_follows_definition - NotImpl...
============================== 5 failed in 0.01s ===============================


[步骤] 生成实现代码
实现代码已生成并写入 app/main.py

[步骤] 运行实现后的单元测试
实现后测试结果：
============================= test session starts ==============================
platform darwin -- Python 3.13.3, pytest-8.4.1, pluggy-1.6.0
rootdir: /Users/song.yue/git/ai-learn-agent
collected 5 items

app/test_main.py .....                                                   [100%]

============================== 5 passed in 0.00s ===============================


[步骤] 检查测试结果
所有测试通过

[步骤] 总结与报告

===== 总结报告 =====

### 自动开发过程总结

本次开发任务是实现一个生成斐波那契数列的 Python 函数，并编写对应的单元测试以验证其正确性。开发过程中，我遵循了以下步骤：

1. **需求分析**：明确用户对斐波那契数列函数的功能要求，包括输入为不同值时的输出行为。
2. **代码实现**：根据斐波那契数列的定义（前两项为 0 和 1，后续每一项为前两项之和），编写 `fibonacci(n)` 函数。
3. **测试用例设计**：针对不同的输入情况（如 n=2、n=5、n=0 或负数、n=1）设计测试点，确保函数在各种边界条件下的行为符合预期。
4. **测试执行与结果验证**：使用 pytest 框架运行测试，确认所有测试用例均通过。

---

### 实现思路

- **函数逻辑**：
  - 如果输入 `n <= 0`，返回空列表。
  - 如果输入 `n == 1`，返回 `[0]`。
  - 如果输入 `n >= 2`，初始化结果列表为 `[0, 1]`，然后通过循环计算后续项。
- **边界处理**：
  - 输入为 0 或负数时，直接返回空列表。
  - 输入为 1 时，只返回第一项 `[0]`。
- **验证逻辑**：
  - 在循环中确保每项等于前两项之和，从而保证数列符合斐波那契定义。

---

### 测试点说明

| 测试点 | 输入 | 预期输出 | 说明 |
|--------|------|----------|------|
| 1 | 2 | [0, 1] | 返回前两项 |
| 2 | 5 | [0, 1, 1, 2, 3] | 返回前五项 |
| 3 | 0 或负数 | [] | 抛出异常或返回空列表 |
| 4 | 1 | [0] | 返回第一项 |
| 5 | 任意正整数 | 符合斐波那契定义 | 每一项等于前两项之和 |

---

### 测试结果

- 所有 5 个测试用例均通过。
- 测试耗时极短（0.00s），表明代码逻辑清晰且无性能问题。
- 未出现异常或错误，说明函数在各种边界条件下表现良好。

---

### 总结

本次开发过程高效且完整，成功实现了符合用户需求的斐波那契数列生成函数，并通过全面的单元测试验证了其正确性。代码结构清晰、逻辑严谨，能够稳定地处理各种输入情况。
```
