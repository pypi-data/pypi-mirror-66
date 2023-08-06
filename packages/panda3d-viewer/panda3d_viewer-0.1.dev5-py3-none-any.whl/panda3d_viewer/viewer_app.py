"""This module contains ViewerApp, an application framework.

ViewerApp responsible for opening a graphical display,
setting up input devices and creating the scene graph.
"""

from panda3d.core import Vec3, Vec4, Quat, Mat4, BitMask32
from panda3d.core import GeomNode, TextNode
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Material
from panda3d.core import AntialiasAttrib, CullFaceAttrib, TransparencyAttrib
from panda3d.core import loadPrcFileData

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText

from .viewer_base import ViewerBase
from .utils import make_axes, make_grid, make_cylinder, make_box, make_sphere

__all__ = ('ViewerApp')


class ViewerApp(ShowBase, ViewerBase):
    """A Panda3D based application."""

    LightMask = BitMask32(1)

    def __init__(self, window_title='Viewer', window_type='onscreen', antialiasing=0):
        """Open a window, setup a scene.

        Keyword Arguments:
            window_title {str} -- window title (default: {'PandaViewer'})
            window_type {str} -- window type, one of onscreen, offscreen (default: {'onscreen'})
            antialiasing {int} -- framebuffer multisamples (default: {0})
        """
        settings = '\n'.join([
            'window-title {}'.format(window_title),
            'window-type {}'.format(window_type),
            'framebuffer-multisample {}'.format(1 if antialiasing else 0),
            'multisamples {}'.format(antialiasing),
            'audio-library-name null',
            'print-pipe-types 0',
        ])
        loadPrcFileData('', settings)

        ShowBase.__init__(self)

        self.render.set_shader_auto()
        self.render.set_antialias(AntialiasAttrib.MAuto)

        self._camera_defaults = [(4.0, -4.0, 1.5), (0.0, 0.0, 0.5)]
        self.reset_camera(*self._camera_defaults)

        self._lights = [
            self._make_light_ambient((0.2, 0.2, 0.2)),
            self._make_light_direct(
                1, (0.6, 0.8, 0.8), pos=(10.0, 10.0, 10.0)),
            self._make_light_direct(
                2, (0.8, 0.6, 0.8), pos=(10.0, -10.0, 10.0)),
            self._make_light_direct(
                3, (0.8, 0.8, 0.6), pos=(-10.0, 10.0, 10.0)),
            self._make_light_direct(
                4, (0.6, 0.6, 0.8), pos=(-10.0, -10.0, 10.0)),
        ]
        self._lights_mask = [True, True, True, False, False]
        self.enable_lights(self.config.GetBool('enable-lights', True))
        self.enable_shadow(self.config.GetBool('enable-shadow', False))

        self._axes = self._make_axes()
        self.show_axes(self.config.GetBool('show-axes', True))

        self._grid = self._make_grid()
        self.show_grid(self.config.GetBool('show-grid', True))

        self._groups = {}

        if self.windowType == 'onscreen':
            self._help_label = None
            self._setup_shortcuts()

    def append_group(self, root_path, remove_if_exists=True):
        """Append a root node for a group of nodes.

        Arguments:
            root_path {str} -- path to the group's root node

        Keyword Arguments:
            remove_if_exists {bool} -- remove group with root_path if exists (default: {True})
        """
        if remove_if_exists and root_path in self._groups:
            self.remove_group(root_path)

        root = self.render
        for name in root_path.split('/'):
            root = root.attach_new_node(name)

        self._groups[root_path] = root

    def remove_group(self, root_path):
        """Remove a group of nodes.

        Arguments:
            root_path {str} -- path to the group's root node
        """
        self._groups.pop(root_path).removeNode()

    def show_group(self, root_path, show):
        """Turn a node group rendering on or off.

        Arguments:
            root_path {str} -- path to the group's root node
            show {bool} -- flag
        """
        root = self._groups[root_path]
        if show:
            root.show()
        else:
            root.hide()

    def move_nodes(self, root_path, name_pose_dict):
        """Set a pose for nodes within a group.

        Arguments:
            root_path {str} -- path to the group's root node
            name_pose_dict {dict} -- {node_name : (pos, quat)} dictionary
        """
        root = self._groups[root_path]
        for node in root.getChildren():
            if node.name in name_pose_dict:
                pos, quat = name_pose_dict[node.name]
                node.set_pos_quat(Vec3(*pos), Quat(*quat))

    def append_mesh(self, root_path, name, mesh_path, scale):
        """Append a mesh node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            mesh_path {str} -- path to the mesh file on disk
            scale {Vec3} -- mesh scale
        """
        root = self._groups[root_path]
        node = root.attach_new_node(name)
        node.set_scale(Vec3(*scale))
        if sum([s < 0 for s in scale]) % 2 != 0:
            # reverse the cull order in case of negative scale values
            node.set_attrib(CullFaceAttrib.makeReverse())
        mesh = self.loader.loadModel(mesh_path)
        mesh.reparent_to(node)
        if mesh_path.lower().endswith('.dae'):
            # converting from Y-up to Z-up axes when import from dae
            mesh.set_mat(Mat4.yToZUpMat())

    def append_capsule(self, root_path, name, radius, length):
        """Append a capsule primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            radius {flaot} -- capsule radius
            length {flaot} -- capsule length
        """
        self.append_cylinder(root_path, name, radius, length)

    def append_cylinder(self, root_path, name, radius, length):
        """Append a cylinder primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            radius {flaot} -- cylinder radius
            length {flaot} -- cylinder length
        """
        geom = GeomNode(name)
        geom.add_geom(make_cylinder())
        root = self._groups[root_path]
        node = root.attach_new_node(geom)
        node.set_scale(Vec3(radius, radius, length))

    def append_box(self, root_path, name, size):
        """Append a box primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            size {Vec3} -- box size
        """
        geom = GeomNode(name)
        geom.add_geom(make_box())
        root = self._groups[root_path]
        node = root.attach_new_node(geom)
        node.set_scale(Vec3(*size))

    def append_sphere(self, root_path, name, radius):
        """Append a sphere primitive node to the group.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            radius {flaot} -- sphere radius
        """
        geom = GeomNode(name)
        geom.add_geom(make_sphere())
        root = self._groups[root_path]
        node = root.attach_new_node(geom)
        node.set_scale(Vec3(radius, radius, radius))

    def set_material(self, root_path, name, color_rgba, texture_path=''):
        """Override material of a node.

        Arguments:
            root_path {str} -- path to the group's root node
            name {str} -- node name within a group
            color {Vec4} -- color RGBA

        Keyword Arguments:
            texture_path {str} -- path to the texture file on disk (default: {''})
        """
        node = self._groups[root_path].find(name)
        node.set_color(Vec4(*color_rgba))

        material = Material()
        material.set_ambient(Vec4(*color_rgba))
        material.set_diffuse(Vec4(*color_rgba))
        material.set_specular(Vec3(1, 1, 1))
        material.set_roughness(0.4)
        node.set_material(material, 1)

        if color_rgba[3] < 1:
            node.set_transparency(TransparencyAttrib.M_alpha)
            node.set_two_sided(1)

        if texture_path:
            texture = self.loader.load_texture(texture_path)
            node.set_texture(texture)

    def reset_camera(self, pos, look_at):
        """Reset camera position.

        Arguments:
            pos {Vec3} -- camera position
            look_at {Vec3} -- camera target point
        """
        self.camera.set_pos(Vec3(*pos))
        self.camera.look_at(Vec3(*look_at))

        if self.windowType == 'onscreen':
            # update mouse control according to the camera position
            cam_mat = Mat4(self.camera.get_mat())
            cam_mat.invert_in_place()
            self.mouseInterfaceNode.set_mat(cam_mat)

    def enable_lights(self, enable):
        """Turn lighting on or off.

        Arguments:
            enable {bool} -- flag
        """
        for light, mask in zip(self._lights, self._lights_mask):
            if enable and mask:
                self.render.set_light(light)
            else:
                self.render.clear_light(light)
        self._lights_enabled = enable

    def enable_light(self, index, enable):
        """Turn a light on or off.

        Arguments:
            index {int} -- light index
            enable {bool} -- flag
        """
        self._lights_mask[index] = enable
        self.enable_lights(self._lights_enabled)

    def enable_shadow(self, enable):
        """Turn shadows rendering on or off.

        Arguments:
            enable {bool} -- flag
        """
        for light in self._lights:
            if not light.node().is_ambient_light():
                light.node().set_shadow_caster(enable, 1024, 1024)
        self.render.set_depth_offset(1 if enable else 0)
        self._shadow_enabled = enable

    def show_axes(self, show):
        """Turn the axes rendering on or off.

        Arguments:
            show {bool} -- flag
        """
        if show:
            self._axes.show()
        else:
            self._axes.hide()

    def show_grid(self, show):
        """Turn the grid rendering on or off.

        Arguments:
            show {bool} -- flag
        """
        if show:
            self._grid.show()
        else:
            self._grid.hide()

    def toggle_help(self):
        """Toggle help label visibility."""
        if self._help_label is None:
            self._help_label = self._make_help_label()
        else:
            self._help_label.removeNode()
            self._help_label = None

    def toggle_fps(self):
        """Toggle the fps label visibility."""
        self.set_frame_rate_meter(self.frameRateMeter is None)

    def step(self):
        """Execute one main loop step."""
        self.task_mgr.step()

    def join(self):
        """Run the application until user close the main window."""
        self.run()

    def stop(self):
        """Stop the application.

        Interrupts the application loop (run() function)
        """
        self.task_mgr.stop()

    def save_screenshot(self, filename):
        """Capture a screenshot from the main window and write it to disk.

        Arguments:
            filename {str} -- filename (including extension) to save image
        """
        self.win.save_screenshot(filename)

    def _load_model(self, path):
        model = self.loader.loadModel(path)
        if path.lower().endswith('.dae'):
            # converting from Y-up to Z-up axes when import from dae
            model.set_mat(Mat4.yToZUpMat())
        return model

    def _make_light_ambient(self, color):
        light = AmbientLight('alight')
        light.set_color(Vec3(*color))
        return self.render.attach_new_node(light)

    def _make_light_direct(self, index, color, pos, target=(0, 0, 1)):
        light = DirectionalLight('dlight{:02d}'.format(index))
        light.set_color(Vec3(*color))
        light.set_camera_mask(self.LightMask)
        lens = light.get_lens()
        lens.set_film_size(2, 2)
        lens.set_near_far(1, 20)
        node = self.render.attach_new_node(light)
        node.set_pos(*pos)
        node.look_at(*target)
        return node

    def _make_axes(self):
        model = GeomNode('axes')
        model.add_geom(make_axes())
        node = self.render.attach_new_node(model)
        node.set_light_off()
        node.set_render_mode_wireframe()
        node.set_render_mode_thickness(4)
        node.set_antialias(AntialiasAttrib.MLine)
        node.hide(self.LightMask)
        return node

    def _make_grid(self):
        model = GeomNode('grid')
        model.add_geom(make_grid())
        node = self.render.attach_new_node(model)
        node.set_light_off()
        node.set_render_mode_wireframe()
        node.set_antialias(AntialiasAttrib.MLine)
        node.hide(self.LightMask)
        return node

    def _setup_shortcuts(self):
        self.accept('space', self.screenshot)
        self.accept('escape', self.stop)
        self.accept('q', self.stop)
        self.accept('r', self.reset_camera, self._camera_defaults)
        self.accept('l', lambda: self.enable_lights(not self._lights_enabled))
        self.accept('s', lambda: self.enable_shadow(not self._shadow_enabled))
        self.accept('a', lambda: self.show_axes(self._axes.is_hidden()))
        self.accept('g', lambda: self.show_grid(self._grid.is_hidden()))
        self.accept('b', self.toggle_backface)
        self.accept('w', self.toggle_wireframe)
        self.accept('f', self.toggle_fps)
        self.accept('h', self.toggle_help)
        self.accept('f1', self.toggle_help)

    def _make_help_label(self):
        text = '\n'.join([
            "Keyboard shortcuts:", " F1, h: show help", " Escape, q: exit", " Space: screenshot",
            " a: toggle axes rendering", " b: toggle backface culling",
            " g: toggle grid rendering", " f: toggle fps meter", " l: toggle lighting",
            " r: reset camera", " s: toggle shadows", " w: toggle wireframe"
        ])
        return OnscreenText(text=text,
                            parent=self.a2dTopLeft,
                            align=TextNode.ALeft,
                            style=1,
                            bg=(0.1, 0.1, 0.1, 0.5),
                            fg=(1, 1, 1, 1),
                            shadow=(0, 0, 0, .4),
                            pos=(0.06, -0.1),
                            scale=.05)
