import numpy as np
import soundcard as sc
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class AudioStreamer(object):
    def __init__(self, num_of_frames, sample_rate):
        self.__num_of_frames = num_of_frames
        self.__sample_rate = sample_rate
        self.__default_mic = sc.default_microphone()
        self.__frame_buffer = np.zeros(num_of_frames)

    def start(self):
        with self.__default_mic.recorder(samplerate=self.__sample_rate) as mic:
            while True:
                data = mic.record(numframes=self.__num_of_frames)
                data_fft = np.abs(np.fft.fft(data))
                data_acf = np.abs(np.fft.fft(data_fft))
                print(data_fft)


if __name__ == "__main__":
    fs = 8000
    frames = 1024

    test = AudioStreamer(frames, fs)
    test.start()
