# -*- coding: UTF-8 -*-
#shiyanlou 测试 https://www.shiyanlou.com/courses/370/labs/1191/document
#环境python3.7.0
#需要使用命令行执行，执行时先将命令行字体，背景调整好，并将窗口最大化
#在实验楼的基础上，不使用argparse库

#图片处理库
from PIL import Image,ImageGrab
#用于windows系统文件夹，文件列表的获取，以及直接命令行命令
import  os
#用来给程序延时
import time
#图片生成GIF，所需要装的库
import imageio

#我们可以创建一个不重复的字符列表，灰度值小（暗）的用列表开头的符号，灰度值大（亮）的用列表末尾的符号。
#多加了几个空格和点，算是增大白色的容差。。
ascii_char = list("$$$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?+~<>i!lI^;:_-,.     ")

#定义默认值的常量
MY_Width = 150
MY_Height = 60
#生成的文件夹名称定义
MY_PATH = '目标路径'
_01_GIF_chaifen_path = '=1=GIF拆分'
_02_TXT_zifuhua_path = '=2=字符画txt'
_03_PNG_jietu_path   = '=3=截图png'
_00_GIF_OutPut_path  = '=0=GIF_output'

def dir_creat(dir_name):
    # 如果不存在此目录，就创建
    if os.path.exists(dir_name):
        pass
    else:
        os.makedirs(dir_name)


# 将256灰度映射到70个字符上
def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)#字符灰度对照表长度
    # RGB 值映射到灰度值的公式，得到像素的灰度值
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    # 灰度值范围为 0-255，而字符集只有 70
    # unit 相当于，真实灰度值大小  转换为  灰度字符集长度的 比例
    unit = (256.0+1)/length
    return ascii_char[int(gray/unit)]

#GIF帧数确定
def gif_zhenshu(image_gif):
    i = 0
    try :
        while True:
            image_gif.seek(i)
            print('&&&   确认到文件的第 “%d” 帧'%(i+1))
            i+=1
    except:
        pass
    print ('文件一共%d帧'%(i))
    return  i



#GIF图片拆分成若干个png
def gif_chaifen(user_input_file_dir,os_dir_list):
#user_input_file_dir 默认为py文件同目录下的  康娜  文件夹
#os_dir_list 默认为康娜文件夹下的  文件及目录列表
    gif_file_name = ''
    for files in os_dir_list:
        houzhui = os.path.splitext(files)[-1][1:]
        #从中只找GIF文件
        if (houzhui == 'GIF') or (houzhui == 'gif'):
            gif_file_name = files
            print('---扫描目录，得到的gif图为：  ' + gif_file_name)
    else:
        pass

    #读取gif文件,这个是专门读取GIF的函数。。返回的是个list
    image_gif = Image.open(user_input_file_dir+'\\'+gif_file_name)
    print ('GIF文件长度:   '+ str(image_gif)+ '  -----------------------------------------------')

    try:
        i = 0
        gif_dir = user_input_file_dir+'\\'+_01_GIF_chaifen_path
        #创建文件夹
        dir_creat(gif_dir)


        #确定GIF一共多少帧,好给文件名补零,如果不补零，后面GIF合并的时候文件顺序会乱
        buling = ''
        zhenshu = gif_zhenshu(image_gif)
        if zhenshu <100:
            buling = "%03d"
        elif  100<=zhenshu<1000:
            buling = "%04d"
        else:

            print('！！！！！非常抱歉，图片帧数太大，不予处理！！！！！')
            raise OSError


        while True:
            #数字前补零，，利于文件顺序的整理
            # 字符串名----------------------------------------因为这里“buling”是字符串
            gif_split_name = (gif_dir+'\\'+ gif_file_name + '_' + buling%i + '.png')

            image_gif.seek(i)
            image_gif.save(gif_split_name)
            print('GIF第{}帧拆解成功...'.format(i + 1))
            i = i + 1
    except EOFError:
        #image_gif.seek(0)
        pass
    print('===function===   拆分结束    =======')
#================================================================================================================



#字符画处理函数
#传入：用户输入文件夹名称、文件夹内容列表，用户输入宽高
#user_input_file_dir  所需要处理的图片所在目录名orPATH
#os_dir_list          所需要处理的图片所在目录下的文件列表
#user_input_wh        用户输入宽高
def wenjianbianli(user_input_file_dir , os_dir_list , user_input_wh):
    #遍历文件列表
    # files 文件列表中每个文件的名称
    # houzhui 获取文件后缀，用于判断是否为png或jpg图片
    # image_path 字符串，将文件夹名称与图片名称合并，用于文件操作
    # Width,Height 用于存储用户输入的高宽
    # Output 设置输出文件名称：文件夹名称+图片名+尾巴
    # txt字符串，用来存储得出的字符画
    '''
    将gif拆分
    '''
    gif_chaifen(user_input_file_dir, os_dir_list)
    time.sleep(0.1)



    image_bianli_dir = user_input_file_dir+'\\'+_01_GIF_chaifen_path
    os_dir_list_2 = os.listdir(image_bianli_dir)

    for files in os_dir_list_2:
        # 获取后缀（文件类型）
        #   assert os.path.splitext(files)[-1] 得到 ".py"  ，后面加个[1:]则得到“py” assert 是断言语句
        houzhui = os.path.splitext(files)[-1][1:]

        if (houzhui == 'png') or (houzhui == 'jpg')or (houzhui == 'PNG')or (houzhui == 'JPG'):

            #os库操作得到的变量houzhui和files貌似不是字符串类型，也不能用type()函数来判断数据类型
            print('！----操作'+houzhui+'图片文件：'+files+'....')
            #  user_input_path = input('请输入文件名或文件路径（如果图片与py文件在目一录下，则只需要输入名称）：')
            # 如果图片文件跟py文件在同一目录就直接输入文件名。
            #  image_path = user_input_path
            image_path = image_bianli_dir+ '\\' + files

            if user_input_wh:
                # 将user_input_wh(用户输入内容)以逗号分隔，（括号里为空，则以空格分隔）得到一个list
                Width = int(user_input_wh.split(',')[0])
                Height = int(user_input_wh.split(',')[1])
            else:
                # 如果用户选择跳过，则设置默认宽高
                Width = MY_Width
                Height = MY_Height

            # Output 设置输出文件名称：文件夹名称+图片名+尾巴
            Output = user_input_file_dir + '\\'+ _02_TXT_zifuhua_path
            Output_file = Output + '\\' + files + '_output.txt'

            #创建文件夹
            dir_creat(Output)

            # 使用PIL库打开图片
            im_00 = Image.open(image_path)
            # Image.NEAREST 低质量、Image.ANTIALIAS 表示输出高质量
            im_00 = im_00.resize((Width, Height), Image.ANTIALIAS)
            im = im_00.convert('RGB')

            # 创建字符串txt后面的结果全部输出到这个字符串里
            txt = ""

            '''
            # 单独的字符变量
            txt_one = ""
            # 原始的灰度判断值
            txt_init = ""
            #用于检测，如果相邻像素相同，就填充空格

            # 遍历resize后的图像的各个像素，每一行以回车结尾
            print('宽高：',Width, Height)
            print('图片实际：',im._size)
            for i in range(Height):
                for j in range(Width):

                    if j == 0 :
                        txt_init = get_char(*im.getpixel((j,i)))
                        txt += txt_init
                        txt_one = txt_init
                    else:
                        txt_init = get_char(*im.getpixel((j, i)))
                        if txt_one == txt_init:
                            txt_one = txt_init
                            txt += ' '
                        else:
                            txt += txt_init
                            txt_one = txt_init
                txt += '\n'
            '''
            # 遍历resize后的图像的各个像素，每一行以回车结尾
            print('宽高：',Width, Height)
            print('图片实际：',im._size)
            for i in range(Height):
                for j in range(Width):
                    txt += get_char(*im.getpixel((j, i)))
                txt += '\n'





            # 字符画输出到文件
            # 直接使用with-open 即可创建文件，文件名为Output，用f来作为文件对象。
            with open(Output_file, 'w') as f:
                # 将txt字符串输入到文件中
                f.write(txt)
            print('OOOOOO__文件默认输出到py文件所在目录下%s，请使用记事本/写字板打开，字体格式设置为“宋体”' % Output_file)
        else:
            #如果不是jpg，png就跳过
            pass
        #到此，字符画就已经转换完毕。。。待下一步，将txt文件截图转gif




#预览及截图拼接函数
def ScreenShot_and_gif_create(user_input_file_dir):
    # 预览gif
    print('！----开始对字符画文件进行截图。。。因为是直接截取整个屏幕，所以建议将命令行窗口最大化 ')
    ScreenShot_and_gif_create = input('————》》》是否已经准备就绪，开始截图?（输入任意字符表示开始，直接回车则放弃）：')
    if ScreenShot_and_gif_create:
        #txt_name,读取的txt文件名称全部存进这个列表
        txt_name_list = []

        #txt文件遍历路径
        image_bianli_dir = user_input_file_dir + '\\' + _02_TXT_zifuhua_path
        os_dir_list_3 = os.listdir(image_bianli_dir)

        #遍历文件夹下所有文件列表，将txt文件名称存进txt_name_list
        for files in os_dir_list_3:
            houzhui = os.path.splitext(files)[-1][1:]
            if houzhui == 'txt':
                txt_name_list.append(files)
            else:
                pass

        #需要输出的字符画的字符串文本，全部存进这个列表
        txt_wenben_list = []
        #截图文件列表：用来把一张张截图整理起来，后面拼成GIF
        ScreenShot_file_list =[]

        #截图保存路径
        ScreenShot_dir = user_input_file_dir +'\\' + _03_PNG_jietu_path

        # 创建文件夹
        dir_creat(ScreenShot_dir)

        #遍历文件名list，将txt，文本内容存进txt_wenben_list
        for files in txt_name_list:
            files_name = str(image_bianli_dir) + '\\' + str(files)
            #逐个打开文本文件
            with open(files_name) as f:
                txt2 = f.read()
                txt_wenben_list.append(txt2)
                #第一边，显示字符画，是为了截图
                os.system("cls")
                print(txt2)
                # 延时
                time.sleep(0.1)

                #截图文件名定义
                ScreenShot_file = ScreenShot_dir +'\\'+ str(files) +'_ScreenShot.png'

                #这里是截屏函数，是截全屏幕的
                #截屏前需要确认目录存在。
                im = ImageGrab.grab()
                im.save(ScreenShot_file)
                #收集截图文件
                #图片文件是numeric文件，不是标准的数据类型，这里需要用imageio.imread(图片名/路径)才能加进列表
                ScreenShot_file_list.append(imageio.imread(ScreenShot_file))

                print('OOOOOO__截图保存到文件：%s'%ScreenShot_file)

        #生成GIF
        gif_output_dir = user_input_file_dir+'\\'+_00_GIF_OutPut_path
        #创建文件夹
        dir_creat(gif_output_dir)
        print('|||======图片合并中======')
        #imageio.mimsave()是专门存储GIF的函数，不能用于存储别的
        imageio.mimsave((gif_output_dir+ '\\' +'output.gif'),ScreenShot_file_list,'GIF',duration=0.1)
        print('!!!------GIF转换完成：......')

        '''
        #命令行死循环预览动态字符画
        #尽可能将死循环的工作内容，弄得最少，显示出来的结果会要好看很多。
        while True:
            # os.system('')python直接在命令行执行括号中的cmd命令
            #os.system("cls")
            for txt2 in txt_wenben_list:
                os.system("cls")
                #print('===========只有命令行执行才会定时清空显示，按ctrl+c中断循环============')
                print(txt2)

                #延时
                time.sleep(0.1)
        '''

    else:
        #输入回车则跳过
        pass








'''
================================================================================================
================================================================================================
主函数：
    路径的输入
    高度宽度的设定    
    调用wenjianbinali函数，将图片处理成txt文档
    调用ScreenShot_and_gif_create函数，将txt文本读取出来，在命令行显示
（完成对异常的判断，给出提示）
'''
#表示如果 本.py文件 被当作 python 模块 被import 的时候，这部分代码不会被执行，要不要这个其实无所谓。
if __name__ == '__main__':

    #os.remove()只能用于空文件夹的删除，要把目录中的文件一起删除的化，需要想其他办法，有点麻烦

    try:
        #获取操作文件夹名称：user_input_file_dir  字符串（用户输入or系统默认）
        #获取文件夹中文件信息：os_dir_list 列表list（需import os库）
        #获取用户设置的高宽：user_input_wh 字符串（用户输入or系统默认）

        user_input_file_dir = input('————》》》输入文件夹名称（若使用“MY_PATH”文件夹，则可以按回车跳过）：')
        #如果用户选择了跳过，则操作默认路径
        if (user_input_file_dir == None)or(user_input_file_dir == ''):
            dir_creat(MY_PATH)
            user_input_file_dir = MY_PATH
        print ('！----已输入文件夹:“ %s ”进入下一步...'%user_input_file_dir)

        '''
        #os.walk 可以获取指定目录下的文件及文件夹情况，并进入子目录，显示子目录情况
        os_walk = os.walk(user_input_file_dir)
        for files in os_walk:
            print (str(files))
        '''
        #os.listdir()函数只获取指定路径的文件夹和文件的名称,返回一个list给左边，不会再调的子一级
        os_dir_list = os.listdir(user_input_file_dir)
        user_input_wh = input("————》》》请输入 ‘宽度’和‘高度’ 以空格或小写的\",\"分隔（可以按回车跳过）：")



        wenjianbianli(user_input_file_dir,os_dir_list,user_input_wh)
        ScreenShot_and_gif_create(user_input_file_dir)

        print('请在.py文件目录下寻找: %s/%s' %(MY_PATH,_00_GIF_OutPut_path))

    except ValueError :
        print ('\nError!!!————图片尺寸设置错误,请重新输入')
#    except FileNotFoundError:
#        print ('\nError!!!————图片名称或路径不存在，请重新输入')
    except IndexError:
        print ('\nError!!!————图片尺寸设置错误,请重新输入')
    except OSError:
        print ('\nError!!!————OS错误，请检查文件夹或gif文件是否存在')
        



