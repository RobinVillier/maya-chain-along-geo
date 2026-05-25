# -*- coding: utf-8 -*-
"""
Joint Chain Tool UI for Autodesk Maya
PySide2 interface only (no joint creation logic yet)

Author: Robin Villier
"""

from pathlib import Path

from maya import cmds

from PySide2 import QtWidgets, QtCore, QtGui
from CreateChainAlongGeo.widgets.custom_widget import CustomWidget

from CreateChainAlongGeo.core import load
from CreateChainAlongGeo.core import maya_utils as mu
from CreateChainAlongGeo.ui import resources_rc

_ROOT_DIR = Path(__file__).parent.parent


class CreateChainAlongGeo(QtWidgets.QDialog):

    WINDOW_TITLE = "Create Chain Along Geo"

    def __init__(self, parent=None):
        super(CreateChainAlongGeo, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.resize(0, 700)
        self.setWindowFlags(QtCore.Qt.Window)
        # self.setWindowIcon(QtGui.QIcon(":icon.png"))

        self._master_layout = QtWidgets.QVBoxLayout(self)
        self._master_layout.setContentsMargins(10, 10, 10, 10)
        self._master_layout.setSpacing(10)
        self._master_layout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        stylesheet = load.load_stylesheet(f"{_ROOT_DIR}/resources/styles/style.qss")
        self.setStyleSheet(stylesheet)

        self.build_widgets()
        self.build_layouts()

    def build_widgets(self):
        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                             QtWidgets.QSizePolicy.Preferred)

        # Widget Description
        self.title_description_label = QtWidgets.QLabel("Description")
        self.title_description_label.setObjectName("sectionTitle")
        self.description_label = QtWidgets.QLabel("This tool creates a chain along the loaded geometries center-lines.")
        self.description_label.setWordWrap(True)

        # Geo Selection
        self.selection_title = QtWidgets.QLabel("1. Selection")
        self.selection_title.setObjectName("sectionTitle")
        self.selection_info_label = QtWidgets.QLabel("No geo loaded")

        self.load_selection_btn = QtWidgets.QPushButton("Load Selected Geo")
        self.load_selection_btn.clicked.connect(lambda: mu.load_selection(self))

        self.selection_list = QtWidgets.QListWidget()
        self.selection_list.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)

        self.clear_list_btn = QtWidgets.QPushButton("Clear List")
        self.clear_list_btn.clicked.connect(lambda: mu.clear_list(self))

        # Chain Settings
        self.chain_settings_title = QtWidgets.QLabel("2. Chain Settings")
        self.chain_settings_title.setObjectName("sectionTitle")
        self.chain_count_label = QtWidgets.QLabel("Joint Count")

        self.chain_count_spinbox = QtWidgets.QSpinBox()
        self.chain_count_spinbox.setMinimum(3)
        self.chain_count_spinbox.setMaximum(999)
        self.chain_count_spinbox.setValue(10)

        self.reverse_direction_checkbox = QtWidgets.QCheckBox("Reverse Direction")

        # Snap Settings
        self.snap_settings_title = QtWidgets.QLabel("3. Snap Settings")
        self.snap_settings_title.setObjectName("sectionTitle")
        self.snap_start_checkbox = QtWidgets.QCheckBox("Snap First Joint To Start")
        self.snap_start_checkbox.setChecked(True)

        self.snap_end_checkbox = QtWidgets.QCheckBox("Snap Last Joint To End")
        self.snap_end_checkbox.setChecked(False)

        # Orient Settings
        self.orient_settings_title = QtWidgets.QLabel("4. Orient Settings")
        self.orient_settings_title.setObjectName("sectionTitle")

        self.orient_joints_checkbox = QtWidgets.QCheckBox("Orient Joints")
        self.orient_joints_checkbox.setChecked(True)

        axis = ["X", "Y", "Z"]

        self.forward_axis_title = QtWidgets.QLabel("Forward Axis")
        self.forward_axis_cbb = QtWidgets.QComboBox()
        self.forward_axis_cbb.addItems(axis)

        self.up_axis_title = QtWidgets.QLabel("Up Axis")
        self.up_axis_cbb = QtWidgets.QComboBox()
        self.up_axis_cbb.addItems(axis)
        self.up_axis_cbb.setCurrentIndex(1)

        # Buttons
        self.create_btn = QtWidgets.QPushButton("Create Joint Chain(s)")
        self.create_btn.setObjectName("createButton")
        self.create_btn.clicked.connect(lambda: mu.create_joint_chains(self))

        self.close_btn = QtWidgets.QPushButton("Close")
        self.close_btn.setObjectName("dangerButton")
        self.close_btn.clicked.connect(self.close)

    def build_layouts(self):
        # Description Group
        description_group = QtWidgets.QGroupBox()
        description_layout = QtWidgets.QVBoxLayout(description_group)

        description_layout.addWidget(self.title_description_label)
        description_layout.addWidget(self.description_label)

        # Selection Group
        selection_group = QtWidgets.QGroupBox()
        selection_layout = QtWidgets.QVBoxLayout(selection_group)

        selection_buttons = QtWidgets.QHBoxLayout()
        selection_buttons.addWidget(self.load_selection_btn, 3)
        selection_buttons.addWidget(self.clear_list_btn, 1)

        selection_layout.addWidget(self.selection_title)
        selection_layout.addWidget(self.selection_info_label)
        selection_layout.addLayout(selection_buttons)
        selection_layout.addWidget(self.selection_list)

        # Chain Settings Group
        chain_group = QtWidgets.QGroupBox()

        reverse_chain_layout = QtWidgets.QGridLayout()
        reverse_chain_layout.addWidget(self.chain_count_label, 0, 0)
        reverse_chain_layout.addWidget(self.spacer, 0, 1)
        reverse_chain_layout.addWidget(self.chain_count_spinbox, 0, 2)

        reverse_chain_layout.setColumnStretch(1, 1)

        join_vbox_layout = QtWidgets.QVBoxLayout(chain_group)
        join_vbox_layout.addWidget(self.chain_settings_title)
        join_vbox_layout.addLayout(reverse_chain_layout)
        join_vbox_layout.addWidget(self.reverse_direction_checkbox)

        # Snap Settings Group
        snap_group = QtWidgets.QGroupBox()
        snap_layout = QtWidgets.QVBoxLayout(snap_group)

        snap_layout.addWidget(self.snap_settings_title)
        snap_layout.addWidget(self.snap_start_checkbox)
        snap_layout.addWidget(self.snap_end_checkbox)

        # Orient Settings Group
        orient_group = QtWidgets.QGroupBox()

        forward_axis_layout = QtWidgets.QGridLayout()
        forward_axis_layout.addWidget(self.forward_axis_title, 0, 0)
        forward_axis_layout.addWidget(self.spacer, 0, 1)
        forward_axis_layout.addWidget(self.forward_axis_cbb, 0, 2)

        forward_axis_layout.setColumnStretch(1, 1)

        up_axis_layout = QtWidgets.QGridLayout()
        up_axis_layout.addWidget(self.up_axis_title, 0, 0)
        up_axis_layout.addWidget(self.spacer, 0, 1)
        up_axis_layout.addWidget(self.up_axis_cbb, 0, 2)

        up_axis_layout.setColumnStretch(1, 1)

        orient_vbox_layout = QtWidgets.QVBoxLayout(orient_group)
        orient_vbox_layout.addWidget(self.orient_settings_title)
        orient_vbox_layout.addLayout(forward_axis_layout)
        orient_vbox_layout.addLayout(up_axis_layout)

        # Bottom Buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.create_btn, 3)
        buttons_layout.addWidget(self.close_btn, 1)

        # Add To Main Layout
        self._master_layout.addWidget(description_group)
        self._master_layout.addWidget(selection_group)
        self._master_layout.addWidget(chain_group)
        self._master_layout.addWidget(snap_group)
        self._master_layout.addWidget(orient_group)
        self._master_layout.addLayout(buttons_layout)

