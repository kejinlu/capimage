A python script that generates resizable image with cap insets.
The script assumes you use Apple's prescribed high-resolution modifier (@2x) to name your high-resolution image.

##Installation

1. (Mac || Linux) && Python2.7 
2. Use pip or easy_install to install [PIL](http://pypi.python.org/pypi/PIL) module,  `sudo pip install PIL`
3. Install capimage
	
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

##Example

If a have tow images:[common_modal_bkg.png](https://raw.github.com/kejinlu/capimage/master/sample/common_modal_bkg.png) and [common_modal_bkg@2x.png](https://raw.github.com/kejinlu/capimage/master/sample/common_modal_bkg@2x.png) in Desktop folder,then I run `capimage detect common_modal_bkg*.png`,and I get the result:

	Luke@LukesMac:~/Desktop » capimage detect common_modal_bkg*.png
	************************************
	Image:common_modal_bkg.png
	This is a low-resolution image
	Image size:451x274
	Starting to detect...
	Repeated rows intervals:[[19, 253]]
	Max row interval:[19, 253]
	Repeated columns intervals:[[19, 430]]
	Max column interval:[19, 430]
	Suggested cap insets:(19, 19, 20, 20)
	************************************
	Image:common_modal_bkg@2x.png
	This is a high-resolution image
	Image size:902x548
	Starting to detect...
	Repeated rows intervals:[[35, 36], [38, 41], [42, 503], [504, 507], [509, 510], [545, 547]]
	Max row interval:[42, 503]
	Repeated columns intervals:[[38, 41], [42, 857], [858, 861], [899, 901]]
	Max column interval:[42, 857]
	Suggested cap insets:(21, 21, 22, 22)
	