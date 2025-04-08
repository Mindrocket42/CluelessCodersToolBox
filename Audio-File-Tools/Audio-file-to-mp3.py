import os
import subprocess

def convert_audio_to_mp3(input_file, output_file):
    """
    Convert an audio file to MP3 format using ffmpeg.
    
    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the output MP3 file.
    """
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found.")
        return

    try:
        subprocess.run(['ffmpeg', '-y', '-i', input_file, '-acodec', 'libmp3lame', output_file], check=True)
        print(f"Conversion successful! Saved as '{output_file}'")
    except subprocess.CalledProcessError as e:
        print("Conversion failed:", e)

def main():
    input_file = input("Enter the full path to the audio file you want to convert: ").strip()

    if not os.path.isfile(input_file):
        print("The specified input file does not exist.")
        return

    base, _ = os.path.splitext(input_file)
    output_file = base + ".mp3"

    convert_audio_to_mp3(input_file, output_file)

if __name__ == "__main__":
    main()
