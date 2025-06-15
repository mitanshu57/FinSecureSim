# FinSecureSim: Responsible Ransomware Simulation for Fintech Security

## Overview

FinSecureSim is a Python-based ransomware simulator designed to mimic real ransomware behavior in a safe, controlled environment. It encrypts dummy or sanitized test files, displays a ransom note GUI, and simulates restricted functionalities without causing any data loss. The tool helps fintech organizations validate their detection, response, and recovery processes, train staff, and ensure backup and monitoring systems work effectively—all while preserving privacy and using only synthetic data.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
   - [Preparing the Sandbox](#preparing-the-sandbox)
   - [Running the Simulator](#running-the-simulator)
   - [Interpreting Results](#interpreting-results)
6. [Logging & Reporting](#logging--reporting)
7. [Safety Precautions](#safety-precautions)
8. [Integration & Testing](#integration--testing)
9. [Extending the Simulator](#extending-the-simulator)
10. [Troubleshooting](#troubleshooting)
11. [Contributing](#contributing)
12. [License](#license)

---

## Features

- **Reversible Encryption/Decryption**: Uses AES symmetric encryption (via PyCryptodome) on configured dummy files; original contents and filenames are fully restored upon correct key entry or backup recovery.
- **Ransom Note GUI**: Displays a customizable ransom message with countdown timer using Tkinter (with optional Pillow support for images), simulating restricted UI without harming data.
- **Configurable Simulation**: JSON/YAML configuration for sandbox paths, file-type filters, ransom note text, timer duration, backup triggers, and more.
- **Logging & Reporting**: Structured logs of encryption/decryption events, GUI interactions, detection and recovery timings; generates a summary report with actionable insights.
- **Backup Integration**: Simulate reliance on backup by forcing backup-based recovery, verifying offline or versioned backup processes using dummy data.
- **Safety Checks**: Verifies target paths to avoid running on real data, enforces sandbox isolation, and handles keys securely.
- **Modular Design**: Code organized into modules for encryption, GUI, logging, configuration, and optional extensions (phishing simulation, network propagation, exfiltration mock-ups).

---

## Prerequisites

- **Python Version**: 3.7 or higher recommended.
- **Libraries**:
  - [`pycryptodome`](https://pypi.org/project/pycryptodome/) for AES encryption/decryption.
  - `tkinter` (usually included in standard Python distributions) for GUI.
  - [`Pillow`](https://pypi.org/project/Pillow/) (optional) if embedding images in the ransom note.
  - `pyyaml` or `json` (built-in) for configuration parsing, if using YAML config.
  - Standard libraries: `os`, `shutil`, `logging`, `argparse`, `datetime`, etc.
- **Environment**:
  - An isolated VM, container, or dedicated test machine to avoid interference with production data.
  - Virtual environment (recommended) to manage dependencies.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/FinSecureSim.git
   cd FinSecureSim
   ```
2. **Set Up Virtual Environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   - If using YAML configs: ensure `pyyaml` is present in `requirements.txt`.
   - Confirm that `tkinter` is available (on Linux, you may need to install system package, e.g., `sudo apt-get install python3-tk`).

---

## Configuration

FinSecureSim uses a configuration file (JSON or YAML) to define simulation parameters. A sample configuration (`config.yaml` or `config.json`) might include:

```yaml
# config.yaml
sandbox_directory: "/path/to/test_sandbox"
file_filters:
  include_extensions: [".csv", ".json", ".xlsx"]
  exclude_patterns: ["secret_prod_data"]
ransom_note:
  title: "Important Notice"
  message: |
    Your files have been encrypted! To recover, provide the decryption key.
    Contact attacker@example.com with payment proof.
  countdown_seconds: 300
  image_path: "assets/ransom_bg.png"  # optional, for GUI background
backup:
  enabled: true
  backup_directory: "/path/to/dummy_backup"
  auto_restore_on_timeout: true
logging:
  log_directory: "logs"
  log_level: "INFO"
safety:
  enforce_sandbox: true
  allowed_paths: ["/path/to/test_sandbox"]
extensions:
  phishing_simulation: false
  network_emulation: false
  exfiltration_simulation: false
```

**Key Configuration Sections**:

- `sandbox_directory`: Path containing dummy or sanitized test files. Must NOT point to real production data.
- `file_filters`: Specifies which files to encrypt. Use extensions lists or regex patterns to include/exclude.
- `ransom_note`: Text shown in Tkinter GUI and countdown timer settings.
- `backup`: Options for simulating backup-based recovery (dummy backup directory with copies of original files).
- `logging`: Where to store logs and at what verbosity.
- `safety`: Enforce sandbox restrictions; list allowed paths; abort if configuration points outside.
- `extensions`: Toggles for advanced modules (phishing trigger, network propagation, exfil simulation).

Adjust the configuration as needed before each simulation run.

---

## Usage

### 1. Preparing the Sandbox

- Create a dedicated sandbox directory with dummy fintech data files. Examples:
  - Fake transaction CSVs (e.g., `transactions_2025Q1.csv`).
  - Sample JSON logs (e.g., `user_activity.json`).
  - Placeholder documents (e.g., `report.xlsx`).
- Ensure backups: copy the sandbox directory contents to a separate dummy backup location if `backup.enabled` is true.
- Verify configuration’s `sandbox_directory` and `backup_directory` paths are correct and isolated.

### 2. Running the Simulator

Invoke the main script, pointing to the configuration file, e.g.:

```bash
python finsecuresim.py --config config.yaml
```

- **Arguments**:
  - `--config`: Path to config file.
  - Other optional flags (e.g., `--dry-run` to list files that would be encrypted without performing encryption).
- **Flow**:
  1. **Safety Check**: Verify sandbox path is within allowed paths.
  2. **AES Key Generation**: Generate a random AES key; store in a secure temp file (e.g., `key.key`) or in-memory. Log key generation event.
  3. **Encryption Phase**:
     - Traverse sandbox directory; for each matching file:
       - Read contents, encrypt using AES (CBC/GCM as configured).
       - Rename (e.g., append `.enc`) and log the event (timestamp, file path, size).
       - Optionally preserve metadata (e.g., original timestamps) in a metadata store.
  4. **Launch Ransom Note GUI**:
     - Display ransom message, countdown timer, and input field for the key.
     - Grey out or disable dummy “Open” buttons if simulating restricted functionality.
     - Provide a “Report Incident” or “Help” button to simulate triggering an incident response workflow.
  5. **Key Verification**:
     - If correct key entered before timeout: proceed to decryption.
     - If incorrect or timeout occurs:
       - Display a “Failed” message or “Key expired” notice, but do not delete data.
       - If `backup.auto_restore_on_timeout` is true: automatically trigger backup-based recovery.
       - Allow repeated attempts or proceed to recovery logic.
  6. **Decryption/Recovery**:
     - Decrypt encrypted files using stored AES key or restore from dummy backup.
     - Restore original filenames and contents; verify integrity (checksum comparison).
     - Log each decryption or restoration event with timestamp and outcome.
  7. **Report Generation**:
     - Compile logs into a summary report: detection timings (if simulated), user interaction times, backup restoration duration, success/failure indicators, and recommendations.
     - Save report to `logging.log_directory` with timestamped filename (e.g., `report_20250615T1530.json` or `.txt`).

### 3. Interpreting Results

- **Encryption Logs**: Show which files were encrypted and when. Useful to confirm correct targeting and to compare with monitoring system alerts.
- **GUI Interaction Logs**: Indicate how quickly a user/participant responded to the ransom note, whether they clicked “Report” or entered the key.
- **Recovery Metrics**: Time taken to decrypt or restore from backup; any integrity failures.
- **Recommendations**: Based on simulated detection times and recovery durations, the tool suggests improvements (e.g., faster backup retrieval, tighter monitoring thresholds).

---

## Logging & Reporting

- **Structured Logs**: Use Python’s `logging` module configured per `config.logging`:
  - **INFO** level: General events (encryption start/end, GUI launch, decryption start/end).
  - **DEBUG** level: Detailed per-file events, internal states, metadata handling.
  - **ERROR/WARNING**: Any unexpected issues or safety-check violations.
- **Log Storage**: Logs written to files under the specified `log_directory`, with timestamped filenames.
- **Summary Report**:
  - Format: JSON or plain text summary.
  - Contents:
    - List of encrypted files and timestamps.
    - User interaction timeline (when GUI appeared, when key entered or “report” clicked).
    - Detection simulation info (if integrated with SIEM/EDR mock): when alerts would have triggered.
    - Recovery timeline and integrity checks.
    - Recommendations for improving response or infrastructure.
- **Integration with Monitoring**:
  - Optionally ship logs or events to SIEM/EDR test endpoints to validate alerting rules.
  - Ensure logs are anonymized if forwarded.

---

## Safety Precautions

- **Strict Sandbox Enforcement**: The simulator verifies that the `sandbox_directory` is within allowed paths defined in configuration. If paths fall outside, the tool aborts with an error.
- **No Real Data**: Confirm that dummy files do not include any real customer PII. Use synthetic or fully sanitized datasets.
- **Key Security**: AES keys are generated per run and stored only in secure temporary files or memory; removed immediately after decryption or finalization.
- **Isolation**: Run the tool in isolated VMs/containers with no connectivity to production systems. Use snapshots or disposable environments for each simulation.
- **User Permissions**: Execute under a non-privileged test account. The tool should not run as root/administrator unless explicitly required in sandbox.
- **Backup Safety**: Dummy backup directory should not overlap with production backups; verify using configuration checks.

---

## Integration & Testing

- **CI/CD Integration**: Add a job in CI pipelines that periodically runs FinSecureSim in a fresh sandbox with sample dummy data, verifying encryption/decryption cycles succeed and logs are generated.
- **Monitoring Tuning**: Use the simulator to generate controlled “mass-file-change” events, feeding into test SIEM/EDR to refine detection rules for ransomware-like patterns.
- **Incident Response Drills**: Combine with tabletop or live drills: trigger the simulator, then practice team coordination, communication channels, and invoking backup restores.
- **API Hooks**: Optionally expose functions via a simple local API to trigger encryption or check status (for automation in larger test frameworks).

---

## Extending the Simulator

- **Phishing Trigger Module**:
  - Simulate a phishing email or malicious attachment: opening the dummy attachment invokes the encryption routine in the sandbox. Useful for end-user training.
- **Network Propagation Emulation**:
  - In a controlled lab network, simulate lateral movement by having the tool attempt to “encrypt” files on other sandboxed VMs (with explicit permission), testing network segmentation controls.
- **Exfiltration Simulation**:
  - Copy dummy files to a staging directory and simulate outbound data flows (e.g., writing to a dummy external endpoint), allowing DLP teams to test detection.
- **Stealthy Behaviors**:
  - Implement delayed encryption, selective file targeting, or partial encryption strategies to test detection of more subtle ransomware tactics.
- **Dashboard & Visualization**:
  - Build a lightweight web dashboard (Flask or similar) to display real-time metrics during simulation: number of files encrypted, elapsed time, user response status.
- **Plugin System**:
  - Design a plugin interface so external scripts can hook into pre-encryption or post-encryption events (e.g., triggering custom alerts, integrating with other test frameworks).

---

## Troubleshooting

- **GUI Doesn’t Appear**:
  - Ensure `tkinter` is installed and available. On Linux, install system package (e.g., `sudo apt-get install python3-tk`).
  - Check for errors in logs indicating GUI initialization issues.
- **Encryption Fails on Certain Files**:
  - Verify file permissions allow read/write operations in sandbox.
  - Check file filters in config: ensure extensions or patterns match desired files.
  - Examine DEBUG logs for exceptions during encryption.
- **Decryption Doesn’t Restore Files**:
  - Confirm the correct key is entered. Check that metadata store persisted original filenames.
  - Ensure backup integration is properly configured if fallback is used.
- **Safety Check Aborts Execution**:
  - Review `allowed_paths` in config. Make sure sandbox directory is listed.
  - If using relative paths, verify resolution to absolute paths within allowed scope.
- **Logging Issues**:
  - Check `log_directory` exists or can be created. Inspect file permissions.
  - Adjust `log_level` to DEBUG to see detailed messages.

---

## Contributing

1. **Fork the Repository** and create a feature branch (e.g., `feature-phishing-module`).
2. **Write Tests**: Add or extend unit tests to cover new functionality (encryption edge cases, GUI flows, config parsing).
3. **Code Style**: Follow PEP8 guidelines. Use linters (e.g., `flake8`) in CI.
4. **Pull Request**: Submit a PR with a clear description of changes, associated issues, and testing steps.
5. **Review Process**: Participate in code review; update documentation (README, examples) as needed.

---

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Inspired by common ransomware behaviors observed in the wild, but designed purely for safe testing.
- Utilizes [PyCryptodome](https://pycryptodome.readthedocs.io/) for cryptographic functions and [Tkinter](https://docs.python.org/3/library/tkinter.html) for GUI.
- Emphasizes fintech security best practices, privacy-first design, and responsible data handling.

---

##
