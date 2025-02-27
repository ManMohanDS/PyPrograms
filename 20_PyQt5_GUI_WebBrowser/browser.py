import sys
from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets  import QWebEngineView
 
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
 
try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)
 
class BrowserDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1024, 768)
        self.qwebview = QWebEngineView(Dialog)
        self.qwebview.setGeometry(QtCore.QRect(0, 50, 1020, 711))
        self.qwebview.setObjectName(_fromUtf8("kwebview"))
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 20, 1000, 25))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
 
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
 
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Browser", "Browser", None))