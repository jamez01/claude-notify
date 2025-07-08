#!/usr/bin/env python3
"""Test the improved watch mode functionality"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from claude_notify.session_monitor import ClaudeSessionMonitor
from pathlib import Path
import tempfile
import time


def create_test_transcript(content: str, project_dir: Path, session_name: str = "test-session") -> Path:
    """Create a test transcript file"""
    claude_dir = project_dir / ".claude" / "tmp" / session_name
    claude_dir.mkdir(parents=True, exist_ok=True)
    
    transcript = claude_dir / "transcript.txt"
    with open(transcript, "w") as f:
        f.write(content)
    
    return transcript


def test_session_monitor():
    """Test the session monitor functionality"""
    print("Testing Claude Session Monitor")
    print("=" * 50)
    
    # Create temporary test directory
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "test-project"
        project_dir.mkdir()
        
        # Test 1: No attention needed
        print("\n1. Testing transcript with no attention needed:")
        transcript1 = create_test_transcript(
            "User: Hello Claude\nClaude: Hello! I'm here to help.\n",
            project_dir
        )
        
        # Create monitor and add our test directory
        monitor = ClaudeSessionMonitor()
        monitor.claude_dirs = [project_dir / ".claude"]  # Override with test directory
        sessions = monitor.check_sessions()
        print(f"   Sessions needing attention: {len(sessions)}")
        assert len(sessions) == 0, "Should not need attention"
        print("   ✓ PASS")
        
        # Test 2: Claude waiting for response
        print("\n2. Testing transcript where Claude is waiting:")
        transcript2 = create_test_transcript(
            "User: Can you help me?\nClaude: Of course! What would you like help with?\n",
            project_dir,
            "session-2"
        )
        time.sleep(0.1)  # Ensure file mtime changes
        
        sessions = monitor.check_sessions()
        print(f"   Sessions needing attention: {len(sessions)}")
        if sessions:
            print(f"   Reason: {sessions[0]['reason']}")
        assert len(sessions) == 1, "Should need attention"
        print("   ✓ PASS")
        
        # Test 3: Error condition
        print("\n3. Testing transcript with error:")
        transcript3 = create_test_transcript(
            "User: Run this command\nClaude: I tried but got an error: Permission denied\n",
            project_dir,
            "session-3"
        )
        time.sleep(0.1)
        
        sessions = monitor.check_sessions()
        print(f"   Sessions needing attention: {len(sessions)}")
        if sessions:
            print(f"   Reason: {sessions[0]['reason']}")
        assert len(sessions) == 1, "Should need attention for error"
        print("   ✓ PASS")
        
        # Test 4: Claude asking a question
        print("\n4. Testing transcript with Claude asking question:")
        transcript4 = create_test_transcript(
            "User: I need to refactor this\nClaude: I can help with that. Should I proceed with the refactoring?\n",
            project_dir,
            "session-4"
        )
        time.sleep(0.1)
        
        sessions = monitor.check_sessions()
        print(f"   Sessions needing attention: {len(sessions)}")
        if sessions:
            print(f"   Reason: {sessions[0]['reason']}")
        assert len(sessions) == 1, "Should need attention for question"
        print("   ✓ PASS")
        
        # Test 5: Multiple patterns
        print("\n5. Testing various waiting patterns:")
        patterns = [
            "I'll wait for your response.",
            "Let me know when you're ready.",
            "Please let me know how to proceed.",
            "Feel free to ask if you need anything else.",
        ]
        
        for i, pattern in enumerate(patterns):
            content = f"Claude: {pattern}\n"
            create_test_transcript(content, project_dir, f"session-{5+i}")
            time.sleep(0.1)
            
            sessions = monitor.check_sessions()
            if sessions:
                print(f"   Pattern '{pattern}' detected: ✓")
            else:
                print(f"   Pattern '{pattern}' NOT detected: ✗")
    
    print("\n" + "=" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    test_session_monitor()