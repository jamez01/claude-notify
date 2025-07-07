#!/usr/bin/env python3
"""Test project path extraction from transcript paths"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from claude_notify.hook_handler import HookHandler

def test_project_path_extraction():
    handler = HookHandler()
    
    # Test cases for different transcript path formats
    test_cases = [
        {
            "name": "Standard Claude project path",
            "data": {
                "transcript_path": "/home/james/projects/misc/claude-notify/.claude/tmp/test-session-123/transcript.txt",
                "session_id": "test-session-123"
            },
            "expected_project": "claude-notify"
        },
        {
            "name": "Global Claude session (home directory)",
            "data": {
                "transcript_path": "/home/james/.claude/tmp/test-session-456/transcript.txt",
                "session_id": "test-session-456"
            },
            "expected_project": "fallback"  # Should use fallback logic
        },
        {
            "name": "Different project structure",
            "data": {
                "transcript_path": "/Users/dev/workspace/my-app/.claude/tmp/abc123/transcript.txt",
                "session_id": "abc123"
            },
            "expected_project": "my-app"
        },
        {
            "name": "Nested project path",
            "data": {
                "transcript_path": "/home/user/Documents/projects/web/frontend/.claude/tmp/xyz789/transcript.txt",
                "session_id": "xyz789"
            },
            "expected_project": "frontend"
        },
        {
            "name": "Global Claude session (different user)",
            "data": {
                "transcript_path": "/home/alice/.claude/tmp/session-def/transcript.txt",
                "session_id": "session-def"
            },
            "expected_project": "fallback"  # Should use fallback logic
        },
        {
            "name": "No .claude directory",
            "data": {
                "transcript_path": "/tmp/some-session/transcript.txt",
                "session_id": "some-session"
            },
            "expected_project": "fallback"  # Should use fallback
        },
        {
            "name": "Missing transcript_path",
            "data": {
                "session_id": "test-session"
            },
            "expected_project": "fallback"  # Should use fallback
        }
    ]
    
    print("Testing project path extraction:")
    print("=" * 50)
    
    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        print(f"Path: {test_case['data'].get('transcript_path', 'N/A')}")
        
        project_info = handler._extract_project_info(test_case['data'])
        print(f"Result: {project_info}")
        
        if test_case['expected_project'] == "fallback":
            # For fallback cases, just check that we got some project info
            if project_info and project_info != "Unknown Project":
                print("✓ PASS (fallback used)")
            else:
                print("✗ FAIL (fallback failed)")
        elif test_case['expected_project']:
            if project_info and test_case['expected_project'] in project_info:
                print("✓ PASS")
            else:
                print("✗ FAIL")
        else:
            if project_info is None:
                print("✓ PASS")
            else:
                print("✗ FAIL")

def test_notification_format():
    handler = HookHandler()
    
    print("\n\nTesting notification format for all event types:")
    print("=" * 50)
    
    base_data = {
        "session_id": "test-session-123",
        "transcript_path": "/home/james/projects/misc/claude-notify/.claude/tmp/test-session-123/transcript.txt"
    }
    
    # Test all event types to ensure they include project info
    event_tests = [
        {
            "event_type": "Stop",
            "data": base_data.copy()
        },
        {
            "event_type": "Notification", 
            "data": {**base_data, "notification_type": "info"}
        },
        {
            "event_type": "SubagentStop",
            "data": base_data.copy()
        },
        {
            "event_type": "PreToolUse",
            "data": {**base_data, "tool_name": "Bash", "tool_input": {"command": "ls"}}
        },
        {
            "event_type": "PostToolUse",
            "data": {**base_data, "tool_name": "Bash", "tool_input": {"command": "ls"}, "tool_response": {"status": "success"}}
        }
    ]
    
    for test in event_tests:
        print(f"\nTesting {test['event_type']} event notification format...")
        success = handler.process_hook_event(test['event_type'], test['data'])
        print(f"Notification sent: {'✓' if success else '✗'}")
        
        # Verify project info is extracted
        project_info = handler._extract_project_info(test['data'])
        if project_info and "claude-notify" in project_info:
            print(f"Project info included: ✓ ({project_info})")
        else:
            print(f"Project info missing: ✗")

if __name__ == "__main__":
    test_project_path_extraction()
    test_notification_format()
    print("\nTest completed!")