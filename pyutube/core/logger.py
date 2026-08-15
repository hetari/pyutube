"""Execution flow logger for pyutube diagnostics."""

import os
import sys
import time
from typing import Any, Dict, List, Optional


class FlowStep:
    """Represent a single execution step in the pyutube workflow."""

    def __init__(self, action: str, params: Optional[Dict[str, Any]] = None) -> None:
        self.timestamp = time.strftime("%H:%M:%S")
        self.action = action
        self.params = dict(params or {})

    def format(self) -> str:
        if self.params:
            formatted_params = ", ".join(
                f"{key}={repr(value)}" for key, value in self.params.items()
            )
            return f"[{self.timestamp}] {self.action}({formatted_params})"
        return f"[{self.timestamp}] {self.action}"


class FlowLogger:
    """Record execution flow breadcrumbs for troubleshooting and bug reports."""

    def __init__(self) -> None:
        self.steps: List[FlowStep] = []

    def log(self, action: str, params: Optional[Dict[str, Any]] = None) -> None:
        """Record an execution step with action name and parameters."""
        self.steps.append(FlowStep(action, params))

    def get_trace(self) -> List[str]:
        """Return formatted breadcrumb steps."""
        return [step.format() for step in self.steps]

    def save_log_file(
        self,
        filepath: str = "pyutube_error.log",
        error_info: str = "",
    ) -> str:
        """Write execution steps and system info to a log file."""
        abs_path = os.path.abspath(filepath)
        lines = [
            "================================================================================",
            "                            Pyutube Execution Log                               ",
            "================================================================================",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Python Executable: {sys.executable}",
            "",
            "------------------------------ Execution Flow Trace ----------------------------",
        ]
        if self.steps:
            for idx, step in enumerate(self.steps, 1):
                lines.append(f" {idx:2d}. {step.format()}")
        else:
            lines.append(" No execution steps recorded.")

        if error_info:
            lines.extend(
                [
                    "",
                    "-------------------------------- Detailed Error --------------------------------",
                    error_info.strip(),
                ]
            )
        lines.append(
            "================================================================================"
        )

        try:
            with open(abs_path, "w", encoding="utf-8") as file:
                file.write("\n".join(lines) + "\n")
        except Exception:
            return filepath

        return abs_path

    def clear(self) -> None:
        """Clear all logged steps."""
        self.steps.clear()


logger = FlowLogger()
