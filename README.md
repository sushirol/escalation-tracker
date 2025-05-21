# escalation-tracker

A minimal command-line tool to track support escalations using plain text files.

## Features
- Track each escalation by unique ID
- Title-based search support
- Timestamped status updates
- One text file per escalation (stored in `~/.escalations`)

## Usage

```bash
# Start a new escalation
esc start 1234 "Abcd Corp || Battery drain"

# Update status
esc update 1234 "Requested debug logs from support team"

# Search escalations
esc search Abcd
esc search "Battery"

# List all
esc list
```

## Project Structure

```
escalation-tracker/
├── escalation_tracker.py  # Main CLI script
├── README.md              # Usage guide
├── setup.py               # Installation script
```

## Installation
Install locally using pip:

```bash
pip install .
```

Once installed, you can run the tool using:

```bash
esc [command]
```

## License
MIT
