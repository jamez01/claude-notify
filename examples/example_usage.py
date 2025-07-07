#!/usr/bin/env python3
"""Example usage of Claude Notify"""

from claude_notify import ClaudeNotifier
import time


def main():
    # Create a notifier instance
    notifier = ClaudeNotifier(app_name="Claude Assistant")
    
    print("Claude Notify Example")
    print("=" * 40)
    
    # Check system dependencies
    deps = notifier.check_dependencies()
    print(f"System: {notifier.system}")
    print(f"Native support: {'Yes' if deps['native'] else 'No'}")
    print(f"Method: {deps.get('method', 'unknown')}")
    print()
    
    # Example 1: Basic notification
    print("1. Sending basic notification...")
    success = notifier.send_notification(
        title="Claude Ready",
        message="Claude is ready to assist you!"
    )
    print(f"   Result: {'Success' if success else 'Failed'}")
    time.sleep(2)
    
    # Example 2: Urgent notification with custom timeout
    print("\n2. Sending urgent notification...")
    success = notifier.send_notification(
        title="Claude Needs Attention",
        message="Your Claude session requires immediate input",
        urgency="critical",
        timeout=15,
        sound=True
    )
    print(f"   Result: {'Success' if success else 'Failed'}")
    time.sleep(2)
    
    # Example 3: Silent notification
    print("\n3. Sending silent notification...")
    success = notifier.send_notification(
        title="Claude Update",
        message="Your task has been completed",
        sound=False,
        timeout=5
    )
    print(f"   Result: {'Success' if success else 'Failed'}")
    
    # Example 4: Different urgency levels
    print("\n4. Testing urgency levels...")
    for urgency in ["low", "normal", "critical"]:
        print(f"   Sending {urgency} urgency notification...")
        notifier.send_notification(
            title=f"Claude - {urgency.title()} Priority",
            message=f"This is a {urgency} priority message",
            urgency=urgency,
            timeout=5
        )
        time.sleep(3)
    
    print("\nExample completed!")


if __name__ == "__main__":
    main()