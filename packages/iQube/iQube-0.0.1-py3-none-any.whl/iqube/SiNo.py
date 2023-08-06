from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
import pyqtgraph as pg
from iqube.calculation import SpectrumAnalysis, path_to_data
import numpy as np
import csv
import glob
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Initiate Main Window of the Application
        MainWindow.setObjectName("SiNo")
        MainWindow.resize(1500, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Button to load the latest added file to the app
        self.Update_File_Button = QtWidgets.QPushButton("Latest File",self.centralwidget)
        self.Update_File_Button.setGeometry(QtCore.QRect(1350, 20, 100, 25))
        self.Update_File_Button.setObjectName("Update_File_Button")

        # Button to select specific file to add to the app
        self.Select_File_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Select_File_Button.setGeometry(QtCore.QRect(1350, 50, 100, 25))
        self.Select_File_Button.setObjectName("Select_File_Button")

        # Plotting Window
        self.graphicsView = pg.PlotWidget(self.centralwidget) # added
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 1300, 780))
        self.graphicsView.setObjectName("graphicsView")
        MainWindow.setCentralWidget(self.centralwidget)

        # Label to show Signal to Noise Ratio
        self.SNR_label = QtWidgets.QLabel('SignalNR:', self.centralwidget)
        self.SNR_label.setGeometry(QtCore.QRect(1305, 80, 180, 25))
        self.SNR_label.setObjectName("SNR_label")

        # Label to show Slope to Noise Ratio
        self.SlopeNR_label = QtWidgets.QLabel('SlopeNR:', self.centralwidget)
        self.SlopeNR_label.setGeometry(QtCore.QRect(1305, 100, 150, 25))
        self.SlopeNR_label.setObjectName("SlopeNR_label")

        # Selection Frame inside Ploting Window
        self.lr = pg.LinearRegionItem([500, 1000])
        self.lr.setZValue(-10)

        # Slider to regulate 3dB Frequency of Butterworth Filter
        self.p_slider = QtWidgets.QSlider(Qt.Horizontal, self.centralwidget)
        self.p_slider.setGeometry(QtCore.QRect(1400, 120, 90, 25))
        self.p_slider.setMinimum(1)
        self.p_slider.setMaximum(20)
        self.p = 5 # kHz
        self.p_slider.setValue(int(self.p))

        # Label for Slider to state 3dB Frequency of Butterworth Filter
        self.label_p = QtWidgets.QLabel("f [kHz]: %0.2f" % (self.p), self.centralwidget)
        self.label_p.setGeometry(QtCore.QRect(1305, 120, 80, 25))

        # Label and editable Line for Probe Beam Power
        self.Probe_label = QtWidgets.QLabel(r'Probe Beam Power [µW]:', self.centralwidget)
        self.Probe_label.setGeometry(QtCore.QRect(1305, 175, 190, 25))
        self.Probe_label.setObjectName("SNR_label")
        self.lineEdit_Probe = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Probe.setGeometry(QtCore.QRect(1305, 200, 190, 25))
        self.lineEdit_Probe.setObjectName("lineEdit_Probe")

        # Label and editable Line for Pump Beam Power
        self.Pump_label = QtWidgets.QLabel(r'Pump Beam Power [µW]:', self.centralwidget)
        self.Pump_label.setGeometry(QtCore.QRect(1305, 225, 190, 25))
        self.Pump_label.setObjectName("SNR_label")
        self.lineEdit_Pump = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Pump.setGeometry(QtCore.QRect(1305, 250, 190, 25))
        self.lineEdit_Pump.setObjectName("lineEdit_Pump")

        # Label and editable Line for Photodiode Power
        self.PD_label = QtWidgets.QLabel(r'Photodiode Power [µW]:', self.centralwidget)
        self.PD_label.setGeometry(QtCore.QRect(1305, 275, 190, 25))
        self.PD_label.setObjectName("SNR_label")
        self.lineEdit_PD = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_PD.setGeometry(QtCore.QRect(1305, 300, 190, 25))
        self.lineEdit_PD.setObjectName("lineEdit_PD")

        # Label and editable Line for Notes
        self.Notes_label = QtWidgets.QLabel(r'Notes:', self.centralwidget)
        self.Notes_label.setGeometry(QtCore.QRect(1305, 325, 190, 25))
        self.Notes_label.setObjectName("Notes_label")
        self.lineEdit_Notes = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_Notes.setGeometry(QtCore.QRect(1305, 350, 190, 25))
        self.lineEdit_Notes.setObjectName("lineEdit_Notes")

        # Button to add Data as Line in document.csv
        self.Add_Button = QtWidgets.QPushButton("Add to CSV", self.centralwidget)
        self.Add_Button.setGeometry(QtCore.QRect(1350, 400, 100, 25))
        self.Add_Button.setObjectName("Add_Button")
        #self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        #self.listWidget.setGeometry(QtCore.QRect(1305, 225, 190, 300))
        #self.listWidget.setObjectName("listWidget")



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect Widgets to functions
        self.Select_File_Button.clicked.connect(self.setImage)
        self.Update_File_Button.clicked.connect(self.setImage_update)
        self.lr.sigRegionChanged.connect(self.update_SNR_label)
        self.p_slider.valueChanged.connect(self.p_valuechange)
        self.Add_Button.clicked.connect(self.addItem)
        self.fileName = None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Select_File_Button.setText(_translate("MainWindow", "Select File"))

    def setImage(self):
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select File", "",
                                                            "JSON-Files (*.json)")  # Ask for file
        if self.fileName:  # If the user gives a file
            self.data, self.signal, self.noise = path_to_data(self.fileName, self.p)
            self.update_plot()
            self.update_SNR_label()

    def setImage_update(self):

        list_of_files = glob.glob('Data/*.json')  # all json files
        self.fileName = max(list_of_files, key=os.path.getctime) # latest json file
        self.data,self.signal,self.noise = path_to_data(self.fileName, self.p)
        self.update_plot()
        self.update_SNR_label()

    def update_SNR_label(self):
        [self.l1,self.l2] = list(self.lr.getRegion())
        self.SNR, self.SlopeNR = SpectrumAnalysis(self.data).calc_snr(self.signal,self.noise,self.l1,self.l2)
        self.SNR_dB, self.SlopeNR_dB = 20*np.log10(self.SNR), 20*np.log10(self.SlopeNR)
        self.SNR_label.setText('SignalNR: %0.2f = %0.2f dB'%(self.SNR,self.SNR_dB))
        self.SlopeNR_label.setText('SlopeNR: %0.2f' % (self.SlopeNR))

    def p_valuechange(self):
        self.p = float(self.p_slider.value())
        if self.fileName:
            self.f_ny = 59/2*np.size(self.data)/1000
            self.signal, self.noise = SpectrumAnalysis(self.data).filtering(self.f_ny,self.p)
            self.update_plot()
            self.update_SNR_label()
        self.label_p.setText("f [kHz]: %0.2f" % (self.p))

    def update_plot(self):
        self.graphicsView.clear()# added
        self.graphicsView.addItem(self.lr) # added  # added
        data = self.data
        noise = self.noise
        signal = self.signal# added
        self.graphicsView.plot(data)
        self.graphicsView.plot(noise,pen = pg.mkPen(color=(255, 255, 0)))
        self.graphicsView.plot(signal,pen = pg.mkPen(color=(255, 0, 0), width = 3))# added
        self.graphicsView.setAlignment(QtCore.Qt.AlignCenter)  # Align the label to center

    def addItem(self):
        self.P_Probe = self.lineEdit_Probe.text()
        self.P_Pump = self.lineEdit_Pump.text()
        self.P_PD = self.lineEdit_PD.text()
        self.Notes = self.lineEdit_Notes.text()
        myCsvRow = [self.fileName, self.l1, self.l2,self.SNR,self.SlopeNR, self.p, self.P_Probe, self.P_Pump, self.P_PD, self.Notes]  # Specify Values
        with open(r'Data/document.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(myCsvRow)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
