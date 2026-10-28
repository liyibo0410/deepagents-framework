"""
api/context.py — ContextVar 会话隔离单元测试

覆盖：
- set/get 基本读写
- 不同 asyncio Task 之间隔离
- reset_session_context 恢复默认值
- thread_context 独立于 session_context
"""
import asyncio
import pytest
from api.context import (
    set_session_context,
    get_session_context,
    set_thread_context,
    get_thread_context,
    reset_session_context,
)


class TestBasicSetGet:
    def test_default_is_none(self):
        assert get_session_context() is None
        assert get_thread_context() is None

    def test_set_and_get_session(self):
        token = set_session_context("/tmp/session_a")
        try:
            assert get_session_context() == "/tmp/session_a"
        finally:
            from api.context import _session_dir_ctx
            _session_dir_ctx.reset(token)

    def test_set_and_get_thread(self):
        token = set_thread_context("thread-001")
        try:
            assert get_thread_context() == "thread-001"
        finally:
            from api.context import _thread_id_ctx
            _thread_id_ctx.reset(token)


class TestResetContext:
    def test_reset_restores_default(self):
        token = set_session_context("/tmp/session_b")
        reset_session_context(token)
        assert get_session_context() is None

    def test_reset_both(self):
        s_token = set_session_context("/tmp/session_c")
        t_token = set_thread_context("thread-002")
        reset_session_context(s_token, t_token)
        assert get_session_context() is None
        assert get_thread_context() is None


class TestAsyncIsolation:
    def test_tasks_are_isolated(self):
        results = {}

        async def task_a():
            set_session_context("/tmp/task_a")
            await asyncio.sleep(0.01)
            results["a"] = get_session_context()

        async def task_b():
            set_session_context("/tmp/task_b")
            await asyncio.sleep(0.01)
            results["b"] = get_session_context()

        async def main():
            await asyncio.gather(task_a(), task_b())

        asyncio.run(main())
        assert results["a"] == "/tmp/task_a"
        assert results["b"] == "/tmp/task_b"

    def test_thread_context_isolated_across_tasks(self):
        results = {}

        async def task_x():
            set_thread_context("x")
            await asyncio.sleep(0.01)
            results["x"] = get_thread_context()

        async def task_y():
            set_thread_context("y")
            await asyncio.sleep(0.01)
            results["y"] = get_thread_context()

        async def main():
            await asyncio.gather(task_x(), task_y())

        asyncio.run(main())
        assert results["x"] == "x"
        assert results["y"] == "y"
