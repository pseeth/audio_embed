import os
from csscompressor import compress
from jsmin import jsmin

f = open('screen.css', 'r')
css = compress(f.read())
f.close()

f = open('player.js', 'r')
js = jsmin(f.read())
f.close()

css = '<style>' + css + '</style>'
js = '<script>' + js + '</script>'

f = open('multitrack.html', 'w')
f.write(css + js)
f.close()
