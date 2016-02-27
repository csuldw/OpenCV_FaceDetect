#-*-coding:utf8-*-#
"""
Created on Sat Feb 27 12:51:35 2016
face detection
@author: liudiwei
"""

import os
import cv2
from PIL import Image, ImageDraw

"""
detectByClf()返回图像中所有检测区域的矩形坐标（矩形左上、右下顶点）
传入的是一张图片和一个分类器，这里使用haar特征的级联分类器，在haarcascades目录下
还有其他的训练好的xml文件可供选择。
提示：haarcascades目录下训练好的分类器必须以灰度图作为输入。
"""
#根据clf来检测
def detectByClf(image_name, clf):
    img = cv2.imread(image_name)
    smiles_cascade = cv2.CascadeClassifier(clf)
    #如果img维度为3，表示非灰度图，先转化为灰度图gray，如果不为3，即2，原图就是灰度图
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img 
    
    print "start detecting..."    
    zones = smiles_cascade.detectMultiScale(gray, 1.3, 5)
    result = []
    for (x, y, width, height) in zones:
        result.append((x, y, x+width, y+height))
    print "end detecting."    
    return result


#将检测到的区域保存到outpath目录中
def saveDetected(image_name, clf, outpath="./"):
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    detected = detectByClf(image_name, clf)
    if detected:
        print "start save detected..."    
        if outpath=="./":
            outdir = outpath + "/" + image_name.split('.')[0]+"_faces"
        else: 
            outdir = outpath
        if not os.path.exists(outdir):        
            os.mkdir(outdir)
        count = 0
        for (x1, y1, x2, y2) in detected:
            #将人脸保存在outdir目录下。
            file_name = os.path.join(outdir,str(count)+".jpg")
            #Image模块：Image.open获取图像句柄
            #crop剪切图像(剪切的区域就是detectFaces返回的坐标)，save保存。
            Image.open(image_name).crop((x1, y1, x2, y2)).save(file_name)
            count+=1
        print "end saved." 
    else:
        print "Not detected!"

#在原图像上绘制检测到的区域
def drawDetected(image_name, clf, outfile):
    detected = detectByClf(image_name, clf)
    if detected:
        print "start drawing detected..."
        img = Image.open(image_name)
        draw_instance = ImageDraw.Draw(img)
        for (x1, y1, x2, y2) in detected:
            draw_instance.rectangle((x1, y1, x2, y2), outline=(255, 0, 0))
        img.save(outfile)
        print "end drawing."   
    else:
        print "Not detected!"


def main():
    #CentOS系统clf的路径在/usr/share/OpenCV/haarcascades/下
    #这里我将其拷贝到本目录
    clf_face = "haarcascades/haarcascade_frontalface_default.xml" #face
    clf_mouth = "haarcascades/haarcascade_mcs_mouth.xml" #mouth
    #clf_eye = "haarcascades/haarcascade_eye.xml" #eye
    #clf_smile = "haarcascades/haarcascade_smile.xml" #smile
    
    picture = "group.jpg" #输入图像
    pic_front = "draw_" + picture.split(".")[0]
    outface = pic_front + "_face.jpg"
    outmouth = pic_front + "_mouth.jpg"
    #outeye = pic_front + "_eye.jpg"
    #outsmile = pic_front + "_smile.jpg"
    
    #开始检测并绘制检测区域
    drawDetected(picture, clf_face, outface)
    drawDetected(picture, clf_mouth, outmouth)
    #drawDetected(picture,  clf_eye, outeye)
    #drawDetected(picture, clf_smile, outsmile) 
    #保存检测到的脸部
    saveDetected(picture, clf_face)

if __name__ == '__main__':
    main()
    
