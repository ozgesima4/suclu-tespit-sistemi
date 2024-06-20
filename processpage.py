from PyQt5 import QtCore, QtGui, QtWidgets
from addperson import Ui_ADDPERSON, ADDPERSON
from main import FaceRecognition
import cv2
import time
import face_recognition
import numpy as np
import os


class Ui_mainpage(object):
    def yeniSayfa(self):
        self.add_person_window = ADDPERSON()
        self.add_person_window.show()

    def baslama(self):
        fr = FaceRecognition()  # FaceRecognition sınıfını doğru bir şekilde oluşturuyoruz
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 60)  # Kamera FPS'sini ayarla
        pTime = 0
        while True:
            success, img = cap.read()

            # Yüz tanıma
            fr.run_face_recognition(img)
            face_locations = fr.face_locations
            face_names = fr.face_names

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.putText(img, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 2)

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
            cv2.imshow("Image", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):  # q tuşuna basıldığında döngüyü kır
                break

        cap.release()
        cv2.destroyAllWindows()

    def setupUi(self, mainpage):
        mainpage.setObjectName("mainpage")
        mainpage.resize(634, 332)
        self.widget = QtWidgets.QWidget(mainpage)
        self.widget.setGeometry(QtCore.QRect(70, 40, 511, 231))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 511, 231))
        self.label.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 98, 112, 255), stop:1 rgba(255,107, 107, 255));\n"
"border-radius:25px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.sahis_ekleme = QtWidgets.QPushButton(self.widget)
        self.sahis_ekleme.setGeometry(QtCore.QRect(10, 20, 241, 191))

        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(19)
        font.setItalic(True)
        font.setUnderline(True)
        self.sahis_ekleme.setFont(font)
        self.sahis_ekleme.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:2px solid rgba(0,0,0,50);\n"
"\n"
"")
        self.sahis_ekleme.setObjectName("sahis_ekleme")
        self.sahis_ekleme.clicked.connect(self.yeniSayfa)
        self.isleme_baslama = QtWidgets.QPushButton(self.widget)
        self.isleme_baslama.setGeometry(QtCore.QRect(260, 20, 241, 191))
        self.isleme_baslama.clicked.connect(self.baslama)

        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(19)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(50)
        self.isleme_baslama.setFont(font)
        self.isleme_baslama.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"border:2px solid rgba(0,0,0,50);\n"
"\n"
"")
        self.isleme_baslama.setObjectName("isleme_baslama")

        self.retranslateUi(mainpage)
        QtCore.QMetaObject.connectSlotsByName(mainpage)

    def retranslateUi(self, mainpage):
        _translate = QtCore.QCoreApplication.translate
        mainpage.setWindowTitle(_translate("mainpage", "Form"))
        self.sahis_ekleme.setText(_translate("mainpage", "ADD NEW PERSON"))
        self.isleme_baslama.setText(_translate("mainpage", "START"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainpage = QtWidgets.QWidget()
    ui = Ui_mainpage()
    ui.setupUi(mainpage)
    mainpage.show()
    sys.exit(app.exec_())
