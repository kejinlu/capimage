from sys import stdout
from optparse import OptionParser
from PIL import Image


def update_progress(progress):
    stdout.write('\r[{0}] {1}%'.format('#'*(progress/2), progress))
    stdout.flush()

def cap_image(image,capinsets):
	source_image_width = image.size[0]
	source_image_height = image.size[1];

	top_inset = capinsets[0]
	left_inset = capinsets[1]
	bottom_inset = capinsets[2]
	right_inset = capinsets[3]
	
	target_image_width = left_inset + right_inset + 1
	target_image_height = top_inset + bottom_inset + 1
	
	target_image = Image.new("RGBA", (target_image_width, target_image_height),"red")
	
	top_left_image = im.crop((0, 0, left_inset, top_inset))
	top_middle_image = im.crop((left_inset, 0, left_inset + 1, top_inset))
	top_right_image = im.crop((source_image_width - right_inset,0,source_image_width,top_inset))
	middle_left_image = im.crop((0, top_inset, left_inset, top_inset + 1))
	middle_middle_image = im.crop((left_inset, top_inset, left_inset + 1, top_inset + 1))
	middle_right_image = im.crop((source_image_width - right_inset,top_inset,source_image_width,top_inset+1))
	bottom_left_image = im.crop((0,source_image_height - bottom_inset,left_inset,source_image_height))
	bottom_middle_image = im.crop((left_inset,source_image_height - bottom_inset,left_inset+1,source_image_height))
	bottom_right_image = im.crop((source_image_width-right_inset,source_image_height- bottom_inset,source_image_width,source_image_height))
	
	
	target_image.paste(top_left_image,(0,0))
	target_image.paste(top_middle_image,(left_inset,0))
	target_image.paste(top_right_image,(left_inset+1,0))
	target_image.paste(middle_left_image,(0,top_inset))
	target_image.paste(middle_middle_image,(left_inset,top_inset))
	target_image.paste(middle_right_image,(left_inset+1,top_inset))
	target_image.paste(bottom_left_image,(0,top_inset+1))
	target_image.paste(bottom_middle_image,(left_inset,top_inset+1))
	target_image.paste(bottom_right_image,(left_inset+1,top_inset+1))
	return target_image





def test_image(image):
	dataList = list(image.getdata())
	source_image_width = image.size[0]
	source_image_height = image.size[1];
	
	rowlist = [];
	for r in range(source_image_height):
		row = dataList[r*source_image_width:(r+1)*source_image_width]
		rowlist.append(row);

	columnlist = []
	for c in range(source_image_width):
		update_progress(100*(c+1)/source_image_width)
		columnlist.append([dataList[i] for i in range(source_image_width * source_image_height) if i % source_image_width == c])
	
	
	
	for i in range(source_image_height-1):
		if rowlist[i]==rowlist[i+1]:
			print "%d=%d  " %(i,i+1)
	
	print "~~~~~~~~~~~~"
	
	for i in range(source_image_width - 1):
		if columnlist[i] == columnlist[i+1]:
			print "%d=%d " %(i,i+1)



im = Image.open("/Users/Luke/Desktop/1111.png")
test_image(im)
target_image = cap_image(im, (20,20,20,20))
target_image.save("/Users/Luke/Desktop/target111.png","PNG")



