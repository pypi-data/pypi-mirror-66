import os
import pyttsx3
import random

from pydub import AudioSegment


class TTSDG:

    def __init__(self, verbose=False):
        self.engine = pyttsx3.init()
        self.volume_range = [0.0, 1.0]
        self.wpm_range = [100, 300]
        self.voices = self.engine.getProperty("voices")
        self.verbose = verbose

    def set_volume_range(self, low: float = None, high: float = None, one: float = None):
        """
        :param low: Lowest volume value
        :param high: Highest volume value
        :param one: If only one value desired, set this value hree
        """
        if one is not None:
            assert 0.0 < one < 1.0, "Value must be between 0.0 and 1.0"
            self.volume_range = [one]
            return
        assert low > 0.0, "Low must be greater than 0.0"
        assert high < 1.0, "High must be less than 1.0"
        self.volume_range = [low, high]

    def set_wpm_range(self, low: int = None, high: int = None, one: int = None):
        """
        :param low: Lowest WPM value
        :param high: Highest WPM value
        :param one: If only one value desired, set this value hree
        """
        if one is not None:
            assert 0 < one < 1, "Value must be between 0 and 1"
            self.wpm_range = [one]
            return
        assert low > 0, "Low must be greater than 0"
        self.wpm_range = [low, high]

    def set_voices(self, voices: list):
        """
        :param voices: List of system voices to be generated from
        """
        self.voices = voices

    def set_engine(self, engine: pyttsx3.Engine):
        """
        :param engine: pyttsx3 engine object to generate from
        """
        self.engine = engine

    def get_engine(self):
        """
        :return: pyttsx3 engine currently being used
        """
        return self.engine

    def generate(self, text, n, out_format="wav"):
        files = []
        if not os.path.isdir(text.replace(" ", "_")):
            os.mkdir(text.replace(" ", "_"))
        for i in range(n):
            if self.verbose:
                print(i + 1)
            voice = random.choice(self.voices)

            if len(self.volume_range) == 1:
                volume = self.volume_range[0]
            else:
                volume = random.uniform(self.volume_range[0], self.volume_range[1])

            if len(self.wpm_range) == 1:
                wpm = self.wpm_range[0]
            else:
                wpm = random.randint(self.wpm_range[0], self.wpm_range[1])

            self.engine.setProperty('volume', volume)
            self.engine.setProperty('rate', wpm)
            self.engine.setProperty('voice', voice.id)

            self.engine.save_to_file(text, "./" + text.replace(" ", "_") + "/" + text + "_" + str(i) + ".mp3")
            files.append("./" + text.replace(" ", "_") + "/" + text + "_" + str(i) + ".mp3")

        self.engine.runAndWait()

        for file in files:
            if out_format is not "mp3":
                AudioSegment.from_file(file).export(file[:-4] + ".wav", format=out_format)
                os.remove(file)
