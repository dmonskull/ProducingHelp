import os
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from pydub import AudioSegment

def get_audio_length(file_path):
    audio = None
    try:
        if file_path.endswith('.mp3'):
            audio = MP3(file_path)
        elif file_path.endswith('.m4a') or file_path.endswith('.mp4'):
            audio = MP4(file_path)
        elif file_path.endswith('.flac'):
            audio = FLAC(file_path)
        elif file_path.endswith('.ogg'):
            audio = OggVorbis(file_path)
        elif file_path.endswith('.wav'):
            audio = AudioSegment.from_wav(file_path)
        
        if audio:
            if hasattr(audio, 'info'):
                return int(audio.info.length)
            else:
                return int(len(audio) / 1000)  # pydub returns length in milliseconds
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

def format_length(length_in_seconds):
    minutes = length_in_seconds // 60
    seconds = length_in_seconds % 60
    return f"{minutes}:{seconds:02}"

def generate_tracklist(tracklist_title, folder_path, tracks):
    tracklist = f"{tracklist_title}\n\n"
    
    total_length = 0
    for track in tracks:
        file_path = os.path.join(folder_path, track)
        length_in_seconds = get_audio_length(file_path)
        if length_in_seconds is not None:
            start_time = format_length(total_length)
            end_time = format_length(total_length + length_in_seconds)
            tracklist += f"{track} : {start_time} - {end_time}\n"
            total_length += length_in_seconds
        else:
            print(f"Skipping file {track} as its length could not be determined.")
    return tracklist

def main():
    # Ask for the folder containing the tracklist
    folder_path = input("Enter the path of the folder containing the tracklist: ").strip().strip('"')
    
    # Validate the folder path
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please try again.")
        return
    
    # Ask if the user wants to use the folder name as the tracklist name
    use_folder_name = input("Do you want to use the folder name as the tracklist name? (1 for yes, 2 for no): ").strip()
    if use_folder_name == '1':
        tracklist_title = os.path.basename(folder_path)
    elif use_folder_name == '2':
        tracklist_title = input("Enter the name of the tracklist: ").strip()
    else:
        print("Invalid choice. Please try again.")
        return
    
    # Find all audio tracks in the folder
    audio_extensions = ('.mp3', '.m4a', '.mp4', '.flac', '.ogg', '.wav')
    tracks = [f for f in os.listdir(folder_path) if f.lower().endswith(audio_extensions)]
    
    # List tracks with numbers
    print("Found the following tracks:")
    for i, track in enumerate(tracks):
        print(f"{i + 1}. {track}")
    
    # Get the order from the user
    order = input("Enter the order of the tracks by typing the numbers separated by commas: ")
    order = [int(x.strip()) - 1 for x in order.split(',')]
    
    # Reorder tracks according to user input
    ordered_tracks = [tracks[i] for i in order]
    
    # Generate tracklist
    tracklist = generate_tracklist(tracklist_title, folder_path, ordered_tracks)
    
    output_file = os.path.join(folder_path, "tracklist.txt")
    with open(output_file, "w") as f:
        f.write(tracklist)
    
    print(f"Tracklist file created: {output_file}")

if __name__ == "__main__":
    main()
