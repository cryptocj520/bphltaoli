#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动脚本

资金费率套利机器人的启动脚本，提供命令行接口
"""

import os
import sys
import asyncio
import logging
import traceback
import argparse
import yaml

# 设置工作目录为项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_root)

# 添加项目根目录到Python路径
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 添加funding_arbitrage_bot目录到Python路径
bot_dir = os.path.join(project_root, 'funding_arbitrage_bot')
if bot_dir not in sys.path:
    sys.path.insert(0, bot_dir)

# 打印当前的Python路径，用于调试
print(f"Python路径: {sys.path}")
print(f"当前工作目录: {os.getcwd()}")

try:
    # 导入主模块
    from funding_arbitrage_bot.main import main
except ImportError as e:
    print(f"导入主模块时出错: {e}")
    print("尝试直接导入...")
    try:
        # 如果直接导入失败，可能是因为funding_arbitrage_bot不在Python路径中
        # 添加父目录到Python路径
        parent_dir = os.path.dirname(project_root)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        print(f"添加父目录到Python路径: {parent_dir}")
        print(f"更新后的Python路径: {sys.path}")
        
        # 再次尝试导入
        from funding_arbitrage_bot.main import main
    except ImportError as e2:
        print(f"第二次尝试导入失败: {e2}")
        print("请确保已正确安装依赖或位于正确的工作目录")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="资金费率套利机器人")
    parser.add_argument("--test", action="store_true", help="测试模式 - 只测试API连接")
    parser.add_argument("--config", help="配置文件路径")
    args = parser.parse_args()
    
    try:
        # Windows系统需要设置事件循环策略
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        # 运行主函数
        asyncio.run(main(test=args.test, config_path=args.config))
        
    except KeyboardInterrupt:
        print("\n程序已被用户中断")
    except FileNotFoundError as e:
        print(f"错误: {e}")
        print(f"当前工作目录: {os.getcwd()}")
    except yaml.YAMLError as e:
        print(f"YAML配置文件格式错误: {e}")
    except Exception as e:
        print(f"程序运行出错: {e}")
        traceback.print_exc()
        sys.exit(1) 