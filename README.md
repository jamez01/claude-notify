# Claude-notify

A simple, cross-platform notification system to alert you when Claude needs your attention.

## Features

- 🖥️ **Cross-platform support**: Works on macOS, Linux, and Windows
- 🔔 **Native notifications**: Uses system-native notification methods when available
- 🪝 **Claude Code hooks**: Integrates seamlessly with Claude's hook system
- ⚙️ **Configurable**: Customize notification preferences
- 🎯 **Simple CLI**: Easy-to-use command-line interface
- 🔄 **Watch mode**: Continuous monitoring with periodic notifications
- 🚨 **Smart alerts**: Critical notifications for potentially destructive operations
- 📁 **Project identification**: All notifications include project name and path

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/claude-notify.git
cd claude-notify

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Using pip (when published)

```bash
pip install claude-notify
```

## Usage

### Claude Code Hook Integration (Recommended)

Claude-notify can be integrated directly with Claude Code as a hook to notify you when Claude needs attention or performs certain actions.

#### Setting up as a Claude Hook

You can configure claude-notify as a hook in two ways:

**Option 1: Using Claude's `/hooks` command** (Recommended)
```bash
# In Claude Code, simply run:
/hooks
# This will automatically add claude-notify hooks for Notification and Stop events
```

**Option 2: Manual configuration**

Add to your Claude settings file (`~/.claude/settings.json` or `.claude/settings.json` in your project):

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "claude-notify hook"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "claude-notify hook"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "(Bash|Write|Edit|MultiEdit)",
        "hooks": [
          {
            "type": "command",
            "command": "claude-notify hook"
          }
        ]
      }
    ]
  }
}
```

This configuration will:
- Notify you when Claude finishes responding (Stop event)
- Alert you before Claude uses potentially destructive tools (Bash, Write, Edit, MultiEdit)
- Show the project name in ALL notification titles and full project path in ALL messages

#### Available Hook Events

- **PreToolUse**: Before Claude uses a tool (can be used to review/block actions)
- **PostToolUse**: After a tool completes successfully
- **Notification**: When Claude sends a notification
- **Stop**: When Claude finishes responding
- **SubagentStop**: When a Claude subagent completes

#### Testing Hook Integration

```bash
# Test hook with sample data (includes project path extraction)
claude-notify hook --test  # Reads from test.json

# Test project path extraction
python examples/test-project-path.py

# Test with specific event type
echo '{"tool_name": "Bash", "tool_input": {"command": "ls"}}' | claude-notify hook --event-type PreToolUse

# Hook command options:
# --event-type, -e: Override event type detection
# --test, -t: Read from test.json instead of stdin
```

#### Project Path Display

For ALL hook events, claude-notify automatically extracts and displays:
- **Project name** in the notification title (e.g., "Claude Tool Request - my-project", "Claude Response Complete - my-project")
- **Full project path** in the notification message (e.g., "Project: my-project (/home/user/projects/my-project)")

This helps you identify which Claude session/project needs your attention when working on multiple projects, regardless of the event type.

### Manual Usage

#### Send a notification

```bash
# Basic notification
claude-notify send

# Custom notification
claude-notify send --title "Custom Title" --message "Custom message" --urgency critical

# Without sound
claude-notify send --no-sound
```

#### Watch mode

Run in watch mode to get periodic notifications:

```bash
# Default interval (5 minutes)
claude-notify watch

# Custom interval (2 minutes)
claude-notify watch --interval 120
```

### Configuration

```bash
# Show current configuration
claude-notify config show

# Set configuration values
claude-notify config set timeout 15
claude-notify config set sound false
claude-notify config set urgency critical

# Reset to defaults
claude-notify config reset
```

### System check

Check if your system is properly configured:

```bash
claude-notify check
```

## Configuration Options

Configuration is stored in:
- Linux/macOS: `~/.config/claude-notify/config.yaml`
- Windows: `%APPDATA%\claude-notify\config.yaml`

Available options:
- `timeout`: Notification display duration in seconds (default: 10)
- `sound`: Play notification sound (default: true)
- `urgency`: Notification urgency level - low, normal, critical (default: normal)
- `interval`: Watch mode check interval in seconds (default: 300)
- `title`: Default notification title
- `message`: Default notification message

## Platform-specific Notes

### macOS
- Uses native `osascript` for notifications
- Sound support included

### Linux
- Requires `notify-send` (usually part of `libnotify-bin` package)
- Install with: `sudo apt-get install libnotify-bin` (Debian/Ubuntu)
- Falls back to Python plyer if notify-send is not available

### Windows
- Uses PowerShell for native Windows 10+ toast notifications
- Falls back to Python plyer if PowerShell method fails

## Development

```bash
# Install in development mode
pip install -e .

# Run tests (when implemented)
python -m pytest
```

## License

MIT License - see LICENSE file for details

