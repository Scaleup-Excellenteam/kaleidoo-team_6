import speech_recognition as sr
import logging
import os

def transcribe_audio_file(audio_file_path, dest_folder):
    """
    Transcribe audio from a file using Google's Web Speech API and save the result to a file.

    Params:
    audio_file_path (str): The path to the audio file (WAV format).
    dest_folder (str): The path to the destination folder where the transcription will be saved.

    Returns:
    None: The result is saved to a text file in the destination folder.
    """
    # Initialize logging
    logging.basicConfig(filename='transcription_log.txt',
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize recognizer
    recognizer = sr.Recognizer()
    language = 'en-US'  # Default to English

    # Extract the audio filename (without extension)
    audio_filename = os.path.splitext(os.path.basename(audio_file_path))[0]
    # Define the path for the output text file
    output_file_path = os.path.join(dest_folder, f"{audio_filename}_fixed.txt")

    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language=language)
            result = f"{text}"
    except sr.UnknownValueError:
        result = "Google Web Speech API could not understand the audio from file"
    except sr.RequestError as e:
        result = f"Could not request results from Google Web Speech API for file; {e}"

    # Save the result to the text file
    with open(output_file_path, 'w') as f:
        f.write(result)

    # Log the result
    logging.info(f"Transcription saved to {output_file_path}")


