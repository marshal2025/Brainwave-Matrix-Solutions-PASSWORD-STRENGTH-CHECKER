
# PassGuard — Password Strength Checker (Brainwave Matrix Solutions Internship)

**Intern:** Marshal Onome Michael  
**For:** Brainwave Matrix Solutions — Cyber Security Intern Task (Password Strength Checker)  
**Contact:** marshalonome@gmail.com

## What this tool does
PassGuard is a lightweight password strength checker that evaluates passwords on:
- Length
- Character variety (lowercase, uppercase, digits, symbols)
- Uniqueness (number of unique characters)
- Estimated Shannon entropy (bits)
- Presence in a small built-in common-password list

Outputs a score (0-100) and a verdict: **Weak / Medium / Strong / Very Strong**, plus suggestions to improve.

## Files
- `passguard.py` — main CLI script (use this for the internship submission).
- `passguard_gui.py` — optional Tkinter GUI for demo (not required).
- `requirements.txt` — minimal deps.
- `submission_notes.txt` — LinkedIn caption + demo script + checklist.

## Quick usage (CLI)
Interactive masked input:
```bash
python passguard.py --interactive
```
Direct password (be cautious on shared machines):
```bash
python passguard.py --password "P@ssw0rd123"
```
Pipe input:
```bash
echo "P@ssw0rd123" | python passguard.py
```

## Example output
```
========================================
PassGuard — Password Strength Report
========================================
Length: 11 chars
Character types: lower, upper, digit, symbol
Unique characters: 9
Estimated entropy: 46.32 bits
----------------------------------------
Score: 71 / 100  -> Strong

Suggestions:
 - Avoid common passwords (e.g., '123456', 'password').
========================================
```

## Notes & safety
- Do not paste highly sensitive passwords into shared devices or public platforms.
- This tool is for educational purposes and gives heuristic guidance — for enterprise use, consider integrating with established libraries (e.g., zxcvbn) and corporate password policies.

## Improvements (optional)
- Integrate a larger common-password database (bcrypt-hashed list or zxcvbn).
- Add password breach checks using HaveIBeenPwned API (k-Anonymity model).
- Add strength-meter widget for web UI.
