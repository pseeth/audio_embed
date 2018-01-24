#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from tempfile import NamedTemporaryFile
import numpy as np
try:
    from nussl import AudioSignal
    nussl_available = True
except:
    nussl_available = False

resource_package = __name__
resource_path = '/'.join(['templates', 'multitrack.html'])

multitrack_template = pkg_resources.resource_string(resource_package, resource_path)


"""
This package has some functions I have found useful for manipulating and embedding audio into Jupyter notebooks.

Requires librosa, ffmpy (which requires ffmpeg), and IPython.
"""

def random_string(N):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(N))

def write_audio(path, d, sr):
    """
	Write a numpy array to a temporary mp3 file using ffmpy, then embeds the mp3 into the notebook.
	Parameters:
	   d: numpy array of audio data.
	   sr: sampling rate for the audio
	"""
    output_file = path
    tmp_wav = NamedTemporaryFile(mode='w', suffix='.wav')
    flags = '-nostdin -write_xing 0 -codec:a libmp3lame -b:a 128k'
    librosa.output.write_wav(tmp_wav.name, d, sr)
    ff = ffmpy.FFmpeg(
        inputs={tmp_wav.name: None},
        outputs={output_file: flags})
    ff.run()
    tmp_wav.close()
    os.remove(tmp_wav.name)

def audio(d, sr=None, ext = '.mp3'):
    """
	Write a numpy array to a temporary mp3 file using ffmpy, then embeds the mp3 into the notebook.
	Parameters:
	   d: numpy array of audio data.
	   sr: sampling rate for the audio
	"""
    if nussl_available:
        if type(d) is AudioSignal:
            sr = d.sample_rate
            d = d.audio_data
        elif sr is None:
            raise ValueError('Sample rate must be provided when d is not an AudioSignal object!')
    tmp_converted = NamedTemporaryFile(mode='w+', suffix='.mp3')
    tmp_wav = NamedTemporaryFile(mode='w+', suffix='.wav')
    librosa.output.write_wav(tmp_wav.name, d, sr)
    ff = ffmpy.FFmpeg(
        inputs={tmp_wav.name: None},
        outputs={tmp_converted.name: '-nostdin -write_xing 0 -codec:a libmp3lame -b:a 128k -y'})
    ff.run()
    IPython.display.display(IPython.display.Audio(data=tmp_converted.name, rate = sr))
    tmp_converted.close()
    tmp_wav.close()

def encode_audio(d, sr, ext='.mp3'):
    """
	Writes the data to a temporary mp3 file using ffmpy, then returns the base64 encoding for further manipulation.
	Parameters:
	   d: numpy array of audio data.
	   sr: sampling rate for the audio
	"""
    if nussl_available:
        if type(d) is AudioSignal:
            sr = d.sample_rate
            d = d.audio_data
        elif sr is None:
            raise ValueError('Sample rate must be provided when d is not an AudioSignal object!')
    tmp_converted = NamedTemporaryFile(mode='w+', suffix=ext)
    tmp_wav = NamedTemporaryFile(mode='w+', suffix='.wav')
    librosa.output.write_wav(tmp_wav.name, d, sr)
    ff = ffmpy.FFmpeg(
        inputs={tmp_wav.name: None},
        outputs={tmp_converted.name: '-nostdin -write_xing 0 -codec:a libmp3lame -b:a 128k -y'})
    ff.run()
    audio = IPython.display.Audio(data=tmp_converted.name, rate=sr)
    tmp_converted.close()
    tmp_wav.close()
    return audio.src_attr()
    

def multitrack(sources, sr=None, ext='.mp3'):
    name = random_string(10)
    """
	Takes a bunch of audio sources, converts them to mp3 to make them smaller, and creates a multitrack audio player in the notebook that lets you toggle between the sources and the mixture. Heavily adapted from https://github.com/binarymind/multitrackHTMLPlayer, designed by Bastien Liutkus.
	Parameters:
	    sources - list of tuples of the form [(source_data, source_name), (source_data, source_name), ...] with each tuple containing a separated source which sum up to a mixture and a name for that source (e.g. harmonic, percussive).
		sr - sampling rate for each audio file
	"""

    template = """
    <div id = 'NAME' class='audio-container' preload = 'auto' name='NAME'>
    """
    for s in sources:
        audio_element = """
        <audio name="source_name" url="source_data">
        </audio>
        """
        b = encode_audio(s[0], sr, ext=ext)
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
