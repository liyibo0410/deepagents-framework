"""
Markdown 文档生成工具模块

提供将文本内容写入 Markdown 文件的功能。
"""
from utils.logger_utils import logger
from pathlib import Path
from typing import Annotated
from langchain_core.tools import tool
from api.monitor import monitor
from api.context import get_session_context
from utils.path_utils import resolve_path


@tool
def generate_markdown(
        content: Annotated[str, "要写入Markdown文档的文本内容"],
        filename: Annotated[str, "Markdown文档的文件名（不包含扩展名或包含.md）"],
        path: Annotated[str, "文件保存的绝对路径"] = ""
) -> str:
    """
     根据提供的文本内容，生成对应的Markdown(.md)文件。

    Args:
        content: 要写入的文本内容
        filename: 文件名（自动补全.md后缀）
        path: 保存路径（可选，默认为会话目录）

    Returns:
        str: 操作结果消息（成功或失败）
    """
    logger.debug(f"[MarkdownTool] 开始生成文件，路径前缀: {path}")
    monitor.report_tool("Markdown文档生成工具", {"写入的文本内容": content})

    # 自动补全文件扩展名
    if not filename.endswith('.md'):
        filename += '.md'

    # 获取会话目录并解析完整路径
    session_dir = get_session_context()
    if path and path != ".":
        full_input_path = str(Path(path) / filename)
    else:
        full_input_path = filename

    full_path_str = resolve_path(full_input_path, session_dir)
    file_path = Path(full_path_str)
    parent_dir = file_path.parent

    logger.debug(f"[MarkdownTool] 目标文件: {file_path}")

    try:
        # 确保父目录存在
        if not parent_dir.exists():
            parent_dir.mkdir(parents=True, exist_ok=True)
            logger.debug(f"[MarkdownTool] 创建目录: {parent_dir}")

        # 写入文件
        file_path.write_text(content, encoding='utf-8')
        logger.info(f"[MarkdownTool] 成功写入: {file_path}")
        return f"Markdown文件 '{file_path}' 已成功生成并保存。"

    except PermissionError as e:
        logger.error(f"[MarkdownTool] 权限不足: {e}")
        return f"生成失败：权限不足 - {str(e)}"
    except OSError as e:
        logger.error(f"[MarkdownTool] 文件系统错误: {e}")
        return f"生成失败：文件系统错误 - {str(e)}"
    except Exception as e:
        logger.error(f"[MarkdownTool] 未知错误: {e}", exc_info=True)
        return f"生成Markdown文件失败: {str(e)}"

# -------------------------- 测试代码（仅修改这里，给session_dir配置固定值） --------------------------
if __name__ == "__main__":
    # ========== 核心：覆盖get_session_context的返回值（仅测试时生效） ==========
    # 不用Mock，直接重新定义这个函数，给session_dir赋值！
    def get_session_context():
        """测试专用：给session_dir配置固定初始化值"""
        return "./test_session_123"  # 你要的session_dir初始化值，随便改

    # ========== 极简测试逻辑（只传path/filename，session_dir已初始化） ==========
    test_content = "# 测试文档\n这是给session_dir配置固定值后的测试内容"
    test_filename = "测试文件2"  # 无.md后缀，测试自动补全
    test_path = "sub_dir"       # 相对路径

    # 调用生成函数
    print("===== 开始测试（session_dir已配置为：./test_session_123） =====")
    result = generate_markdown.invoke({
        "content": test_content,
        "filename": test_filename,
        "path": test_path
    })

    # 验证结果
    print(f"\n调用结果：{result}")
    if "已成功生成" in result:
        file_path = Path(result.split("'")[1])
        print(f"✅ 验证：文件 {file_path} {'存在' if file_path.exists() else '不存在'}")
