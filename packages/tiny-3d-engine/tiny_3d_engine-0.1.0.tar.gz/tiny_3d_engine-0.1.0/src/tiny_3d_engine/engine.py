"""
3D interaction engine
---------------------

This module load a **Scene3D** object, 
pass to a **ViewField** object** 
(i.e the coordinates of the scene transformed with
respect to the user POV),
and dialog with e **Screen** Object.

**Note that there is NO Graphical Toolkit here.
The Graphical part is totally imiter to the Screen Object**

"""
import time
import numpy as np

from tiny_3d_engine.viewfield import ViewField
from tiny_3d_engine.screen import Screen


__all__ = ["Engine3D"]


class Engine3D:
    def __init__(
            self,
            scene=None,
            root=None,
            width=1000,
            height=700,
            background="#666699",
            title="Tiny 3D Engine"):
        

        self.title = title

        self.view = ViewField(width, height)
        self.screen = Screen(
            width,
            height,
            background,
            root=root,
            title=self.title
        )

        self.scene = None
        self.screen.can.bind('<B1-Motion>', self.__drag)
        self.screen.can.bind('<Shift-B1-Motion>', self.__shiftdrag)
        self.screen.can.bind('<ButtonRelease-1>', self.__resetDrag)
        self.screen.can.bind_all('<Key>', self.__keypress)
        self.__dragprev = []

        if scene is not None:
            self.update(scene)

    def update(self, scene):
        """ Update the scene to show."""
        if scene.is_void():
            self.scene = None
            self.clear()
        else:
            self.scene = scene
            self.conn = scene.conn()
            self.tags = scene.tags()
            self.screen.update(scene.colors())
            self.reset_view()
            self.screen.add_tags_bindings(scene.parts())
            
    def reset_view(self):
        if self.scene is not None:
            self.view.update(self.scene.points())
        self.scale = float(self.view.init_scale)
        self.distance = 64

    def rotate(self, axis, angle):
        """rotate model around axis"""
        if self.scene is not None:
            self.view.rotate(axis, angle)
    def translate(self, axis, angle):
        """rotate model around axis"""
        if self.scene is not None:
            self.view.translate(axis, angle)


    def dump(self, fname):
        """Dump the scene into a file."""
        if self.scene is not None:
            self.scene.dump(fname)
        else:
            raise ValueError("No scene to dump...")

    def render(self):
        """Render the viewfield on screen."""
        if self.scene is not None:
            #calculate flattened coordinates (x_pix, y_pix)
            projxy = self.view.flatten(self.distance, self.scale)

            ordered_z_indices = np.flip(np.argsort(
                self.view.pts[self.conn[:, 0], 2]
            ))
            # store the shape of connectivity
            (m_elements, n_vertices) = self.conn.shape

            reordered_conn = self.conn[ordered_z_indices]
            # get the serie of polygons, in z order
            poly_coords = np.take(
                projxy,
                reordered_conn.ravel(),
                axis=0)

            # reshape to n_elements
            poly_coords = poly_coords.reshape(m_elements, n_vertices, 2)
            # loop on the polygons to map on the screen
            for i, elmt in enumerate(poly_coords):
                tag = self.tags[ordered_z_indices[i]]
                # adujsting polyline to vertices seem slower on my tests
                #coords = elmt.tolist()[:self.scene.n_vtx(tag)*3]
                self.screen.createShape(
                    elmt.tolist(),
                    tag,
                    self.elmt_color(tag))

    def elmt_color(self, tag):
        """Redirects to part color

        colors shades should be computed
        with numpy in integers, not at drawing step"""
        return self.scene.part_color(tag)

    def clear(self):
        """clear display"""
        self.screen.clear()

    def after(self, time, function):
        """call screen after() method, for animations"""
        self.screen.after(time, function)

    def mainloop(self):
        """call screen mainloop() method to stay interactive"""
        self.screen.mainloop()

    def bench_speed(self, trials=10):
        """Benchmark on rendering speed"""
        print("Benchmark on speed")
        perf_list = list()
        for i in range(trials):
            start = time.time()
            self.rotate('y', 1.)
            end = time.time()
            perf_list.append(end-start)

        perf = sum(perf_list) / len(perf_list)

        print("Rotate", str(round(1000*perf, 3)) + " ms")

        perf_list = list()
        for i in range(trials):
            start = time.time()
            self.clear()
            self.render()
            end = time.time()
            perf_list.append(end-start)

        perf = sum(perf_list) / len(perf_list)

        print("Render", str(round(1/perf, 3)) + " fps")

    def __drag(self, event):
        """handler for mouse drag event"""
        if self.__dragprev:
            self.rotate('y', -(event.x - self.__dragprev[0]) / 20)
            self.rotate('x', -(event.y - self.__dragprev[1]) / 20)
            self.clear()
            self.render()
        self.__dragprev = [event.x, event.y]

    def __shiftdrag(self, event):
        """handler for mouse drag event"""
        if self.__dragprev:
            self.translate('x', -(event.x - self.__dragprev[0]) / 100)
            self.translate('y', -(event.y - self.__dragprev[1]) / 100)
            self.clear()
            self.render()
        self.__dragprev = [event.x, event.y]

    def __resetDrag(self, event):
        """reset mouse drag handler"""
        self.__dragprev = []

    def __keypress(self, event):
        """handler for keyboard events"""
        if event.keysym == 'Z':
            self.scale *= 2

        elif event.keysym == 'z':
            if self.scale > 20:
                self.scale /= 2
        elif event.keysym == 'd':
            if self.distance < 128:
                self.distance *= 2
        elif event.keysym == 'D':
            if self.distance > 2:
                self.distance /= 2

        elif event.keysym == 'r':
            self.reset_view()

        self.clear()
        self.render()
