"""Cross-platform notification system for Claude"""

import platform
import subprocess
import os
from typing import Optional, Dict, Any
from plyer import notification as plyer_notification


class ClaudeNotifier:
    """Cross-platform notification handler for Claude alerts"""
    
    def __init__(self, app_name: str = "Claude"):
        self.app_name = app_name
        self.system = platform.system().lower()
        
    def send_notification(
        self, 
        title: str, 
        message: str, 
        urgency: str = "normal",
        timeout: int = 10,
        sound: bool = True
    ) -> bool:
        """
        Send a notification across different platforms
        
        Args:
            title: Notification title
            message: Notification message
            urgency: Urgency level (low, normal, critical)
            timeout: Notification timeout in seconds
            sound: Whether to play a sound
            
        Returns:
            bool: True if notification was sent successfully
        """
        try:
            if self.system == "darwin":  # macOS
                return self._send_macos_notification(title, message, sound)
            elif self.system == "linux":
                return self._send_linux_notification(title, message, urgency, timeout)
            elif self.system == "windows":
                return self._send_windows_notification(title, message, timeout)
            else:
                # Fallback to plyer for unknown systems
                return self._send_plyer_notification(title, message, timeout)
        except Exception as e:
            print(f"Notification error: {e}")
            # Try fallback method
            return self._send_plyer_notification(title, message, timeout)
    
    def _send_macos_notification(self, title: str, message: str, sound: bool) -> bool:
        """Send notification on macOS using osascript"""
        sound_arg = "with sound" if sound else ""
        script = f'''
        display notification "{message}" with title "{title}" subtitle "{self.app_name}" {sound_arg}
        '''
        
        try:
            subprocess.run(
                ["osascript", "-e", script],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _send_linux_notification(
        self, 
        title: str, 
        message: str, 
        urgency: str, 
        timeout: int
    ) -> bool:
        """Send notification on Linux using notify-send"""
        try:
            # Check if notify-send is available
            subprocess.run(
                ["which", "notify-send"],
                check=True,
                capture_output=True
            )
            
            cmd = [
                "notify-send",
                f"--app-name={self.app_name}",
                f"--urgency={urgency}",
                f"--expire-time={timeout * 1000}",  # Convert to milliseconds
                title,
                message
            ]
            
            subprocess.run(cmd, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _send_windows_notification(self, title: str, message: str, timeout: int) -> bool:
        """Send notification on Windows using PowerShell"""
        try:
            ps_script = f'''
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] | Out-Null
            
            $template = @"
            <toast duration="long">
                <visual>
                    <binding template="ToastText02">
                        <text id="1">{title}</text>
                        <text id="2">{message}</text>
                    </binding>
                </visual>
                <audio src="ms-winsoundevent:Notification.Default" />
            </toast>
"@
            
            $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
            $xml.LoadXml($template)
            $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("{self.app_name}").Show($toast)
            '''
            
            subprocess.run(
                ["powershell", "-Command", ps_script],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _send_plyer_notification(self, title: str, message: str, timeout: int) -> bool:
        """Fallback notification using plyer library"""
        try:
            plyer_notification.notify(
                title=title,
                message=message,
                app_name=self.app_name,
                timeout=timeout
            )
            return True
        except Exception:
            return False
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Check which notification methods are available"""
        deps = {
            "plyer": True,  # Always available if installed
            "native": False
        }
        
        if self.system == "darwin":
            # macOS always has osascript
            deps["native"] = True
            deps["method"] = "osascript"
        elif self.system == "linux":
            # Check for notify-send
            try:
                subprocess.run(
                    ["which", "notify-send"],
                    check=True,
                    capture_output=True
                )
                deps["native"] = True
                deps["method"] = "notify-send"
            except subprocess.CalledProcessError:
                deps["method"] = "plyer"
        elif self.system == "windows":
            # Windows with PowerShell
            deps["native"] = True
            deps["method"] = "powershell"
        
        return deps