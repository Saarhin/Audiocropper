import pyaudio
import wave
import keyboard
import time
from pydub import AudioSegment

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "test.wav"

# p = pyaudio.PyAudio()

# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     print(f"{i}: {info['name']} - Inputs: {info['maxInputChannels']}")

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT,input_device_index=0, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)


frames = []
print("Press SPACE to start recording.")
keyboard.wait('space')
print("Recording... Press SPACE to stop.")
time.sleep(0.2)

while True:
    try:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    except KeyboardInterrupt:
        break

    if keyboard.is_pressed('space'):
        print("Stopping recording after a brief delay...")
        time.sleep(0.2)
        break

stream.start_stream()
stream.close()
audio.terminate()

wf = wave.open(OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Convert from WAV to MP3
sound = AudioSegment.from_wav("test.wav")
sound.export("output.mp3", format="mp3")
