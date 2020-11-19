# System monitorowania otwartych portów z funkcją porównania z wzorcowym zestawem i systemem powiadamiania (np. w oparciu o ndiff)

## Requirements

nmap

## Usage

Add script user to /etc/sudoers, example [here](https://phoenixnap.com/kb/how-to-create-sudo-user-on-ubuntu). Otherwise cron won't be able to start the script automatically, it would require to enter the password manually.

```bash
sudo python3 main.py wzorcowe_porty
```

### Input file format

Monitored ports:
`ip;protocol;port_number`

Users to be notified:
`<email-address>`