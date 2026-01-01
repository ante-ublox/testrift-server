# Server Configuration

The server can be configured using a YAML configuration file named `testrift_server.yaml`.

## Configuration File

### Where to put `testrift_server.yaml`

Use one of these options:

- **Working directory config (recommended)**: create `testrift_server.yaml` in the directory you run `testrift-server` from.
- **Explicit config path**: set `TESTRIFT_SERVER_CONFIG` to the path of your config file (absolute path recommended).

Example (PowerShell):

```powershell
$env:TESTRIFT_SERVER_CONFIG = "C:\\path\\to\\testrift_server.yaml"
testrift-server
```

### Configuration structure

Create a `testrift_server.yaml` file with the following structure:

```yaml
server:
  # Port number for the server to listen on
  port: 8080
  
  # Whether to only accept connections from localhost (127.0.0.1)
  # Set to false to allow connections from any IP address
  localhost_only: true

data:
  # Directory path for storing test runs
  directory: "data"
  
  # Default retention days for test runs when not specified by client
  # Set to null for no automatic cleanup
  default_retention_days: 7

attachments:
  # Whether attachment upload is enabled
  enabled: true
  
  # Maximum attachment file size (supports B, KB, MB, GB, TB)
  max_size: "10MB"
```

## Configuration Options

### Server Settings

- **port** (integer, default: 8080): The port number for the server to listen on. Must be between 1 and 65535.
- **localhost_only** (boolean, default: true): If true, the server only accepts connections from localhost (127.0.0.1). If false, it accepts connections from any IP address.

### Data Settings

- **directory** (string, default: "data"): The directory path where test run data is stored.
- **default_retention_days** (integer, null, or 0, default: 7): Default number of days to retain test runs when not specified by the client. Set to `null` or `0` for no automatic cleanup.

### Attachment Settings

- **enabled** (boolean, default: true): Whether attachment upload functionality is enabled. When disabled, attachment upload endpoints return 403 Forbidden.
- **max_size** (string, default: "10MB"): Maximum file size for attachments. Supports units: B (bytes), KB (kilobytes), MB (megabytes), GB (gigabytes), TB (terabytes). Examples: "10MB", "1GB", "500KB".

## Examples

### Development Configuration
```yaml
server:
  port: 8080
  localhost_only: true

data:
  directory: "data"
  default_retention_days: 1

attachments:
  enabled: true
  max_size: "5MB"
```

### Production Configuration
```yaml
server:
  port: 9000
  localhost_only: false

data:
  directory: "/var/log/test_runs"
  default_retention_days: 30

attachments:
  enabled: true
  max_size: "50MB"
```

### No Cleanup Configuration
```yaml
server:
  port: 8080
  localhost_only: true

data:
  directory: "data"
  default_retention_days: null

attachments:
  enabled: true
  max_size: "10MB"
```

### Attachments Disabled Configuration
```yaml
server:
  port: 8080
  localhost_only: true

data:
  directory: "data"
  default_retention_days: 7

attachments:
  enabled: false
  max_size: "10MB"  # Ignored when disabled
```

## Default Behavior

If no `testrift_server.yaml` file is found, the server will use these defaults:
- Port: 8080
- Localhost only: true
- Default retention days: 7
- Data directory: "data"
- Attachments enabled: true
- Max attachment size: "10MB"

## Error Handling

The server will exit with an error if:
- The configuration file contains invalid YAML syntax
- The required `server` section is missing
- Configuration values are invalid (e.g., port out of range)

A warning will be displayed if the configuration file is not found, and defaults will be used.
