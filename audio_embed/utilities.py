import ffmpy
import IPython
import os
from IPython.core.display import HTML
from IPython.display import IFrame
import librosa
import base64
import pkg_resources
import random
import string
import numpy as np

resource_package = __name__
resource_path = '/'.join(['templates', 'multitrack.html'])

multitrack_template = pkg_resources.resource_string(resource_package, resource_path)


"""
This package has some functions I have found useful for manipulating and embedding audio into Jupyter notebooks.

Requires librosa, ffmpy (which requires ffmpeg), and IPython.
"""

def random_string(N):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(N))

def audio(d, sr):
    """
	Write a numpy array to a temporary mp3 file using ffmpy, then embeds the mp3 into the notebook.
	Parameters:
	   d: numpy array of audio data.
	   sr: sampling rate for the audio
	"""
    rand_str = random_string(5)
    tmp_file = rand_str + 'tmp.mp3'
    tmp_wav = rand_str + 'tmp.wav'
    librosa.output.write_wav(tmp_wav, d, sr)
    ff = ffmpy.FFmpeg(
        inputs={tmp_wav: None},
        outputs={tmp_file: '-write_xing 0 -codec:a libmp3lame -qscale:a 2'})
    ff.run()
    IPython.display.display(IPython.display.Audio(data=tmp_file, rate = sr))
    os.remove(tmp_file)
    os.remove(tmp_wav)

def encode_audio(d, sr):
    """
	Writes the data to a temporary mp3 file using ffmpy, then returns the base64 encoding for further manipulation.
	Parameters:
	   d: numpy array of audio data.
	   sr: sampling rate for the audio
	"""
    rand_str = random_string(5)
    tmp_file = rand_str + 'tmp.mp3'
    tmp_wav = rand_str + 'tmp.wav'
    librosa.output.write_wav(tmp_wav, d, sr)
    ff = ffmpy.FFmpeg(
        inputs={tmp_wav: None},
        outputs={tmp_file: '-write_xing 0 -codec:a libmp3lame -qscale:a 2'})
    ff.run()
    
    f = open(tmp_file, 'rb')
    b = base64.b64encode(f.read()).decode('ascii')
    f.close()
    
    os.remove(tmp_file)
    os.remove(tmp_wav)
    return """data:audio/mpeg;base64,""" + b
    

def multitrack(sources, sr, name):
    """
	Takes a bunch of audio sources, converts them to mp3 to make them smaller, and creates a multitrack audio player in the notebook that lets you toggle between the sources and the mixture. Heavily adapted from https://github.com/binarymind/multitrackHTMLPlayer, designed by Bastien Liutkus.
	Parameters:
	    sources - list of tuples of the form [(source_data, source_name), (source_data, source_name), ...] with each tuple containing a separated source which sum up to a mixture and a name for that source (e.g. harmonic, percussive).
		sr - sampling rate for each audio file
        name - a uniquely identifiable name in your notebook, no spaces or special characters.
	"""

    template = """
    <div id = 'NAME' class='audio-container'  name='NAME'>
    """
    #check lengths
    for s in sources:
        audio_element = """
        <audio name="source_name" url="source_data">
        </audio>
        """
        b = encode_audio(s[0], sr)
        audio_element = audio_element.replace('source_data', b)
        audio_element = audio_element.replace('source_name', s[1])
        template += audio_element
    template += "</div>"
    template += multitrack_template
    template = template.replace('NAME', name)
    IPython.display.display(HTML(template))

def apply_style():
    """
	Useful styles for displaying graphs and audio elements.
	"""
    style = HTML("""
        <style>
            audio {
            width: 100% !important;
        }
        .output_png {
            text-align: center !important;
        }
        </style>
        """)
    IPython.display.display(style)
