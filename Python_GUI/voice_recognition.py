import wave
import os
import speech_recognition as sr
import librosa
import numpy as np
import soundfile as sf
from sklearn.metrics.pairwise import cosine_similarity

# Record voice input
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)
    return audio

# Convert speech to text
def speech_to_text(audio):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    

# Save voice sample to database
def save_voice_sample(audio, filename):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(audio.channel_count)
        wf.setsampwidth(audio.sample_width)
        wf.setframerate(audio.sample_rate)
        wf.writeframes(audio.get_wav_data())


# Train voice model
def train_voice_model(name):
    print("Please speak the following sentence for voice enrollment:")
    enrollment_audio = record_audio()
    sr = 16000  # Sample rate, you can adjust this value as needed
    
    # Convert audio data to NumPy array
    enrollment_audio_np = np.frombuffer(enrollment_audio.frame_data, dtype=np.int16)
    
    save_voice_sample(enrollment_audio_np, f"{name}_voice.wav", sr)


# Load voice model from database
def load_voice_model(name):
    filename = f"{name}_voice.wav"
    if os.path.exists(filename):
        voice, sr = librosa.load(filename)
        return voice, sr
    else:
        return None, None

# Compare recorded voice with reference voice
def compare_voices(recorded_voice, reference_voice):
    similarity = cosine_similarity([recorded_voice], [reference_voice])
    return similarity[0][0]

# Main function
def main():
    name = input("Enter your name or ID: ")
    filename = f"{name}_voice.wav"

    # Load reference voice sample from the database
    reference_voice, sr = load_voice_model(name)

    if reference_voice is None:
        print("No voice model found. Creating a new one...")
        train_voice_model(name)
        reference_voice, sr = load_voice_model(name)

    # Display sentence
    print("Please read the following sentence: Hello, how are you today?")

    # Record voice input
    recorded_audio = record_audio()
    save_voice_sample(recorded_audio.get_raw_data(), "recorded_audio.wav", recorded_audio.sample_rate)

    # Load recorded audio for feature extraction
    recorded_voice, sr_recorded = librosa.load("recorded_audio.wav", sr=None)

    # Convert speech to text
    text = speech_to_text(recorded_audio)

    if text is not None:
        # Compute MFCC features for recorded and reference voices
        recorded_mfcc = librosa.feature.mfcc(y=recorded_voice, sr=sr_recorded)
        reference_mfcc = librosa.feature.mfcc(y=reference_voice, sr=sr)

        # Compare recorded voice with reference voice
        similarity = cosine_similarity(np.transpose(recorded_mfcc), np.transpose(reference_mfcc))

        if np.max(similarity) > 0.5:  # Adjust threshold as needed
            print("Congratulations! Welcome back.")
        else:
            print("Voice did not match.")
    else:
        print("Failed to convert speech to text.")

    # Remove temporary recorded audio file
    os.remove("recorded_audio.wav")

if __name__ == "__main__":
    main()