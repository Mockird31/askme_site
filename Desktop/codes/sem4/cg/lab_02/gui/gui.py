# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1024, 640)
        self.horizontalLayout_5 = QHBoxLayout(Widget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.dx_line = QLineEdit(Widget)
        self.dx_line.setObjectName(u"dx_line")

        self.horizontalLayout.addWidget(self.dx_line)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Widget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.dy_line = QLineEdit(Widget)
        self.dy_line.setObjectName(u"dy_line")

        self.horizontalLayout_2.addWidget(self.dy_line)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.btn_move = QPushButton(Widget)
        self.btn_move.setObjectName(u"btn_move")

        self.verticalLayout_2.addWidget(self.btn_move)


        self.verticalLayout_5.addLayout(self.verticalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(Widget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.angle_edit = QLineEdit(Widget)
        self.angle_edit.setObjectName(u"angle_edit")

        self.horizontalLayout_3.addWidget(self.angle_edit)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.btn_rotate = QPushButton(Widget)
        self.btn_rotate.setObjectName(u"btn_rotate")

        self.verticalLayout_3.addWidget(self.btn_rotate)


        self.verticalLayout_5.addLayout(self.verticalLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Widget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.coef_edit = QLineEdit(Widget)
        self.coef_edit.setObjectName(u"coef_edit")

        self.horizontalLayout_4.addWidget(self.coef_edit)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.btn_scale = QPushButton(Widget)
        self.btn_scale.setObjectName(u"btn_scale")

        self.verticalLayout_4.addWidget(self.btn_scale)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.btn_reset = QPushButton(Widget)
        self.btn_reset.setObjectName(u"btn_reset")

        self.verticalLayout_5.addWidget(self.btn_reset)


        self.horizontalLayout_5.addLayout(self.verticalLayout_5)

        self.graphicsView = QGraphicsView(Widget)
        self.graphicsView.setObjectName(u"graphicsView")

        self.horizontalLayout_5.addWidget(self.graphicsView)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 5)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.label.setText(QCoreApplication.translate("Widget", u"dx:", None))
        self.dx_line.setText("")
        self.label_2.setText(QCoreApplication.translate("Widget", u"dy:", None))
        self.btn_move.setText(QCoreApplication.translate("Widget", u"\u041f\u0435\u0440\u0435\u043c\u0435\u0441\u0442\u0438\u0442\u044c", None))
        self.label_3.setText(QCoreApplication.translate("Widget", u"\u0423\u0433\u043e\u043b:", None))
        self.btn_rotate.setText(QCoreApplication.translate("Widget", u"\u041f\u043e\u0432\u0435\u043d\u0443\u0442\u044c", None))
        self.label_4.setText(QCoreApplication.translate("Widget", u"\u041a\u043e\u044d\u0444:", None))
        self.btn_scale.setText(QCoreApplication.translate("Widget", u"\u041c\u0430\u0441\u0448\u0442\u0430\u0431\u0438\u0440\u043e\u0432\u0430\u0442\u044c", None))
        self.btn_reset.setText(QCoreApplication.translate("Widget", u"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c", None))
    # retranslateUi

