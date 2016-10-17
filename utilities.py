import ffmpy
import IPython
import os
from IPython.core.display import HTML
from IPython.display import IFrame
import librosa
import base64

"""
This package has some functions I have found useful for manipulating and embedding audio into Jupyter notebooks.

Requires librosa, ffmpy (which requires ffmpeg), and IPython.
"""

def audio(d, sr):
    """
	Write a numpy array to a temporary mp3 file using ffmpy, then embeds the mp3 into the notebook.
	Parameters:
	   d: numpy array of audio data.
	   sr: sampling rate for the audio
	"""
    tmp_file = 'tmp.mp3'
    file_path = 'tmp.wav'
    librosa.output.write_wav('tmp.wav', d, sr)
    ff = ffmpy.FFmpeg(
        inputs={file_path: None},
        outputs={tmp_file: None})
    ff.run()
    IPython.display.display(IPython.display.Audio(data=tmp_file, rate = sr))
    os.remove('tmp.mp3')
    os.remove('tmp.wav')

def encode_audio(d, sr):
    """
	Writes the data to a temporary mp3 file using ffmpy, then returns the base64 encoding for further manipulation.
	Parameters:
	   d: numpy array of audio data.
	   sr: sampling rate for the audio
	"""
    tmp_file = 'tmp.mp3'
    file_path = 'tmp.wav'
    librosa.output.write_wav('tmp.wav', d, sr)
    ff = ffmpy.FFmpeg(
        inputs={file_path: None},
        outputs={tmp_file: None})
    ff.run()
    f = open('tmp.mp3', 'rb')
    b = base64.b64encode(f.read())
    f.close()
    os.remove('tmp.mp3')
    os.remove('tmp.wav')
    return 'data:audio/mpeg;base64,' + b
    

def multitrack(sources, sr, name):
    """
	Takes a bunch of audio sources, converts them to mp3 to make them smaller, and creates a multitrack audio player in the notebook that lets you toggle between the sources and the mixture. Heavily adapted from https://github.com/binarymind/multitrackHTMLPlayer, designed by Bastien Liutkus.
	Parameters:
	    sources - list of numpy arrays, each containing a separated source which sum up to a mixture.
		sr - sampling rate for each audio file
        name - a uniquely identifiable name in your notebook, no spaces or special characters.
	"""

    template = """
    <div id = 'NAME' class='audio-container'  name='NAME'>
    <audio name="Foreground" url="<foreground_data>"></audio>
    <audio name="Background" url="<background_data>"></audio>
    </div>
    """
    f = open('multitrack.html', 'r')
    footer = f.read()
    f.close()
    
    replace_points = ['<foreground_data>', '<background_data>']
    for s, r in zip(sources, replace_points):
        b = encode_audio(s, sr)
        template = template.replace(r, b)
    template += footer
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
