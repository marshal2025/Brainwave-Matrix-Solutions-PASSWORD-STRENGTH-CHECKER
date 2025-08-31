
#!/usr/bin/env python3
"""Optional GUI for PassGuard (Tkinter). Not required for the internship but included for demo."""
import tkinter as tk
from tkinter import ttk, messagebox
from passguard import score_password, print_report

def on_check():
    pw = entry.get()
    if not pw:
        messagebox.showwarning("PassGuard", "Please enter a password to evaluate.")
        return
    r = score_password(pw)
    # show a simple summary
    summary = f"Score: {r['score']} / 100  ({r['verdict']})\nEntropy: {r['entropy_bits']} bits"
    messagebox.showinfo("PassGuard Result", summary)

app = tk.Tk()
app.title("PassGuard - Password Strength Checker")
app.geometry("420x140")
frame = ttk.Frame(app, padding=12)
frame.pack(fill="both", expand=True)
ttk.Label(frame, text="Enter password:").pack(anchor="w")
entry = ttk.Entry(frame, show="*")
entry.pack(fill="x", pady=6)
ttk.Button(frame, text="Check Strength", command=on_check).pack(pady=6)
app.mainloop()
