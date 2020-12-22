# Webtemp
## Usage:
The only files you need are main.py and csettings.json

You can compile your website very easily. Just run `python main.py` and your website is compiled in a new directory called build.
You can find an example of usage in the site and template directory.

Webtemp uses *.webcontent (content) files, filling the blocks of *.webtemp (template) files. Both *.webcontent and *.webtemp are presets and can be changed in a single line from main.py. Webtemp does not touch other files (images, code etc) and just copies them in the build directory. Finally, webcontent and webtemp are html files. 
