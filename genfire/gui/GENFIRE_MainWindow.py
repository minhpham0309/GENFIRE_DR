# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\minhrose\Desktop\GENFIRE-Python-master\genfire\gui\GENFIRE_MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GENFIRE_MainWindow(object):
    def setupUi(self, GENFIRE_MainWindow):
        GENFIRE_MainWindow.setObjectName("GENFIRE_MainWindow")
        GENFIRE_MainWindow.setEnabled(True)
        GENFIRE_MainWindow.resize(1093, 876)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GENFIRE_MainWindow.sizePolicy().hasHeightForWidth())
        GENFIRE_MainWindow.setSizePolicy(sizePolicy)
        self.centralWidget = QtWidgets.QWidget(GENFIRE_MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.scrollArea = QtWidgets.QScrollArea(self.centralWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, -181, 1039, 1012))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.nameWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameWidget.sizePolicy().hasHeightForWidth())
        self.nameWidget.setSizePolicy(sizePolicy)
        self.nameWidget.setMinimumSize(QtCore.QSize(512, 93))
        self.nameWidget.setStyleSheet("background-image: url(:/GENFIRE.png)")
        self.nameWidget.setObjectName("nameWidget")
        self.horizontalLayout_3.addWidget(self.nameWidget)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_io = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.lineEdit_io.setObjectName("lineEdit_io")
        self.gridLayout.addWidget(self.lineEdit_io, 9, 2, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout.addWidget(self.line_4, 10, 0, 1, 3)
        self.lineEdit_pj = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.lineEdit_pj.setObjectName("lineEdit_pj")
        self.gridLayout.addWidget(self.lineEdit_pj, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 12, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 3)
        self.line_3 = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 7, 0, 1, 3)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 13, 2, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 5, 0, 1, 3)
        self.lineEdit_results = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.lineEdit_results.setObjectName("lineEdit_results")
        self.gridLayout.addWidget(self.lineEdit_results, 12, 2, 1, 1)
        self.btn_support = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.btn_support.setObjectName("btn_support")
        self.gridLayout.addWidget(self.btn_support, 3, 0, 1, 1)
        self.btn_angles = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.btn_angles.setObjectName("btn_angles")
        self.gridLayout.addWidget(self.btn_angles, 6, 0, 1, 1)
        self.checkBox_default_support = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_default_support.setObjectName("checkBox_default_support")
        self.gridLayout.addWidget(self.checkBox_default_support, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout.addLayout(self.horizontalLayout, 13, 0, 1, 1)
        self.lineEdit_support = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.lineEdit_support.setObjectName("lineEdit_support")
        self.gridLayout.addWidget(self.lineEdit_support, 3, 2, 1, 1)
        self.btn_io = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.btn_io.setObjectName("btn_io")
        self.gridLayout.addWidget(self.btn_io, 9, 0, 1, 1)
        self.checkBox_provide_io = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_provide_io.setObjectName("checkBox_provide_io")
        self.gridLayout.addWidget(self.checkBox_provide_io, 8, 0, 1, 1)
        self.lineEdit_angle = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.lineEdit_angle.setObjectName("lineEdit_angle")
        self.gridLayout.addWidget(self.lineEdit_angle, 6, 2, 1, 1)
        self.btn_projections = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.btn_projections.setObjectName("btn_projections")
        self.gridLayout.addWidget(self.btn_projections, 0, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_on = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_on.setObjectName("radioButton_on")
        self.verticalLayout.addWidget(self.radioButton_on)
        self.radioButton_off = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_off.setObjectName("radioButton_off")
        self.verticalLayout.addWidget(self.radioButton_off)
        self.radioButton_extension = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_extension.setObjectName("radioButton_extension")
        self.verticalLayout.addWidget(self.radioButton_extension)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_3 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_10.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_10.setSpacing(6)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.radioButton_ER = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_ER.setObjectName("radioButton_ER")
        self.verticalLayout_10.addWidget(self.radioButton_ER)
        self.radioButton_DR = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_DR.setObjectName("radioButton_DR")
        self.verticalLayout_10.addWidget(self.radioButton_DR)
        self.horizontalLayout_2.addWidget(self.groupBox_3)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBox_multiGridding = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_multiGridding.setChecked(True)
        self.checkBox_multiGridding.setObjectName("checkBox_multiGridding")
        self.gridLayout_2.addWidget(self.checkBox_multiGridding, 3, 0, 1, 2)
        self.line_6 = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridLayout_2.addWidget(self.line_6, 2, 3, 1, 1)
        self.checkBox_rfree = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_rfree.setObjectName("checkBox_rfree")
        self.gridLayout_2.addWidget(self.checkBox_rfree, 4, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.checkBox_resCircle = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_resCircle.setChecked(True)
        self.checkBox_resCircle.setObjectName("checkBox_resCircle")
        self.gridLayout_2.addWidget(self.checkBox_resCircle, 2, 0, 1, 2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        self.checkBox_positivity_constraint = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_positivity_constraint.setObjectName("checkBox_positivity_constraint")
        self.verticalLayout_5.addWidget(self.checkBox_positivity_constraint)
        self.checkBox_support_constraint = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_2)
        self.checkBox_support_constraint.setObjectName("checkBox_support_constraint")
        self.verticalLayout_5.addWidget(self.checkBox_support_constraint)
        self.gridLayout_2.addLayout(self.verticalLayout_5, 1, 3, 1, 1)
        self.btn_displayResults = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.btn_displayResults.setObjectName("btn_displayResults")
        self.gridLayout_2.addWidget(self.btn_displayResults, 6, 3, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.radioButton_FFT = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_FFT.setObjectName("radioButton_FFT")
        self.verticalLayout_7.addWidget(self.radioButton_FFT)
        self.radioButton_DFT = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_DFT.setObjectName("radioButton_DFT")
        self.verticalLayout_7.addWidget(self.radioButton_DFT)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 4, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 4, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 4, 2, 1, 1)
        self.lineEdit_numIterations = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_numIterations.sizePolicy().hasHeightForWidth())
        self.lineEdit_numIterations.setSizePolicy(sizePolicy)
        self.lineEdit_numIterations.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_numIterations.setObjectName("lineEdit_numIterations")
        self.gridLayout_2.addWidget(self.lineEdit_numIterations, 0, 1, 1, 1)
        self.lineEdit_interpolationCutoffDistance = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_interpolationCutoffDistance.sizePolicy().hasHeightForWidth())
        self.lineEdit_interpolationCutoffDistance.setSizePolicy(sizePolicy)
        self.lineEdit_interpolationCutoffDistance.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_interpolationCutoffDistance.setObjectName("lineEdit_interpolationCutoffDistance")
        self.gridLayout_2.addWidget(self.lineEdit_interpolationCutoffDistance, 6, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 6, 0, 1, 1)
        self.line_5 = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridLayout_2.addWidget(self.line_5, 0, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2.addLayout(self.gridLayout_3, 0, 5, 7, 1)
        self.lineEdit_oversamplingRatio = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_oversamplingRatio.sizePolicy().hasHeightForWidth())
        self.lineEdit_oversamplingRatio.setSizePolicy(sizePolicy)
        self.lineEdit_oversamplingRatio.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_oversamplingRatio.setObjectName("lineEdit_oversamplingRatio")
        self.gridLayout_2.addWidget(self.lineEdit_oversamplingRatio, 4, 1, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btn_reconstruct = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_reconstruct.sizePolicy().hasHeightForWidth())
        self.btn_reconstruct.setSizePolicy(sizePolicy)
        self.btn_reconstruct.setMinimumSize(QtCore.QSize(775, 50))
        self.btn_reconstruct.setObjectName("btn_reconstruct")
        self.horizontalLayout_4.addWidget(self.btn_reconstruct)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.log = QtWidgets.QTextEdit(self.scrollAreaWidgetContents_2)
        self.log.setMinimumSize(QtCore.QSize(100, 0))
        self.log.setObjectName("log")
        self.verticalLayout_2.addWidget(self.log)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_4.addWidget(self.scrollArea, 0, 0, 1, 1)
        GENFIRE_MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(GENFIRE_MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        GENFIRE_MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(GENFIRE_MainWindow)
        self.statusBar.setObjectName("statusBar")
        GENFIRE_MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(GENFIRE_MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1093, 31))
        self.menuBar.setObjectName("menuBar")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        self.menuView_Volume = QtWidgets.QMenu(self.menuBar)
        self.menuView_Volume.setObjectName("menuView_Volume")
        GENFIRE_MainWindow.setMenuBar(self.menuBar)
        self.action_Create_Support = QtWidgets.QAction(GENFIRE_MainWindow)
        self.action_Create_Support.setObjectName("action_Create_Support")
        self.action_Volume_Slicer = QtWidgets.QAction(GENFIRE_MainWindow)
        self.action_Volume_Slicer.setObjectName("action_Volume_Slicer")
        self.action_2 = QtWidgets.QAction(GENFIRE_MainWindow)
        self.action_2.setObjectName("action_2")
        self.menuTools.addAction(self.action_Create_Support)
        self.menuView_Volume.addAction(self.action_Volume_Slicer)
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuView_Volume.menuAction())

        self.retranslateUi(GENFIRE_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(GENFIRE_MainWindow)
        GENFIRE_MainWindow.setTabOrder(self.lineEdit_pj, self.lineEdit_support)
        GENFIRE_MainWindow.setTabOrder(self.lineEdit_support, self.lineEdit_angle)
        GENFIRE_MainWindow.setTabOrder(self.lineEdit_angle, self.lineEdit_io)
        GENFIRE_MainWindow.setTabOrder(self.lineEdit_io, self.lineEdit_numIterations)
        GENFIRE_MainWindow.setTabOrder(self.lineEdit_numIterations, self.lineEdit_oversamplingRatio)
        GENFIRE_MainWindow.setTabOrder(self.lineEdit_oversamplingRatio, self.lineEdit_interpolationCutoffDistance)
        GENFIRE_MainWindow.setTabOrder(self.lineEdit_interpolationCutoffDistance, self.radioButton_on)
        GENFIRE_MainWindow.setTabOrder(self.radioButton_on, self.radioButton_off)
        GENFIRE_MainWindow.setTabOrder(self.radioButton_off, self.radioButton_extension)
        GENFIRE_MainWindow.setTabOrder(self.radioButton_extension, self.btn_angles)
        GENFIRE_MainWindow.setTabOrder(self.btn_angles, self.btn_io)
        GENFIRE_MainWindow.setTabOrder(self.btn_io, self.btn_projections)
        GENFIRE_MainWindow.setTabOrder(self.btn_projections, self.btn_support)

    def retranslateUi(self, GENFIRE_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        GENFIRE_MainWindow.setWindowTitle(_translate("GENFIRE_MainWindow", "GENFIRE"))
        self.label_4.setText(_translate("GENFIRE_MainWindow", "Results Filename"))
        self.label_5.setText(_translate("GENFIRE_MainWindow", "*.mrc, *.npy, or *.mat"))
        self.btn_support.setText(_translate("GENFIRE_MainWindow", "Select Support File"))
        self.btn_angles.setText(_translate("GENFIRE_MainWindow", "Select Angle File"))
        self.checkBox_default_support.setText(_translate("GENFIRE_MainWindow", "Use default support"))
        self.btn_io.setText(_translate("GENFIRE_MainWindow", "Select Inital Object File"))
        self.checkBox_provide_io.setText(_translate("GENFIRE_MainWindow", "Provide initial object"))
        self.btn_projections.setText(_translate("GENFIRE_MainWindow", "Select Projection File"))
        self.groupBox.setTitle(_translate("GENFIRE_MainWindow", "Resolution Extension/Suppression"))
        self.radioButton_on.setText(_translate("GENFIRE_MainWindow", "On"))
        self.radioButton_off.setText(_translate("GENFIRE_MainWindow", "Off"))
        self.radioButton_extension.setText(_translate("GENFIRE_MainWindow", "Extension Only"))
        self.groupBox_3.setTitle(_translate("GENFIRE_MainWindow", "Method"))
        self.radioButton_ER.setText(_translate("GENFIRE_MainWindow", "ER"))
        self.radioButton_DR.setText(_translate("GENFIRE_MainWindow", "DR"))
        self.checkBox_multiGridding.setText(_translate("GENFIRE_MainWindow", "Permit Multiple Grid-Point Matches"))
        self.checkBox_rfree.setText(_translate("GENFIRE_MainWindow", "Calculate Rfree"))
        self.label_7.setText(_translate("GENFIRE_MainWindow", "Gridding Method"))
        self.checkBox_resCircle.setText(_translate("GENFIRE_MainWindow", "Enforce Resolution Circle"))
        self.label_6.setText(_translate("GENFIRE_MainWindow", "Constraints"))
        self.checkBox_positivity_constraint.setText(_translate("GENFIRE_MainWindow", "Positivity"))
        self.checkBox_support_constraint.setText(_translate("GENFIRE_MainWindow", "Support"))
        self.btn_displayResults.setText(_translate("GENFIRE_MainWindow", "Summarize Results"))
        self.radioButton_FFT.setText(_translate("GENFIRE_MainWindow", "FFT"))
        self.radioButton_DFT.setText(_translate("GENFIRE_MainWindow", "DFT"))
        self.label_2.setText(_translate("GENFIRE_MainWindow", "Oversampling Ratio"))
        self.label_3.setText(_translate("GENFIRE_MainWindow", "Interpolation Cutoff Distance (pixels)"))
        self.label.setText(_translate("GENFIRE_MainWindow", "Number of Iterations"))
        self.btn_reconstruct.setText(_translate("GENFIRE_MainWindow", "Launch Reconstruction"))
        self.menuTools.setTitle(_translate("GENFIRE_MainWindow", "Projection Calculator"))
        self.menuView_Volume.setTitle(_translate("GENFIRE_MainWindow", "View Volume"))
        self.action_Create_Support.setText(_translate("GENFIRE_MainWindow", "Launch Projection Calculator"))
        self.action_Volume_Slicer.setText(_translate("GENFIRE_MainWindow", "Launch Volume Slicer"))
        self.action_2.setText(_translate("GENFIRE_MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    GENFIRE_MainWindow = QtWidgets.QMainWindow()
    ui = Ui_GENFIRE_MainWindow()
    ui.setupUi(GENFIRE_MainWindow)
    GENFIRE_MainWindow.show()
    sys.exit(app.exec_())
