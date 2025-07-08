"""Command-line interface for Claude Notify"""

import click
import time
import sys
from pathlib import Path
from typing import Optional
from .notifier import ClaudeNotifier
from .config import load_config, save_config, get_default_config
from .hook_handler import HookHandler
from .session_monitor import ClaudeSessionMonitor


@click.group()
@click.version_option(version="0.1.1", prog_name="claude-notify")
def cli():
    """Claude Notify - Cross-platform notifications for Claude"""
    pass


@cli.command()
@click.option(
    "--title", "-t",
    default="Claude needs your attention",
    help="Notification title"
)
@click.option(
    "--message", "-m",
    default="Claude is waiting for your response",
    help="Notification message"
)
@click.option(
    "--urgency", "-u",
    type=click.Choice(["low", "normal", "critical"]),
    default="normal",
    help="Notification urgency level"
)
@click.option(
    "--timeout", "-s",
    type=int,
    default=10,
    help="Notification timeout in seconds"
)
@click.option(
    "--sound/--no-sound",
    default=True,
    help="Play notification sound"
)
def send(title: str, message: str, urgency: str, timeout: int, sound: bool):
    """Send a notification immediately"""
    notifier = ClaudeNotifier()
    
    success = notifier.send_notification(
        title=title,
        message=message,
        urgency=urgency,
        timeout=timeout,
        sound=sound
    )
    
    if success:
        click.echo("✓ Notification sent successfully")
    else:
        click.echo("✗ Failed to send notification", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--interval", "-i",
    type=int,
    default=30,
    help="Check interval in seconds (default: 30)"
)
@click.option(
    "--all-projects", "-a",
    is_flag=True,
    help="Monitor all Claude projects, not just current directory"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Show detailed monitoring information"
)
def watch(interval: int, all_projects: bool, verbose: bool):
    """Watch for Claude activity and notify when attention is needed"""
    config = load_config()
    notifier = ClaudeNotifier()
    monitor = ClaudeSessionMonitor()
    
    # Track which sessions we've already notified about
    notified_sessions = set()
    
    click.echo("🔍 Starting Claude session monitor...")
    click.echo(f"📁 Monitoring: {'All projects' if all_projects else 'Current project only'}")
    click.echo(f"⏱️  Check interval: {interval} seconds")
    click.echo("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Check for sessions needing attention
            sessions = monitor.check_sessions()
            
            # Filter to current project if not monitoring all
            if not all_projects and sessions:
                cwd = str(Path.cwd())
                sessions = [s for s in sessions if s["project_path"] == cwd]
            
            # Process sessions needing attention
            for session in sessions:
                session_key = session["transcript_path"]
                
                # Only notify once per session unless it changes again
                if session_key not in notified_sessions:
                    # Send notification
                    project_name = session["project"]
                    reason = session["reason"]
                    
                    success = notifier.send_notification(
                        title=f"Claude needs attention - {project_name}",
                        message=f"{reason}\nProject: {project_name} ({session['project_path']})",
                        urgency="normal" if "question" not in reason.lower() else "critical",
                        timeout=config.get("timeout", 10),
                        sound=config.get("sound", True)
                    )
                    
                    if success:
                        notified_sessions.add(session_key)
                        click.echo(f"🔔 [{time.strftime('%H:%M:%S')}] Notification sent for {project_name}: {reason}")
                    else:
                        click.echo(f"❌ [{time.strftime('%H:%M:%S')}] Failed to send notification for {project_name}")
                    
                    if verbose:
                        click.echo(f"   📄 Transcript: {session['transcript_path']}")
                        click.echo(f"   🕐 Last update: {session['last_update']}")
            
            # Clear notified sessions if their state changes (file modified again)
            current_states = monitor.transcript_states
            notified_sessions = {
                session for session in notified_sessions
                if session in current_states and 
                current_states[session].get("needs_attention", False)
            }
            
            if verbose and not sessions:
                click.echo(f"[{time.strftime('%H:%M:%S')}] No sessions need attention")
            
            # Wait for next check
            time.sleep(interval)
            
    except KeyboardInterrupt:
        click.echo("\n\n✋ Stopping watch mode...")
        click.echo(f"📊 Monitored {len(monitor.transcript_states)} session(s)")
        click.echo("👋 Goodbye!")


@cli.command()
def check():
    """Check notification system dependencies"""
    notifier = ClaudeNotifier()
    deps = notifier.check_dependencies()
    
    click.echo("Claude Notify System Check")
    click.echo("=" * 30)
    click.echo(f"Operating System: {notifier.system}")
    click.echo(f"Native support: {'✓' if deps['native'] else '✗'}")
    click.echo(f"Notification method: {deps.get('method', 'unknown')}")
    click.echo(f"Plyer fallback: {'✓' if deps['plyer'] else '✗'}")
    
    # Test notification
    click.echo("\nSending test notification...")
    success = notifier.send_notification(
        title="Claude Notify Test",
        message="This is a test notification",
        timeout=5
    )
    
    if success:
        click.echo("✓ Test notification sent successfully")
    else:
        click.echo("✗ Test notification failed", err=True)


@cli.group()
def config():
    """Manage notification preferences"""
    pass


@config.command("show")
def config_show():
    """Show current configuration"""
    config_data = load_config()
    click.echo("Current Configuration:")
    click.echo("=" * 30)
    for key, value in config_data.items():
        click.echo(f"{key}: {value}")


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str):
    """Set a configuration value"""
    config_data = load_config()
    
    # Convert value types
    if key in ["timeout", "interval"]:
        value = int(value)
    elif key in ["sound"]:
        value = value.lower() in ["true", "yes", "1", "on"]
    
    config_data[key] = value
    save_config(config_data)
    click.echo(f"✓ Set {key} = {value}")


@config.command("reset")
def config_reset():
    """Reset configuration to defaults"""
    save_config(get_default_config())
    click.echo("✓ Configuration reset to defaults")


@cli.command()
@click.option(
    "--event-type", "-e",
    help="Override the event type (PreToolUse, PostToolUse, Notification, Stop, SubagentStop)"
)
@click.option(
    "--test", "-t",
    is_flag=True,
    help="Test mode - read from test.json file instead of stdin"
)
def hook(event_type: Optional[str], test: bool):
    """
    Process Claude Code hook events from JSON input
    
    This command reads JSON from stdin and sends notifications based on the hook event.
    It's designed to be used in Claude Code hook configurations.
    
    Example usage in settings.json:
    
    \b
    {
      "hooks": {
        "PreToolUse": [{
          "matcher": ".*",
          "hooks": [{
            "type": "command",
            "command": "claude-notify hook"
          }]
        }]
      }
    }
    """
    handler = HookHandler()
    
    if test:
        # Test mode - read from file
        try:
            import json
            with open("test.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            click.echo("Error: test.json not found", err=True)
            sys.exit(1)
        except Exception as e:
            click.echo(f"Error reading test.json: {e}", err=True)
            sys.exit(1)
    else:
        # Read JSON from stdin
        data = handler.read_stdin_json()
        if not data:
            click.echo("Error: No JSON data received from stdin", err=True)
            sys.exit(1)
    
    # Determine event type
    if not event_type:
        event_type = handler.determine_event_type(data)
        if not event_type:
            click.echo("Error: Could not determine event type from JSON data", err=True)
            click.echo("Use --event-type to specify the event type explicitly", err=True)
            sys.exit(1)
    
    # Process the hook event
    success = handler.process_hook_event(event_type, data)
    
    if not success:
        click.echo("Warning: Failed to send notification", err=True)
        # Don't exit with error code to avoid blocking Claude operations
    
    # Exit successfully to not block Claude
    sys.exit(0)


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()