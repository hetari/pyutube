"""Tests for the pyutube FlowLogger module."""

import os
import tempfile

from pyutube.core.logger import FlowLogger, FlowStep


def test_flow_step_formatting():
    """Verify FlowStep formats timestamp, action, and parameters correctly."""
    step = FlowStep("test_action", {"url": "https://example.com", "count": 5})
    formatted = step.format()

    assert "test_action" in formatted
    assert "url='https://example.com'" in formatted
    assert "count=5" in formatted


def test_flow_logger_log_and_trace():
    """Verify FlowLogger records steps and returns formatted traces."""
    logger = FlowLogger()
    logger.log("step_one", {"a": 1})
    logger.log("step_two", {"b": 2})

    trace = logger.get_trace()
    assert len(trace) == 2
    assert "step_one(a=1)" in trace[0]
    assert "step_two(b=2)" in trace[1]

    logger.clear()
    assert len(logger.get_trace()) == 0


def test_flow_logger_save_log_file():
    """Verify FlowLogger creates and writes execution steps to a log file."""
    logger = FlowLogger()
    logger.log("download_step", {"file": "video.mp4"})

    with tempfile.TemporaryDirectory() as tmp_dir:
        log_file = os.path.join(tmp_dir, "test_error.log")
        created_path = logger.save_log_file(log_file, error_info="Test exception trace")

        assert os.path.exists(created_path)
        with open(created_path, "r", encoding="utf-8") as f:
            content = f.read()

        assert "Pyutube Execution Log" in content
        assert "download_step(file='video.mp4')" in content
        assert "Test exception trace" in content
