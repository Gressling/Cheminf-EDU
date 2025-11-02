# Browser Opening and Port Scanning Implementation

This document explains the technical implementation of single-instance browser opening and dynamic port detection in the ISO 42001 AI Management System.

## Overview

The application implements two key mechanisms:
1. **Dynamic Port Detection**: Automatically finds available ports when the default port (8050) is occupied
2. **Single-Instance Browser Opening**: Ensures only one browser tab opens regardless of multiple application instances

## Dynamic Port Scanning

### Implementation

The port scanning uses Python's `socket` module to test port availability through binding attempts:

```python
def find_free_port(start_port=8050, max_attempts=100):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find a free port in range {start_port}-{start_port + max_attempts}")
```

### Technical Details

- **Protocol**: Uses TCP sockets (SOCK_STREAM) for HTTP compatibility
- **Binding Test**: Attempts to bind to `127.0.0.1:port` to verify availability
- **Range**: Scans ports 8050-8149 (configurable via `max_attempts`)
- **Exception Handling**: `OSError` indicates port is occupied or restricted
- **Resource Management**: Uses context manager (`with`) for automatic socket cleanup

### Usage

```python
# Find next available port starting from 8050
port = find_free_port()

# Custom starting port and range
port = find_free_port(start_port=9000, max_attempts=50)
```

## Single-Instance Browser Opening

### Problem Statement

The application needed to prevent multiple browser tabs from opening when:
- Multiple application instances are started simultaneously
- PyInstaller executables spawn multiple processes due to reloader behavior
- Users double-click the executable multiple times

### Solution Architecture

The implementation uses a **global lock file mechanism** combined with **process detection**:

```python
def open_browser(port):
    """Open the default browser after a short delay"""
    time.sleep(1.5)  # Wait for server to start
    
    # Create a global lock file that persists across all instances
    lock_file = os.path.join(tempfile.gettempdir(), f'iso42001_browser_global.lock')
    
    try:
        # Try to create the lock file exclusively with a timeout check
        if os.path.exists(lock_file):
            # Check if lock file is older than 10 seconds (stale lock)
            lock_age = time.time() - os.path.getmtime(lock_file)
            if lock_age > 10:
                os.remove(lock_file)
        
        with open(lock_file, 'x') as f:
            f.write(f'{os.getpid()}:{port}:{time.time()}')
        
        # Clean up lock file on exit
        def cleanup_lock():
            try:
                if os.path.exists(lock_file):
                    os.remove(lock_file)
            except:
                pass
        
        atexit.register(cleanup_lock)
        
        # Open browser
        webbrowser.open(f'http://127.0.0.1:{port}')
        
    except FileExistsError:
        # Lock file exists, browser already opened by another process
        pass
```

### Lock File Mechanism

- **Location**: System temporary directory (`tempfile.gettempdir()`)
- **Naming**: `iso42001_browser_global.lock`
- **Content**: `PID:PORT:TIMESTAMP` format for debugging
- **Exclusive Creation**: Uses `open(file, 'x')` for atomic lock creation
- **Stale Lock Detection**: Removes locks older than 10 seconds
- **Cleanup**: `atexit.register()` ensures lock removal on process termination

### Process Detection

For Python script execution (non-executable), the system uses process detection:

```python
def is_first_instance():
    """Check if this is the first instance of the application"""
    current_process = psutil.Process()
    current_exe = current_process.exe()
    current_name = os.path.basename(current_exe)
    
    # Count how many processes with the same executable are running
    count = 0
    for proc in psutil.process_iter(['pid', 'exe', 'name']):
        try:
            if proc.info['exe'] == current_exe or proc.info['name'] == current_name:
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return count <= 1
```

### Threading Implementation

Browser opening runs in a separate daemon thread to prevent blocking:

```python
if should_open_browser:
    # Start browser opening in a separate thread
    browser_thread = threading.Thread(target=open_browser, args=(port,))
    browser_thread.daemon = True
    browser_thread.start()
```

## Execution Context Detection

The system behaves differently based on execution context:

```python
# Check if running as PyInstaller executable
if getattr(sys, 'frozen', False):
    # Running as executable - always try to open browser unless explicitly skipped
    should_open_browser = not should_skip_browser
    debug_mode = False
    use_reloader = False
else:
    # Running as Python script - use first instance detection
    should_open_browser = not should_skip_browser and is_first_instance()
    use_reloader = debug_mode
```

### PyInstaller vs Script Behavior

| Context | Browser Logic | Debug Mode | Reloader |
|---------|--------------|------------|----------|
| PyInstaller Executable | Global lock file only | Disabled | Disabled |
| Python Script | Process detection + lock file | Configurable | Enabled |

## Environment Variables

The system supports configuration through environment variables:

```bash
# Skip browser opening entirely
export ISO42001_SKIP_BROWSER=true

# Control debug mode (Python scripts only)
export ISO42001_DEBUG=false
```

## Error Handling

### Port Scanning Failures
```python
try:
    port = find_free_port()
except RuntimeError as e:
    print(f"Error: {e}")
    print("Please close some applications and try again.")
    sys.exit(1)
```

### Lock File Race Conditions
- **FileExistsError**: Silently ignored (browser already opened)
- **Stale locks**: Automatically cleaned up based on timestamp
- **Permission errors**: Handled gracefully in cleanup function

## Dependencies

- **socket**: Built-in Python module for network operations
- **threading**: Built-in module for concurrent browser opening
- **tempfile**: Cross-platform temporary directory location
- **atexit**: Cleanup registration for graceful shutdown
- **psutil**: Third-party library for process information
- **webbrowser**: Built-in module for system browser integration

## Testing Scenarios

The implementation handles these scenarios:

1. **Single Launch**: Normal browser opening
2. **Rapid Multiple Launches**: Only first instance opens browser
3. **Port Conflicts**: Automatically finds alternative port
4. **Stale Locks**: Automatic cleanup of old lock files
5. **Process Termination**: Cleanup on normal and abnormal exit
6. **Cross-Platform**: Works on Windows, macOS, and Linux

This dual-mechanism approach ensures reliable single-instance browser behavior across different deployment scenarios while maintaining robust port conflict resolution.