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
        self.custom_settings = False

    def set_volume_range(self, low: float = None, high: float = None, one: float = None):
        """
        :param low: Lowest volume value
        :param high: Highest volume value
        :param one: If only one value desired, set this value hree
        """
        if one is not None:
            assert 0.0 < one < 1.0, "Value must be between 0.0 and 1.0"
            self.volume_range = [one]
            self.custom_settings = True
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
            self.custom_settings = True
            return
        assert low > 0, "Low must be greater than 0"
        self.wpm_range = [low, high]

    def set_voices(self, voices: list):
        """
        :param voices: List of system voices to be generated from
        """
        self.voices = voices
        if len(voices) == 1:
            self.custom_settings = True

    def set_engine(self, engine: pyttsx3.Engine):
        """
        :param engine: pyttsx3 engine object to generate from
        """
        self.engine = engine
        self.custom_settings = True

    def get_engine(self):
        """
        :return: pyttsx3 engine currently being used
        """
        return self.engine

    def __get_params(self):
        """
        :return: Voice, Volume, WPM params
        """
        voice = random.choice(self.voices)

        # If volume_range only has one value, that's what volume is set to
        if len(self.volume_range) == 1:
            volume = self.volume_range[0]
        else:
            volume = random.uniform(self.volume_range[0], self.volume_range[1])

        # Same with WPM
        if len(self.wpm_range) == 1:
            wpm = self.wpm_range[0]
        else:
            wpm = random.randint(self.wpm_range[0], self.wpm_range[1])

        return voice, volume, wpm

    def __dupes_exist(self, prev: list, tup: tuple):
        """
        :param prev: List of previous tuples in the form of (Voice, Volume, WPM)
        :param tup: Tuple to be checked against prev, in the same format as above
        :return: True if tup is a duplicate (or close to a duplicate) of a tuple in prev
        """
        # Empty prev list will have no dupes
        if len(prev) == 0:
            return False
        # If the user has set custom settings that would break __dupes_exist, always return False
        if self.custom_settings:
            return False

        rls = list(tup)
        for t in prev:
            tls = list(t)
            # Check voices
            if tls[0] is rls[0]:
                # Check volumes
                if abs(tls[1] - rls[1]) < 0.1:
                    # Check WPMs
                    if abs(tls[2] - rls[2]) < 10:
                        return True
        return False

    def generate(self, text, n, out_format="wav"):
        """
        :param text: The text to appear in each sound file
        :param n: The number of sound files to generate
        :param out_format: The audio format the sound files will be converted to
        """
        # files - list of file names for mp3 -> out_format conversion
        # prev - list of previously used voice, volume, and wpm combos so duplicates don't happen
        files = []
        prev = []

        # Make output dir
        if not os.path.isdir(text.replace(" ", "_")):
            os.mkdir(text.replace(" ", "_"))

        for i in range(n):

            if self.verbose:
                print(i + 1)

            # Get params
            voice, volume, wpm = self.__get_params()
            tup = (voice, volume, wpm)

            # While dupes exist, pick new params
            while self.__dupes_exist(prev, tup):
                voice, volume, wpm = self.__get_params()
                tup = (voice, volume, wpm)

            # Add params to prev
            prev.append(tup)

            # Set engine property params
            self.engine.setProperty('volume', volume)
            self.engine.setProperty('rate', wpm)
            self.engine.setProperty('voice', voice.id)

            # Generate the audio files, but don't save them yet (seems counter-intuitive)
            self.engine.save_to_file(text, "./" + text.replace(" ", "_") + "/" + text + "_" + str(i) + ".mp3")
            # Add the filename to files so we can change the format later on
            files.append("./" + text.replace(" ", "_") + "/" + text + "_" + str(i) + ".mp3")

        # This will actually save the audio files
        self.engine.runAndWait()

        # Change the format to out_format, remove the MP3s if needed
        for file in files:
            # Default pyttsx3 output is mp3, so if that's what the user wants, don't convert it
            if out_format is not "mp3":
                AudioSegment.from_file(file).export(file[:-4] + ".wav", format=out_format)
                os.remove(file)
