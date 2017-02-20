from distutils.core import setup

setup(
    name='audio_embed',
    version='1.0.0',
    packages=['', 'audio_embed'],
    url='http://github.com/pseeth/audio_embed',
    license='MIT',
    author='Prem Seetharaman',
    author_email='prem@u.northwestern.edu',
    description='Useful utilities for embedding audio into Jupyter notebooks.',
    package_data={'': ['templates/multitrack.html']},
    include_package_data = True
)
