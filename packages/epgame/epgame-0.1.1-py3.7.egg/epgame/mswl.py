from pygame.locals import *
import pygame
import sys
import time
import random
import math
import datetime
########################
# author:   bbks/康帅  #
# version：	0.4.0      #
# update:   2019/7/30  #
########################

pygame.init()

deepPink = (255, 20, 147)
violet = (238, 130, 238)
purple = (128, 0, 128)
skyBlue = (135, 206, 235)
yellow = (255, 255, 0)
gold = (255, 215, 0)
orange = (255, 165, 0)
tomato = (255, 99, 71)
snow = (255, 250, 250)
silver = (192, 192, 192)
brown = (165, 42, 42)
white = (255, 255, 255)
pink = (255, 192, 203)
black = (0, 0, 0)
blue = (0, 0, 255)
grey = (128, 128, 128)
red = (255, 0, 0)
green = (0, 128, 0)
darkGreen = (0, 100, 0)
################################################
# 自定义事件
userEvent =  pygame.USEREVENT

################################################
# 获取当前秒数
def get_now_second():
	return datetime.datetime.now().second

################################################
# 键盘事件
# 键盘按下事件
def key_down(a):
	return a.type == KEYDOWN

# 键盘弹起事件
def key_up(a):
	return a.type == KEYUP

################################################
# 鼠标事件
# 鼠标点击事件
def mouse_down(a):
	return a.type == MOUSEBUTTONDOWN

# 鼠标点击事件
def mouse_up(a):
	return a.type == MOUSEBUTTONUP

# 鼠标移动事件
def mouse_move(a):
	return a.type == MOUSEMOTION

################################################
# 设置间隔时间
def setInterval(a,b):
	return pygame.time.set_timer(a,b)

################################################
# 返回事件类型
def event_type(a,b):
	return a.type == b

################################################
# 关闭窗口
def window_close(a):
	if a.type == QUIT:
		pygame.quit()
		sys.exit()

################################################
# 获取事件
def get_event():
	return pygame.event.get()

################################################
# 更新屏幕
def update_screen():
	return pygame.display.update()

################################################
# 设置屏幕大小
def set_screen(a,b):
	return pygame.display.set_mode((a, b),0,32)  # 设置窗口大小

################################################
# 图片碰撞
def collide_img(a,b):
	return pygame.sprite.collide_rect(a,b)

################################################
# 方行方行碰撞
def collide_shape(a, b):
	x1 = a.x
	y1 = a.y
	w1 = a.width
	h1 = a.height
	x2 = b.x
	y2 = b.y
	w2 = b.width
	h2 = b.height

	lx = max(x1 + w1 - x2, x2 + w2 - x1)
	ly = max(y1 + h1 - y2, y2 + h2 - y1)
	if lx < w1 + w2 and ly < h1 + h2:
		if w1 + w2 - lx < h1 + h2 - ly:
			return True
		else:
			return True

################################################
# 圆形和方形碰撞
def c_collide_r(a,b):
	DeltaX = a.x - max(b.x, min(a.x, b.x + b.width))
	DeltaY = a.y - max(b.y, min(a.y, b.y + b.height))
	return (DeltaX * DeltaX + DeltaY * DeltaY) <= (a.r * a.r)

################################################
# 清除屏幕
def clear(a):
	a.fill(black)

################################################
# 画出坐标
def drawXY():
	pygame.display.set_caption('x,y:'+str(pygame.mouse.get_pos()))

################################################
# 画出方格
def drawGrid(a, w, h, size, co=darkGreen):
	# 画出底线格子
	for x in range(0, w+size, size):  # draw vertical lines
		x_line = Line(x, 0, x, h, co)
		x_line.draw(a)
	for y in range(0, h+size, size):  # draw horizontal lines
		y_line = Line(0, y, w, y, co)
		y_line.draw(a)

################################################
# 播放声音
def playSound(a):
	pygame.mixer.init()
	pygame.mixer.music.load(a)
	pygame.mixer.music.play()

################################################
# 图片对象
class Image(pygame.sprite.Sprite):
	def __init__(self, img, x, y, w, h, index = 0, down=False, up=False):
		pygame.sprite.Sprite.__init__(self)
		self.src = img
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.flip_x = False
		self.flip_y = False
		self.degree = 0
		self.speedx = 0
		self.speedy = 0
		self.isFeed = 0
		self.isExited = False
		self.isRotated = True
		self.image = pygame.image.load(self.src).convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
		self.rect = self.image.get_rect(topleft=(self.x, self.y))
		self.state = 0
		self.index = index
		self.down = down
		self.up = up

	def isClicked(self, a, b=0, c=0, d=0, e=0):
		if a.type == MOUSEBUTTONDOWN:
			x, y = a.pos
			pressed_array = pygame.mouse.get_pressed()
			if self.rect.left + b <= x <= self.rect.right + c and \
				self.rect.top + d <= y <= self.rect.bottom + e and pressed_array[0]:
				return True

	def flip(self, a=False, b=False):
		self.image = pygame.transform.flip(self.image, a, b)

	def rotate(self, a):
		self.image = pygame.image.load(self.src).convert_alpha()
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
		self.image = pygame.transform.rotate(self.image, a)

	def scale(self, a, b):
		self.image = pygame.image.load(self.src).convert_alpha()
		self.image = pygame.transform.scale(self.image, (int(self.width*a), int(self.height*b)))

	def draw(self, a):
		a.blit(self.image, self.rect)

	def drawRotate(self, a):
		w = self.image.get_rect().width
		h = self.image.get_rect().height
		a.blit(self.image, (self.rect.x - w//2, self.rect.y - h//2))

################################################
# 文本对象
class Text(object):
	def __init__(self, text, x, y, size, co=(255, 255, 255), style=None):
		self.x = x
		self.y = y
		self.color = co
		self.src = text
		self.style = style
		self.size = size
		self.font = None
		self.text = None
		self.rect = None

	def draw(self, a):
		self.font = pygame.font.Font(self.style, self.size)
		self.text = self.font.render(self.src, True, self.color)
		self.rect = self.text.get_rect(topleft=(self.x, self.y))
		a.blit(self.text, self.rect)

	def isClicked(self, a):
		if a.type == MOUSEBUTTONDOWN:
			x, y = a.pos
			pressed_array = pygame.mouse.get_pressed()
			if self.x <= x <= self.x + self.size/2*len(self.src) and \
				self.y <= y <= self.y + self.size/2 and pressed_array[0]:
				return True

################################################
# 长方形
class Rectangle(object):
	def __init__(self, x=100, y=100, w=50, h=50, co=blue, a=0):
		self.fillStyle = co
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.lineWidth = a
		self.index = 0
		self.state = 0

	def draw(self, a):
		pygame.draw.rect(a, self.fillStyle, Rect((self.x, self.y), (self.width, self.height)), self.lineWidth)

	def isClicked(self, a):
		if a.type == MOUSEBUTTONDOWN:
			x, y = a.pos
			pressed_array = pygame.mouse.get_pressed()
			if self.x <= x <= self.x + self.width and \
				self.y <= y <= self.y + self.height and pressed_array[0]:
				return True

################################################
# 圆形
class Circle(object):
	def __init__(self, x, y, r, co=blue):
		self.x = x
		self.y = y
		self.r = r
		self.fillStyle = co

	def draw(self, a):
		pygame.draw.circle(a, self.fillStyle, (self.x, self.y), self.r)

	def isClicked(self, a):
		if a.type == MOUSEBUTTONDOWN:
			x, y = a.pos
			pressed_array = pygame.mouse.get_pressed()
			if self.x - self.r <= x <= self.x + self.r and \
				self.y - self.r <= y <= self.y + self.r and pressed_array[0]:
				return True
	def dropOn(self,b):
		if c_collide_r(self,b) and self.y<b.y:
			self.state = b.index
			boxMoveX = 0

			# if self.fillStyle != b.fillStyle:
			# 	if self.x>(b.x+b.width/2-5) and self.x<(b.x+b.width/2+5):
			# 		pass
			# 	else:
			# 		pass

			self.fillStyle = b.fillStyle

################################################
# 三角形
class Triangle(object):
	def __init__(self, x1, y1, x2, y2, x3, y3, co=blue, a=0):
		self.fillStyle = co
		self.lineWidth = a
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.x3 = x3
		self.y3 = y3
		self.pointList = ((x1, y1), (x2, y2), (x3, y3))

	def draw(self, a):
		pygame.draw.polygon(a, self.fillStyle, self.pointList, self.lineWidth)

################################################
# 多边形
class Polygon(object):
	def __init__(self, pl, co=blue, a=0):
		self.fillStyle = co
		self.lineWidth = a
		# self.x1 = x1
		# self.y1 = y1
		# self.x2 = x2
		# self.y2 = y2
		# self.x3 = x3
		# self.y3 = y3
		self.pointList = pl

	def draw(self, a):
		pygame.draw.polygon(a, self.fillStyle, self.pointList, self.lineWidth)

################################################
# 线
class Line(object):
	def __init__(self, x1, y1, x2, y2, co=blue, a=1):
		self.color = co
		self.lineWidth = a
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

	def draw(self, a):
		pygame.draw.line(a, self.color, (self.x1, self.y1), (self.x2, self.y2), self.lineWidth)

################################################
# 椭圆形
class Ellipse(object):
	def __init__(self, x, y, w, h, co=blue, a=0):
		self.fillStyle = co
		self.lineWidth = a
		self.x = x
		self.y = y
		self.width = w
		self.height = h

	def draw(self, a):
		pygame.draw.ellipse(a, self.fillStyle, (self.x, self.y, self.width, self.height), self.lineWidth)

	def isClicked(self, a):
		if a.type == MOUSEBUTTONDOWN:
			x, y = a.pos
			pressed_array = pygame.mouse.get_pressed()
			if self.x <= x <= self.x + self.width and \
				self.y <= y <= self.y + self.height and pressed_array[0]:
				return True
def set_interval(a,b):
	return pygame.time.set_timer(a,b)
# class Button(object):
# 	def __init__(self, name, col, position, size):
# 		self.name = name
# 		self.col = col
# 		self.size = size
# 		self.position = position
# 	def isOver(self):
# 		point_x, point_y = pygame.mouse.get_pos()
# 		x, y = self. position
# 		w, h = self.size
# 		in_x = x - w < point_x < x
# 		in_y = y - h < point_y < y
# 		return in_x and in_y
# 	def render(self, a):
# 		w, h = self.size
# 		x, y = self.position
# 		pygame.draw.rect(a, self.col, ((x - w, y - h), (w, h)), 0)
# 		num_font = pygame.font.Font(None, h - 1)
# 		font_test = num_font.render(self.name, True, (255, 255, 255))
# 		fsetting = font_test.get_rect()
# 		fsetting.center = (x - w / 2, y - h / 2)
# 		a.blit(font_test, fsetting)
# class Sprite(pygame.sprite.Sprite):
# 	def __init__(self, filename, x, y, width, height, columns):
# 		pygame.sprite.Sprite.__init__(self)
# 		self.image = None
# 		self.frame = 0
# 		self.old_frame = -1
# 		self.frame_width = 1
# 		self.frame_height = 1
# 		self.first_frame = 0
# 		self.last_frame = 0
# 		self.columns = 1
# 		self.last_time = 0
# 		self.master_image = pygame.image.load(filename).convert_alpha()
# 		self.frame_width = width
# 		self.frame_height = height
# 		self.rect = 0, 0, width, height
# 		self.columns = columns
# 		self.rect = self.master_image.get_rect(topleft=(x, y))
# 		self.last_frame = (self.rect.width // width) * (self.rect.height // height) - 1
# 	def update(self, current_time, rate=60):
# 		if current_time > self.last_time + rate:
# 			self.frame += 1
# 			if self.frame > self.last_frame:
# 				self.frame = self.first_frame
# 			self.last_time = current_time
# 		if self.frame != self.old_frame:
# 			frame_x = (self.frame % self.columns) * self.frame_width
# 			frame_y = (self.frame // self.columns) * self.frame_height
# 			rect = (frame_x, frame_y, self.frame_width, self.frame_height)
# 			self.image = self.master_image.subsurface(rect)
# 			self.old_frame = self.frame
# 	def draw(self, a):
# 		a.blit(self.image, self.rect)
