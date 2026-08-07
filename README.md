### Host & Port Monitor


This project verifies the availability of ports on your network.

This dashboard is made for developers that need to check if their servers, databases etc work correctly


## Features
- TCP Status Checking
- HTML Dashboard
- Uptime & Latency Tracking
- Storing Old Data


## Installation
1. Clone the directory
Open folder where you want to clone this repository.
Open the terminal and use the command
git clone https://github.com/deqfo/hostportmonitor.git
cd hostportmonitor
2. Use command "uv sync" to set up a virutal environment
3. Verify the installation - open your terminal, first use the command "uv run pytest" to check the errors and then use "uv run ruff check" to check if the code is okay


## Usage
1. Running the Monitor
Use the command: uv run python -m src.main
Output could look like this:
[ONLINE] Google DNS (8.8.8.8:53) - 44.33 ms / Uptime: 100.0%
[ONLINE] Google Web (google.com:80) - 61.21 ms / Uptime: 100.0%
2. You can add or modify hosts and ports by editing data/config.json
3. After running the script you can open site/index.html in your browser to see a dashboard


## How it works
<img width="1118" height="584" alt="{8EEDBBED-1328-42ED-8141-9B57367E866F}" src="https://github.com/user-attachments/assets/3d04701b-4e0f-4eaa-b9de-b19763f80fdb" />


## Tech Stack
Language: Python
Dependency & Environment Management: uv
Testing: pytest
Code Checking: ruff
Automation: GitHub automation
Hosting: GitHub pages
Note on the synthetic data:
The targets listen in data/config.json use public IP adresses like google.com or local adresses such as 127.0.0.1 to verify the connection.
The data/history.json file stores a timeline of all previous results

## Example output
<img width="1186" height="447" alt="{95A2D2A4-278F-4005-BF5C-EE411D390233}" src="https://github.com/user-attachments/assets/37b7d03a-d000-436c-b74c-1a89ec500e29" />


Kristián Eliaš 2026 ©
