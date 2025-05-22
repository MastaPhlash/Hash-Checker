import os
import sys
import json
import hashlib
import argparse

def compute_hash(filepath, algo='sha256'):
    """
    Compute the hash of a file using the specified algorithm (default: sha256).
    Reads the file in chunks for efficiency.
    """
    hash_func = hashlib.new(algo)  # Create a new hash object (sha256 or md5)
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(8192)  # Read file in 8KB chunks
            if not chunk:
                break
            hash_func.update(chunk)  # Update hash with chunk
    return hash_func.hexdigest()  # Return the hex digest string

def scan_directory(directory, algo='sha256'):
    """
    Recursively scan a directory and compute hashes for all files.
    Returns a dict mapping file paths to their hashes.
    """
    hashes = {}
    for root, _, files in os.walk(directory):  # Walk through all subdirectories
        for name in files:
            path = os.path.join(root, name)  # Full path to the file
            try:
                hashes[path] = compute_hash(path, algo)  # Compute and store hash
            except Exception as e:
                print(f"Error hashing {path}: {e}")  # Print error if file can't be hashed
    return hashes

def save_baseline(hashes, baseline_file):
    """
    Save the hashes dictionary to a JSON file.
    Used to create or update the baseline.
    """
    with open(baseline_file, 'w') as f:
        json.dump(hashes, f, indent=2)  # Write hashes as pretty-printed JSON

def load_baseline(baseline_file):
    """
    Load the baseline hashes from a JSON file.
    Handles missing or corrupted files gracefully.
    """
    if not os.path.isfile(baseline_file):
        # If the baseline file doesn't exist, prompt user to initialize
        print(f"Baseline file '{baseline_file}' does not exist. Please initialize with --init.")
        sys.exit(1)
    try:
        with open(baseline_file, 'r') as f:
            return json.load(f)  # Load and return the JSON data
    except json.JSONDecodeError:
        # If the file is empty or corrupted, prompt user to re-initialize
        print(f"Baseline file '{baseline_file}' is empty or corrupted. Please re-initialize with --init.")
        sys.exit(1)

def compare_hashes(baseline, current):
    """
    Compare baseline and current hashes.
    Returns a list of (path, status) tuples for changed, removed, or new files.
    """
    changed = []
    # Check for removed or modified files
    for path, old_hash in baseline.items():
        new_hash = current.get(path)
        if new_hash is None:
            changed.append((path, 'REMOVED'))  # File was removed
        elif new_hash != old_hash:
            changed.append((path, 'MODIFIED'))  # File was modified
    # Check for new files
    for path in current:
        if path not in baseline:
            changed.append((path, 'NEW'))  # File is new
    return changed

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Hash Checker")
    parser.add_argument('directory', nargs='?', help="Directory to scan")
    parser.add_argument('--algo', choices=['sha256', 'md5'], default='sha256', help="Hash algorithm")
    parser.add_argument('--baseline', default='baseline.json', help="Baseline file")
    parser.add_argument('--init', action='store_true', help="Initialize baseline")
    parser.add_argument(
        '--file',
        help="Hash a single file and print its hash (for testing or verification; skips directory scan)"
    )
    # Show help if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(0)
    args = parser.parse_args()

    # If --file is specified, hash the given file and exit
    if args.file:
        if not os.path.isfile(args.file):
            print(f"File not found: {args.file}")
            sys.exit(1)
        hash_value = compute_hash(args.file, args.algo)
        print(f"{args.algo.upper()} hash of {args.file}: {hash_value}")
        sys.exit(0)

    # Require directory argument unless --file is used
    if not args.directory:
        parser.error("the following arguments are required: directory (unless using --file)")

    if args.init:
        # Initialize and save baseline hashes for the directory
        hashes = scan_directory(args.directory, args.algo)
        save_baseline(hashes, args.baseline)
        print(f"Baseline saved to {args.baseline}")
    else:
        # Load baseline and compare with current hashes
        baseline = load_baseline(args.baseline)
        current = scan_directory(args.directory, args.algo)
        changes = compare_hashes(baseline, current)
        if not changes:
            print("No changes detected.")
        else:
            print("Changes detected:")
            for path, status in changes:
                print(f"{status}: {path}")

if __name__ == "__main__":
    # Entry point for the script
    main()