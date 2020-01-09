#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import time
import sys, os
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from cv2 import *
# from main_thread_1 import objrThread
from main_thread import objrThread
from PyQt5.QtWidgets import QMainWindow



similar_char = \
	{"A":["A","4"], "B":["B","8"], "C":["C","G","6"], "D":["D","0","Q"],
	"E":["E"], "F":["F"], "G":["C","G","6"], "H":["M","N","W","H"],
	"I":[],    "J":["J"], "K":["K"],     "L":["L"],
	"M":["M","N","W","H"], "N":["M","N","W","H"],
	"O":[],    "P":["P"], "Q":["D","0","Q"], "R":["R"],
	"S":["S"], "T":["T"], "U":["U"],     "V":["V"],
	"W":["M","N","W","H"], "X":["X"], "Y":["Y"], "Z":["Z"],
	"0":["D","0","Q"], "1":["1","7"], "2":["2"], "3":["3"],
	"4":["A","4"], "5":["5"], "6":["C","G","6"], "7":["1","7"],
	"8":["B","8"], "9":["9"]}


class Ui_MainWindow(object):
	signal = pyqtSignal(np.ndarray)
	signal_finish = pyqtSignal()
	STATUS_INIT = 0
	STATUS_PLAYING = 1
	STATUS_PAUSE = 2
	
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		# MainWindow.setFixedSize(835, 498)
		MainWindow.setFixedSize(950, 900)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		font_13 = QtGui.QFont()
		font_13.setPointSize(10)
		font_14 = QtGui.QFont()
		font_14.setPointSize(12)
		# QGroupBox 1 -- VideoView
		self.VideoView = QtWidgets.QGroupBox(self.centralwidget)
		# self.VideoView.setGeometry(QtCore.QRect(20, 113, 586, 340))
		self.VideoView.setGeometry(QtCore.QRect(20, 113, 900, 720))
		self.VideoView.setObjectName("VideoViewBox")
		self.VideoView.setFont(font_14)
		# QLabel 1 -- Video
		self.widget_video = QtWidgets.QLabel(self.VideoView)
		# self.widget_video.setGeometry(QtCore.QRect(0, 30, 300,586))
		self.widget_video.setGeometry(QtCore.QRect(10, 30, 890, 670))
		self.widget_video.setObjectName("widget_video")
		self.widget_video.setFont(font_13)
		self.widget_video.setAlignment(QtCore.Qt.AlignCenter)
		# # QGroupBox 2 -- PlatesView
		# self.PlatesResultView = QtWidgets.QGroupBox(self.centralwidget)
		# # self.PlatesResultView.setGeometry(QtCore.QRect(620, 113, 201, 161))
		# self.PlatesResultView.setGeometry(QtCore.QRect(950, 113, 201, 350))  #(X,Y,W,H)
		# self.PlatesResultView.setObjectName("PlatesViewBox")
		# self.PlatesResultView.setFont(font_14)
		# # QListWidget 1 -- PlateTimeRecord
		# self.PlateTimeRecord = QListWidget(self.PlatesResultView)
		# # self.PlateTimeRecord.setGeometry(QtCore.QRect(15, 51, 171, 94))
		# self.PlateTimeRecord.setGeometry(QtCore.QRect(15, 51, 171, 270))
		# self.PlateTimeRecord.setObjectName("PlateTimeRecordLabel")
		# self.PlateTimeRecord.clicked.connect(self.click_plate)
		# # QLabel 2 -- TipPlateInfo
		# self.PlateInfo = QtWidgets.QLabel(self.PlatesResultView)
		# self.PlateInfo.setGeometry(QtCore.QRect(15, 30, 171, 16))
		# self.PlateInfo.setObjectName("PlateInfo")
		# self.PlateInfo.setFont(font_13)
		# self.PlateInfo.setStyleSheet("color:grey")
		# # QGroupBox 3 -- PedesView
		# self.PersonResultView = QtWidgets.QGroupBox(self.centralwidget)
		# # self.PersonResultView.setGeometry(QtCore.QRect(620, 293, 201, 161))
		# self.PersonResultView.setGeometry(QtCore.QRect(950, 480, 201, 350))
		# self.PersonResultView.setObjectName("PedesViewBox")
		# self.PersonResultView.setFont(font_14)
		# # QListWidget 2 -- PersonTimeRecord
		# self.PersonTimeRecord = QListWidget(self.PersonResultView)
		# # self.PersonTimeRecord.setGeometry(QtCore.QRect(15, 51, 171, 94))
		# self.PersonTimeRecord.setGeometry(QtCore.QRect(15, 51, 171, 270))
		# self.PersonTimeRecord.setObjectName("PersonTimeRecordLabel")
		# self.PersonTimeRecord.clicked.connect(self.click_person)
		# # QLabel 3 -- TipPersonInfo
		# self.PersonInfo = QtWidgets.QLabel(self.PersonResultView)
		# self.PersonInfo.setGeometry(QtCore.QRect(15, 30, 171, 16))
		# self.PersonInfo.setObjectName("PersonInfo")
		# self.PersonInfo.setFont(font_13)
		# self.PersonInfo.setStyleSheet("color:grey")
		# QGroupBox 4 -- FileSelection
		self.FileSelectView = QtWidgets.QGroupBox(self.centralwidget)
		self.FileSelectView.setGeometry(QtCore.QRect(20, 10, 900, 80))
		self.FileSelectView.setObjectName("FileSelectView")
		self.FileSelectView.setFont(font_14)
		# LineEdit 1 -- FilePathEdit
		self.FilePathEdit = QtWidgets.QLineEdit(self.FileSelectView)
		self.FilePathEdit.setGeometry(QtCore.QRect(100, 38, 491, 21))
		self.FilePathEdit.setObjectName("FilePathEdit")
		self.path = ""
		self.FilePathEdit.setText(self.path)
		self.FilePathEdit.setFont(font_13)
		self.FilePathEdit.setStyleSheet("color:grey")
		# QLabel 4 -- PathSelectTitle
		self.PathSelectTitle = QtWidgets.QLabel(self.FileSelectView)
		self.PathSelectTitle.setGeometry(QtCore.QRect(30, 40, 60, 16))
		self.PathSelectTitle.setObjectName("PathSelectTitle")
		self.PathSelectTitle.setAlignment(QtCore.Qt.AlignCenter)
		self.PathSelectTitle.setFont(font_13)
		# PushButton 1 -- select
		self.SelectBT = QtWidgets.QPushButton(self.FileSelectView)
		self.SelectBT.setGeometry(QtCore.QRect(610, 34, 50, 32))
		self.SelectBT.setObjectName("SelectBT")
		self.SelectBT.setFont(font_13)
		self.SelectBT.clicked.connect(self.change_path)
		# PushButton 2 -- start
		self.StartBT = QtWidgets.QPushButton(self.FileSelectView)
		self.StartBT.setGeometry(QtCore.QRect(670, 34, 50, 32))
		self.StartBT.setObjectName("StartBT")
		self.StartBT.setFont(font_13)
		self.StartBT.clicked.connect(self.start_backEnd)
		# PushButton 3 -- pause
		self.QuitBT = QtWidgets.QPushButton(self.FileSelectView)
		self.QuitBT.setGeometry(QtCore.QRect(730, 34, 50, 32))
		self.QuitBT.setObjectName("QuitBT")
		self.QuitBT.setFont(font_13)
		self.QuitBT.clicked.connect(self.quit_backend)

		self.WaitBT = QtWidgets.QPushButton(self.FileSelectView)
		self.WaitBT.setGeometry(QtCore.QRect(790, 34, 50, 32))
		self.WaitBT.setObjectName("WaitBT")
		self.WaitBT.setFont(font_13)
		self.WaitBT.clicked.connect(self.wait_backend)

		self.breakPauseBT = QtWidgets.QPushButton(self.FileSelectView)
		self.breakPauseBT.setGeometry(QtCore.QRect(840, 34, 50, 32))
		self.breakPauseBT.setObjectName("breakPauseBTBT")
		self.breakPauseBT.setFont(font_13)
		self.breakPauseBT.clicked.connect(self.breakPause_backend)



		# QLabel 5 -- time info
		self.timeCost = QtWidgets.QLabel(self.centralwidget)
		self.timeCost.setGeometry(QtCore.QRect(20, 850, 821, 32))
		self.timeCost.setObjectName("timeCost")
		self.timeCost.setAlignment(QtCore.Qt.AlignLeft)
		self.timeCost.setFont(font_13)
		
		MainWindow.setCentralWidget(self.centralwidget)
		
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		
		# number of characters per line in QMessagebox
		self.width = 15
		# Compare with last cmp_num records in plate_dict_bynow to
		# see if there is any similar plate appears before.
		self.cmp_num = 5
		# Time space for every two records.
		self.time_space = 1.0 # second
		# True if play the first video
		self.firstPlay = True
		# play status
		self.isPlaying = self.STATUS_INIT
		# signals
		self.signal.connect(self.refresh_video_frame)
		self.signal_finish.connect(self.finish_last_video)

		self.objrThread = objrThread(self.path, self.signal, self.signal_finish)
		self.objrThread.start()

	def retranslateUi(self, MainWindow):
		"""
		:param MainWindow: MainWindow
		:return: noun
		Set the titles, names of the main window
		"""
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Defect Detector demo"))
		
		self.VideoView.setTitle(_translate("MainWindow", "检测结果"))
		self.widget_video.setText(_translate("MainWindow", "尚未开始任务"))
		# self.PlatesResultView.setTitle(_translate("MainWindow", "检测结果"))
		# self.PersonResultView.setTitle(_translate("MainWindow", "检测结果"))
		self.FileSelectView.setTitle(_translate("MainWindow", "选择文件路径"))
		self.PathSelectTitle.setText(_translate("MainWindow", "文件路径:"))
		self.FilePathEdit.setText(_translate("MainWindow", "请选择文件路径"))
		self.SelectBT.setText(_translate("MainWindow", "选择"))
		self.StartBT.setText(_translate("MainWindow", "开始"))
		self.QuitBT.setText(_translate("MainWindow", "停止"))
		self.WaitBT.setText(_translate("MainWindow", "暂停"))
		self.breakPauseBT.setText(_translate("MainWindow", "继续"))
		# self.PlateInfo.setText(_translate("MainWindow", "点击下方车牌获取时间信息"))
		# self.PersonInfo.setText(_translate("MainWindow", "点击下方人名获取时间信息"))
		self.timeCost.setText(_translate("MainWindow", "* 耗时信息将显示在这里"))
	
	def refresh_video_frame(self, reframe):
		"""
		:param reframe: current frame
		:param plate_time_prob_dict: a dict, plate is the key,
		        (time, prob) is the corresponding value
		:return: noun
		Set the current video pixmap, record the time of people and plates
		appear if it is n sec later than the time it appears last time, and
		solve the problem that one plate might be recognized as several
		different results.
		Set the current time information.
		"""
		# # 目前帧数
		# self.index += 1
		# # 到目前这一帧为止的所有值做平均
		# if avg_det_time != 0.0:
		# 	self.avg_det_time = (self.avg_det_time*(self.index-1)+avg_det_time)/self.index
		# if avg_plate_det_time != 0.0:
		# 	self.avg_plate_det_time = (self.avg_plate_det_time*(self.index-1)+avg_plate_det_time)/self.index
		# if avg_plate_reg_time != 0.0:
		# 	self.avg_plate_reg_time = (self.avg_plate_reg_time*(self.index-1)+avg_plate_reg_time)/self.index
		# if avg_person_reg_time != 0.0:
		# 	self.avg_person_reg_time = (self.avg_person_reg_time*(self.index-1)+avg_person_reg_time)/self.index
		# # 模块处理时间统计
		# t1 = "%.5f" % self.avg_det_time
		# t2 = "%.5f" % self.avg_plate_det_time
		# t3 = "%.5f" % self.avg_plate_reg_time
		# t4 = "%.5f" % self.avg_person_reg_time
		# # 显示模块处理时间
		# self.timeCost.setText("* avg_det_time : "+t1+"s, "
		# 					  "avg_plate_det_time : "+t2+"s, "
		# 					  "avg_plate_reg_time : "+t3+"s, "
		# 					  "avg_person_reg_time : "+t4+"s")
		# Set the video frame
		# print('uiupdate')
		height, width = reframe.shape[:2]
		rgb = cvtColor(reframe, COLOR_BGR2RGB)
		curr_image = QImage(rgb.flatten(), width, height, width*3,
							QImage.Format_RGB888)
		# curr_image_scaled = curr_image.scaled(300,570,  QtCore.Qt.IgnoreAspectRatio,
		# 									  QtCore.Qt.SmoothTransformation)
		curr_image_scaled = curr_image.scaled(870, 660, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
		curr_pixmap = QPixmap.fromImage(curr_image_scaled)
		self.widget_video.setPixmap(curr_pixmap)
		# update the database
		# frameTime = 0.0
		# # update the plate database
		# print("2222")
		# for (k, tuple) in plate_time_prob_dict.items():
		# 	frameTime = tuple[0]
		# 	prob = tuple[1]
		# 	prob = float(prob[0,0])
		#
		# 	if k not in self.plate_count_prob_bynow.keys():
		# 		# print("检测到COUNT字典中没有的车牌"+k)
		# 		print("111")
		# 		self.plate_count_prob_bynow[k] = (1, prob)
		# 		self.update_plate_database(k, frameTime, prob)
		# 		print("111******")
		# 	else:
		# 		# print("检测到COUNT字典存在的车牌"+k)
		# 		count, old_prob = self.plate_count_prob_bynow[k]
		# 		count += 1
		# 		if old_prob >= prob:
		# 			prob = old_prob
		# 		self.plate_count_prob_bynow[k] = (count, prob)
		# 		print("55555")
		# 		if k in self.plate_dict_bynow.keys():
		# 			self.add_time_record(k, frameTime, self.plate_dict_bynow)
		# 			print("999999")
		# 		else:
		# 			print("66666")
		# 			self.update_plate_database(k, frameTime, prob)
		# 		print("55555*********")
		# print("333")
		# # update the people database
		# for (id, tuple) in person_name_prob_dict.items():
		# 	name = tuple[0]
		# 	# prob = tuple[1]
		# 	if name != "NO PERSON":
		# 		if name not in self.person_dict_bynow.keys():
		# 			# print("检测到TIME字典中没有的人名" + name)
		# 			self.create_new_record(name, frameTime, self.PersonTimeRecord,
		# 								   self.person_list, self.person_dict_bynow)
		# 		else:
		# 			# print("检测到TIME字典中存在的人名" + name)
		# 			self.add_time_record(name, frameTime, self.person_dict_bynow)

	def create_new_record(self, k, time, widget, list, time_dict):
		"""
		:param k: plate/person String
		:param time: a new time record
		:return: noun
		obj k never appears before, and we believe this is
		a new one, so we create a new record in both
		QListwidget and time_dict.
		"""
		print("this is create new record")
		widget.addItem(str(k))
		list.append(str(k))
		records_k = []
		records_k.append("%.2f" % time)
		time_dict[k] = records_k

	def add_time_record(self, k, time, time_dict):
		"""
		:param k: plate String
		:param time: a new time record
		:return: noun
		Simply update the time record for plate k.
		"""
		records_k = time_dict[k]
		lastRecord_k = records_k[-1]
		print("add time")
		if time - float(lastRecord_k) >= self.time_space:
			records_k.append("%.2f" % time)
			time_dict[k] = records_k

	def replace_item_widget(self, old, new, widget, list, time_dict):
		"""
		:param old: old plate String
		:param new: new plate String
		:return: noun
		Replace the old plate with new plate in both
		plate_dict_bynow and QListwidget, and the new
		one will inherit all the time records of the old
		one.
		"""
		time_dict[new] = time_dict.pop(old)
		widget.removeItemWidget(
			widget.takeItem(
				list.index(old)))
		list.remove(old)
		widget.addItem(str(new))
		widget.scrollTo(len(widget.items())-1)
		list.append(str(new))

	def update_plate_database(self, k, time, prob):
		"""
		:param k: plate String
		:param time: a new time record
		:param prob: probability of plate k
		:return: noun
		When a new plate recognition result is obtained, make decision
		on how to update our database.
		"""
		curr_count = self.plate_count_prob_bynow[k][0]
		curr_prob = self.plate_count_prob_bynow[k][1]
		for data in [i for i in self.plate_dict_bynow.keys()][-self.cmp_num:]:
			data_count = self.plate_count_prob_bynow[data][0]
			data_prob = self.plate_count_prob_bynow[data][1]
			if self.same_plate(k, data):
				if curr_count < data_count:
					# print("当前车牌count小于字典中相似车牌的count")
					self.add_time_record(data, time, self.plate_dict_bynow)
				elif curr_count == data_count:
					# print("当前车牌count等于字典中相似车牌的count")
					if curr_prob >= data_prob:
						# print("当前车牌为真的可能性很大")
						self.replace_item_widget(data, k, self.PlateTimeRecord,
												 self.plate_list, self.plate_dict_bynow)
						self.add_time_record(k, time, self.plate_dict_bynow)
				else:
					# print("当前车牌count大于字典中相似车牌的count")
					self.replace_item_widget(data, k, self.PlateTimeRecord,
												 self.plate_list, self.plate_dict_bynow)
					self.add_time_record(k, time, self.plate_dict_bynow)
				# print("之前可能出现过类似车牌")
				# return
		self.create_new_record(k, time, self.PlateTimeRecord,
							   self.plate_list, self.plate_dict_bynow)
		# print("之前未出现过类似车牌")
		# return
	
	def change_path(self):
		"""
		:return: noun
		Change the file path
		"""
		_translate = QtCore.QCoreApplication.translate
		open = QFileDialog()
		# self.path = open.getExistingDirectory()
		self.path = open.getOpenFileName()
		if self.path[0] == "":
			self.FilePathEdit.setText(_translate("MainWindow", "请选择文件路径"))
		else:
			# self.FilePathEdit.setText(self.path)
			self.FilePathEdit.setText(self.path[0])

	def start_backEnd(self):
		"""
		:return: noun
		Start a new video, if the file path is not set, start a default video
		"""
		if self.isPlaying != self.STATUS_PLAYING:

			# self.PlateTimeRecord.clear()
			# self.PersonTimeRecord.clear()
			self.person_dict_bynow = dict()
			self.plate_dict_bynow = dict()
			self.plate_count_prob_bynow = dict()
			# self.person_count_prob_bynow = dict()
			self.plate_list = []
			self.person_list = []
			
			self.avg_det_time = 0.0
			self.avg_plate_det_time = 0.0
			self.avg_plate_reg_time = 0.0
			self.avg_person_reg_time = 0.0
			self.index = 0
			
			_translate = QtCore.QCoreApplication.translate
			if self.firstPlay == True:
				self.widget_video.setText(_translate
							("MainWindow", "开始检测...\n（首次加载时间较慢，请耐心等待。）"))
			else:
				self.widget_video.setText(_translate
										  ("MainWindow", "正在进行检测..."))


			if not self.path == "":
				if not self.path[0] =="":
					print('path{}'.format(self.path))
					# self.objrThread.setFilePath(self.path[0])
					self.objrThread.startCamera(self.path[0])
					self.firstPlay = False
					self.isPlaying = self.STATUS_PLAYING
			else:
				QMessageBox.information(self, "警告", "请选择文件。")

			# if self.path == "":
			# 	self.objrThread = objrThread( self.path[0], self.signal,self.signal_finish)
			# else:
			# 	self.objrThread = objrThread( self.path[0], self.signal,self.signal_finish)
			# 	# self.objrThread = objrThread(self.signal, self.path[0], self.signal_finish)
			# self.objrThread.start()
		else:
			QMessageBox.information(self, "警告", "正在检测！请先停止其他\n正在检测的任务。")
	
	def quit_backend(self):
		"""
		:return: noun
		Stop the backend thread
		"""
		# if self.isPlaying == self.STATUS_PLAYING:
		# 	self.isPlaying = self.STATUS_PAUSE
		# 	_translate = QtCore.QCoreApplication.translate
		# 	self.objrThread.stop()
		# 	self.widget_video.setText(_translate("MainWindow", "检测结束"))
		# 	QMessageBox.information(self, "提示", "检测结束。\n自动关闭。")
		# else:
		# 	return
		self.objrThread.stopCamera()
		self.firstPlay = False
		self.isPlaying = self.STATUS_INIT


	def wait_backend(self):
		self.objrThread.Pause()


	def breakPause_backend(self):
		self.objrThread.breakPause()

	def closeEvent(self, e):
		print("close.. main window")
		self.objrThread.stopMainThread()


	
	def click_plate(self):
		"""
		:return: noun
		Pop up a information window to show the time record of the
		current plate.
		"""
		item = self.PlateTimeRecord.currentItem().text()
		time_record = self.plate_dict_bynow[item]
		show_text = item + "出现的时间点为："
		for record in time_record:
			if record == time_record[-1]:
				show_text += "第" + record + "秒"
			else:
				show_text += "第" + record + "秒" + ", "
		show_text = self.form_text(show_text)
		
		QMessageBox.information(self, item, show_text)

	def click_person(self):
		"""
		:return: noun
		Pop up a information window to show the time record of
		the current person
		"""
		item = self.PersonTimeRecord.currentItem().text()
		time_record = self.person_dict_bynow[item]
		show_text = item + "出现的时间点为："
		for record in time_record:
			if record == time_record[-1]:
				show_text += "第" + record + "秒"
			else:
				show_text += "第" + record + "秒" + ", "
		show_text = self.form_text(show_text)
		QMessageBox.information(self, item, show_text)

	def form_text(self, text):
		"""
		:param text: text String
		:param width: an int number
		:return: new text String in width characters per line.
		Reform the input text.
		"""
		result = ""
		len_text = len(text)
		if text == "":
			return text
		elif len_text <= self.width:
			return text
		elif len_text > self.width:
			space_need = self.width - len_text%self.width
			text += " "*space_need
			for i in range(0,len_text,self.width):
				if i == self.width - 1:
					result += text[i:i+self.width]
				else:
					result += text[i:i + self.width] + "\n"
		return result

	def finish_last_video(self):
		"""
		:return: noun
		Set the play status to STATUS_PAUSE, and pop up an
		information window to inform the end of the video.
		"""
		_translate = QtCore.QCoreApplication.translate
		# self.widget_video.setText(_translate("MainWindow", "检测结束"))
		self.isPlaying = self.STATUS_PAUSE
		QMessageBox.information(self, "提示", "检测结束。\n自动关闭。")

	def same_plate(self, plateA, plateB):
		"""
		:param plateA: plate String
		:param plateB: plate String
		:return: True if the two plates are largely possible to be
		the same one, and vice versa.
		"""
		len_plate = len(plateA)
		similar_num = 0
		for i in range(1,len_plate):
			if plateA[i] == plateB[i] or \
				similar_char[plateA[i]] == similar_char[plateB[i]]:
				similar_num += 1
		if similar_num == 6:
			return True


class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)



if __name__ == '__main__':
	#仅测试Ui_MainWindow
	# app = QApplication(sys.argv)
	# MainWindow = QMainWindow()
	# ui = Ui_MainWindow(MainWindow)
	# ui.setupUi(MainWindow)
	# MainWindow.show()
	# sys.exit(app.exec_())

	app = QtWidgets.QApplication(sys.argv)
	mainForm = MainWindow()
	mainForm.show()
	sys.exit(app.exec_())

