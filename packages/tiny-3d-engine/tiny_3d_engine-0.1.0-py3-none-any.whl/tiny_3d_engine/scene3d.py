"""
Scen3D object :
---------------

This module handle the Scene3D object.
This handle several parts
in absolute coordinates, without transformations.

"""

import numpy as np
from tiny_3d_engine.geo_loader import load_geo
from tiny_3d_engine.part3d import Part3D

__all__ = ["Scene3D", "comp_min_max", "load_geo_as_scene"]


def comp_min_max(points):
    """Compute the bounding box of a point cloud (n.3)

    Returns :
        min_ : nparray (3) of lower_left_front coordinate
        max_ : nparray (3) of upper_right_back coordinate
    """
    max_ = np.amax(points, axis=0)
    min_ = np.amin(points, axis=0)
    return min_, max_


def load_geo_as_scene(fname, scene=None, color=None):
    """Return a Scene object built from a geofile"""
    out = load_geo(fname)
    if scene is None:
        scene = Scene3D()

    for part in out:

        name = part
        if "#" in part:
            name = part.split("#")[0]
            color = "#"+part.split("#")[1]
        coor = out[part]["coor"]
        conn = out[part][out[part]["el_type"]]
        scene.add_or_update_part(name, coor, conn, color=color)
    return scene


class Scene3D:
    """Gather part3D objects to be shown in a renderer"""
    def __init__(self, title="Tiny 3D engine"):
        """Startup."""
        self._data = dict()
        self.title = title

    def parts(self):
        """Return parts list"""
        return self._data.keys()

    def add_or_update_part(self, name, points, conn, color=None):
        """Create or replace a part."""
        self._data[name] = dict()
        self._data[name]["points"] = np.array(points,  dtype="float")
        self._data[name]["conn"] = np.array(conn, dtype="int_")
        self._data[name]["n_pts"] = self._data[name]["points"].shape[0]
        self._data[name]["n_elmts"] = self._data[name]["conn"].shape[0]
        self._data[name]["n_vtx"] = self._data[name]["conn"].shape[1]
        self._data[name]["tags"] = np.full((self._data[name]["n_elmts"]), name)

        if color is None:
            color = "#ffffff"

        if not color.startswith("#"):
            raise ValueError(
                "part color must be in hexadecimal format: #ffffff for white:" 
                + color)
        self._data[name]["color"] = color

    def add_axes(self):
        """add axes to the scene"""

        (self.min, self.max) = comp_min_max(self.points())

        str_fmt = "{:.5g}m"

        shift = 0.1*(self.max - self.min)
        ax_x = Part3D()
        start = [
            self.min[0],
            self.min[1] - shift[1],
            self.min[2] - shift[2]]
        end = [
            self.max[0],
            self.min[1] - shift[1],
            self.min[2] - shift[2]]
        title = ('axis-x_'
            + str_fmt.format(self.min[0]) 
            + "_" + str_fmt.format(self.max[0]))
        ax_x.add_line(start, end, 10)
        self.add_or_update_part(
            title, ax_x.points, ax_x.conn, color="#ff0000")

        ax_y = Part3D()
        start = [
            self.min[0] - shift[0],
            self.min[1],
            self.min[2] - shift[2]]
        end = [
            self.min[0] - shift[0],
            self.max[1],
            self.min[2] - shift[2]]
        title = (
            'axis-y_'
            + str_fmt.format(self.min[1])
            + "_" + str_fmt.format(self.max[1]))
        ax_y.add_line(start, end, 10)
        self.add_or_update_part(
            title, ax_y.points, ax_y.conn, color="#00ff00")

        start = [
            self.min[0] - shift[0],
            self.min[1] - shift[1],
            self.min[2]]
        end = [
            self.min[0] - shift[0],
            self.min[1] - shift[1],
            self.max[2]]
        title = (
            'axis-z_'
            + str_fmt.format(self.min[2])
            + "_|_" + str_fmt.format(self.max[2]))
        ax_z = Part3D()
        ax_z.add_line(start, end, 10)
        self.add_or_update_part(
            title, ax_z.points, ax_z.conn, color="#0000ff")

        print("axes added")

    def del_part(self, partname):
        """Remove a part from the scene."""
        if partname in self._data:
            del self._data[partname]

    def points(self, partname=None):
        """Return points coordinates.

        :param partname: str, name of part.

        If no partname provided, all parts concatenated are returned

        returns:
        --------
        numpy array of shape (n_pts, 3)

        """
        if self.is_void():
            return None

        if partname is not None:
            self.check_partname(partname)
            out = self._data[partname]["points"]
        else:
            list_data = list(self._data.keys())
            out = self._data[list_data[0]]["points"]

            for part in list_data[1:]:
                out = np.concatenate(
                    (out, self._data[part]["points"]),
                    axis=0)
        return out

    def tags(self, partname=None):
        """Return tags as an array.

        returns:
        --------
        numpy array of shape (n_elemts), repeating the Tag string
        """

        if self.is_void():
            return None

        if partname is not None:
            self.check_partname(partname)
            out = self._data[partname]["tags"]
        else:
            list_data = list(self._data.keys())

            out = self._data[list_data[0]]["tags"]

            for part in list_data[1:]:
                out = np.concatenate(
                    (out, self._data[part]["tags"]),
                    axis=0)
        return out

    def conn(self, partname=None):
        """Return connectivity.

        :param partname: str, name of part.

        If no partname provided, all parts concatenated are returned

        returns:
        --------
        numpy array of shape (n_elements x n_vtx_max)

        """
        if self.is_void():
            return None

        if partname is not None:
            self.check_partname(partname)
            out = self._data[partname]["conn"]
        else:
            list_data = list(self._data.keys())

            max_nvertex = 0
            for part in list_data:
                max_nvertex = max(self._data[part]["n_vtx"], max_nvertex)

            def ax1_padded(arr_, ax1_size):
                """repeat the last column of the matrix with edge value.

                In other wort it extend the array along axis 1

                arr_ =
                [[1, 2, 3]
                 [4, 5, 6]]

                becomes

                ax1_padded(arr_, 5) =
                [[1, 2, 3, 3, 3]
                 [4, 5, 6, 6, 6]]

                """
                pad = ax1_size - arr_.shape[1]
                return np.pad(arr_, ((0, 0), (0, pad)), 'edge')

            part0 = list_data[0]
            out = ax1_padded(self._data[part0]["conn"], max_nvertex)

            shift = self.n_pts(part0)

            for part in list_data[1:]:
                out = np.concatenate(
                    (out, ax1_padded(
                        self._data[part]["conn"] + shift,
                        max_nvertex)),
                    axis=0)
                shift += self.n_pts(part)

        return out

    def colors(self):
        """Return dictionart of colors

        returns:
        --------
        dict of string with a hex color.
        """

        if self.is_void():
            return None

        out = dict()
        for part in self._data:
            out[part] = self._data[part]["color"]

        return out

    def part_color(self, partname):
        """Return dictionart of colors

        returns:
        --------
        dict of string with a hex color.
        """
        if self.is_void():
            return None

        return self._data[partname]["color"]

    def n_vtx(self, partname):
        """Return Number of vertices for part.

        :param partname: str, name of part.

        returns:
        --------
        str for a hex color.
        """
        if self.is_void():
            return None

        self.check_partname(partname)
        out = self._data[partname]["n_vtx"]
        return out

    def n_pts(self, partname):
        """Return Number of pts for part.

        :param partname: str, name of part.

        returns:
        --------
        str for a hex color.
        """

        if self.is_void():
            return None

        self.check_partname(partname)
        out = self._data[partname]["n_pts"]
        return out

    def check_partname(self, partname):
        """check that partnae is in the scene"""
        if partname not in self._data:
            msg_err = "Part " + partname + "does not belong to scene. t(-,-t)"
            raise RuntimeError(msg_err)

    def is_void(self):
        """return true is the scene is void"""
        out = False
        if not self._data:
            out = True
        return out

    def dump(self, fname="dummy"):
        """ dump part3D as ensight ASCI file """

        if self.is_void():
            raise RuntimeError("Scene is void, nothing to dump.")

        cnt = list()

        cnt.append(self.title)
        cnt.append("Scene 3D object")
        cnt.append("node id off")
        cnt.append("element id off")

        for i, part in enumerate(self.parts()):
            n_vtx = self.n_vtx(part)
            n_pts = self.n_pts(part)
            n_elmts = self._data[part]["n_elmts"]
            cnt.append("part")
            cnt.append(str(i+1))
            cnt.append(part + self.part_color(part))
            cnt.append("coordinates")
            cnt.append(str(n_pts))
            for dim in range(3):
                for n in range(n_pts):
                    cnt.append(str(self._data[part]["points"][n, dim]))

            el_type = None
            if n_vtx == 2:
                el_type = "bar2"
            elif n_vtx == 3:
                el_type = "tri3"
            elif n_vtx == 4:
                el_type = "quad4"
            else:
                msgerr = (
                    part + " uses elements with "
                    + str(n_vtx) + " vertices")
                msgerr += "\n Element not supported.  t(-,-t)"
                raise NotImplementedError(msgerr)

            cnt.append(el_type)
            cnt.append(str(n_elmts))
            for m in range(n_elmts):
                cnt.append(" ".join(
                    [str(item + 1) for item in
                     self._data[part]["conn"][m, :].tolist()]
                ))
        with open(fname+".geo", "w") as fout:
            fout.write("\n".join(cnt))
        with open(fname+".case", "w") as fout:
            cnt2 = str()
            cnt2 += "FORMAT\n"
            cnt2 += "type: ensight gold\n"
            cnt2 += "\n"
            cnt2 += "GEOMETRY\n"
            cnt2 += "model: " + fname + ".geo"
            fout.write(cnt2)
