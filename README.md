# System monitorowania otwartych portów z funkcją porównania z wzorcowym zestawem i systemem powiadamiania (np. w oparciu o ndiff)

## Requirements

- nmap

- `pip install -r requirements.txt`

## Usage

Add script user to /etc/sudoers, example [here](https://phoenixnap.com/kb/how-to-create-sudo-user-on-ubuntu). Otherwise cron won't be able to start the script automatically after a failure, it will require to enter the password manually.

```bash
sudo python3 app.py wzorcowe_porty
```

## Input file format

Monitored open port:
`ip;protocol;port_number`

Users to be notified:
`<email-address>`

```
192.168.0.1;tcp;22
notified@admin.com
```

> **EVERY ENTRY MUST BE IN A NEW LINE**

## Configuration file parameters

**File name:** `settings.py`

- SMTP_PORT
- SMTP_SERVER
- SMTP_LOGIN
- SMTP_PASSWORD

- SMTP_SENDER
- SCAN_INTERVAL_MIN
