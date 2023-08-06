# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sceneeditorwidget.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from graphicseditorwidget import GraphicsEditorWidget


class Ui_SceneEditorWidget(object):
    def setupUi(self, SceneEditorWidget):
        if not SceneEditorWidget.objectName():
            SceneEditorWidget.setObjectName(u"SceneEditorWidget")
        SceneEditorWidget.resize(227, 736)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SceneEditorWidget.sizePolicy().hasHeightForWidth())
        SceneEditorWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(SceneEditorWidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.graphics_listview = QListView(SceneEditorWidget)
        self.graphics_listview.setObjectName(u"graphics_listview")

        self.verticalLayout.addWidget(self.graphics_listview)

        self.frame = QFrame(SceneEditorWidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 7, 0, 7)
        self.add_graphics_combobox = QComboBox(self.frame)
        self.add_graphics_combobox.addItem("")
        self.add_graphics_combobox.addItem("")
        self.add_graphics_combobox.addItem("")
        self.add_graphics_combobox.addItem("")
        self.add_graphics_combobox.addItem("")
        self.add_graphics_combobox.addItem("")
        self.add_graphics_combobox.addItem("")
        self.add_graphics_combobox.addItem("")
        self.add_graphics_combobox.addItem("")
        self.add_graphics_combobox.addItem("")
        self.add_graphics_combobox.setObjectName(u"add_graphics_combobox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.add_graphics_combobox.sizePolicy().hasHeightForWidth())
        self.add_graphics_combobox.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.add_graphics_combobox)

        self.delete_graphics_button = QPushButton(self.frame)
        self.delete_graphics_button.setObjectName(u"delete_graphics_button")

        self.horizontalLayout.addWidget(self.delete_graphics_button)


        self.verticalLayout.addWidget(self.frame)

        self.graphics_editor = GraphicsEditorWidget(SceneEditorWidget)
        self.graphics_editor.setObjectName(u"graphics_editor")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.graphics_editor.sizePolicy().hasHeightForWidth())
        self.graphics_editor.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.graphics_editor)


        self.retranslateUi(SceneEditorWidget)
        self.graphics_listview.clicked.connect(SceneEditorWidget.graphicsListItemClicked)
        self.add_graphics_combobox.currentIndexChanged.connect(SceneEditorWidget.addGraphicsEntered)
        self.delete_graphics_button.clicked.connect(SceneEditorWidget.deleteGraphicsClicked)

        QMetaObject.connectSlotsByName(SceneEditorWidget)
    # setupUi

    def retranslateUi(self, SceneEditorWidget):
        SceneEditorWidget.setWindowTitle(QCoreApplication.translate("SceneEditorWidget", u"Scene Editor", None))
        self.add_graphics_combobox.setItemText(0, QCoreApplication.translate("SceneEditorWidget", u"Add...", None))
        self.add_graphics_combobox.setItemText(1, QCoreApplication.translate("SceneEditorWidget", u"---", None))
        self.add_graphics_combobox.setItemText(2, QCoreApplication.translate("SceneEditorWidget", u"point", None))
        self.add_graphics_combobox.setItemText(3, QCoreApplication.translate("SceneEditorWidget", u"node points", None))
        self.add_graphics_combobox.setItemText(4, QCoreApplication.translate("SceneEditorWidget", u"data points", None))
        self.add_graphics_combobox.setItemText(5, QCoreApplication.translate("SceneEditorWidget", u"element points", None))
        self.add_graphics_combobox.setItemText(6, QCoreApplication.translate("SceneEditorWidget", u"lines", None))
        self.add_graphics_combobox.setItemText(7, QCoreApplication.translate("SceneEditorWidget", u"surfaces", None))
        self.add_graphics_combobox.setItemText(8, QCoreApplication.translate("SceneEditorWidget", u"contours", None))
        self.add_graphics_combobox.setItemText(9, QCoreApplication.translate("SceneEditorWidget", u"streamlines", None))

        self.delete_graphics_button.setText(QCoreApplication.translate("SceneEditorWidget", u"Delete", None))
    # retranslateUi

