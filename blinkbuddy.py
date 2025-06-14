import tkinter as tk
import pyttsx3
import sys
import os

# -------------------- Constants --------------------
REMINDER_INTERVAL = 20 * 60  # 20 minutes
REMINDER_DURATION = 20       # 20 seconds

# -------------------- Text-to-Speech --------------------
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
except Exception as e:
    print(f"Text-to-speech initialization failed: {e}")

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech error: {e}")

# -------------------- Logic --------------------
is_running = False  # Track session state

def start_session():
    global is_running
    if not is_running:
        is_running = True
        start_button.config(state="disabled")
        stop_button.config(state="normal")
        status_label.config(text="Session started! Reminder every 20 minutes.")
        speak("Session started!")
        run_countdown(REMINDER_INTERVAL)

def stop_session():
    global is_running
    is_running = False
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    timer_label.config(text="")
    message_label.config(text="")
    countdown_label.config(text="")
    status_label.config(text="Session stopped.")
    speak("Session stopped.")
    root.attributes('-topmost', False)  # Ensure window isn't topmost
    root.deiconify()  # Restore window if minimized

def run_countdown(t):
    if not is_running:
        return
    if t >= 0:
        mins, secs = divmod(t, 60)
        timer_label.config(text=f"Next reminder in: {mins:02d}:{secs:02d}")
        root.after(1000, run_countdown, t - 1)
    else:
        do_reminder()

def do_reminder():
    if not is_running:
        return
    root.deiconify()  # Restore window if minimized
    root.attributes('-topmost', True)  # Bring window to top
    root.focus_force()  # Ensure window gains focus
    speak("Time to relax your eyes.")
    message_label.config(text="🔔 Look 20 feet away for 20 seconds")
    
    def run_20s_countdown(t):
        if not is_running:
            countdown_label.config(text="")
            message_label.config(text="")
            root.attributes('-topmost', False)  # Restore normal window state
            return
        if t >= 0:
            countdown_label.config(text=f"{t} s")
            root.after(1000, run_20s_countdown, t - 1)
        else:
            countdown_label.config(text="")
            message_label.config(text="✅ Done! Eyes say thank you!")
            speak("20 seconds done. You may continue.")
            root.attributes('-topmost', False)  # Restore normal window state
            root.iconify()  # Minimize window after break
            root.after(2000, lambda: message_label.config(text="") if is_running else None)
            run_countdown(REMINDER_INTERVAL)

    run_20s_countdown(REMINDER_DURATION)

# -------------------- GUI --------------------
root = tk.Tk()
root.title("BlinkBuddy - 20-20-20 Rule")
root.geometry("420x350")
root.resizable(False, False)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root.iconbitmap(resource_path("blink.ico"))

# Heading
heading_label = tk.Label(
    root,
    text="       BlinkBuddy 👁️",
    font=("Helvetica", 18, "bold"),
    anchor="center"
)
heading_label.pack(pady=10, fill="x", expand=True)

# Welcome
welcome_msg = tk.Label(
    root,
    text="Hi, I’m BlinkBuddy,\nFriend of your beautiful eyes 👀",
    font=("Helvetica", 12),
    justify="center"
)
welcome_msg.pack()

# Start and Stop Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(
    button_frame,
    text="Start Session ✅",
    font=("Helvetica", 13),
    bg="lightgreen",
    command=start_session,
    cursor="hand2"
)
start_button.pack(side="left", padx=5)

stop_button = tk.Button(
    button_frame,
    text="Stop Session 🛑",
    font=("Helvetica", 13),
    bg="salmon",
    command=stop_session,
    cursor="hand2",
    state="disabled"
)
stop_button.pack(side="left", padx=5)

# Timer
timer_label = tk.Label(root, text="", font=("Helvetica", 14), fg="blue")
timer_label.pack()

# Reminder message
message_label = tk.Label(root, text="", font=("Helvetica", 13), fg="red")
message_label.pack(pady=(5, 0))

# 20 sec countdown
countdown_label = tk.Label(root, text="", font=("Helvetica", 30, "bold"), fg="black")
countdown_label.pack(pady=(5, 10))

# Status
status_label = tk.Label(root, text="", font=("Helvetica", 11), fg="green")
status_label.pack()

# Footer
footer = tk.Label(root, text="Made with ❤️ by Shubham Kumar", font=("Helvetica", 10))
footer.pack(side="bottom", pady=10, fill="x")

# Intro voice
root.after(800, lambda: speak("Hi, I am BlinkBuddy. I am here to help you relax your eyes so they don't feel strain. Just click on Start Session."))

root.mainloop()