"""Claude Notify - Cross-platform notifications for Claude"""

__version__ = "0.1.1"
__author__ = "Your Name"

from .notifier import ClaudeNotifier
from .hook_handler import HookHandler
from .session_monitor import ClaudeSessionMonitor

__all__ = ["ClaudeNotifier", "HookHandler", "ClaudeSessionMonitor"]