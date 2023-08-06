"""This module contains ViewerBase, a viewer interface description."""

__all__ = ('ViewerBase')


class ViewerBase:
    """Viewer interface."""

    def join(self):
        """Run the application until a user close the main window."""
        raise NotImplementedError()

    def stop(self):
        """Stop the application."""
        raise NotImplementedError()

    def append_group(self, root_path, remove_if_exists):
        """Append a root node for a group of nodes.

        Arguments:
            root_path {str} -- path to the group's root node
            remove_if_exists {bool} -- remove group with root_path if exists
        """
        raise NotImplementedError()

    def remove_group(self, root_path):
        """Remove a group of nodes.

        Arguments:
            root_path {str} -- path to the group's root node
        """
        raise NotImplementedError()

    def show_group(self, root_path, show):
        """Turn a node group rendering on or off.

        Arguments:
            root_path {str} -- path to the group's root node
            show {bool} -- flag
        """
        raise NotImplementedError()

    def move_nodes(self, root_path, name_pose_dict):
        """Set a pose for nodes within a group.

        Arguments:
            root_path {str} -- path to the group's root node
            name_pose_dict {dict} -- {node_name : (pos, quat)} dictionary
        """
        raise NotImplementedError()

    def append_mesh(self, root_path, name, mesh_path, scale):
        """Append a mesh node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            mesh_path {str} -- path to the mesh file on disk
            scale {Vec3} -- mesh scale
        """
        raise NotImplementedError()

    def append_capsule(self, root_path, name, radius, length):
        """Append a capsule primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            radius {flaot} -- capsule radius
            length {flaot} -- capsule length
        """
        raise NotImplementedError()

    def append_cylinder(self, root_path, name, radius, length):
        """Append a cylinder primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            radius {flaot} -- cylinder radius
            length {flaot} -- cylinder length
        """
        raise NotImplementedError()

    def append_box(self, root_path, name, size):
        """Append a box primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            size {Vec3} -- box size
        """
        raise NotImplementedError()

    def append_sphere(self, root_path, name, radius):
        """Append a sphere primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            radius {flaot} -- sphere radius
        """
        raise NotImplementedError()

    def set_material(self, root_path, name, color_rgba, texture_path):
        """Override material of a node.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            color {Vec4} -- color RGBA
            texture_path {str} -- path to the texture file on disk
        """
        raise NotImplementedError()

    def reset_camera(self, pos, look_at):
        """Reset camera position.

        Arguments:
            pos {Vec3} -- camera position
            look_at {Vec3} -- camera target point
        """
        raise NotImplementedError()

    def enable_lights(self, enable):
        """Turn lighting on or off.

        Arguments:
            enable {bool} -- flag
        """
        raise NotImplementedError()

    def enable_light(self, index, enable):
        """Turn a light on or off.

        Arguments:
            index {int} -- light index
            enable {bool} -- flag
        """
        raise NotImplementedError()

    def enable_shadow(self, enable):
        """Turn shadows rendering on or off.

        Arguments:
            enable {bool} -- flag
        """
        raise NotImplementedError()

    def show_axes(self, show):
        """Turn the axes rendering on or off.

        Arguments:
            show {bool} -- flag
        """
        raise NotImplementedError()

    def show_grid(self, show):
        """Turn the grid rendering on or off.

        Arguments:
            show {bool} -- flag
        """
        raise NotImplementedError()

    def save_screenshot(self, filename):
        """Capture a screenshot from the main window and write it to disk.

        Arguments:
            filename {str} -- filename (including extension) to save image
        """
        raise NotImplementedError()
