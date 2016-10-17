# Embedding audio into jupyter notebooks.

This repository contains useful functions for embedding audio into Jupyter notebooks. 

Usage:

This is used in Jupyter notebooks so everything should be within the notebook environment. Check out the example notebook here: http://nbviewer.jupyter.org/github/pseeth/audio_embed/blob/master/example_notebook.ipynb (the preview on Github does not include any audio elements when rendering notebooks!).

~~~~
import librosa
from audio_embed import utilities
filename = librosa.util.example_audio_file()

#Apply a style sheet that makes audio elements stretch the page, and centers images.
utilities.apply_style()

#Load the librosa example audio file and embed it into the page. 
#The package converts it to mp3 to make the notebook more lightweight, as notebooks over 100MB DO NOT SAVE.
d, sr = librosa.load(filename)
utilities.audio(d, sr)

stft = librosa.stft(d)

#Separate it into two sources using some algorithn (in thie case HPSS)
harmonic, percussive = librosa.decompose.hpss(stft)

harmonic = librosa.istft(harmonic)
percussive = librosa.istft(percussive)

#Display the multitrack player which allows you to toggle between sources and the mixture.
utilities.multitrack([harmonic, percussive], sr, 'test')
~~~~

It contains a minified and handy multitrack HTML audio player designed by Bastien Liutkus (https://github.com/binarymind/multitrackHTMLPlayer) that is useful for looking at source separation algorithms.
