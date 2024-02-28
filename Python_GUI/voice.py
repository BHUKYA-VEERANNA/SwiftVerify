import os
import speech_recognition as sr

def capture_voice(username):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Please say your name, {username}:")
        audio = recognizer.listen(source)
        
    try:
        voice_data = recognizer.recognize_google(audio)
        return voice_data
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return None

def save_voice(username, voice_data):
    directory = "voices"
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, f"{username}.wav")
    with open(filename, "wb") as f:
        f.write(voice_data)
    print(f"Voice sample saved for {username}.")

def authenticate_user(username):
    recognizer = sr.Recognizer()
    with sr.AudioFile(f"voices/{username}.wav") as source:
        audio_data = recognizer.record(source)
    
    try:
        voice_data = recognizer.recognize_google(audio_data)
        if voice_data.lower() == username.lower():
            print("Authentication successful!")
            return True
        else:
            print("Authentication failed. Voice doesn't match.")
            return False
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand the audio.")
        return False

if __name__ == "__main__":
    username = input("Enter your username: ")
    voice_data = capture_voice(username)
    if voice_data:
        save_voice(username, voice_data)
        print("Please repeat your name for verification.")
        if authenticate_user(username):
            print("Access granted.")
        else:
            print("Access denied.")
    else:
        print("Voice capture failed. Please try again.")
