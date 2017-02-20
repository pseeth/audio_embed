from csscompressor import compress
from jsmin import jsmin

f = open('screen.css', 'r')
css = compress(f.read())
f.close()

f = open('player.js', 'r')
js = jsmin(f.read())
f.close()

css = '<style>' + css + '</style>'
js = '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>' \
     '<script>' + js + '</script>'

f = open('multitrack.html', 'w')
f.write(css + js)
f.close()
