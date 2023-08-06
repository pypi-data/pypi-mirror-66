"""This module contains Viewer, a simpe and efficient cross-platform 3D viewer."""

from .viewer_base import ViewerBase
from .viewer_proxy import ViewerAppProxy

__all__ = ('Viewer')


class Viewer(ViewerBase):
    """A Panda3D based viewer."""

    def __init__(self, window_title='PandaViewer', window_type='onscreen', antialiasing=0):
        """Open a window, setup a scene.

        Keyword Arguments:
            window_title {str} -- window title (default: {'PandaViewer'})
            window_type {str} -- window type, one of onscreen, offscreen (default: {'onscreen'})
            antialiasing {int} -- anti-alising multisamples 0,2,4... (default: {0})
        """
        # run the viewer application in a new process
        self._app = ViewerAppProxy(window_title, window_type, antialiasing)

    def join(self):
        """Run the application until a user close the main window."""
        self._app.join()

    def stop(self):
        """Stop the application."""
        self._app.stop()

    def append_group(self, root_path, remove_if_exists=True):
        """Append a root node for a group of nodes.

        Arguments:
            root_path {str} -- path to the group's root node

        Keyword Arguments:
            remove_if_exists {bool} -- remove group with root_path if exists (default: {True})
        """
        self._app.append_group(root_path)

    def remove_group(self, root_path):
        """Remove a group of nodes.

        Arguments:
            root_path {str} -- path to the group's root node
        """
        self._app.remove_group(root_path)

    def show_group(self, root_path, show):
        """Turn a node group rendering on or off.

        Arguments:
            root_path {str} -- path to the group's root node
            show {bool} -- flag
        """
        self._app.show_group(root_path, show)

    def move_nodes(self, root_path, name_pose_dict):
        """Set a pose for nodes within a group.

        Arguments:
            root_path {str} -- path to the group's root node
            name_pose_dict {dict} -- {node_name : (pos, quat)} dictionary
        """
        self._app.move_nodes(root_path, name_pose_dict)

    def append_mesh(self, root_path, name, mesh_path, scale):
        """Append a mesh node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            mesh_path {str} -- path to the mesh file on disk
            scale {Vec3} -- mesh scale
        """
        self._app.append_mesh(root_path, name, mesh_path, scale)

    def append_capsule(self, root_path, name, radius, length):
        """Append a capsule primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            radius {flaot} -- capsule radius
            length {flaot} -- capsule length
        """
        self._app.append_capsule(root_path, name, radius, length)

    def append_cylinder(self, root_path, name, radius, length):
        """Append a cylinder primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            radius {flaot} -- cylinder radius
            length {flaot} -- cylinder length
        """
        self._app.append_cylinder(root_path, name, radius, length)

    def append_box(self, root_path, name, size):
        """Append a box primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            size {Vec3} -- box size
        """
        self._app.append_box(root_path, name, size)

    def append_sphere(self, root_path, name, radius):
        """Append a sphere primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            radius {flaot} -- sphere radius
        """
        self._app.append_sphere(root_path, name, radius)

    def set_material(self, root_path, name, color_rgba, texture_path=''):
        """Override material of a node.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            color {Vec4} -- color RGBA

        Keyword Arguments:
            texture_path {str} -- path to the texture file on disk (default: {''})
        """
        self._app.set_material(root_path, name, color_rgba, texture_path)

    def reset_camera(self, pos, look_at):
        """Reset camera position.

        Arguments:
            pos {Vec3} -- camera position
            look_at {Vec3} -- camera target point
        """
        self._app.reset_camera(pos, look_at)

    def enable_lights(self, enable):
        """Turn lighting on or off.

        Arguments:
            enable {bool} -- flag
        """
        self._app.enable_lights(enable)

    def enable_light(self, index, enable):
        """Turn a light on or off.

        Arguments:
            index {int} -- light index
            enable {bool} -- flag
        """
        self._app.enable_light(index, enable)

    def enable_shadow(self, enable):
        """Turn shadows rendering on or off.

        Arguments:
            enable {bool} -- flag
        """
        self._app.enable_shadow(enable)

    def show_axes(self, show):
        """Turn the axes rendering on or off.

        Arguments:
            show {bool} -- flag
        """
        self._app.show_axes(show)

    def show_grid(self, show):
        """Turn the grid rendering on or off.

        Arguments:
            show {bool} -- flag
        """
        self._app.show_grid(show)

    def save_screenshot(self, filename):
        """Capture a screenshot from the main window and write it to disk.

        Arguments:
            filename {str} -- filename (including extension) to save image
        """
        self._app.step()  # ensure all previous commands have been executed
        self._app.save_screenshot(filename)
