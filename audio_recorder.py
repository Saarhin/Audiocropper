import pyaudio
import wave
import time
from pydub import AudioSegment
import threading
import os

AUDIO_FOLDER = "recordings"
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
INPUT_DEVICE_INDEX = 0

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.is_recording = False

    def start_recording(self):
        self.frames = []
        self.stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      input_device_index=INPUT_DEVICE_INDEX,
                                      frames_per_buffer=CHUNK)
        self.is_recording = True
        threading.Thread(target=self._record).start()

    def _record(self):
        while self.is_recording:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False
        time.sleep(0.1)
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def save(self, filename):
        os.makedirs(AUDIO_FOLDER, exist_ok=True)
        wav_path = os.path.join(AUDIO_FOLDER, f"{filename}.wav")
        mp3_path = os.path.join(AUDIO_FOLDER, f"{filename}.mp3")

        wf = wave.open(wav_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        sound = AudioSegment.from_wav(wav_path)
        sound.export(mp3_path, format="mp3")




# p = pyaudio.PyAudio()
# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     print(f"{i}: {info['name']} - Inputs: {info['maxInputChannels']}")
