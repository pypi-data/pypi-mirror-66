# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sceneviewereditorwidget.ui'
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


class Ui_SceneviewerEditorWidget(object):
    def setupUi(self, SceneviewerEditorWidget):
        if not SceneviewerEditorWidget.objectName():
            SceneviewerEditorWidget.setObjectName(u"SceneviewerEditorWidget")
        SceneviewerEditorWidget.resize(227, 689)
        self.verticalLayout = QVBoxLayout(SceneviewerEditorWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.view_all_button = QPushButton(SceneviewerEditorWidget)
        self.view_all_button.setObjectName(u"view_all_button")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view_all_button.sizePolicy().hasHeightForWidth())
        self.view_all_button.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.view_all_button)

        self.perspective_checkbox = QCheckBox(SceneviewerEditorWidget)
        self.perspective_checkbox.setObjectName(u"perspective_checkbox")
        self.perspective_checkbox.setChecked(True)

        self.verticalLayout.addWidget(self.perspective_checkbox)

        self.view_angle_label = QLabel(SceneviewerEditorWidget)
        self.view_angle_label.setObjectName(u"view_angle_label")

        self.verticalLayout.addWidget(self.view_angle_label)

        self.view_angle = QLineEdit(SceneviewerEditorWidget)
        self.view_angle.setObjectName(u"view_angle")
        sizePolicy.setHeightForWidth(self.view_angle.sizePolicy().hasHeightForWidth())
        self.view_angle.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.view_angle)

        self.eye_point_label = QLabel(SceneviewerEditorWidget)
        self.eye_point_label.setObjectName(u"eye_point_label")

        self.verticalLayout.addWidget(self.eye_point_label)

        self.eye_point = QLineEdit(SceneviewerEditorWidget)
        self.eye_point.setObjectName(u"eye_point")
        sizePolicy.setHeightForWidth(self.eye_point.sizePolicy().hasHeightForWidth())
        self.eye_point.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.eye_point)

        self.lookat_point_label = QLabel(SceneviewerEditorWidget)
        self.lookat_point_label.setObjectName(u"lookat_point_label")

        self.verticalLayout.addWidget(self.lookat_point_label)

        self.lookat_point = QLineEdit(SceneviewerEditorWidget)
        self.lookat_point.setObjectName(u"lookat_point")
        sizePolicy.setHeightForWidth(self.lookat_point.sizePolicy().hasHeightForWidth())
        self.lookat_point.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.lookat_point)

        self.up_vector_label = QLabel(SceneviewerEditorWidget)
        self.up_vector_label.setObjectName(u"up_vector_label")

        self.verticalLayout.addWidget(self.up_vector_label)

        self.up_vector = QLineEdit(SceneviewerEditorWidget)
        self.up_vector.setObjectName(u"up_vector")
        sizePolicy.setHeightForWidth(self.up_vector.sizePolicy().hasHeightForWidth())
        self.up_vector.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.up_vector)

        self.clipping_planes_groupbox = QGroupBox(SceneviewerEditorWidget)
        self.clipping_planes_groupbox.setObjectName(u"clipping_planes_groupbox")
        sizePolicy.setHeightForWidth(self.clipping_planes_groupbox.sizePolicy().hasHeightForWidth())
        self.clipping_planes_groupbox.setSizePolicy(sizePolicy)
        self.clipping_planes_groupbox.setMinimumSize(QSize(0, 0))
        self.formLayout = QFormLayout(self.clipping_planes_groupbox)
        self.formLayout.setObjectName(u"formLayout")
        self.near_clipping_label = QLabel(self.clipping_planes_groupbox)
        self.near_clipping_label.setObjectName(u"near_clipping_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.near_clipping_label)

        self.far_clipping_label = QLabel(self.clipping_planes_groupbox)
        self.far_clipping_label.setObjectName(u"far_clipping_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.far_clipping_label)

        self.near_clipping_slider = QSlider(self.clipping_planes_groupbox)
        self.near_clipping_slider.setObjectName(u"near_clipping_slider")
        self.near_clipping_slider.setMaximum(10000)
        self.near_clipping_slider.setPageStep(100)
        self.near_clipping_slider.setTracking(True)
        self.near_clipping_slider.setOrientation(Qt.Horizontal)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.near_clipping_slider)

        self.far_clipping_slider = QSlider(self.clipping_planes_groupbox)
        self.far_clipping_slider.setObjectName(u"far_clipping_slider")
        self.far_clipping_slider.setMaximum(10000)
        self.far_clipping_slider.setPageStep(100)
        self.far_clipping_slider.setOrientation(Qt.Horizontal)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.far_clipping_slider)


        self.verticalLayout.addWidget(self.clipping_planes_groupbox)

        self.background_colour_label = QLabel(SceneviewerEditorWidget)
        self.background_colour_label.setObjectName(u"background_colour_label")

        self.verticalLayout.addWidget(self.background_colour_label)

        self.background_colour = QLineEdit(SceneviewerEditorWidget)
        self.background_colour.setObjectName(u"background_colour")
        sizePolicy.setHeightForWidth(self.background_colour.sizePolicy().hasHeightForWidth())
        self.background_colour.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.background_colour)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(SceneviewerEditorWidget)
        self.view_all_button.clicked.connect(SceneviewerEditorWidget.viewAll)
        self.perspective_checkbox.clicked.connect(SceneviewerEditorWidget.perspectiveStateChanged)
        self.view_angle.editingFinished.connect(SceneviewerEditorWidget.viewAngleEntered)
        self.eye_point.editingFinished.connect(SceneviewerEditorWidget.eyePointEntered)
        self.lookat_point.editingFinished.connect(SceneviewerEditorWidget.lookatPointEntered)
        self.up_vector.editingFinished.connect(SceneviewerEditorWidget.upVectorEntered)
        self.near_clipping_slider.valueChanged.connect(SceneviewerEditorWidget.nearClippingChanged)
        self.far_clipping_slider.valueChanged.connect(SceneviewerEditorWidget.farClippingChanged)
        self.background_colour.editingFinished.connect(SceneviewerEditorWidget.backgroundColourEntered)

        QMetaObject.connectSlotsByName(SceneviewerEditorWidget)
    # setupUi

    def retranslateUi(self, SceneviewerEditorWidget):
        SceneviewerEditorWidget.setWindowTitle(QCoreApplication.translate("SceneviewerEditorWidget", u"Sceneviewer Editor", None))
        self.view_all_button.setText(QCoreApplication.translate("SceneviewerEditorWidget", u"View All", None))
        self.perspective_checkbox.setText(QCoreApplication.translate("SceneviewerEditorWidget", u"Perspective projection", None))
        self.view_angle_label.setText(QCoreApplication.translate("SceneviewerEditorWidget", u"View angle:", None))
        self.eye_point_label.setText(QCoreApplication.translate("SceneviewerEditorWidget", u"Eye point:", None))
        self.lookat_point_label.setText(QCoreApplication.translate("SceneviewerEditorWidget", u"Look at point:", None))
        self.up_vector_label.setText(QCoreApplication.translate("SceneviewerEditorWidget", u"Up vector:", None))
        self.clipping_planes_groupbox.setTitle(QCoreApplication.translate("SceneviewerEditorWidget", u"Clipping planes:", None))
        self.near_clipping_label.setText(QCoreApplication.translate("SceneviewerEditorWidget", u"Near:", None))
        self.far_clipping_label.setText(QCoreApplication.translate("SceneviewerEditorWidget", u"Far:", None))
        self.background_colour_label.setText(QCoreApplication.translate("SceneviewerEditorWidget", u"Background colour R, G, B:", None))
    # retranslateUi

