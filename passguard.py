
#!/usr/bin/env python3
"""
PassGuard - Password Strength Checker (CLI)
Usage:
  python passguard.py --password "P@ssw0rd123"
  or interactively: python passguard.py
"""

import argparse
import math
import sys
import getpass
from pathlib import Path

COMMON_PASSWORDS = {
    "123456","password","123456789","12345678","12345","111111","1234567","qwerty",
    "abc123","123123","iloveyou","password1","000000","qwerty123","letmein","monkey",
    "dragon","baseball","master","sunshine","ashley","football","jesus","ninja","mustang"
}

SYMBOLS = r"""!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

def shannon_entropy(s: str) -> float:
    # Shannon entropy per character (bits/char) * length = total bits
    if not s:
        return 0.0
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    entropy = 0.0
    length = len(s)
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy * length  # total entropy bits

def score_password(pw: str) -> dict:
    length = len(pw)
    categories = {
        "lower": any(c.islower() for c in pw),
        "upper": any(c.isupper() for c in pw),
        "digit": any(c.isdigit() for c in pw),
        "symbol": any(c in SYMBOLS for c in pw),
    }
    unique_chars = len(set(pw))
    entropy_bits = shannon_entropy(pw)
    is_common = pw.lower() in COMMON_PASSWORDS
    suggestions = []

    # Heuristics for scoring
    score = 0
    # length buckets
    if length >= 12:
        score += 30
    elif length >= 8:
        score += 15
    elif length >= 6:
        score += 5
    # variety
    score += sum(10 for v in categories.values() if v)
    # uniqueness and entropy
    if unique_chars >= max(8, length // 2):
        score += 10
    # entropy contribution (scaled)
    score += min(40, int(entropy_bits))  # cap contribution

    # Penalties
    if is_common:
        suggestions.append("Avoid common passwords (e.g., '123456', 'password').")
        score = max(0, score - 50)
    if length < 6:
        suggestions.append("Use at least 8-12 characters.")
    if not categories["digit"]:
        suggestions.append("Include digits (0-9).")
    if not categories["upper"]:
        suggestions.append("Include uppercase letters (A-Z).")
    if not categories["lower"]:
        suggestions.append("Include lowercase letters (a-z).")
    if not categories["symbol"]:
        suggestions.append("Include symbols (e.g., !@#$%).")
    if unique_chars < 4:
        suggestions.append("Avoid repeated characters (e.g., 'aaaa').")

    # Normalize score to 0-100
    score = max(0, min(100, score))

    # Verdict
    if score < 30:
        verdict = "Weak"
    elif score < 60:
        verdict = "Medium"
    elif score < 85:
        verdict = "Strong"
    else:
        verdict = "Very Strong"

    return {
        "password": pw if len(pw) <= 50 else pw[:47] + "...",
        "length": length,
        "categories": categories,
        "unique_chars": unique_chars,
        "entropy_bits": round(entropy_bits, 2),
        "is_common": is_common,
        "score": score,
        "verdict": verdict,
        "suggestions": suggestions
    }

def print_report(r: dict):
    print("="*40)
    print("PassGuard — Password Strength Report")
    print("="*40)
    print(f"Length: {r['length']} chars")
    cats = [k for k,v in r['categories'].items() if v]
    print(f"Character types: {', '.join(cats) if cats else 'None'}")
    print(f"Unique characters: {r['unique_chars']}")
    print(f"Estimated entropy: {r['entropy_bits']} bits")
    print(f"Common password: {'Yes' if r['is_common'] else 'No'}")
    print("-"*40)
    print(f"Score: {r['score']} / 100  -> {r['verdict']}")
    if r['suggestions']:
        print("\nSuggestions:")
        for s in r['suggestions']:
            print(" - " + s)
    print("="*40)

def main():
    parser = argparse.ArgumentParser(prog="passguard", description="Password Strength Checker (PassGuard)")
    parser.add_argument("--password", "-p", help="Password to evaluate (use cautiously on shared machines)")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive prompt (masked input)")
    args = parser.parse_args()

    if args.password and args.interactive:
        print("[!] Use either --password or --interactive, not both.")
        return

    if args.password:
        pw = args.password
    elif args.interactive or sys.stdin.isatty():
        try:
            pw = getpass.getpass("Enter password to evaluate: ")
        except Exception:
            pw = input("Enter password to evaluate: ")
    else:
        # Read from stdin (pipe)
        pw = sys.stdin.read().strip()

    if not pw:
        print("[!] No password provided.")
        return

    report = score_password(pw)
    print_report(report)

if __name__ == "__main__":
    main()
