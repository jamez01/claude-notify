"""Monitor Claude sessions for activity that requires user attention"""

import os
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta


class ClaudeSessionMonitor:
    """Monitor Claude sessions for activity requiring user attention"""
    
    def __init__(self):
        self.claude_dirs = self._find_claude_directories()
        self.last_check_times = {}
        self.transcript_states = {}
        
    def _find_claude_directories(self) -> List[Path]:
        """Find all .claude directories to monitor"""
        claude_dirs = []
        
        # Check home directory for global .claude
        home_claude = Path.home() / ".claude"
        if home_claude.exists():
            claude_dirs.append(home_claude)
        
        # Check current directory and parents for project .claude
        current = Path.cwd()
        while current != current.parent:
            project_claude = current / ".claude"
            if project_claude.exists():
                claude_dirs.append(project_claude)
                break
            current = current.parent
        
        return claude_dirs
    
    def _get_active_sessions(self) -> List[Tuple[Path, str]]:
        """Get list of active Claude sessions from all .claude directories"""
        sessions = []
        
        for claude_dir in self.claude_dirs:
            tmp_dir = claude_dir / "tmp"
            if not tmp_dir.exists():
                continue
            
            # Look for session directories
            for session_dir in tmp_dir.iterdir():
                if session_dir.is_dir():
                    transcript_file = session_dir / "transcript.txt"
                    if transcript_file.exists():
                        # Check if session is recent (within last 24 hours)
                        mtime = datetime.fromtimestamp(transcript_file.stat().st_mtime)
                        if datetime.now() - mtime < timedelta(hours=24):
                            sessions.append((transcript_file, str(claude_dir.parent)))
        
        return sessions
    
    def _read_transcript_tail(self, transcript_path: Path, lines: int = 50) -> List[str]:
        """Read the last N lines of a transcript file"""
        try:
            with open(transcript_path, 'r', encoding='utf-8') as f:
                content = f.readlines()
                return content[-lines:] if len(content) > lines else content
        except Exception:
            return []
    
    def _analyze_transcript_state(self, transcript_lines: List[str]) -> Dict[str, any]:
        """Analyze transcript to determine if Claude needs attention"""
        if not transcript_lines:
            return {"needs_attention": False, "reason": None}
        
        # Join lines for analysis
        recent_text = "".join(transcript_lines[-20:])  # Last 20 lines
        
        # Patterns that indicate Claude is waiting for user
        waiting_patterns = [
            "I'll wait for your",
            "waiting for your response",
            "Let me know when",
            "Please let me know",
            "What would you like",
            "How would you like",
            "Should I proceed",
            "Would you like me to",
            "please provide",
            "please specify",
            "I need more information",
            "Could you clarify",
            "awaiting your",
            "ready when you are",
            "let me know if you'd like",
            "Feel free to ask",
            "Is there anything else",
            "What else can I help",
        ]
        
        # Check for waiting patterns
        for pattern in waiting_patterns:
            if pattern.lower() in recent_text.lower():
                return {
                    "needs_attention": True,
                    "reason": f"Claude is waiting: '{pattern}' detected",
                    "pattern": pattern
                }
        
        # Check if last message appears to be from Claude (heuristic)
        last_non_empty_lines = [line.strip() for line in transcript_lines if line.strip()]
        if last_non_empty_lines:
            last_line = last_non_empty_lines[-1]
            # If the last line ends with a question mark, Claude might be waiting
            if last_line.endswith("?"):
                return {
                    "needs_attention": True,
                    "reason": "Claude asked a question",
                    "pattern": "question"
                }
        
        # Check for error patterns that might need attention
        error_patterns = [
            "error:",
            "failed:",
            "unable to",
            "cannot",
            "permission denied",
            "not found",
        ]
        
        for pattern in error_patterns:
            if pattern.lower() in recent_text.lower():
                return {
                    "needs_attention": True,
                    "reason": f"Potential issue: '{pattern}' detected",
                    "pattern": pattern
                }
        
        return {"needs_attention": False, "reason": None}
    
    def check_sessions(self) -> List[Dict[str, any]]:
        """Check all active sessions for those needing attention"""
        sessions_needing_attention = []
        
        # Get active sessions
        active_sessions = self._get_active_sessions()
        
        for transcript_path, project_dir in active_sessions:
            # Get file modification time
            current_mtime = transcript_path.stat().st_mtime
            
            # Check if file has changed since last check
            last_mtime = self.transcript_states.get(str(transcript_path), {}).get("mtime", 0)
            
            if current_mtime > last_mtime:
                # File has changed, analyze it
                transcript_lines = self._read_transcript_tail(transcript_path)
                state = self._analyze_transcript_state(transcript_lines)
                
                # Update state tracking
                self.transcript_states[str(transcript_path)] = {
                    "mtime": current_mtime,
                    "needs_attention": state["needs_attention"],
                    "last_check": time.time()
                }
                
                if state["needs_attention"]:
                    # Extract project name
                    project_name = Path(project_dir).name
                    
                    sessions_needing_attention.append({
                        "project": project_name,
                        "project_path": project_dir,
                        "transcript_path": str(transcript_path),
                        "reason": state["reason"],
                        "pattern": state.get("pattern"),
                        "last_update": datetime.fromtimestamp(current_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    })
        
        return sessions_needing_attention
    
    def get_session_info(self, transcript_path: str) -> Optional[Dict[str, any]]:
        """Get information about a specific session"""
        path = Path(transcript_path)
        if not path.exists():
            return None
        
        # Extract session ID from path
        session_id = path.parent.name
        
        # Get project info
        claude_dir = None
        for parent in path.parents:
            if parent.name == ".claude":
                claude_dir = parent
                break
        
        if not claude_dir:
            return None
        
        project_dir = claude_dir.parent
        project_name = project_dir.name
        
        return {
            "session_id": session_id,
            "project": project_name,
            "project_path": str(project_dir),
            "transcript_path": str(path),
            "last_update": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        }