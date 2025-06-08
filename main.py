import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import yt_dlp
import re
import time

# --- Helper functions ---
def remove_ansi_escape_codes(s):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', s).strip()

# --- Download functions from main.py ---
def progress_hook_tk(d, label, progress_bar):
    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0%').strip().replace('%', '')
        title = d.get('info_dict', {}).get('title', 'Downloading...')
        label.config(text=title)
        try:
            percent_float = float(percent_str)
            progress_bar['value'] = percent_float
        except:
            progress_bar['value'] = 0
    elif d['status'] == 'finished':
        label.config(text="Download Finished! Converting...")

def download_audio(url, format_choice, label, progress_bar):
    ffmpeg_path = os.path.abspath(os.path.join("ytdldata", "ffmpeg", "ffmpeg.exe"))
    output_dir = os.path.join(os.getcwd(), 'download')
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': ffmpeg_path,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format_choice.lower(),
            'preferredquality': '192',
        }],
        'progress_hooks': [lambda d: progress_hook_tk(d, label, progress_bar)],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# --- Function to check if URL is valid ---
def is_supported(url: str) -> bool:
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'ignoreerrors': True,
        'nocheckcertificate': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)
            return bool(info_dict)
        except Exception as e:
            print(f"Error: {e}")
            return False

# --- GUI setup ---
window = tk.Tk()
link_input1 = tk.StringVar()
format_choice = ['MP3', 'WAV', 'MP3']
sound_format = tk.StringVar(value="MP3")

def start_download_thread():
    url = link_input1.get()
    if not is_supported(url):
        messagebox.showerror(title='YouTube DL', message='Invalid URL!!')
        return

    # Create progress window
    progress_win = tk.Toplevel(window)
    progress_win.title("Downloading")
    progress_win.geometry("500x100")
    progress_win.resizable(False, False)
    tk.Label(progress_win, text="Downloading...", font=("Helvetica", 12)).pack(pady=5)
    title_label = tk.Label(progress_win, text="", font=("Helvetica", 10))
    title_label.pack()
    progress_bar = ttk.Progressbar(progress_win, orient='horizontal', length=250, mode='determinate', maximum=100)
    progress_bar.pack(pady=10)

    # Start download in a new thread
    def download_task():
        download_audio(url, sound_format.get(), title_label, progress_bar)
        title_label.config(text="Done!")
        progress_bar['value'] = 100

    threading.Thread(target=download_task, daemon=True).start()

# --- GUI Elements ---
tk.Label(window, text='Enter URL from YouTube', fg='white', bg="#2D2D2D", font=('Arial', 10)).grid(row=0, column=0, sticky='SW', pady=2)
tk.Entry(window, textvariable=link_input1, font=('calibre',10,'normal'), width=35).grid(row=1, column=0, padx=5)
tk.Button(window, text='Download', relief='solid', bg='white', height=1, font=('calibre',9,'normal'), command=start_download_thread).grid(row=1, column=1)
ttk.OptionMenu(window, sound_format, *format_choice).grid(row=1, column=2, padx=5)

# --- Window styling ---
icon_path = os.path.join(os.getcwd(), "ytdldata", "youtube_icon.ico")
window.geometry("400x65")
window.title('YouTube WAV/MP3')
window.config(bg='#2D2D2D')
window.iconbitmap(icon_path)
window.resizable(False, False)

window.mainloop()
