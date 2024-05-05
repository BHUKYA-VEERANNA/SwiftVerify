import os
import customtkinter
import subprocess
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkTextbox, CTkProgressBar, set_appearance_mode, set_default_color_theme, CTkFont
from tkinter import filedialog
import sounddevice as sd
import soundfile as sf
from datetime import datetime
from scipy.spatial.distance import pdist
from pyannote.audio import Inference
from pyannote.audio import Model

# Load the model
try:
    model = Model.from_pretrained("pyannote/embedding", use_auth_token="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")
    vec = Inference(model, window='whole')
except Exception as e:
    print("Error loading the model:", e)

# Create database
dataset = {"1": "elon musk", "2": "veeranna"}

def select():
    try:
        global test, distance, name
        distance = 0.7
        name = "unknown"
        textbox.delete(0.0, 'end')
        textbox1.delete(0.0, 'end')
        label3.configure(text="0%")
        progressbar.set(0)
        app.filename = filedialog.askopenfilename(initialdir="C:/Users/bveer/OneDrive/Desktop/Major Project/Code/PyQt/Audios",
                                                  title="Select a file", filetypes=(("mp3 files", "*.mp3"), ("wav files", "*.wav"), ("AAC File", "*.aac")))
        textbox.insert(0.0, app.filename)
        test = vec(app.filename)
    except Exception as e:
        print("Error:", e)
        textbox.insert(0.0, "Please select an audio file")

def record_voice():
    try:
        global test, distance, name
        distance = 0.7
        name = "unknown"
        textbox.delete(0.0, 'end')
        textbox1.delete(0.0, 'end')
        label3.configure(text="0%")
        progressbar.set(0)
        
        # Record voice
        fs = 44100  # Sample rate
        seconds = 5  # Duration of recording
        
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording is finished
        
        # Specify full path to the recorded_audios folder
        recorded_audios_path = "C:/Users/bveer/OneDrive/Desktop/Major Project/Code/PyQt/recorded_audios"
        
        # Create recorded_audios folder if it doesn't exist
        if not os.path.exists(recorded_audios_path):
            os.makedirs(recorded_audios_path)
        
        # Save recorded voice to file
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        voice_file = f"{recorded_audios_path}/{dt_string}.wav"
        sf.write(voice_file, recording, fs)

        # Process recorded voice
        test = vec(voice_file)

        # Search for speaker
        search()

    except Exception as e:
        print("Error:", e)
        textbox.insert(0.0, "Error recording voice")

def search():
    global distance, name
    num = len(dataset)
    for i in range(num):
        percent = (i+1) / num
        audio_file_path = os.path.join("C:/Users/bveer/OneDrive/Desktop/Major Project/Code/PyQt/Audios/", f"{i+1}.mp3")
        a = vec(audio_file_path)
        x = [test, a]
        y = pdist(x, metric='cosine')
        if round(y[0], 4) <= distance:
            distance = round(y[0], 4)
            name = dataset[f"{i+1}"]
        progressbar.set(percent)
        label3.configure(text=f"{int(percent*100)}%")
        label3.update()

    textbox1.insert('end', "\n The speaker is : " + name)

set_appearance_mode("dark")
set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("780x580")
app.title('Voice Verification')

frame = customtkinter.CTkFrame(app, width=760, height=100, corner_radius=15)
frame.place(x=10, y=20)

label = customtkinter.CTkLabel(
    frame, text="File Name :", font=customtkinter.CTkFont(family='calibre', size=15, weight="bold"))
label.place(x=30, y=5)

textbox = customtkinter.CTkTextbox(
    frame, width=630, height=40, font=customtkinter.CTkFont(family='calibre', size=17))
textbox.place(x=15, y=40)

record_button = customtkinter.CTkButton(frame, corner_radius=5, width=150, height=40, command=record_voice, text="Record Voice",
                                        font=customtkinter.CTkFont(size=15, weight="bold"))
record_button.place(x=320, y=70)  # Adjusted position

button = customtkinter.CTkButton(frame, corner_radius=5, width=60, height=40, command=select, text="Select File",
                                 font=customtkinter.CTkFont(size=15, weight="bold"))
button.place(x=655, y=40)

frame1 = customtkinter.CTkFrame(app, width=760, height=200, corner_radius=15)
frame1.place(x=10, y=140)

label1 = customtkinter.CTkLabel(
    frame1, text="Progress Bar :", font=customtkinter.CTkFont(family='calibre', size=15, weight="bold"))
label1.place(x=30, y=5)

label3 = customtkinter.CTkLabel(
    frame1, text="0%", width=40, font=customtkinter.CTkFont(family='arial', size=20))
label3.place(x=690, y=5)

progressbar = customtkinter.CTkProgressBar(
    frame1, width=740, height=10, corner_radius=15)
progressbar.set(0)
progressbar.place(x=10, y=40)

label2 = customtkinter.CTkLabel(
    frame1, text="The Speaker :", font=customtkinter.CTkFont(family='calibre', size=15, weight="bold"))
label2.place(x=30, y=70)

textbox1 = customtkinter.CTkTextbox(
    frame1, width=530, height=90, font=customtkinter.CTkFont(size=20, weight="bold"))
textbox1.place(x=10, y=100)

button1 = customtkinter.CTkButton(frame1, corner_radius=5, width=200, height=90, command=search,
                                  text="Search For The Speaker", font=customtkinter.CTkFont(size=15, weight="bold"))
button1.place(x=550, y=100)

def go_to_home():
    app.destroy()  # Close the current window
    # Get the directory of the current script
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Construct the path to mark_attendance.py
    mark_attendance_path = os.path.join(current_directory, 'app.py')

    # Check if mark_attendance.py exists
    if os.path.exists(mark_attendance_path):
        # Execute mark_attendance.py using subprocess
        subprocess.Popen(['python', mark_attendance_path])
    else:
        print("Error: mark_attendance.py file not found at:", mark_attendance_path)

go_to_home_button = customtkinter.CTkButton(app, corner_radius=5, width=100, height=40, command=go_to_home, text="Go to home", # type: ignore
                                             font=customtkinter.CTkFont(size=15, weight="bold"))
go_to_home_button.place(x=150, y=400)

app.mainloop()
