import os
import hashlib
import json
import argparse
import sys

def compute_hash(filepath, algo='sha256'):
    hash_func = hashlib.new(algo)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def scan_directory(directory, algo='sha256'):
    hashes = {}
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            try:
                hashes[path] = compute_hash(path, algo)
            except Exception as e:
                print(f"Error hashing {path}: {e}")
    return hashes

def save_baseline(hashes, baseline_file):
    with open(baseline_file, 'w') as f:
        json.dump(hashes, f, indent=2)

def load_baseline(baseline_file):
    with open(baseline_file, 'r') as f:
        return json.load(f)

def compare_hashes(baseline, current):
    changed = []
    for path, old_hash in baseline.items():
        new_hash = current.get(path)
        if new_hash is None:
            changed.append((path, 'REMOVED'))
        elif new_hash != old_hash:
            changed.append((path, 'MODIFIED'))
    for path in current:
        if path not in baseline:
            changed.append((path, 'NEW'))
    return changed

def main():
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

    if args.file:
        if not os.path.isfile(args.file):
            print(f"File not found: {args.file}")
            sys.exit(1)
        hash_value = compute_hash(args.file, args.algo)
        print(f"{args.algo.upper()} hash of {args.file}: {hash_value}")
        sys.exit(0)

    if not args.directory:
        parser.error("the following arguments are required: directory (unless using --file)")

    if args.init:
        hashes = scan_directory(args.directory, args.algo)
        save_baseline(hashes, args.baseline)
        print(f"Baseline saved to {args.baseline}")
    else:
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
    main()