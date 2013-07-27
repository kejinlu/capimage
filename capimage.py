#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stdout
from os import path
import argparse
from PIL import Image
import glob


def update_progress(progress):
    stdout.write('\r[{0}] {1}%'.format('#'*(progress/2), progress))
    stdout.flush()

def cap_image(image,capinsets,isretina=False):
	horizontal_fill_width = 1
	vertical_fill_height = 1
	top_inset = capinsets[0]
	left_inset = capinsets[1]
	bottom_inset = capinsets[2]
	right_inset = capinsets[3]

	if isretina:
		horizontal_fill_width*=2
		vertical_fill_height*=2
		top_inset*=2
		left_inset*=2
		bottom_inset*=2
		right_inset*=2

	source_image_width = image.size[0]
	source_image_height = image.size[1];
	
	target_image_width = left_inset + right_inset + horizontal_fill_width
	target_image_height = top_inset + bottom_inset + vertical_fill_height
	
	target_image = Image.new("RGBA", (target_image_width, target_image_height),"red")
	
	top_left_image = im.crop((0, 0, left_inset, top_inset))
	top_middle_image = im.crop((left_inset, 0, left_inset + horizontal_fill_width, top_inset))
	top_right_image = im.crop((source_image_width - right_inset,0,source_image_width,top_inset))
	middle_left_image = im.crop((0, top_inset, left_inset, top_inset + vertical_fill_height))
	middle_middle_image = im.crop((left_inset, top_inset, left_inset + horizontal_fill_width, top_inset + vertical_fill_height))
	middle_right_image = im.crop((source_image_width - right_inset,top_inset,source_image_width,top_inset+vertical_fill_height))
	bottom_left_image = im.crop((0,source_image_height - bottom_inset,left_inset,source_image_height))
	bottom_middle_image = im.crop((left_inset,source_image_height - bottom_inset,left_inset+horizontal_fill_width,source_image_height))
	bottom_right_image = im.crop((source_image_width-right_inset,source_image_height- bottom_inset,source_image_width,source_image_height))
	
	
	target_image.paste(top_left_image,(0,0))
	target_image.paste(top_middle_image,(left_inset,0))
	target_image.paste(top_right_image,(left_inset+horizontal_fill_width,0))
	target_image.paste(middle_left_image,(0,top_inset))
	target_image.paste(middle_middle_image,(left_inset,top_inset))
	target_image.paste(middle_right_image,(left_inset+horizontal_fill_width,top_inset))
	target_image.paste(bottom_left_image,(0,top_inset+vertical_fill_height))
	target_image.paste(bottom_middle_image,(left_inset,top_inset+vertical_fill_height))
	target_image.paste(bottom_right_image,(left_inset+horizontal_fill_width,top_inset+vertical_fill_height))
	return target_image





def detect_image(image,isretina=False):
	dataList = list(image.getdata())
	source_image_width = image.size[0]
	source_image_height = image.size[1];
	
	rowlist = [];
	for i in xrange(source_image_height):
		rowlist.append([])

	columnlist = []
	for i in xrange(source_image_width):
		columnlist.append([])

	for i in xrange(len(dataList)):
		data = dataList[i]
		rowlist[i/source_image_width].append(data)
		columnlist[i%source_image_width].append(data)
	
	repeatedrow_intervals = []
	max_repeatedrow_interval = [0,0]
	for i in xrange(source_image_height-1):
		if rowlist[i]==rowlist[i+1]:
			rowpair = [i,i+1]
			if len(repeatedrow_intervals) > 0 and repeatedrow_intervals[-1][1] == rowpair[0]:
				repeatedrow_intervals[-1][1] = rowpair[1]
			else:
				repeatedrow_intervals.append(rowpair)

			if max_repeatedrow_interval[1] - max_repeatedrow_interval[0] < repeatedrow_intervals[-1][1] - repeatedrow_intervals[-1][0]:
				max_repeatedrow_interval = repeatedrow_intervals[-1];

	print repeatedrow_intervals
	print "   max   "
	print max_repeatedrow_interval
	print "~~~~~~~~~~~~"

	repeatedcol_intervals = []
	max_repeatedcol_interval = [0,0]
	for i in xrange(source_image_width - 1):
		if columnlist[i] == columnlist[i+1]:
			colpair = [i,i+1]
			if len(repeatedcol_intervals) > 0 and repeatedcol_intervals[-1][1] == colpair[0]:
				repeatedcol_intervals[-1][1] = colpair[1]
			else:
				repeatedcol_intervals.append(colpair)

			if max_repeatedcol_interval[1]-max_repeatedcol_interval[0] < repeatedcol_intervals[-1][1] - repeatedcol_intervals[-1][0]:
				max_repeatedcol_interval = repeatedcol_intervals[-1]

	print repeatedcol_intervals

	print "建议capinsts"
	print "(%d,%d,%d,%d)" %(max_repeatedrow_interval[0],max_repeatedcol_interval[0],source_image_height-1- max_repeatedrow_interval[1],source_image_width -1 -max_repeatedcol_interval[1])

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="subparser_name")
parser_image_detect = subparsers.add_parser("detect")
parser_image_detect.add_argument('imagefiles',nargs='+')
parser_image_gen = subparsers.add_parser("gen")
parser_image_gen.add_argument('-c','--capinsets',nargs=4,type=int,metavar=('top', 'left', 'bottom', 'right'))
parser_image_gen.add_argument('imagefile',nargs='+')
args=parser.parse_args()

print args.capinsets
print args.subparser_name
for imagefile in args.imagefiles:
	imagefile = path.expanduser(imagefile)
	for f in glob.iglob(imagefile):
		print f
		im = Image.open(f)
		detect_image(im)

