import numpy as np
from PySide2 import QtWidgets

from maya import cmds


def load_selection(window: QtWidgets.QDialog):
    selection = cmds.ls(sl=True)
    # Check if there is selection before clear
    window.selection_list.clear()

    if not selection:
        window.selection_info_label.setText("No object selected !")
        window.selection_info_label.setObjectName("errorLabel")
    else:
        window.selection_info_label.setText("{} object(s) loaded".format(len(selection)))
        window.selection_info_label.setObjectName("successLabel")

        window.selection_list.addItems(selection)

    refresh_widget_style(window.selection_info_label)


def clear_list(window: QtWidgets.QDialog):
    window.selection_list.clear()

    window.selection_info_label.setText("No geo loaded")
    window.selection_info_label.setObjectName("No geo loaded")

    refresh_widget_style(window.selection_info_label)


def refresh_widget_style(widget: QtWidgets.QWidget):
    widget.style().unpolish(widget)
    widget.style().polish(widget)


def create_joint_chains(window):
    selected_objects = [
        window.selection_list.item(i).text()
        for i in range(window.selection_list.count())
    ]

    settings = {
        "joint_count": window.chain_count_spinbox.value(),
        "reverse_direction": window.reverse_direction_checkbox.isChecked(),
        "snap_start": window.snap_start_checkbox.isChecked(),
        "snap_end": window.snap_end_checkbox.isChecked(),
        "orient_joints": window.orient_joints_checkbox.isChecked(),
    }

    print("=" * 50)
    print("CREATE JOINT CHAINS")
    print("=" * 50)

    print("Settings:")
    for key, value in settings.items():
        print("{} : {}".format(key, value))

    print("\nSelected Objects:")

    cmds.undoInfo(openChunk=True)
    for obj in selected_objects:
        print(" - {}".format(obj))
        create_joint_chain_centerline(
            obj,
            joint_count=settings["joint_count"],
            reverse_direction=settings["reverse_direction"]
        )
    cmds.undoInfo(closeChunk=True)


def create_joint_chain_centerline(obj, joint_count=8, slice_count=30, slice_thickness=0.1, reverse_direction=False):
    """
    Create a joint chain following the centerline of a cylindrical-like mesh.

    :param obj: Mesh name
    :param joint_count: Number of joints
    :param slice_count: Number of slices along axis
    :param slice_thickness: Thickness of each slice (normalized)
    :param reverse_direction: Reverse the chain direction
    """

    if not cmds.objExists(obj):
        raise RuntimeError("Object does not exist.")

    # --- Get vertices
    verts = cmds.ls(f"{obj}.vtx[*]", flatten=True)
    points = np.array([cmds.xform(v, q=True, ws=True, t=True) for v in verts])

    # --- PCA for main axis
    centroid = np.mean(points, axis=0)
    centered = points - centroid
    cov = np.cov(centered.T)
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    axis = eigenvectors[:, np.argmax(eigenvalues)]
    axis = axis / np.linalg.norm(axis)

    # --- Project points on axis
    projections = np.dot(centered, axis)
    min_p, max_p = projections.min(), projections.max()

    slice_positions = np.linspace(min_p, max_p, slice_count)

    centers = []

    # --- Slice and compute local centers
    for sp in slice_positions:
        mask = np.abs(projections - sp) < (max_p - min_p) * slice_thickness
        slice_pts = points[mask]

        if len(slice_pts) < 10:
            continue

        local_center = np.mean(slice_pts, axis=0)
        centers.append(local_center)

    centers = np.array(centers)

    if len(centers) < 2:
        cmds.error("Not enough valid slices to build centerline.")

    # --- Resample to joint_count
    # cumulative distance
    dists = np.cumsum([0] + [np.linalg.norm(centers[i] - centers[i - 1]) for i in range(1, len(centers))])
    total_len = dists[-1]

    target_dists = np.linspace(0, total_len, joint_count)

    sampled_points = []

    for td in target_dists:
        idx = np.searchsorted(dists, td)

        if idx == 0:
            sampled_points.append(centers[0])
        elif idx >= len(centers):
            sampled_points.append(centers[-1])
        else:
            t = (td - dists[idx - 1]) / (dists[idx] - dists[idx - 1])
            p = centers[idx - 1] * (1 - t) + centers[idx] * t
            sampled_points.append(p)

    if reverse_direction:
        sampled_points.reverse()

    # --- Create joints
    joints = []
    for i, p in enumerate(sampled_points):
        j = cmds.createNode("joint", ss=True)
        name = f"{obj}_{i + 1:02d}_Jnt"
        cmds.rename(j, name)

        cmds.xform(name, t=p.tolist(), ws=True)
        if joints:
            cmds.parent(name, joints[-1])
        joints.append(name)

    return joints

