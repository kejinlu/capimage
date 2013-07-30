A python script that generates resizable image from original image with cap insets.
The script assumes you use Apple's prescribed high-resolution modifier (@2x) to name your high-resolution image.

###Installation

1. Use pip or easy_install to install [PIL](http://pypi.python.org/pypi/PIL) modules.  `sudo pip install PIL`
2. Install capimage
	
	git clone https://github.com/kejinlu/capimage.git
	cd capimage
	sudo python setup.py install

###Usage
For example, if you want to generate a resizable image for 'my_image.png',the script will also check if high-resolution image exists. 