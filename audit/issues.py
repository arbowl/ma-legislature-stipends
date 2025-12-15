"""Keep track of inconsistencies"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Literal


class _IssueLevel(str, Enum):
    """Encodes severity of issue"""

    WARNING = "WARNING"
    ERROR = "ERROR"


IssueLevel = Literal[_IssueLevel.ERROR, _IssueLevel.WARNING]


@dataclass(frozen=True)
class AuditIssue:
    """Severity and type of issue"""

    level: IssueLevel
    code: str
    message: str
    context: dict[str, Any]

    @staticmethod
    def error(code: str, message: str, **context: Any) -> AuditIssue:
        """Builds an error"""
        return AuditIssue(
            level=_IssueLevel.ERROR.value,
            code=code,
            message=message,
            context=context,
        )

    @staticmethod
    def warning(code: str, message: str, **context: Any) -> AuditIssue:
        """Builds a warning"""
        return AuditIssue(
            level=_IssueLevel.WARNING.value,
            code=code,
            message=message,
            context=context,
        )