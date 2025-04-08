import os
import subprocess

def compress_audio(input_file, output_file):
    """
    Convert any audio file to mono MP3, compressed to 10MB or less.

    The function:
    - Accepts any audio file format supported by ffmpeg.
    - Converts audio to mono.
    - Calculates maximum bitrate based on input duration to target ≤10MB output.
    - Caps bitrate to a minimum of 32 kbps to avoid unusable quality.
    - Saves output as MP3 format.

    Args:
    input_file (str): Path to the input audio file.
    output_file (str): Path to save the compressed MP3 file.
    """
    # Check if the input file exists
    if not os.path.exists(input_file):
        print("Input file not found.")
        return

    # Get duration of input file in seconds using ffprobe
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', input_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        duration = float(result.stdout.strip())
    except Exception as e:
        print("Failed to get audio duration:", e)
        return

    # Calculate target bitrate in kbps
    target_size_bits = 10 * 8 * 1024 * 1024  # 10MB in bits
    bitrate_kbps = int(target_size_bits / duration / 1000)

    # Enforce minimum bitrate of 32 kbps
    min_bitrate = 32
    if bitrate_kbps < min_bitrate:
        print(f"Warning: audio too long to fit 10MB at reasonable quality. Using minimum bitrate {min_bitrate} kbps.")
        bitrate_kbps = min_bitrate
    else:
        print(f"Calculated bitrate: {bitrate_kbps} kbps")

    # Compress audio using ffmpeg: mono, mp3 codec, target bitrate
    try:
        subprocess.run([
            'ffmpeg', '-i', input_file,
            '-ac', '1',
            '-codec:a', 'libmp3lame',
            '-b:a', f'{bitrate_kbps}k',
            output_file
        ], check=True)
        print("Compression successful!")
    except subprocess.CalledProcessError as e:
        print("Compression failed:", e)

# Example usage:
input_file = r"input_file"  # Replace with the path to your input audio file
output_file = r"ouput_file.mp3"  # Replace with the desired path for the compressed audio file

compress_audio(input_file, output_file)
