# rexec: A Python Script Execution Utility

`rexec` was created to execute Python scripts within their own namespaces. It saves the script to your local drive and caches it for future use. Each `rexec` call checks the local cache to avoid downloading the same script from the URL multiple times.

## Installation

To "install" this utility, save the [/core/boot.py](https://github.com/jesusjorge/rexec/blob/main/core/boot.py) file into your project folder and modify the `basePath` string inside the file.

### Recommended Paths

- **Linux:** `/home/{user}/lib/`
- **Windows:** `C:\ProgramData\lib\`

## Usage

To call the utility in your Python script, use the following code:

```python
with open('/home/user/lib/boot.py') as file:
    exec(file.read())
