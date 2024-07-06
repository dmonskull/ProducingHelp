from pytube import YouTube
from pydub import AudioSegment
import os

def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).rstrip()

def convert_to_wav(file_path, output_path, title):
    try:
        audio = AudioSegment.from_file(file_path)
        output_file = os.path.join(output_path, f"{title}.wav")
        audio.export(output_file, format="wav")
        os.remove(file_path)
        print(f"Audio converted successfully to {output_file}")
    except Exception as e:
        print(f"Error converting audio to WAV: {e}")

def download_audio(url):
    try:
        yt = YouTube(url)
        audio_title = sanitize_filename(yt.title)
        base_path = os.getcwd()
        output_path = os.path.join(base_path, "downloaded songs")

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()

        if not audio_streams:
            print("No available audio streams.")
            return

        print("Available audio streams (sorted by quality):")
        for i, stream in enumerate(audio_streams):
            stream_info = f"{i}: {stream.abr} - {stream.mime_type.split('/')[-1].upper()}"
            print(stream_info)

        choice = int(input("Enter the number of the stream you want to download: "))
        if choice < 0 or choice >= len(audio_streams):
            print("Invalid stream choice.")
            return

        selected_stream = audio_streams[choice]
        file_path = selected_stream.download(output_path=output_path)
        convert_to_wav(file_path, output_path, audio_title)
    except Exception as e:
        print(f"Error downloading audio: {e}")

if __name__ == "__main__":
    try:
        url = input("Enter the URL of the YouTube video: ").strip()
        if not url:
            print("URL cannot be empty.")
            exit()

        download_audio(url)
    except Exception as e:
        print(f"An error occurred: {e}")
