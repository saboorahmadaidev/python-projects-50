from plyer import notification
import time

if __name__ == "__main__":
    while True:
        notification.notify(
            title="Desktop Notifier",
            message="This is a desktop notification.",
            timeout=10
        )
        time.sleep(60)  # Wait for 60 seconds before showing the next notification