"""Claude Notify - Cross-platform notifications for Claude"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .notifier import ClaudeNotifier
from .hook_handler import HookHandler

__all__ = ["ClaudeNotifier", "HookHandler"]