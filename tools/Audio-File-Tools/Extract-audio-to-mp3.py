import os
import subprocess

def convert_to_mp3(input_file, output_file):
    """
    Convert an audio or video file to MP3 format.
    
    Args:
    input_file (str): Path to the input audio or video file.
    output_file (str): Path to save the output MP3 audio file.
    """
    # Check if the input file exists
    if not os.path.exists(input_file):
        print("Input file not found.")
        return
    
    # Extract audio from video files
    if input_file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.flv')):
        try:
            subprocess.run(['ffmpeg', '-i', input_file, '-vn', '-acodec', 'copy', 'temp_audio.aac'], check=True)
            input_file = 'temp_audio.aac'
        except subprocess.CalledProcessError as e:
            print("Audio extraction failed:", e)
            return
    
    # Convert audio to MP3
    try:
        subprocess.run(['ffmpeg', '-i', input_file, '-acodec', 'libmp3lame', output_file], check=True)
        print("Conversion successful!")
    except subprocess.CalledProcessError as e:
        print("Conversion failed:", e)
    finally:
        # Clean up temporary audio file
        if input_file == 'temp_audio.aac':
            os.remove('temp_audio.aac')
        

# Example usage:
input_file = "input_file.ext"  # Replace with the path to your input audio or video file
output_file = "output_audio.mp3"  # Replace with the desired path for the converted MP3 file

convert_to_mp3(input_file, output_file)
