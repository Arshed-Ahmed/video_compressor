import os
import subprocess

def compress_video(input_file, output_file, compress_percent):
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return

    # Calculate target bitrate
    probe_cmd = f"ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 {input_file}"
    result = subprocess.run(probe_cmd, capture_output=True, text=True, shell=True)
    
    if result.returncode != 0:
        print("Error running ffprobe command.")
        print(result.stderr)
        return

    try:
        original_bitrate = int(result.stdout.strip())
    except ValueError:
        print("Error: Could not retrieve the original bitrate. Please check the input file.")
        return
    
    target_bitrate = int(original_bitrate * (1 - compress_percent / 100))

    # Compress video
    compress_cmd = f"ffmpeg -i {input_file} -b:v {target_bitrate} -maxrate {target_bitrate} -bufsize {target_bitrate*2} {output_file}"
    
    try:
        process = subprocess.Popen(compress_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        
        for line in process.stdout:
            if "frame=" in line:
                progress = line.strip()
                print(f"\r{progress}", end="")
        
        process.wait()
        print("\nCompression completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during compression: {e}")
        
def main():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define input and output folders
    input_folder = os.path.join(script_dir, 'input')
    output_folder = os.path.join(script_dir, 'output')
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # List all files in the input folder
    input_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    
    if not input_files:
        print("No files found in the input folder.")
        return
    
    print("Files in the input folder:")
    for i, file in enumerate(input_files):
        print(f"{i+1}. {file}")
    
    file_index = int(input("Enter the number of the file you want to compress: ")) - 1
    if file_index < 0 or file_index >= len(input_files):
        print("Invalid file number.")
        return
    
    input_file = os.path.join(input_folder, input_files[file_index])
    output_file = os.path.join(output_folder, f"compressed_{input_files[file_index]}")
    
    compression_percent = float(input("Enter the compression percentage (0-100): "))
    
    if compression_percent < 0 or compression_percent > 100:
        print("Compression percentage must be between 0 and 100.")
        return
    
    compress_video(input_file, output_file, compression_percent)
    
    print(f"Video compressed successfully. Output saved to {output_file}")

if __name__ == "__main__":
    main()
    
stop = 0