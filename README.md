# Hash Checker

## What it does

Hash Checker is a simple Python tool for monitoring file integrity. It calculates SHA-256 or MD5 hashes of files in a directory, saves a baseline of these hashes, and later checks if any files have been added, removed, or modified by comparing current hashes to the baseline. This is useful for detecting unauthorized changes to important files.

## How to use it

1. **Install Python 3** if you haven't already.

2. **Save the script** (`main.py`) in your desired directory.

3. **Open a terminal** and navigate to the script's directory.

4. **Initialize a baseline** of file hashes:
   ```
   python main.py <directory_to_scan> --init
   ```
   - Example:
     ```
     python main.py C:\important\files --init
     ```
   - This creates a `baseline.json` file with the hashes.

5. **Check for changes** later by running:
   ```
   python main.py <directory_to_scan>
   ```
   - Example:
     ```
     python main.py C:\important\files
     ```

6. **Hash a single file** (for testing or verification):
   ```
   python main.py --file <path_to_file>
   ```
   - Example:
     ```
     python main.py --file C:\important\files\config.txt
     ```
   - You can also specify the algorithm:
     ```
     python main.py --file C:\important\files\config.txt --algo md5
     ```

7. **Optional arguments:**
   - `--algo md5` : Use MD5 instead of SHA-256.
   - `--baseline <file>` : Specify a custom baseline file.

**Note:**  
If your directory or file path contains spaces, enclose the path in quotes.  
For example:
```
python main.py "C:\Coding\Python\Hash Checker\Hash-Checker" --init
python main.py --file "C:\Coding\Python\Hash Checker\Hash-Checker\config.txt"
```

## Example outputs

**No changes detected:**
```
No changes detected.
```

**Changes detected:**
```
Changes detected:
MODIFIED: C:\important\files\config.txt
REMOVED: C:\important\files\oldfile.log
NEW: C:\important\files\newfile.docx
```

**Hash a single file:**
```
SHA256 hash of C:\important\files\config.txt: 3a7bd3e2360a3d...
```

---

Feel free to modify or extend the script for your needs!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
