import yt_dlp
import os

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').strip()
        speed = d.get('_speed_str', '0 B/s')
        eta = d.get('_eta_str', '?')
        print(f"\rDownloading: {percent} yay at {speed} (ETA: {eta})", end='', flush=True)
    elif d['status'] == 'finished':
        print('\nDownload finished! Converting...')


def download_audio_as_wav(url):
    # Absolute path to ffmpeg.exe
    ffmpeg_path = os.path.abspath("ffmpeg/ffmpeg.exe")
    print(f"Using ffmpeg at: {ffmpeg_path}")

    # Ensure download directory exists
    output_dir = os.path.join(os.getcwd(), 'download')
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',  # Only audio
        'ffmpeg_location': ffmpeg_path,
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',  # Convert audio to wav
            'preferredquality': '192',  # Bitrate (optional)
        }],
        'progress_hooks': [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example usage
download_audio_as_wav('https://youtu.be/SwUpMhp-DEc?si=6JGMeIXFGRHYpKzi')
