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
3. 运行主程序：`python agent/flow.py`

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