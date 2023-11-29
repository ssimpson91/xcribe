import os
import textwrap
import spacy

# Load the English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

def format_text_as_book(transcript):
    # Parse the text with SpaCy
    doc = nlp(transcript)

    # Group sentences into paragraphs
    paragraphs = []
    paragraph = ""
    for sent in doc.sents:
        paragraph += sent.text + " "
        if len(paragraph.split()) > 200:  # Assuming roughly 100 words per paragraph
            paragraphs.append(paragraph.strip())
            paragraph = ""
    if paragraph:
        paragraphs.append(paragraph.strip())

    # Format paragraphs with indentation
    formatted_paragraphs = ["\t" + textwrap.fill(p, width=80) for p in paragraphs]
    return "\n\n".join(formatted_paragraphs)

# Process all .txt files in the current directory
for filename in os.listdir():
    if filename.endswith(".txt"):
        with open(filename, 'r') as file:
            text = file.read()

        formatted_text = format_text_as_book(text)

        # Save the formatted text back to the file
        with open(filename, 'w') as file:
            file.write(formatted_text)

        print(f"Formatted {filename}")
