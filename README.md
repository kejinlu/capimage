A python script that generates resizable image with cap insets.
The script assumes you use Apple's prescribed high-resolution modifier (@2x) to name your high-resolution image.

##Installation


1. Use pip or easy_install to install [PIL](http://pypi.python.org/pypi/PIL) modules,  `sudo pip install PIL`
2. Install capimage
	
		git clone https://github.com/kejinlu/capimage.git
		cd capimage
		sudo python setup.py install

##Usage


1. Image Detection   
   	
		capimage detect my_image.png
		capimage detect *.png
   
2. Image Generation

>usage: capimage.py gen [-h] [-c top left bottom right] [-t target_directory]
                       source_file [source_file ...]

>positional arguments:
  source_file           The source image file paths

>optional arguments:   
  -h, --help            show this help message and exit   
  -c top left bottom right, --capinsets top left bottom right
                        The cap insets for the resizable image   
  -t target_directory, --target-directory target_directory
                        The directory where save the generated image
                        
		capimage gen -c 20 20 20 20 my_image.png
		capimage gen -t ./ ~/Desktop/*.png
	
If the optional argument `capinsets` is ignored, the script will get the capinsets from the result of the detection. For example,if you want to generate a resizable image for `my_image.png`,Besides that get the capinsets with the `my_image.png`, the script will also check for the capinsets of the high-resolution image if exists,and then figure out the final capinsets used for generating. 