# WCA Competition Notifier
A Python-based automation script that monitors the World Cube Association (WCA) API for new or updated speedcubing competitions in a specific country. When a change is detected, it sends a push notification to your phone or desktop via ntfy.sh.

## Setup

### Prerequisites
- Python 3.12 or newer
- requests module

### Configuration
Create a config.json file in the root directory:
```json
{
  "country": "PL",
  "ntfy_topic": "my_private_comp_alerts_123"
}
```
- **country**: The ISO 2-letter code for your country (e.g. `US`, `PL`, `GB`).
- **ntfy_topic**: A unique string for your notification channel.

### ntfy.sh App
To receive notifications on your mobile device:
1. Download the ntfy app (iOS/Android).
1. "Subscribe to topic" using the same `ntfy_topic` you put in your config.

See [ntfy.sh](https://ntfy.sh/) for more information.

### Automation
To run this automatically every day, add it to your crontab (Linux/Mac) or Task Scheduler (Windows).
