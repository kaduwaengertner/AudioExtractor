import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import subprocess

def extract_audio_tracks(video_path, audio_format):
    try:
        ffmpeg_path = os.path.join(os.path.dirname(__file__), "bin", "ffmpeg.exe")

        video_dir = os.path.dirname(video_path)
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        cmd = [
            ffmpeg_path, "-i", video_path, "-hide_banner", "-f", "null", "-"
        ]
        result = subprocess.run(
            cmd, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        output = result.stderr

        audio_tracks = [
            line for line in output.splitlines()
            if "Stream #" in line and "Audio:" in line
        ]

        if not audio_tracks:
            messagebox.showerror("Error", "No audio tracks found in the video.")
            progress_label.config(text="No audio tracks found.")
            return

        progress_bar["maximum"] = len(audio_tracks)
        progress_bar["value"] = 0

        for idx, track in enumerate(audio_tracks, start=1):
            output_file = os.path.join(video_dir, f"{video_name}_ExAudio_{idx}.{audio_format}")
            cmd = [
                ffmpeg_path, "-i", video_path,
                "-map", f"0:a:{idx - 1}", "-c:a", "pcm_f32le" if audio_format == "wav" else "libmp3lame", "-y", output_file
            ]
            subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW
            )

            progress_bar["value"] = idx
            progress_label.config(text=f"Extracted track {idx}/{len(audio_tracks)}")
            root.update_idletasks()

        progress_label.config(text="Extraction complete!")
        messagebox.showinfo("Success", f"Extracted {len(audio_tracks)} audio tracks to {video_dir}")

    except Exception as e:
        progress_label.config(text="An error occurred.")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def select_video():
    video_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=(
            ("Video Files", "*.mkv *.mp4 *.avi *.mov"),
            ("All Files", "*.*")
        )
    )
    if video_path:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, video_path)
        progress_label.config(text="Waiting to start extraction...")
        progress_bar["value"] = 0

def start_extraction():
    video_path = video_entry.get()
    audio_format = format_selector.get()

    if not video_path or not os.path.isfile(video_path):
        messagebox.showerror("Error", "Please select a valid video file.")
        progress_label.config(text="No valid video file selected.")
        return

    if audio_format not in ["mp3", "wav"]:
        messagebox.showerror("Error", "Please select a valid audio format.")
        progress_label.config(text="No valid audio format selected.")
        return

    progress_label.config(text="Starting extraction...", fg="black")
    progress_bar["value"] = 0
    root.update_idletasks()
    extract_audio_tracks(video_path, audio_format)

root = tk.Tk()
root.title("Audio Track Extractor")

icon_path = os.path.join(os.path.dirname(__file__), "kae_icon.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

app_width = 550
app_height = 350
root.geometry(f"{app_width}x{app_height}")
root.resizable(False, False)
root.overrideredirect(False)

tk.Label(root, text="Select Video File:").pack(pady=5)
video_entry = tk.Entry(root, width=50)
video_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_video).pack(pady=5)

tk.Label(root, text="Select Audio Format:").pack(pady=5)
format_selector = ttk.Combobox(root, values=["mp3", "wav"], state="readonly")
format_selector.set("wav")
format_selector.pack(pady=5)

tk.Label(root, text="Extracted audio will be placed in the same folder as the original video.", fg="gray", wraplength=400).pack(pady=5)

tk.Button(root, text="Extract Audio Tracks", command=start_extraction).pack(pady=10)

progress_label = tk.Label(root, text="Waiting to start extraction...", fg="gray")
progress_label.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=5)

# Footer bar
footer_frame = tk.Frame(root)
footer_frame.pack(side="bottom", pady=5)
footer_label1 = tk.Label(footer_frame, text="Developed by ", fg="black")
footer_label1.pack(side="left")
footer_link1 = tk.Label(footer_frame, text="@kaduwaengertner", fg="blue", cursor="hand2")
footer_link1.pack(side="left")
footer_link1.bind("<Button-1>", lambda e: os.system("start https://twitter.com/kaduwaengertner"))
footer_label2 = tk.Label(footer_frame, text=" - ", fg="black")
footer_label2.pack(side="left")
footer_link2 = tk.Label(footer_frame, text="Join Discord server for support and suggestions", fg="blue", cursor="hand2")
footer_link2.pack(side="left")
footer_link2.bind("<Button-1>", lambda e: os.system("start https://discord.gg/s7bMQA9ZtS"))

root.mainloop()