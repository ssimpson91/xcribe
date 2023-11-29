import os
import re

def natural_sort_key(s):
    """
    Sort strings containing numbers in a way that humans expect.
    """
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

def merge_text_files(directory, output_filename="merged.txt"):
    # Create or overwrite the output file
    with open(output_filename, 'w') as outfile:
        # Iterate over all files in the directory, sorted in natural order
        for filename in sorted(os.listdir(directory), key=natural_sort_key):
            # Process only .txt files (excluding the output file itself)
            if filename.endswith(".txt") and filename != output_filename:
                with open(filename, 'r') as infile:
                    # Write the content of the current file to the output file
                    outfile.write(infile.read())
                    # Add a newline for separation between files
                    outfile.write("\n\n")

    print(f"All .txt files in {directory} have been merged into {output_filename}.")

# Call the function to merge files in the current directory
merge_text_files(os.getcwd())
