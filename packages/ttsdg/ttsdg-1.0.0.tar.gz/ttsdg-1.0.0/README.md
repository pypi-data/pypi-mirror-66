# TTSDG
TTSDG, or Text-To-Speech Data Generator, automates the simple-but-frustrating task of generating large amounts of TTS
data for tasks like machine learning. TTSDG contains an easy-to-use class that can generate text offline, in large 
batches, and with control over the system voices that you have installed. TTSDG randomizes volume, speed, and voice of 
each sample if desired.

TTSDG utilizes [pyttsx3](https://pypi.org/project/pyttsx3/) and [pydub](https://pypi.org/project/pydub/) to generate the
audio and convert it into multiple formats. All pydub-supported formats are supported in TTSDG, like WAV, MP3, and AIFF.

# Installation
TTSDG is available through pip:

`python3 -m pip install ttsdg`

# Usage
```python
from ttsdg import TTSDG

gen = TTSDG(verbose=True)

gen.volume_range = [.5, 1.0]
gen.wpm_range = [200, 400]

gen.generate("Hello World!", 100, out_format="wav")
```

# Methods
- `set_volume_range(low, high, one)` - Set low or high volume bounds, or set `one` for a specific value.
- `set_wpm_range(low, high, one)` - Set low or high speed bounds (in words per minute), or set `one` for a specific 
value.
- `set_voices(voices)` - Only mess around with this if you know what you're doing. Sets the list of voices to choose
from, relies on what system voices you have installed. 
- `set_engine(engine)` - Only mess around with this if you know what you're doing. Sets the pyttsx3 Engine object,
useful for importing settings if your project already has an engine.
- `get_engine()` - Gets the pyttsx3 engine object.
- `generate(text, samples, out_format)` - Generates `n` samples of the input `text`, saves them to 
`./(text)/(text)_index.(out_format)`