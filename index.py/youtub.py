

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import os
from os import path
import sys
import pafy
import bitmath
import urllib.request


from main import Ui_MainWindow




class MainApp(QMainWindow , Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        

        self.setupUi(self)

        self.Handel_ui()

    def Handel_ui(self):
        self.setWindowTitle("Youtube_Doweloader")
        self.setFixedSize(452, 499)
        self.Handel_Buttons()

    def Handel_Buttons(self):
        self.pushButton3.clicked.connect(self.Get_Youtube_Video)
        self.pushButton7.clicked.connect(self.Dowenload_Youtube_Video)
        self.pushButton_2.clicked.connect(self.Save_Browse)

    def Save_Browse(self):
        save = QFileDialog.getExistingDirectory(self, "Select Dowenload Directory")
        self.lineEdit_2.setText(save)

    def Get_Youtube_Video(self, filepath=None):
                video_url = self.lineEdit.text()
                print(video_url)

                if video_url == '' :
                   QMessageBox.warning(self, "Data Error", "Provide a valid Video URL")

                else:
                    video = pafy.new(video_url)
                    print(video.title)
                    print(video.duration)
                    print(video.author)
                    print(video.length)
                    print(video.viewcount)
                    print(video.likes)
                    print(video.dislikes)

                    video_streams = video.videostreams
                    for stream in video_streams :

                        print(stream.get_filesize())
                        size = bitmath.Mb((stream.get_filesize()))
                        data = "{} {} {} {}".format(stream.mediatype , stream.extension , stream.quality , size)
                        self.comboBox.addItem(data)
                
    def Dowenload_Youtube_Video(self):

        video_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid Video URL or save location")

        else:
            video = pafy.new(video_url)
            video_stream = video.videostreams
            video_quality = self.comboBox.currentIndex()
            download = video_stream[video_quality].download(filepath=save_location, callback=self.Video_Progress)
            QMessageBox.information(self, "Download Completed", "The Download Completed Successfully ")

            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.progressBar.setValue(0)
    
        

    def Video_Progress(self, total, received, ratio, rate, time):
        read_data = received
        if total > 0:
            download_percentage = read_data * 100 / total
            self.progressBar.setValue(download_percentage)
            remaining_time = round(time / 60, 2)

            self.label_5.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
