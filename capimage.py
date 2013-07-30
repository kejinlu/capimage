#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stdout
from os import path
from glob import iglob
from math import ceil
from itertools import izip
import argparse

from PIL import Image

__author__ = "Luke"
__copyright__ = "Copyright 2012, geeklu.com"
__license__ = "BSD License"
__version__ = "0.1.0"
__maintainer__ = "Luke"
__email__ = "kejinlu@gmail.com"
__status__ = "Beta"


def check_image_with_pil(path):
	try:
		Image.open(path)
	except IOError:
		return False
	return True

def update_progress(progress):
    stdout.write('\r[{0}] {1}%'.format('#'*(progress/2), progress))
    stdout.flush()

def cap_image(source_image, capinsets, isretina=False):
	horizontal_fill_width = 1
	vertical_fill_height = 1
	top_inset = capinsets[0]
	left_inset = capinsets[1]
	bottom_inset = capinsets[2]
	right_inset = capinsets[3]

	if isretina:
		horizontal_fill_width *= 2
		vertical_fill_height *= 2
		top_inset *= 2
		left_inset *= 2
		bottom_inset *= 2
		right_inset *= 2

	source_image_width = source_image.size[0]
	source_image_height = source_image.size[1];
	
	target_image_width = left_inset + right_inset + horizontal_fill_width
	target_image_height = top_inset + bottom_inset + vertical_fill_height
	
	target_image = Image.new("RGBA", (target_image_width, target_image_height),None)

	top_left_image = source_image.crop((0, 0, left_inset, top_inset))
	top_middle_image = source_image.crop((left_inset, 
										0, 
										left_inset + horizontal_fill_width, 
										top_inset))
	top_right_image = source_image.crop((source_image_width - right_inset,
										0,
										source_image_width,
										top_inset))
	middle_left_image = source_image.crop((0, 
										top_inset, 
										left_inset, 
										top_inset + vertical_fill_height))
	middle_middle_image = source_image.crop((left_inset, 
											top_inset, 
											left_inset + horizontal_fill_width, 
											top_inset + vertical_fill_height))
	middle_right_image = source_image.crop((source_image_width - right_inset,
										top_inset,
										source_image_width,
										top_inset + vertical_fill_height))
	bottom_left_image = source_image.crop((0,
										source_image_height - bottom_inset,
										left_inset,
										source_image_height))
	bottom_middle_image = source_image.crop((left_inset,
											source_image_height - bottom_inset,
											left_inset + horizontal_fill_width,
											source_image_height))
	bottom_right_image = source_image.crop((source_image_width - right_inset,
											source_image_height - bottom_inset,
											source_image_width,
											source_image_height))
	
	
	target_image.paste(top_left_image, (0, 0))
	target_image.paste(top_middle_image, (left_inset,0))
	target_image.paste(top_right_image, (left_inset + horizontal_fill_width,0))
	target_image.paste(middle_left_image, (0, top_inset))
	target_image.paste(middle_middle_image, (left_inset, top_inset))
	target_image.paste(middle_right_image, (left_inset + horizontal_fill_width, top_inset))
	target_image.paste(bottom_left_image, (0, top_inset + vertical_fill_height))
	target_image.paste(bottom_middle_image, (left_inset, top_inset + vertical_fill_height))
	target_image.paste(bottom_right_image, (left_inset + horizontal_fill_width, top_inset + vertical_fill_height))
	
	return target_image


def detect_image(image, isretina=False):
	dataList = list(image.getdata())
	source_image_width = image.size[0]
	source_image_height = image.size[1];
	
	rowlist = []; #keep pixels for each row
	for i in xrange(source_image_height):
		rowlist.append([])

	columnlist = [] #keep pixels for each column
	for i in xrange(source_image_width):
		columnlist.append([])

	for i in xrange(len(dataList)):
		data = dataList[i]
		rowlist[i / source_image_width].append(data)
		columnlist[i % source_image_width].append(data)
	
	repeatedrow_intervals = []
	max_repeatedrow_interval = [0, 0]
	for i in xrange(source_image_height - 1):
		if rowlist[i]==rowlist[i + 1]:
			rowpair = [i, i + 1]
			if len(repeatedrow_intervals) > 0 and repeatedrow_intervals[-1][1] == rowpair[0]:
				repeatedrow_intervals[-1][1] = rowpair[1]
			else:
				repeatedrow_intervals.append(rowpair)

			if max_repeatedrow_interval[1] - max_repeatedrow_interval[0] < repeatedrow_intervals[-1][1] - repeatedrow_intervals[-1][0]:
				max_repeatedrow_interval = repeatedrow_intervals[-1];

	repeatedcol_intervals = []
	max_repeatedcol_interval = [0,0]
	for i in xrange(source_image_width - 1):
		if columnlist[i] == columnlist[i + 1]:
			colpair = [i, i + 1]
			if len(repeatedcol_intervals) > 0 and repeatedcol_intervals[-1][1] == colpair[0]:
				repeatedcol_intervals[-1][1] = colpair[1]
			else:
				repeatedcol_intervals.append(colpair)

			if max_repeatedcol_interval[1] - max_repeatedcol_interval[0] < repeatedcol_intervals[-1][1] - repeatedcol_intervals[-1][0]:
				max_repeatedcol_interval = repeatedcol_intervals[-1]

	capinsets = (max_repeatedrow_interval[0],
							max_repeatedcol_interval[0],
							source_image_height - 1 - max_repeatedrow_interval[1],
							source_image_width - 1 - max_repeatedcol_interval[1])
	if isretina:
			capinsets = tuple(int(ceil(capinset/2.0)) for capinset in capinsets)

	detection_info = {
	'repeatedrow_intervals' : repeatedrow_intervals,
	'max_repeatedrow_interval' : max_repeatedrow_interval,
	'repeatedcol_intervals' : repeatedcol_intervals,
	'max_repeatedcol_interval' : max_repeatedcol_interval,
	'suggested_capinsets' : capinsets
	}

	return detection_info



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers(dest="subparser_name")
	parser_image_detect = subparsers.add_parser("detect",help='Make a detection for the source image, get the suggested cap insets')
	parser_image_detect.add_argument('source_file',nargs='+',metavar='source file', help='The source image file paths')
	parser_image_gen = subparsers.add_parser("gen")
	parser_image_gen.add_argument('-c','--capinsets',dest='capinsets', nargs = 4,type = int,metavar=('top', 'left', 'bottom', 'right') ,help='The cap insets for the resizable image')
	parser_image_gen.add_argument('-t','--target-directory',dest='target_directory', metavar='target_directory', help='The directory where save the generated image')
	parser_image_gen.add_argument('source_file',nargs='+',metavar='source_file',help='The source image file paths')
	args=parser.parse_args()
	
	subparser_name = args.subparser_name
	capinsets_dic = {}
	for filepath in args.source_file:
		filepath = path.expanduser(filepath)
		for f in iglob(filepath):
			if check_image_with_pil(f):
				print '************************************'
				print 'Image:%s'%(f,)
				is_retina_image = False
				if '@2x.' in f:
					print 'This is a high-resolution image'
					is_retina_image = True
				else:
					print 'This is a low-resolution image'
	
				image = Image.open(f)
				print "Image size:%sx%s"%(image.size[0],image.size[1])
				
				if subparser_name == 'detect':
					print "Starting to detect..."
					detection_info = detect_image(image,is_retina_image)
					print "Repeated rows intervals:%s" % (detection_info['repeatedrow_intervals'],)
					print "Max row interval:%s" % (detection_info['max_repeatedrow_interval'],)
					print "Repeated columns intervals:%s" % (detection_info['repeatedcol_intervals'],)
					print "Max column interval:%s" % (detection_info['max_repeatedcol_interval'],)
					print "Suggested cap insets:%s" % (detection_info['suggested_capinsets'],)
				
				if subparser_name == 'gen':
					print "Starting to generate resizable image..."
					args_dic = vars(args)
					if 'capinsets' in args_dic and args_dic['capinsets'] is not None:
						capinsets = tuple(i for i in args.capinsets)
						print "Using cap insets with provided:%s"%(capinsets,)
					else:
						print "Cap insets for the resizable image will be got from the result of the detection"
						if f in capinsets_dic:
							capinsets = capinsets_dic[f]
						else:
							detection_info = detect_image(image,is_retina_image)
							capinsets = detection_info['suggested_capinsets']
							capinsets_dic[f] = capinsets
						print "Cap insets got from the results with detection:%s" %(capinsets,)
	
						if is_retina_image:
							unretina_file = ''.join(f.rsplit('@2x',1))
							if unretina_file in capinsets_dic:
								paired_capinsets = capinsets_dic[unretina_file]
							else:
								if check_image_with_pil(unretina_file):
									unretina_image = Image.open(unretina_file)
									unretina_detection_info = detect_image(unretina_image,False)
									paired_capinsets = unretina_detection_info['suggested_capinsets']
									capinsets_dic[unretina_file] = paired_capinsets
							print 'The cap insets of the paired low-resolution image is:%s' %(paired_capinsets,)
						else:
							retina_file = '@2x.'.join(f.rsplit('.',1))
							if retina_file in capinsets_dic:
								paired_capinsets = capinsets_dic[retina_file]
							else:
								if check_image_with_pil(retina_file):
									retina_image = Image.open(retina_file)
									retina_detection_info = detect_image(retina_image,True)
									paired_capinsets = retina_detection_info['suggested_capinsets']
									capinsets_dic[retina_file] = paired_capinsets
							print 'The cap insets of the paired high-resolution image is:%s' %(paired_capinsets,)
	
	
						capinsets = tuple(max(x, y) for x, y in izip(capinsets,paired_capinsets))
						print 'The final cap insets is :%s' %(capinsets,)
	
	
					if 'target_directory' in args_dic and args_dic['target_directory'] is not None:
						target_directory = args.target_directory
					else:
						target_directory = '.'
	
					target_image = cap_image(image, capinsets,is_retina_image)
					filename = path.split(f)[1]
					if is_retina_image:
						sep = '@2x.'
					else:
						sep = '.'
					
					filename_components = filename.rsplit(sep,1)
	
	
					capstring = '-'.join("%d"%i for i in capinsets)
					newfilename = '%s-%s%s%s'%(filename_components[0], capstring, sep, filename_components[1])
					target_file_path = path.join(path.expanduser(target_directory),newfilename)
					target_image.save(target_file_path,image.format)
					print 'The resizable image generated successful:%s' %(target_file_path,)
	
	
			else:
				print "******************************************"
				print "'%s' is not a valid image !" %(f)

