
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'naver_real_estate_uiEsqsNR.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QThread, Signal,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,QDialog,QVBoxLayout,
    QSpinBox, QSplitter, QStatusBar, QWidget, QAbstractItemView)
import pandas as pd
import os
from datetime import datetime
from module.naver_land.Naver_seoul_land import Naver_seoul_land
from module.naver_land.Naver_fetch_articles import Naver_fetch_articles

# 위젯
from widget.ProgressBarWidget import ProgressBarWidget  # 추가된 부분



class Ui_MainWindow(object):
    def __init__(self) :
        path = os.path.join('부동산', '전국.csv')
        self.naver = Naver_fetch_articles()
        self.data = pd.read_csv(path, encoding='cp949',) 
        self.result = pd.DataFrame()
        self.folder_path = '부동산'



    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1273, 1042)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.progressBar = ProgressBarWidget(self.centralwidget)  # 수정된 부분


        self.pushButton_start = QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName(u"pushButton_start")
        self.pushButton_start.setGeometry(QRect(1120, 950, 131, 41))
        self.pushButton_start.setStyleSheet(u"background-color:green;\n"
"color:white;\n"
"font-size:20px;\n"
"")
        self.pushButton_start.clicked.connect(self.fetching)    

        self.pushButton_to_excel = QPushButton(self.centralwidget)
        self.pushButton_to_excel.setObjectName(u"pushButton_to_excel")
        self.pushButton_to_excel.setGeometry(QRect(980, 950, 131, 41))
        self.pushButton_to_excel.clicked.connect(lambda : self.download(saving_format='csv'))
        self.pushButton_openFolder = QPushButton(self.centralwidget)
        self.pushButton_openFolder.setObjectName(u"pushButton_openFolder")
        self.pushButton_openFolder.setGeometry(QRect(840, 950, 131, 41))
        self.pushButton_openFolder.setStyleSheet(u"")
        self.pushButton_openFolder.clicked.connect(self.open_folder)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(1010, 520, 231, 411))
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 20, 141, 21))
        self.label_3.setStyleSheet(u"font-size :15px;")
        self.listWidget_selected = QListWidget(self.groupBox_2)
        self.listWidget_selected.setObjectName(u"listWidget_selected")
        self.listWidget_selected.setGeometry(QRect(10, 50, 211, 361))
        self.pushButton_add = QPushButton(self.centralwidget)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setGeometry(QRect(920, 640, 75, 61))
        self.pushButton_add.clicked.connect(self.get_selected_complex_data)
        self.pushButton_delete = QPushButton(self.centralwidget)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        self.pushButton_delete.setGeometry(QRect(920, 720, 75, 61))
        self.pushButton_delete.clicked.connect(self.delete_selected_items)
        
        self.splitter_17 = QSplitter(self.centralwidget)
        self.splitter_17.setObjectName(u"splitter_17")
        self.splitter_17.setGeometry(QRect(10, 20, 1231, 491))
        self.splitter_17.setOrientation(Qt.Vertical)
        self.groupBox_4 = QGroupBox(self.splitter_17)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setStyleSheet(u"font-size :15px;")
        self.splitter_16 = QSplitter(self.groupBox_4)
        self.splitter_16.setObjectName(u"splitter_16")
        self.splitter_16.setGeometry(QRect(20, 30, 681, 20))
        self.splitter_16.setOrientation(Qt.Horizontal)
        self.checkBox_realEstateType_APT = QCheckBox(self.splitter_16)
        self.checkBox_realEstateType_APT.setObjectName(u"checkBox_realEstateType_APT")
        self.checkBox_realEstateType_APT.stateChanged.connect(self.get_infos)
        self.checkBox_realEstateType_APT.setChecked(True)
        self.splitter_16.addWidget(self.checkBox_realEstateType_APT)
        self.checkBox_realEstateType_ABYG = QCheckBox(self.splitter_16)
        self.checkBox_realEstateType_ABYG.setObjectName(u"checkBox_realEstateType_ABYG")
        self.checkBox_realEstateType_ABYG.stateChanged.connect(self.get_infos)
        self.splitter_16.addWidget(self.checkBox_realEstateType_ABYG)
        self.checkBox_realEstateType_JGC = QCheckBox(self.splitter_16)
        self.checkBox_realEstateType_JGC.setObjectName(u"checkBox_realEstateType_JGC")
        self.checkBox_realEstateType_JGC.stateChanged.connect(self.get_infos)
        self.splitter_16.addWidget(self.checkBox_realEstateType_JGC)
        self.checkBox_realEstateType_OPST = QCheckBox(self.splitter_16)
        self.checkBox_realEstateType_OPST.setObjectName(u"checkBox_realEstateType_OPST")
        self.checkBox_realEstateType_OPST.stateChanged.connect(self.get_infos)
        self.splitter_16.addWidget(self.checkBox_realEstateType_OPST)
        self.checkBox_realEstateType_OBYG = QCheckBox(self.splitter_16)
        self.checkBox_realEstateType_OBYG.setObjectName(u"checkBox_realEstateType_OBYG")
        self.checkBox_realEstateType_OBYG.stateChanged.connect(self.get_infos)
        self.splitter_16.addWidget(self.checkBox_realEstateType_OBYG)
        self.checkBox_realEstateType_JGB = QCheckBox(self.splitter_16)
        self.checkBox_realEstateType_JGB.setObjectName(u"checkBox_realEstateType_JGB")
        self.checkBox_realEstateType_JGB.stateChanged.connect(self.get_infos)
        self.splitter_16.addWidget(self.checkBox_realEstateType_JGB)
        self.checkBox_realEstateType_PRE = QCheckBox(self.splitter_16)
        self.checkBox_realEstateType_PRE.setObjectName(u"checkBox_realEstateType_PRE")
        self.checkBox_realEstateType_PRE.stateChanged.connect(self.get_infos)
        self.checkBox_realEstateType_PRE.setChecked(True)
        self.splitter_16.addWidget(self.checkBox_realEstateType_PRE)
        self.splitter_17.addWidget(self.groupBox_4)
        self.groupBox_3 = QGroupBox(self.splitter_17)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setStyleSheet(u"font-size:15px")
        self.splitter_4 = QSplitter(self.groupBox_3)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setGeometry(QRect(20, 30, 201, 20))
        self.splitter_4.setOrientation(Qt.Horizontal)
        self.checkBox_tradeType_A1 = QCheckBox(self.splitter_4)
        self.checkBox_tradeType_A1.setObjectName(u"checkBox_tradeType_A1")
        self.checkBox_tradeType_A1.stateChanged.connect(self.get_infos)
        self.checkBox_tradeType_A1.setChecked(True)
        self.checkBox_tradeType_A1.setAutoRepeat(False)
        self.checkBox_tradeType_A1.setAutoExclusive(False)
        self.splitter_4.addWidget(self.checkBox_tradeType_A1)
        self.checkBox_tradeType_B1 = QCheckBox(self.splitter_4)
        self.checkBox_tradeType_B1.setObjectName(u"checkBox_tradeType_B1")
        self.checkBox_tradeType_B1.stateChanged.connect(self.get_infos)
        self.splitter_4.addWidget(self.checkBox_tradeType_B1)
        self.splitter_17.addWidget(self.groupBox_3)
        self.groupBox_5 = QGroupBox(self.splitter_17)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setStyleSheet(u"font-size :15px;")
        self.spinBox_minPrice = QSpinBox(self.groupBox_5)
        self.spinBox_minPrice.setObjectName(u"spinBox_minPrice")
        self.spinBox_minPrice.valueChanged.connect(self.get_infos)
        self.spinBox_minPrice.setGeometry(QRect(20, 40, 161, 31))
        self.spinBox_minPrice.setMaximum(899999999)
        self.spinBox_minPrice.setSingleStep(1000)
        self.spinBox_maxPrice = QSpinBox(self.groupBox_5)
        self.spinBox_maxPrice.setObjectName(u"spinBox_maxPrice")
        self.spinBox_maxPrice.valueChanged.connect(self.get_infos)
        self.spinBox_maxPrice.setGeometry(QRect(260, 40, 161, 31))
        self.spinBox_maxPrice.setMinimum(1)
        self.spinBox_maxPrice.setMaximum(900000000)
        self.spinBox_maxPrice.setSingleStep(1000)
        self.spinBox_maxPrice.setValue(900000000)
        self.label_4 = QLabel(self.groupBox_5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(440, 50, 201, 16))
        self.label_5 = QLabel(self.groupBox_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(210, 50, 21, 16))
        self.label_dealRange = QLabel(self.groupBox_5)
        self.label_dealRange.setObjectName(u"label_dealRange")
        self.label_dealRange.setGeometry(QRect(800, 20, 411, 51))
        self.label_dealRange.setStyleSheet(u"color : red;\n"
"")
        self.splitter_17.addWidget(self.groupBox_5)
        self.groupBox_6 = QGroupBox(self.splitter_17)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setStyleSheet(u"font-size :15px;")
        self.splitter_10 = QSplitter(self.groupBox_6)
        self.splitter_10.setObjectName(u"splitter_10")
        self.splitter_10.setGeometry(QRect(30, 30, 731, 20))
        self.splitter_10.setOrientation(Qt.Horizontal)
        self.splitter_11 = QSplitter(self.splitter_10)
        self.splitter_11.setObjectName(u"splitter_11")
        self.splitter_11.setOrientation(Qt.Horizontal)
        self.checkBox_area_10 = QCheckBox(self.splitter_11)
        self.checkBox_area_10.setObjectName(u"checkBox_area_10")
        self.checkBox_area_10.stateChanged.connect(self.get_infos)
        self.checkBox_area_10.setChecked(True)
        self.splitter_11.addWidget(self.checkBox_area_10)
        self.checkBox_area_20 = QCheckBox(self.splitter_11)
        self.checkBox_area_20.setObjectName(u"checkBox_area_20")
        self.checkBox_area_20.stateChanged.connect(self.get_infos)
        self.checkBox_area_20.setChecked(True)
        self.splitter_11.addWidget(self.checkBox_area_20)
        self.checkBox_area_30 = QCheckBox(self.splitter_11)
        self.checkBox_area_30.setObjectName(u"checkBox_area_30")
        self.checkBox_area_30.stateChanged.connect(self.get_infos)
        self.checkBox_area_30.setChecked(True)
        self.splitter_11.addWidget(self.checkBox_area_30)
        self.checkBox_area_40 = QCheckBox(self.splitter_11)
        self.checkBox_area_40.setObjectName(u"checkBox_area_40")
        self.checkBox_area_40.stateChanged.connect(self.get_infos)
        self.checkBox_area_40.setChecked(True)
        self.splitter_11.addWidget(self.checkBox_area_40)
        self.checkBox_area_50 = QCheckBox(self.splitter_11)
        self.checkBox_area_50.setObjectName(u"checkBox_area_50")
        self.checkBox_area_50.stateChanged.connect(self.get_infos)
        self.checkBox_area_50.setChecked(True)
        self.splitter_11.addWidget(self.checkBox_area_50)
        self.checkBox_area_60 = QCheckBox(self.splitter_11)
        self.checkBox_area_60.setObjectName(u"checkBox_area_60")
        self.checkBox_area_60.stateChanged.connect(self.get_infos)
        self.checkBox_area_60.setChecked(True)
        self.splitter_11.addWidget(self.checkBox_area_60)
        self.checkBox_area_70 = QCheckBox(self.splitter_11)
        self.checkBox_area_70.setObjectName(u"checkBox_area_70")
        self.checkBox_area_70.stateChanged.connect(self.get_infos)
        self.checkBox_area_70.setChecked(True)
        self.checkBox_area_70.setTristate(False)
        self.splitter_11.addWidget(self.checkBox_area_70)
        self.splitter_10.addWidget(self.splitter_11)
        self.label_areaRange = QLabel(self.groupBox_6)
        self.label_areaRange.setObjectName(u"label_areaRange")
        self.label_areaRange.setGeometry(QRect(800, 10, 411, 51))
        self.label_areaRange.setStyleSheet(u"color : red;\n"
"")
        self.splitter_17.addWidget(self.groupBox_6)
        self.groupBox_7 = QGroupBox(self.splitter_17)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setStyleSheet(u"font-size :15px;")
        self.splitter_12 = QSplitter(self.groupBox_7)
        self.splitter_12.setObjectName(u"splitter_12")
        self.splitter_12.setGeometry(QRect(10, 40, 581, 20))
        self.splitter_12.setOrientation(Qt.Horizontal)
        self.splitter_13 = QSplitter(self.splitter_12)
        self.splitter_13.setObjectName(u"splitter_13")
        self.splitter_13.setOrientation(Qt.Horizontal)
        self.checkBox_approvalDate_0 = QCheckBox(self.splitter_13)
        self.checkBox_approvalDate_0.setObjectName(u"checkBox_approvalDate_0")
        self.checkBox_approvalDate_0.stateChanged.connect(self.get_infos)
        self.checkBox_approvalDate_0.setChecked(True)
        self.splitter_13.addWidget(self.checkBox_approvalDate_0)
        self.checkBox_approvalDate_2 = QCheckBox(self.splitter_13)
        self.checkBox_approvalDate_2.setObjectName(u"checkBox_approvalDate_2")
        self.checkBox_approvalDate_2.stateChanged.connect(self.get_infos)
        self.checkBox_approvalDate_2.setChecked(True)
        self.splitter_13.addWidget(self.checkBox_approvalDate_2)
        self.checkBox_approvalDate_4 = QCheckBox(self.splitter_13)
        self.checkBox_approvalDate_4.setObjectName(u"checkBox_approvalDate_4")
        self.checkBox_approvalDate_4.stateChanged.connect(self.get_infos)
        self.checkBox_approvalDate_4.setChecked(True)
        self.splitter_13.addWidget(self.checkBox_approvalDate_4)
        self.checkBox_approvalDate_10 = QCheckBox(self.splitter_13)
        self.checkBox_approvalDate_10.setObjectName(u"checkBox_approvalDate_10")
        self.checkBox_approvalDate_10.stateChanged.connect(self.get_infos)
        self.checkBox_approvalDate_10.setChecked(True)
        self.splitter_13.addWidget(self.checkBox_approvalDate_10)
        self.checkBox_approvalDate_15 = QCheckBox(self.splitter_13)
        self.checkBox_approvalDate_15.setObjectName(u"checkBox_approvalDate_15")
        self.checkBox_approvalDate_15.stateChanged.connect(self.get_infos)
        self.checkBox_approvalDate_15.setChecked(True)
        self.splitter_13.addWidget(self.checkBox_approvalDate_15)
        self.checkBox_approvalDate_20 = QCheckBox(self.splitter_13)
        self.checkBox_approvalDate_20.setObjectName(u"checkBox_approvalDate_20")
        self.checkBox_approvalDate_20.stateChanged.connect(self.get_infos)
        self.checkBox_approvalDate_20.setChecked(True)
        self.splitter_13.addWidget(self.checkBox_approvalDate_20)
        self.checkBox_approvalDate_25 = QCheckBox(self.splitter_13)
        self.checkBox_approvalDate_25.setObjectName(u"checkBox_approvalDate_25")
        self.checkBox_approvalDate_25.stateChanged.connect(self.get_infos)
        self.checkBox_approvalDate_25.setChecked(True)
        self.splitter_13.addWidget(self.checkBox_approvalDate_25)
        self.checkBox_approvalDate_30 = QCheckBox(self.splitter_13)
        self.checkBox_approvalDate_30.setObjectName(u"checkBox_approvalDate_30")
        self.checkBox_approvalDate_30.stateChanged.connect(self.get_infos)
        self.checkBox_approvalDate_30.setChecked(True)
        self.splitter_13.addWidget(self.checkBox_approvalDate_30)
        self.splitter_12.addWidget(self.splitter_13)
        self.label_approvalDateRange = QLabel(self.groupBox_7)
        self.label_approvalDateRange.setObjectName(u"label_approvalDateRange")
        self.label_approvalDateRange.setGeometry(QRect(800, 20, 411, 51))
        self.label_approvalDateRange.setStyleSheet(u"color : red;\n"
"")
        self.splitter_17.addWidget(self.groupBox_7)
        self.groupBox_8 = QGroupBox(self.splitter_17)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.groupBox_8.setStyleSheet(u"font-size :15px;")
        self.label_totalHouseholdsRange = QLabel(self.groupBox_8)
        self.label_totalHouseholdsRange.setObjectName(u"label_totalHouseholdsRange")
        self.label_totalHouseholdsRange.setGeometry(QRect(800, 10, 411, 51))
        self.label_totalHouseholdsRange.setStyleSheet(u"color : red;\n"
"")
        self.splitter_14 = QSplitter(self.groupBox_8)
        self.splitter_14.setObjectName(u"splitter_14")
        self.splitter_14.setGeometry(QRect(20, 30, 571, 24))
        self.splitter_14.setOrientation(Qt.Horizontal)
        self.checkBox_totalHouseholds_100 = QCheckBox(self.splitter_14)
        self.checkBox_totalHouseholds_100.setObjectName(u"checkBox_totalHouseholds_100")
        self.checkBox_totalHouseholds_100.stateChanged.connect(self.get_infos)
        self.checkBox_totalHouseholds_100.setChecked(True)
        self.splitter_14.addWidget(self.checkBox_totalHouseholds_100)
        self.checkBox_totalHouseholds_300 = QCheckBox(self.splitter_14)
        self.checkBox_totalHouseholds_300.setObjectName(u"checkBox_totalHouseholds_300")
        self.checkBox_totalHouseholds_300.stateChanged.connect(self.get_infos)
        self.checkBox_totalHouseholds_300.setChecked(True)
        self.splitter_14.addWidget(self.checkBox_totalHouseholds_300)
        self.checkBox_totalHouseholds_500 = QCheckBox(self.splitter_14)
        self.checkBox_totalHouseholds_500.setObjectName(u"checkBox_totalHouseholds_500")
        self.checkBox_totalHouseholds_500.stateChanged.connect(self.get_infos)
        self.checkBox_totalHouseholds_500.setChecked(True)
        self.splitter_14.addWidget(self.checkBox_totalHouseholds_500)
        self.checkBox_totalHouseholds_700 = QCheckBox(self.splitter_14)
        self.checkBox_totalHouseholds_700.setObjectName(u"checkBox_totalHouseholds_700")
        self.checkBox_totalHouseholds_700.stateChanged.connect(self.get_infos)
        self.checkBox_totalHouseholds_700.setChecked(True)
        self.splitter_14.addWidget(self.checkBox_totalHouseholds_700)
        self.checkBox_totalHouseholds_1000 = QCheckBox(self.splitter_14)
        self.checkBox_totalHouseholds_1000.setObjectName(u"checkBox_totalHouseholds_1000")
        self.checkBox_totalHouseholds_1000.stateChanged.connect(self.get_infos)
        self.checkBox_totalHouseholds_1000.setChecked(True)
        self.splitter_14.addWidget(self.checkBox_totalHouseholds_1000)
        self.checkBox_totalHouseholds_1500 = QCheckBox(self.splitter_14)
        self.checkBox_totalHouseholds_1500.setObjectName(u"checkBox_totalHouseholds_1500")
        self.checkBox_totalHouseholds_1500.stateChanged.connect(self.get_infos)
        self.checkBox_totalHouseholds_1500.setChecked(True)
        self.splitter_14.addWidget(self.checkBox_totalHouseholds_1500)
        self.checkBox_totalHouseholds_2001 = QCheckBox(self.splitter_14)
        self.checkBox_totalHouseholds_2001.setObjectName(u"checkBox_totalHouseholds_2001")
        self.checkBox_totalHouseholds_2001.stateChanged.connect(self.get_infos)
        self.checkBox_totalHouseholds_2001.setChecked(True)
        self.splitter_14.addWidget(self.checkBox_totalHouseholds_2001)
        self.splitter_17.addWidget(self.groupBox_8)
        self.splitter_18 = QSplitter(self.centralwidget)
        self.splitter_18.setObjectName(u"splitter_18")
        self.splitter_18.setGeometry(QRect(10, 520, 901, 411))
        self.splitter_18.setOrientation(Qt.Horizontal)
        self.groupBox = QGroupBox(self.splitter_18)
        self.groupBox.setObjectName(u"groupBox")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 101, 21))
        self.label.setStyleSheet(u"font-size :15px;")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(680, 20, 101, 21))
        self.label_2.setStyleSheet(u"font-size :15px;")
        self.splitter = QSplitter(self.groupBox)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setGeometry(QRect(20, 50, 0, 361))
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter_2 = QSplitter(self.splitter)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.splitter_3 = QSplitter(self.splitter_2)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.splitter_2.addWidget(self.splitter_3)
        self.splitter.addWidget(self.splitter_2)
        self.splitter_5 = QSplitter(self.groupBox)
        self.splitter_5.setObjectName(u"splitter_5")
        self.splitter_5.setGeometry(QRect(20, 50, 871, 361))
        self.splitter_5.setOrientation(Qt.Horizontal)
        self.listWidget_1 = QListWidget(self.splitter_5)
        self.listWidget_1.setObjectName(u"listWidget_1")

        
        # item1 = self.dataSetting(type='province')
        # self.listWidget_1.addItem(item1)
        self.listWidget_1.addItems(list(self.data['provinceName'].unique()))
        self.listWidget_1.itemSelectionChanged.connect(self.display_district)
        self.splitter_5.addWidget(self.listWidget_1)
        self.listWidget_2 = QListWidget(self.splitter_5)
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.itemSelectionChanged.connect(self.display_dong)
        self.splitter_5.addWidget(self.listWidget_2)
        self.listWidget_3 = QListWidget(self.splitter_5)
        self.listWidget_3.setObjectName(u"listWidget_3")
        self.listWidget_3.itemSelectionChanged.connect(self.display_complex)
        self.splitter_5.addWidget(self.listWidget_3)
        
        self.listWidget_4 = QListWidget(self.splitter_5)
        self.listWidget_4.setObjectName(u"listWidget_4")

        
        
        
        

        self.splitter_5.addWidget(self.listWidget_4)


        # 다중 선택 가능하게 설정
        # self.listWidget_1.setSelectionMode(QAbstractItemView.MultiSelection)  # 다중 선택 가능하게 설정
        self.listWidget_2.setSelectionMode(QAbstractItemView.MultiSelection)  # 다중 선택 가능하게 설정
        self.listWidget_3.setSelectionMode(QAbstractItemView.MultiSelection)  # 다중 선택 가능하게 설정
        self.listWidget_4.setSelectionMode(QAbstractItemView.MultiSelection)  # 다중 선택 가능하게 설정


        self.splitter_18.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1273, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

        self.get_infos()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"\uc218\uc9d1\uc2dc\uc791", None))
        self.pushButton_to_excel.setText(QCoreApplication.translate("MainWindow", u"\uc5d1\uc140\ub2e4\uc6b4\ub85c\ub4dc", None))
        self.pushButton_openFolder.setText(QCoreApplication.translate("MainWindow", u"\ub2e4\uc6b4\ub85c\ub4dc \ud3f4\ub354 \uc5f4\uae30", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\uc120\ud0dd\ub41c \uc9c0\uc5ed/\ubb3c\uac74", None))
        self.pushButton_add.setText(QCoreApplication.translate("MainWindow", u"\ucd94\uac00 \u25b6", None))
        self.pushButton_delete.setText(QCoreApplication.translate("MainWindow", u"\u25c0 \uc81c\uac70", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\uc885\ub958", None))
        self.checkBox_realEstateType_APT.setText(QCoreApplication.translate("MainWindow", u"\uc544\ud30c\ud2b8", None))
        self.checkBox_realEstateType_ABYG.setText(QCoreApplication.translate("MainWindow", u"\uc544\ud30c\ud2b8\ubd84\uc591\uad8c", None))
        self.checkBox_realEstateType_JGC.setText(QCoreApplication.translate("MainWindow", u"\uc7ac\uac74\ucd95", None))
        self.checkBox_realEstateType_OPST.setText(QCoreApplication.translate("MainWindow", u"\uc624\ud53c\uc2a4\ud154", None))
        self.checkBox_realEstateType_OBYG.setText(QCoreApplication.translate("MainWindow", u"\uc624\ud53c\uc2a4\ud154\ubd84\uc591\uad8c", None))
        self.checkBox_realEstateType_JGB.setText(QCoreApplication.translate("MainWindow", u"\uc7ac\uac1c\ubc1c", None))
        self.checkBox_realEstateType_PRE.setText(QCoreApplication.translate("MainWindow", u"\ubd84\uc591\uc911 / \uc608\uc815", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\ub9e4\ub9e4\ubc29\uc2dd", None))
        self.checkBox_tradeType_A1.setText(QCoreApplication.translate("MainWindow", u"\ub9e4\ub9e4", None))
        self.checkBox_tradeType_B1.setText(QCoreApplication.translate("MainWindow", u"\uc804\uc138", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\ub9e4\ub9e4\uac00/\ubd84\uc591\uac00/\uc804\uc138\uac00", None))
        self.spinBox_maxPrice.setSuffix("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"(\ub9cc\uc6d0) (\uc608\uc2dc : 10000 = 1\uc5b5)", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"~", None))
        self.label_dealRange.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc2b9\uc778\uc77c : ( ) ~ ( ) ", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"\uba74\uc801", None))
        self.checkBox_area_10.setText(QCoreApplication.translate("MainWindow", u"~10\ud3c9\ub300", None))
        self.checkBox_area_20.setText(QCoreApplication.translate("MainWindow", u"20\ud3c9", None))
        self.checkBox_area_30.setText(QCoreApplication.translate("MainWindow", u"30\ud3c9", None))
        self.checkBox_area_40.setText(QCoreApplication.translate("MainWindow", u"40\ud3c9", None))
        self.checkBox_area_50.setText(QCoreApplication.translate("MainWindow", u"50\ud3c9", None))
        self.checkBox_area_60.setText(QCoreApplication.translate("MainWindow", u"60\ud3c9", None))
        self.checkBox_area_70.setText(QCoreApplication.translate("MainWindow", u"70\ud3c9~", None))
        self.label_areaRange.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc2b9\uc778\uc77c : ( ) ~ ( ) ", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc2b9\uc778\uc77c", None))
        self.checkBox_approvalDate_0.setText(QCoreApplication.translate("MainWindow", u"\uc785\uc8fc\uc608\uc815", None))
        self.checkBox_approvalDate_2.setText(QCoreApplication.translate("MainWindow", u"2\ub144", None))
        self.checkBox_approvalDate_4.setText(QCoreApplication.translate("MainWindow", u"4\ub144", None))
        self.checkBox_approvalDate_10.setText(QCoreApplication.translate("MainWindow", u"10\ub144", None))
        self.checkBox_approvalDate_15.setText(QCoreApplication.translate("MainWindow", u"15\ub144", None))
        self.checkBox_approvalDate_20.setText(QCoreApplication.translate("MainWindow", u"20\ub144", None))
        self.checkBox_approvalDate_25.setText(QCoreApplication.translate("MainWindow", u"25\ub144", None))
        self.checkBox_approvalDate_30.setText(QCoreApplication.translate("MainWindow", u"30\ub144~", None))
        self.label_approvalDateRange.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc2b9\uc778\uc77c : ( ) ~ ( ) ", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"\uc138\ub300\uc218", None))
        self.label_totalHouseholdsRange.setText(QCoreApplication.translate("MainWindow", u"\uc0ac\uc6a9\uc2b9\uc778\uc77c : ( ) ~ ( ) ", None))
        self.checkBox_totalHouseholds_100.setText(QCoreApplication.translate("MainWindow", u"~100", None))
        self.checkBox_totalHouseholds_300.setText(QCoreApplication.translate("MainWindow", u"300", None))
        self.checkBox_totalHouseholds_500.setText(QCoreApplication.translate("MainWindow", u"500", None))
        self.checkBox_totalHouseholds_700.setText(QCoreApplication.translate("MainWindow", u"700", None))
        self.checkBox_totalHouseholds_1000.setText(QCoreApplication.translate("MainWindow", u"1000", None))
        self.checkBox_totalHouseholds_1500.setText(QCoreApplication.translate("MainWindow", u"1500", None))
        self.checkBox_totalHouseholds_2001.setText(QCoreApplication.translate("MainWindow", u"2000~", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\uc9c0\uc5ed\uc120\ud0dd", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\ubb3c\uac74\uc120\ud0dd", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\ub124\uc774\ubc84\ubd80\ub3d9\uc0b0", None))
    # retranslateUi

    def collect_realEstateType(self):
        # 체크박스 상태 정보 모으기
        checkboxes = {
            "ABYG": self.checkBox_realEstateType_ABYG.isChecked(),
            "JGC": self.checkBox_realEstateType_JGC.isChecked(),
            "OPST": self.checkBox_realEstateType_OPST.isChecked(),
            "OBYG": self.checkBox_realEstateType_OBYG.isChecked(),
            "JGB": self.checkBox_realEstateType_JGB.isChecked(),
            "PRE": self.checkBox_realEstateType_PRE.isChecked()
        }
        checked_ordered = [key for key in ["ABYG", "JGC", "OPST", "OBYG", "PRE", "JGB"] if checkboxes[key]]
        real_estate_result = ":".join(checked_ordered)
        return real_estate_result
    
    


    def collect_tradeType(self) :
                # Trade Type 체크박스 상태 정보 모으기
        trade_type_checkboxes = {
            "A1": self.checkBox_tradeType_A1.isChecked(),
            "B1": self.checkBox_tradeType_B1.isChecked()
        }
        checked_trade_type_ordered = [key for key in ["A1", "B1"] if trade_type_checkboxes[key]]
        trade_type_result = ":".join(checked_trade_type_ordered)

        return trade_type_result

    
    
    

    def collect_area(self):
        # 체크박스 상태 정보 모으기
        area_checkboxes = {
            "10": self.checkBox_area_10,
            "20": self.checkBox_area_20,
            "30": self.checkBox_area_30,
            "40": self.checkBox_area_40,
            "50": self.checkBox_area_50,
            "60": self.checkBox_area_60,
            "70": self.checkBox_area_70
        }

        # 체크된 체크박스들을 리스트로 모으기
        checked_areas = [int(area) for area, checkbox in area_checkboxes.items() if checkbox.isChecked()]

        if not checked_areas:
            return None, None

        areaMin = min(checked_areas)
        areaMax = max(checked_areas)

        # 중간 범위 체크박스들 체크 상태로 설정
        for area, checkbox in area_checkboxes.items():
            if areaMin < int(area) < areaMax:
                checkbox.setChecked(True)

        return areaMin, areaMax
    
    

    def collect_approval_date(self):
        approval_date_checkboxes = {
            "0": self.checkBox_approvalDate_0,
            "2": self.checkBox_approvalDate_2,
            "4": self.checkBox_approvalDate_4,
            "10": self.checkBox_approvalDate_10,
            "15": self.checkBox_approvalDate_15,
            "20": self.checkBox_approvalDate_20,
            "25": self.checkBox_approvalDate_25,
            "30": self.checkBox_approvalDate_30
        }

        checked_dates = [int(date) for date, checkbox in approval_date_checkboxes.items() if checkbox.isChecked()]

        if not checked_dates:
            return None, None

        recently_build_years = min(checked_dates)
        old_build_years = max(checked_dates)

        for date, checkbox in approval_date_checkboxes.items():
            if recently_build_years < int(date) < old_build_years:
                checkbox.setChecked(True)

        return recently_build_years, old_build_years

    def collect_total_households(self):
        total_households_checkboxes = {
            "100": self.checkBox_totalHouseholds_100,
            "300": self.checkBox_totalHouseholds_300,
            "500": self.checkBox_totalHouseholds_500,
            "700": self.checkBox_totalHouseholds_700,
            "1000": self.checkBox_totalHouseholds_1000,
            "1500": self.checkBox_totalHouseholds_1500,
            "2001": self.checkBox_totalHouseholds_2001
        }

        checked_households = [int(count) for count, checkbox in total_households_checkboxes.items() if checkbox.isChecked()]

        if not checked_households:
            return None, None

        minHouseHoldCount = min(checked_households)
        maxHouseHoldCount = max(checked_households)

        for count, checkbox in total_households_checkboxes.items():
            if minHouseHoldCount < int(count) < maxHouseHoldCount:
                checkbox.setChecked(True)

        return minHouseHoldCount, maxHouseHoldCount
    
    

    def get_infos(self) : 
        self.tradeType = self.collect_tradeType()
        self.minPrice = int(self.spinBox_minPrice.value())
        self.maxPrice = int(self.spinBox_maxPrice.value())
        self.areaMin, self.areaMax = self.collect_area()
        self.recentlyBuildYears, self.oldBuildYears = self.collect_approval_date()
        self.minHouseHoldCount, self.maxHouseHoldCount = self.collect_total_households()
        self.names, self.ids = self.get_selected_items_data(self.listWidget_selected, searching_type='all')
        
        self.label_dealRange.setText(f'조회가격범위 : {self.minPrice/10000} ~ {self.maxPrice/10000}(억원)')
        self.label_areaRange.setText(f'조회평수범위 : {self.areaMin} ~ {self.areaMax}(평)')
        self.label_approvalDateRange.setText(f'조회사용승인범위 : {self.recentlyBuildYears} ~ {self.oldBuildYears}(년 전)')
        self.label_totalHouseholdsRange.setText(f'조회세대수 : {self.minHouseHoldCount} ~ {self.maxHouseHoldCount}(세대)')

    def display_district(self):
        selected_items = self.listWidget_1.selectedItems()
        district_names = []
        province_names = []
        for item in selected_items:
            province_name = item.text()
            province_names.append(province_name)
        matching_rows = self.data[self.data['provinceName'].isin(province_names) ]
        district_names.extend(matching_rows['districtName'].unique())
        self.listWidget_2.clear()
        self.listWidget_2.addItems(district_names)
        # self.listWidget_2.selectAll()
        # for i in range(self.listWidget_2.count()):
        #     self.listWidget_2.item(i).setSelected(True)

    def display_dong(self):
        selected_items = self.listWidget_2.selectedItems()
        dong_names = []
        district_names = []        
        for item in selected_items:
            dong_name = item.text()
            district_names.append(dong_name)
        matching_rows = self.data[self.data['districtName'].isin(district_names) ]
        dong_names.extend(matching_rows['dongName'].unique())
        self.listWidget_3.clear()
        self.listWidget_3.addItems(dong_names)
        # self.listWidget_3.selectAll()

    def display_complex(self):
        selected_items = self.listWidget_3.selectedItems()
        dong_names = []
        for item in selected_items:
            dong_name = item.text()
            dong_names.append(dong_name)
        
        matching_rows = self.data[self.data['dongName'].isin(dong_names)]
        unique_provinces = matching_rows[['complexName', 'complexNo']].drop_duplicates()
        
        self.listWidget_4.clear()
        for i in range(len(unique_provinces)):
            item = QListWidgetItem(unique_provinces.iloc[i]['complexName'])
            item.setData(Qt.UserRole, unique_provinces.iloc[i]['complexNo'])
            self.listWidget_4.addItem(item)
        
        # self.listWidget_4.selectAll()
        # complex_names.extend(matching_rows['complexName'].unique())
    
    def get_selected_complex_data(self):
     selected_items = self.listWidget_4.selectedItems()
     for index in range(len(selected_items)):
         item = selected_items[index]
         item_data = item.data(Qt.UserRole)  # 고유한 데이터 가져오기
 
         # 중복 여부를 확인
         duplicate_found = False
         for i in range(self.listWidget_selected.count()):
             existing_item = self.listWidget_selected.item(i)
             if existing_item.data(Qt.UserRole) == item_data:
                 duplicate_found = True
                 break
 
         if not duplicate_found:
             copied_item = QListWidgetItem(item)
             copied_item.setData(Qt.UserRole, item_data)  # 데이터 설정
             self.listWidget_selected.addItem(copied_item)

    def delete_selected_items(self):
        selected_items = self.listWidget_selected.selectedItems()
        for item in selected_items:
            row = self.listWidget_selected.row(item)
            self.listWidget_selected.takeItem(row)

        

    

    def get_selected_items_data(self, target_widget, searching_type='selected'):
        selected_items= []
        if searching_type == 'selected' :
            selected_items = target_widget.selectedItems()
        elif searching_type == 'all' :
            for index in range(target_widget.count()):
                selected_items.append(target_widget.item(index))
            
            
        texts, datas = [], []
        for item in selected_items:
            texts.append(item.text())
            datas.append(str(item.data(Qt.UserRole)))  # 데이터를 문자열로 변환
        return texts, datas

    

        
    def fetching(self):
        self.get_infos()
        dialog = QDialog(self)
        dialog.setWindowTitle("Popup Dialog")

        # 레이아웃 생성
        layout = QVBoxLayout(dialog)

        # 라벨 생성
        label = QLabel(f"""
    self.tradeType : {self.tradeType}
    self.minPrice : {self.minPrice}
    self.maxPrice : {self.maxPrice}
    self.areaMin : {self.areaMin}
    self.recentlyBuildYears : {self.recentlyBuildYears}
    self.minHouseHoldCount : {self.minHouseHoldCount}
    self.names : {self.names}
    self.areaMax : {self.areaMax}
    self.oldBuildYears : {self.oldBuildYears}
    self.maxHouseHoldCount : {self.maxHouseHoldCount}
    self.ids : {self.ids}
    """, dialog)

        # 수행 버튼 생성
        diag_start_button = QPushButton("수집시작", dialog)
        diag_start_button.clicked.connect(lambda: self.start_fetching(dialog))  # start_fetching 메서드를 연결

        # 취소 버튼 생성
        diag_cancel_button = QPushButton("취소", dialog)
        diag_cancel_button.clicked.connect(dialog.accept)  # QDialog의 accept 메서드를 연결

        self.res = QLabel(dialog)  # self.res를 다이얼로그에 다시 정의

        # 레이아웃에 위젯 추가
        layout.addWidget(label)
        layout.addWidget(diag_start_button)
        layout.addWidget(diag_cancel_button)
        layout.addWidget(self.res)  # self.res를 레이아웃에 추가

        # 다이얼로그 실행
        dialog.exec()

    def start_fetching(self, dialog):
        dialog.accept()  # 다이얼로그 닫기
        self.req()

    def req(self):
        import requests

        self.res.setText('시작합니다.')
        worker = self.Worker(self)
        worker.progressChanged.connect(self.update_progress)
        
        worker.start()
    
    def update_progress(self, value):
        self.progressBar.setValue(value)
    
    def download(self, saving_format = "csv") :
        # 현재 시간을 YYYYMMDDhhmm 형식으로 추출
        current_time = datetime.now().strftime('%Y%m%d%H%M')
        self.result.to_csv(os.path.join(self.folder_path, f'비조건문{current_time}.csv'), encoding='cp949', index=False)
        if saving_format == 'csv' :
            self.result.to_csv(os.path.join(self.folder_path, f'조건문{current_time}.csv'), encoding='cp949', index=False)
        # if format == 'excel' :
        #     self.result.to_excel(os.path.join(self.folder_path, f'결과{current_time}.xlsx'), encoding='cp949', index=False)
        

    def open_folder(self):
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
        os.startfile(self.folder_path)  # For Windows


    class Worker(QThread) :
        progressChanged = Signal(int)
        def __init__(self, parent) :
            super().__init__(parent)
            self.parent = parent
        
        def run(self):
            self.parent.result = self.parent.naver.fetch(
                complexNos=[int(id) for id in self.parent.ids],
                tradeType=self.parent.tradeType,
                areaNos='',
                page=1,
                rentPriceMin=self.parent.minPrice,
                rentPriceMax=self.parent.maxPrice,
                priceMin=self.parent.minPrice,
                priceMax=self.parent.maxPrice,
                areaMin=self.parent.areaMin,
                areaMax=self.parent.areaMax,
                oldBuildYears=self.parent.oldBuildYears,
                recentlyBuildYears=self.parent.recentlyBuildYears,
                minHouseHoldCount=self.parent.minHouseHoldCount,
                maxHouseHoldCount=self.parent.maxHouseHoldCount,
                progressChanged=self.progressChanged,
            )