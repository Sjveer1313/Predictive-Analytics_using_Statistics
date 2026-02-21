import sys
import os
import yt_dlp
from pydub import AudioSegment

def download_videos(singer, count):
    print(f"\nDownloading {count} videos of {singer}...\n")

    search_query = f"ytsearch{count}:{singer}"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])

def convert_and_trim(duration):
    final_audio = AudioSegment.empty()

    print("\nProcessing audio files...\n")

    for file in os.listdir("downloads"):
        path = os.path.join("downloads", file)

        try:
            audio = AudioSegment.from_file(path)
            clip = audio[:duration * 1000]
            final_audio += clip
        except Exception as e:
            print(f"Error processing {file}: {e}")

    return final_audio

def main():

    if len(sys.argv) != 5:
        print("Usage: python <file.py> <SingerName> <NumberOfVideos> <Duration> <OutputFile>")
        sys.exit()

    singer = sys.argv[1]

    try:
        num_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
    except ValueError:
        print("Number of videos and duration must be integers.")
        sys.exit()

    output = sys.argv[4]

    if num_videos <= 10:
        print("Number of videos must be greater than 10.")
        sys.exit()

    if duration <= 20:
        print("Duration must be greater than 20 seconds.")
        sys.exit()

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    try:
        download_videos(singer, num_videos)
        merged_audio = convert_and_trim(duration)
        merged_audio.export(output, format="mp3")
        print(f"\nMashup created successfully → {output}\n")
    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    main()
