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
from CreateChainAlongGeo.ui import resources_rc

_ROOT_DIR = Path(__file__).parent.parent


class CreateChainAlongGeo(QtWidgets.QDialog):

    WINDOW_TITLE = "Create Chain Along Geo"

    def __init__(self, parent=None):
        super(CreateChainAlongGeo, self).__init__(parent)

        self.setWindowTitle(self.WINDOW_TITLE)
        # self.setMinimumSize(400, 300)
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
        # Geo Selection
        self.selection_title = QtWidgets.QLabel("Selection")
        self.selection_info_label = QtWidgets.QLabel("No geo loaded")

        self.load_selection_btn = QtWidgets.QPushButton("Load Selected Geo")
        self.load_selection_btn.clicked.connect(self.load_selection)

        self.selection_list = QtWidgets.QListWidget()
        self.selection_list.addItems(["Test 01", "Test 02", "Test 03"])
        self.selection_list.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        # self.selection_list.setMinimumHeight(120)

        self.clear_list_btn = QtWidgets.QPushButton("Clear List")
        self.clear_list_btn.clicked.connect(self.selection_list.clear)

        # Chain Settings
        self.chain_settings_title = QtWidgets.QLabel("Joint Settings")
        self.chain_count_label = QtWidgets.QLabel("Joint Count")

        self.chain_count_spinbox = QtWidgets.QSpinBox()
        self.chain_count_spinbox.setMinimum(3)
        self.chain_count_spinbox.setMaximum(999)
        self.chain_count_spinbox.setValue(10)

        self.reverse_direction_checkbox = QtWidgets.QCheckBox("Reverse Direction")

        # Snap Settings
        self.snap_settings_title = QtWidgets.QLabel("Snap Settings")
        self.snap_start_checkbox = QtWidgets.QCheckBox("Snap First Joint To Start")
        self.snap_start_checkbox.setChecked(True)

        self.snap_end_checkbox = QtWidgets.QCheckBox("Snap Last Joint To End")
        self.snap_end_checkbox.setChecked(True)

        # Misc Settings
        self.misc_settings_title = QtWidgets.QLabel("Misc Settings")

        self.create_curve_checkbox = QtWidgets.QCheckBox("Create Helper Curve")

        self.orient_joints_checkbox = QtWidgets.QCheckBox("Orient Joints")
        self.orient_joints_checkbox.setChecked(True)

        # Buttons
        self.create_btn = QtWidgets.QPushButton("Create Joint Chain(s)")
        self.create_btn.setObjectName("createButton")
        self.create_btn.clicked.connect(self.create_joint_chains)

        self.close_btn = QtWidgets.QPushButton("Close")
        self.close_btn.setObjectName("dangerButton")
        self.close_btn.clicked.connect(self.close)

    def build_layouts(self):
        # Selection Group
        selection_group = QtWidgets.QGroupBox()
        selection_layout = QtWidgets.QVBoxLayout(selection_group)

        selection_buttons = QtWidgets.QHBoxLayout()
        selection_buttons.addWidget(self.load_selection_btn, 3)
        selection_buttons.addWidget(self.clear_list_btn, 1  )

        selection_layout.addWidget(self.selection_title)
        selection_layout.addWidget(self.selection_info_label)
        selection_layout.addLayout(selection_buttons)
        selection_layout.addWidget(self.selection_list)

        # Joint Settings Group
        joint_group = QtWidgets.QGroupBox()
        joint_layout = QtWidgets.QFormLayout(joint_group)

        joint_layout.addRow(self.chain_settings_title)
        joint_layout.addRow(
            self.chain_count_label,
            self.chain_count_spinbox
        )

        joint_layout.addRow(self.reverse_direction_checkbox)

        # Snap Settings Group
        snap_group = QtWidgets.QGroupBox()
        snap_layout = QtWidgets.QVBoxLayout(snap_group)

        snap_layout.addWidget(self.snap_settings_title)
        snap_layout.addWidget(self.snap_start_checkbox)
        snap_layout.addWidget(self.snap_end_checkbox)

        # Misc Settings Group
        misc_group = QtWidgets.QGroupBox()
        misc_layout = QtWidgets.QVBoxLayout(misc_group)

        misc_layout.addWidget(self.misc_settings_title)
        misc_layout.addWidget(self.create_curve_checkbox)
        misc_layout.addWidget(self.orient_joints_checkbox)

        # Bottom Buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(self.create_btn)
        buttons_layout.addWidget(self.close_btn)

        # Add To Main Layout
        self._master_layout.addWidget(selection_group)
        self._master_layout.addWidget(joint_group)
        self._master_layout.addWidget(snap_group)
        self._master_layout.addWidget(misc_group)
        self._master_layout.addStretch()
        self._master_layout.addLayout(buttons_layout)

    # Logic
    def load_selection(self):
        selection = cmds.ls(sl=True)

        if not selection:
            self.selection_info_label.setText(
                "No object selected"
            )
            # self.selection_info_label.setObjectName("")
            return

        # Check if there is selection before clear
        self.selection_list.clear()

        self.selection_info_label.setText(
            "{} object(s) loaded".format(len(selection))
        )

        for obj in selection:
            self.selection_list.addItem(obj)

    def create_joint_chains(self):

        selected_objects = [
            self.selection_list.item(i).text()
            for i in range(self.selection_list.count())
        ]

        settings = {
            "joint_count": self.chain_count_spinbox.value(),
            "axis": self.axis_combo.currentText(),
            "reverse_direction": self.reverse_direction_checkbox.isChecked(),
            "snap_start": self.snap_start_checkbox.isChecked(),
            "snap_end": self.snap_end_checkbox.isChecked(),
            "force_center": self.center_chain_checkbox.isChecked(),
            "create_curve": self.create_curve_checkbox.isChecked(),
            "orient_joints": self.orient_joints_checkbox.isChecked(),
            "delete_history": self.delete_history_checkbox.isChecked(),
        }

        print("=" * 50)
        print("CREATE JOINT CHAINS")
        print("=" * 50)

        print("Selected Objects:")
        for obj in selected_objects:
            print(" - {}".format(obj))

        print("\nSettings:")
        for key, value in settings.items():
            print("{} : {}".format(key, value))

        print("\nTODO: Implement joint creation logic")

