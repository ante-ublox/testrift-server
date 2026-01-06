## TestRift Server (`testrift-server`)

Python server for TestRift real-time test runs: live log streaming, result storage, and a web UI for browsing and analysis.

### Experimental

TestRift is currently in an **experimental** phase. APIs, configuration, and data formats may change at any time **without notice**.

### Install

```bash
pip install testrift-server
```

### Run

```bash
testrift-server
```

Or:

```bash
python -m testrift_server
```

### Configuration

- The server loads configuration from either:
  - `testrift_server.yaml` in the directory you run `testrift-server` from, or
  - `TESTRIFT_SERVER_YAML` (a filesystem path to a YAML config file; absolute path recommended).

For the full configuration reference, see [server_config.md](docs/server_config.md).


