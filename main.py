from PySide2 import QtWidgets
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance


def get_maya_main_window() -> QtWidgets.QWidget:
    ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QMainWindow)


def launch():
    from CreateChainAlongGeo.ui.main_window import CreateChainAlongGeo

    parent = get_maya_main_window()
    window = CreateChainAlongGeo(parent)
    window.show()
