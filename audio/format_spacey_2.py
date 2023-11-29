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
        if should_start_new_paragraph(paragraph, sent):
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

def should_start_new_paragraph(current_paragraph, sentence):
    # Start a new paragraph if the current one is sufficiently long
    if len(current_paragraph.split()) > 30:
        return True

    # Check if the sentence has words
    sentence_words = sentence.text.split()
    if not sentence_words:  # Skip empty or non-alphanumeric sentences
        return False

    # Avoid starting new paragraphs with certain conjunctions or transitions
    transitional_words = ['so', 'and', 'but', 'or', 'because', 'however', 'therefore']
    first_word = sentence_words[0].lower()
    if first_word in transitional_words:
        return False

    # Start a new paragraph if the sentence starts with a capital letter and the current paragraph is not too short
    return sentence.text[0].isupper() and len(current_paragraph.split()) > 20

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
