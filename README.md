# Fake-screenshots-of-wechat
朋友圈截图生成器

## 说明

不用转发也可以得到朋友圈截图

## 使用

首先，将head.jpg更换为自己的微信头像，name.txt的内容修改成自己的微信昵称

默认情况下无需改动config.txt参数即可正常使用，默认小米手机MIUI12界面截图

也可以将自己手机截图替换至screen.jpg，处理成原来screen.jpg的样子即可；之后对config.txt的参数进行修改，重新定位不同元素的位置即可生成不同机型的截图

## config含义及默认值

1.title_size:38;				  //文章题目字号

2.title_position:358,370;         //文章题目所在位置（单位为坐标，左上为坐标原点，下同）

3.time_size:35;                   //状态栏时间字号

4.time_position:64,29;            //状态栏时间位置

5.time_out_size:32;               //朋友圈发送时间字号

6.time_out_position:256,550;      //朋友圈发送时间位置

7.name_size:46;                   //昵称字号

8.name_position:183,248;          //昵称位置

9.face_size:136,136;              //文章封面大小

10.face_position:199,353;         //文章封面位置

11.head_size:125,125;             //头像大小

12.head_position:40, 247;         //头像位置
