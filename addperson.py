import firebase_admin
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import os
from main import FaceRecognition
from firebase_admin import credentials, initialize_app, db
import face_recognition


class Ui_ADDPERSON(object):
    def setupUi(self, ADDPERSON):
        ADDPERSON.setObjectName("ADDPERSON")
        ADDPERSON.resize(710, 497)
        self.label = QtWidgets.QLabel(ADDPERSON)
        self.label.setGeometry(QtCore.QRect(360, -23, 681, 461))
        self.label.setStyleSheet("background-color:rgba(255,107,107,255);\n"
                                 "border-radius:20px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.addperson_buton = QtWidgets.QPushButton(ADDPERSON)
        self.addperson_buton.setGeometry(QtCore.QRect(390, 350, 241, 51))
        self.addperson_buton.setCheckable(True)
        self.addperson_buton.setObjectName("addperson_buton")

        self.persondate = QtWidgets.QDateEdit(ADDPERSON)
        self.persondate.setGeometry(QtCore.QRect(110, 290, 211, 21))
        self.persondate.setObjectName("persondate")
        self.name_textedit = QtWidgets.QLineEdit(ADDPERSON)
        self.name_textedit.setGeometry(QtCore.QRect(110, 70, 211, 31))
        self.name_textedit.setObjectName("name_textedit")
        self.surname_textedit = QtWidgets.QLineEdit(ADDPERSON)
        self.surname_textedit.setGeometry(QtCore.QRect(110, 130, 211, 31))
        self.surname_textedit.setObjectName("surname_textedit")
        self.adlabeli = QtWidgets.QLabel(ADDPERSON)
        self.adlabeli.setGeometry(QtCore.QRect(30, 80, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.adlabeli.setFont(font)
        self.adlabeli.setObjectName("adlabeli")
        self.soyadlabeli = QtWidgets.QLabel(ADDPERSON)
        self.soyadlabeli.setGeometry(QtCore.QRect(20, 140, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.soyadlabeli.setFont(font)
        self.soyadlabeli.setObjectName("soyadlabeli")
        self.idnumber_textedit = QtWidgets.QLineEdit(ADDPERSON)
        self.idnumber_textedit.setGeometry(QtCore.QRect(110, 190, 211, 31))
        self.idnumber_textedit.setObjectName("idnumber_textedit")
        self.label_2 = QtWidgets.QLabel(ADDPERSON)
        self.label_2.setGeometry(QtCore.QRect(20, 200, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(ADDPERSON)
        self.label_3.setGeometry(QtCore.QRect(20, 250, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gender_comboBox = QtWidgets.QComboBox(ADDPERSON)
        self.gender_comboBox.setGeometry(QtCore.QRect(110, 250, 211, 21))
        self.gender_comboBox.setObjectName("gender_comboBox")
        self.gender_comboBox.addItem("male")
        self.gender_comboBox.addItem("female")
        self.label_4 = QtWidgets.QLabel(ADDPERSON)
        self.label_4.setGeometry(QtCore.QRect(20, 300, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(ADDPERSON)
        QtCore.QMetaObject.connectSlotsByName(ADDPERSON)

    def retranslateUi(self, ADDPERSON):
        _translate = QtCore.QCoreApplication.translate
        self.addperson_buton.setText(_translate("ADDPERSON", "ADD NEW PERSON"))
        self.adlabeli.setText(_translate("ADDPERSON", "NAME:"))
        self.soyadlabeli.setText(_translate("ADDPERSON", "SURNAME:"))
        self.label_2.setText(_translate("ADDPERSON", "ID NUMBER:"))
        self.label_3.setText(_translate("ADDPERSON", "GENDER:"))
        self.label_4.setText(_translate("ADDPERSON", "BİRTHDAY:"))

    def updateUiWithNewPersonData(self, name, surname, id_number, gender, birthday):
        cred = credentials.Certificate("ServiseAccountKey.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": "https://facerecognitionrealtime-47eb1-default-rtdb.firebaseio.com/"})

        ref = db.reference("criminals")
        new_criminals_data = {
            "name": name + " " + surname,
            "id_number": id_number,
            "gender": gender,
            "birthday": birthday,
        }
        ref.push(new_criminals_data)
        print("Başarıyla kaydedildi.")


class ADDPERSON(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ADDPERSON()
        self.ui.setupUi(self)

        self.camera = cv2.VideoCapture(0)

        self.ui.addperson_buton.clicked.connect(self.save_image)

        self.update_frame()  # Kameradan ilk kareyi göstermek için update_frame fonksiyonunu çağır

    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(320, 240, QtCore.Qt.KeepAspectRatio)
            self.ui.label.setPixmap(QtGui.QPixmap.fromImage(p))  # Kameradan alınan görüntüyü QLabel üzerinde göster

            QtCore.QTimer.singleShot(1,
                                     self.update_frame)  # Bir sonraki kareyi almak için update_frame fonksiyonunu tekrar çağır
    def save_image(self):
        name = self.ui.name_textedit.text()
        surname = self.ui.surname_textedit.text()
        id_number = self.ui.idnumber_textedit.text()
        gender = self.ui.gender_comboBox.currentText()
        birthday = self.ui.persondate.date().toString("yyyy-MM-dd")

        if name == "" or surname == "" or id_number == "":
            QtWidgets.QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")
            return

        ret, frame = self.camera.read()
        if ret:
            # Yüz algılama işlemi
            face_locations = face_recognition.face_locations(frame)
            if len(face_locations) > 0:  # Yüz algılandıysa
                image_path = os.path.join("images", f"{name}.jpg")
                cv2.imwrite(image_path, frame)
                print(f"{name} adlı kişi kaydedildi.")
                # Update UI with new person data
                self.ui.updateUiWithNewPersonData(name, surname, id_number, gender, birthday)
            else:
                print("Yüz algılanamadı. Lütfen yüzünüzü kameraya gösterin.")



    def closeEvent(self, event):
        self.save_image()
        fr = FaceRecognition()
        fr.encode_faces()
        self.camera.release()
        cv2.destroyAllWindows()
        event.accept()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ADDPERSON()
    window.show()
    sys.exit(app.exec_())
