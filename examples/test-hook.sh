#!/bin/bash
# Test script for claude-notify hook functionality

echo "Testing claude-notify hook integration..."
echo

# Test PreToolUse event
echo "1. Testing PreToolUse event (Bash command):"
cat test-hook-data.json | claude-notify hook --event-type PreToolUse
echo

# Test PostToolUse event
echo "2. Testing PostToolUse event:"
cat <<EOF | claude-notify hook --event-type PostToolUse
{
  "session_id": "test-session-123",
  "transcript_path": "/home/james/projects/misc/claude-notify/.claude/tmp/test-session-123/transcript.txt",
  "tool_name": "Bash",
  "tool_input": {"command": "ls -la"},
  "tool_response": {"status": "success", "output": "file1.txt\nfile2.txt"}
}
EOF
echo

# Test Stop event
echo "3. Testing Stop event:"
cat <<EOF | claude-notify hook --event-type Stop
{
  "session_id": "test-session-123",
  "transcript_path": "/home/james/projects/misc/claude-notify/.claude/tmp/test-session-123/transcript.txt"
}
EOF
echo

# Test auto-detection
echo "4. Testing event type auto-detection:"
cat test-hook-data.json | claude-notify hook
echo

# Test SubagentStop event
echo "5. Testing SubagentStop event:"
cat <<EOF | claude-notify hook --event-type SubagentStop
{
  "session_id": "test-session-123",
  "transcript_path": "/home/james/projects/misc/claude-notify/.claude/tmp/test-session-123/transcript.txt"
}
EOF
echo

# Test Notification event
echo "6. Testing Notification event:"
cat <<EOF | claude-notify hook --event-type Notification
{
  "session_id": "test-session-123",
  "transcript_path": "/home/james/projects/misc/claude-notify/.claude/tmp/test-session-123/transcript.txt",
  "notification_type": "info"
}
EOF
echo

echo "Hook tests completed!"