import os
import textwrap
import spacy

# Load the English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

def format_text_as_book(transcript, title, playlist):
    # Parse the text with SpaCy
    doc = nlp(transcript)

    # Group sentences into paragraphs
    paragraphs = []
    paragraph = ""
    for sent in doc.sents:
        # Check if the sentence is a potential paragraph starter
        if len(sent.text.split()) > 20 or sent.text[0].isupper() or not paragraph:
            if paragraph:  # Add the previous paragraph to the list
                paragraphs.append(paragraph.strip())
                paragraph = ""
            paragraph += sent.text + " "
        else:
            paragraph += sent.text + " "

    if paragraph:
        paragraphs.append(paragraph.strip())

    # Format paragraphs with indentation
    formatted_paragraphs = ["\t" + textwrap.fill(p, width=70) for p in paragraphs]

    # Add header with title and playlist
    header = f"Title: {title}\nPlaylist: {playlist}\n\n"
    return header + "\n\n".join(formatted_paragraphs)

# Specify the root directory where your audio files are located
root_directory = '/media/omega_c/X/whisper/audio/'

# Walk through all subdirectories in the root directory
for subdir, dirs, files in os.walk(root_directory):
    print(f"Entering directory: {subdir}")
    for filename in files:
        if filename.endswith(".txt"):
            print(f"Found file: {filename}")
            # Extract title from filename
            title = filename.rsplit('.', 1)[0]

            # Extract playlist name from the subdirectory name
            playlist = os.path.basename(subdir)

            with open(os.path.join(subdir, filename), 'r') as file:
                text = file.read()

            formatted_text = format_text_as_book(text, title, playlist)

            # Save the formatted text back to the file
            with open(os.path.join(subdir, filename), 'w') as file:
                file.write(formatted_text)

            print(f"Formatted {filename} in {playlist}")

print("Formatting complete.")
