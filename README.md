##介绍
在很多编程语言中都有resizable image这样的概念，比如android中的NinePatch graphic ，css3中的border image，微软的Nine-Grid Rendering，还有就是iOS中UIImage的resizable image。			
<table border="1">
  <tr>
    <td>1</td>
    <td>2</td>
    <td>3</td>
  </tr>
    <tr>
    <td>4</td>
    <td>5</td>
    <td>6</td>
  </tr>
    <tr>
    <td>7</td>
    <td>8</td>
    <td>9</td>
  </tr>
</table>
可以将resizable image分成9部分，通过它生成大图片的时候遵循以下规则：四个角(1,3,7,9)保持不变，上下(2,8)进行横向平铺或拉伸，左右（4,6）进行纵向的平铺或拉伸，中央(5)则是双向平铺或拉伸。   


<img  width="160" height="160" src="http://ww4.sinaimg.cn/large/65cc0af7jw1e7fp6jnvapg205u05ua9u.gif
"/>    
此9宫格的模型可以使用cap insets来进行描述，cap insets有四个参数，top,left,bottom,right,分别描述9宫格上左下右的大小。
   
capimage.py是一个使用python的PIL库写的脚本，用于将一个普通的图片去除重复部分生成一个可伸缩的图片（resizable image），这样使得图片资源的使用更加灵活和节省空间。cap image支持苹果格式的高清图片（命名格式为xxx@2x.png），脚本会智能的进行检查，上面所提及的capinsets的单位是point而非pixel，在高清的情况下1point等于2pixel。


##安装

1. Mac或者Linux平台， Python2.7 
2. 使用pip或者easy_install 安装 [PIL](http://pypi.python.org/pypi/PIL) 模块,  `sudo pip install PIL`
3. 安装 capimage
	
		git clone https://github.com/kejinlu/capimage.git
		cd capimage
		sudo python setup.py install

##用法


1. 图片检测   
   	
		capimage detect my_image.png
		capimage detect *.png
图片检测所做的事情就是对单个图片进行逐行以及逐列的像素对比，找出其所有的行像素连续相等的区间，以及列像素连续相等的区间。
   
2. 生成图片

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
	
如果生成的时候没有指定 cap insets，那么脚本会自动去进行检测，算出最终的cap insets，计算capinsets并不是简单的根据当前图片来进行计算，还会检测与之配对的高清（或非高清）的图片的cap insets，然后算出最终的cap insets。这是因为一般情况下非高清和高清图片并不是简单的把每一个行或者列的像素重复一次，而是有很多矢量的放大效果，所以高清和非高清图片算出来的cap insets往往不一样。

##使用案例

假设我有两个原始图片:[common_modal_bkg.png](https://raw.github.com/kejinlu/capimage/master/sample/common_modal_bkg.png) and [common_modal_bkg@2x.png](https://raw.github.com/kejinlu/capimage/master/sample/common_modal_bkg@2x.png)    

<img  width="451" height="274" src="https://raw.github.com/kejinlu/capimage/master/sample/common_modal_bkg.png
"/>    

<img  width="902" height="548" src="https://raw.github.com/kejinlu/capimage/master/sample/common_modal_bkg@2x.png
"/>   

然后我运行 `capimage detect common_modal_bkg*.png`,得到如下结果:

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
	
	
若运行 `capimage gen common_modal_bkg*.png`,便生成两个可伸缩的图片			
<img  width="44" height="44" src="https://raw.github.com/kejinlu/capimage/master/sample/common_modal_bkg-21-21-22-22.png
"/>       
<img  width="88" height="88" src="https://raw.github.com/kejinlu/capimage/master/sample/common_modal_bkg-21-21-22-22@2x.png
"/>  