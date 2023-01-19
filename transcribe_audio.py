from pydub import AudioSegment
import speech_recognition as sr
import time
import os

def transcribe_audio(audio_file, output_dir, output_file):
    try:
        sound = AudioSegment.from_file(audio_file)
        sound = sound.set_frame_rate(16000)
        sound = sound.set_sample_width(2)
        sound = sound.set_channels(1)
        sound.export("temp.wav", format="wav")
        audio_file = "temp.wav"
        duration = sound.duration_seconds
        chunk_duration = 30  # duration of each chunk in sec
        chunks = int(duration / chunk_duration)  # number of chunks
        recognizer = sr.Recognizer()
        text = ""  # variable to store the final text
        for i in range(chunks):
            start = i * chunk_duration * 1000
            end = (i + 1) * chunk_duration * 1000
            chunk = sound[start:end]
            audio = sr.AudioData(chunk.raw_data, chunk.frame_rate, chunk.sample_width)
            while True:
                try:
                    text += recognizer.recognize_google(audio, language='ar-EG')
                    break
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    if 'timed out' in str(e):
                        print("Request timed out, retrying...")
                        time.sleep(5)
                    else:
                        print("Could not request results from Google Speech Recognition service; {0}".format(e))
                        time.sleep(5)
        with open(f"{output_dir}/{output_file}.txt", "w") as f:
            f.write(text)
        os.remove("temp.wav")
        return text
    except Exception as e:
        return "Error; {0}".format(e)
