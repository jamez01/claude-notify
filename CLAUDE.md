# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Claude-notify is a cross-platform notification system that integrates with Claude Code hooks to alert users when Claude needs their attention or performs certain actions. It can be used both as a Claude hook and as a standalone notification tool.

## Development Approach
This project follows the SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) methodology as configured in the global CLAUDE.md settings.

## Project Status
- **Current State**: Initial setup phase - no implementation yet
- **Goal**: Create a multi-OS script for Claude attention notifications

## Implementation Notes
When implementing this project, consider:
1. Cross-platform compatibility (Windows, macOS, Linux)
2. Different notification mechanisms per OS:
   - macOS: `osascript` or terminal-notifier
   - Linux: `notify-send` or similar
   - Windows: PowerShell notifications or toast notifications
3. Trigger mechanisms for when Claude needs attention
4. Configuration options for notification preferences

## Suggested Technology Stack
Based on the cross-platform requirement, consider:
- **Python**: Good cross-platform support with libraries like `plyer` for notifications
- **Node.js**: Cross-platform with packages like `node-notifier`
- **Shell scripts**: Platform-specific implementations with a wrapper script

## SPARC Workflow for This Project
Use the following SPARC commands to develop this project:

1. **Specification Phase**: 
   ```bash
   npx claude-flow sparc run spec-pseudocode "Define notification requirements for Claude attention events"
   ```

2. **Architecture Phase**:
   ```bash
   npx claude-flow sparc run architect "Design cross-platform notification architecture"
   ```

3. **Implementation Phase**:
   ```bash
   npx claude-flow sparc tdd "implement notification system"
   ```

## Development Commands

### Installation
```bash
# Install in development mode
pip install -e .

# Install dependencies only
pip install -r requirements.txt
```

### Testing the Notification System
```bash
# Check system dependencies
claude-notify check

# Send a test notification
claude-notify send --title "Test" --message "Testing claude-notify"

# Run the example script
python examples/example_usage.py
```

### CLI Commands
- `claude-notify send`: Send a notification immediately
- `claude-notify watch`: Run in watch mode with periodic notifications
- `claude-notify hook`: Process Claude Code hook events (reads JSON from stdin)
- `claude-notify check`: Check system dependencies
- `claude-notify config show`: Display current configuration
- `claude-notify config set <key> <value>`: Update configuration
- `claude-notify config reset`: Reset to default configuration

### Claude Hook Integration
The application is designed to work as a Claude Code hook. Key features:
- Reads hook JSON data from stdin
- Automatically determines event type from JSON structure
- Sends appropriate notifications based on event type
- Special handling for critical tools (Bash, Write, Edit, MultiEdit)
- Non-blocking operation to avoid interrupting Claude's workflow
- **Project identification**: All notifications include project name in title and full path in message

### Project Structure
```
claude-notify/
├── claude_notify/
│   ├── __init__.py          # Package initialization
│   ├── notifier.py          # Cross-platform notification logic
│   ├── cli.py               # Command-line interface with hook support
│   ├── config.py            # Configuration management
│   └── hook_handler.py      # Claude hook event processing
├── examples/
│   ├── example_usage.py     # Example usage script
│   ├── claude-settings.json # Example Claude hook configuration
│   ├── test-hook-data.json  # Test data for hook functionality
│   └── test-hook.sh         # Test script for hook integration
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup configuration
└── README.md               # User documentation with hook setup
```