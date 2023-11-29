import whisper
import os
import torch

# Check if CUDA (GPU support) is available and set the device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Load the Whisper model
model = whisper.load_model("large-v2")

# Specify the root directory where your audio files are located
root_directory = './audio'

# Walk through all subdirectories in the root directory
for subdir, dirs, files in os.walk(root_directory):
    for filename in files:
        # Check if the file is an MP3 file
        if filename.endswith('.mp3'):
            
                print(f"Transcribing {filename}...")
                input_filename = os.path.join(subdir, filename)
                
                # Transcribe the audio file
                result = model.transcribe(input_filename, language="English")

                # Extract the base name without the extension
                base_name = os.path.splitext(filename)[0]

                # Define the output file name in the same subdirectory
                output_filename = os.path.join(subdir, f"{base_name}.txt")

                # Write the transcription to the text file
                with open(output_filename, 'w') as file:
                    file.write(result["text"])
                
                print(f"Transcription saved to {output_filename}")
            except Exception as e:
                print(f"An error occurred while processing {filename}: {e}")
