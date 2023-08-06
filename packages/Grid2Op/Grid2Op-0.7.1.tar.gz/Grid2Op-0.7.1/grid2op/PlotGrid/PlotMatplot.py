# Copyright (c) 2019-2020, RTE (https://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
# If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
# you can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of Grid2Op, Grid2Op a testbed platform to model sequential decision making in power systems.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.lines import Line2D

from grid2op.PlotGrid.BasePlot import BasePlot
from grid2op.PlotGrid.LayoutUtil import layout_obs_sub_load_and_gen
from grid2op.PlotGrid.PlotUtil import PlotUtil as pltu


class PlotMatplot(BasePlot):
    def __init__(self,
                 observation_space,
                 width=1280,
                 height=720,
                 grid_layout=None,
                 dpi=96,
                 scale=2000.0,
                 sub_radius = 15,
                 load_radius = 8,
                 gen_radius = 8):
        self._scale = scale
        self.dpi = dpi
        super().__init__(observation_space, width, height, grid_layout)

        self._sub_radius = sub_radius
        self._sub_face_color = "w"
        self._sub_edge_color = "blue"
        self._sub_txt_color = "black"
        
        self._load_radius = load_radius
        self._load_face_color = "w"
        self._load_edge_color = "orange"
        self._load_txt_color = "black"
        self._load_line_color = "black"
        self._load_line_width = 1
        
        self._gen_radius = gen_radius
        self._gen_face_color = "w"
        self._gen_edge_color = "green"
        self._gen_txt_color = "black"
        self._gen_line_color = "black"
        self._gen_line_width = 1

        #cx = np.linspace(0.0, 0.70, 10)
        #self._line_color_scheme = cm.get_cmap("inferno")(cx)
        self._line_color_scheme = [ "blue", "orange", "red"]
        self._line_color_width = 1
        self._line_bus_radius = 5
        self._line_bus_face_colors = ["black", "red", "magenta"]
        self._line_arrow_len = 10
        self._line_arrow_width = 10.0

        self.xlim = [0, 0]
        self.xpad = 50
        self.ylim = [0, 0]
        self.ypad = 50

    def _v_textpos_from_dir(self, dirx, diry):
        if diry > 0:
            return "bottom"
        else:
            return "top"
    
    def _h_textpos_from_dir(self, dirx, diry):
        if dirx == 0:
            return "center"
        elif dirx > 0:
            return "left"
        else:
            return "right"
        
    def create_figure(self):
        w_inch = self.width / self.dpi
        h_inch = self.height / self.dpi
        f = plt.figure(figsize=(w_inch, h_inch), dpi=self.dpi)
        self.ax = f.subplots()
        return f
    
    def clear_figure(self, figure):
        self.xlim = [0, 0]
        self.ylim = [0, 0]
        figure.clear()
        self.ax = figure.subplots()

    def convert_figure_to_numpy_HWC(self, figure):
        figure.canvas.draw()
        w, h = figure.canvas.get_width_height()
        buf = np.fromstring(figure.canvas.tostring_rgb(), dtype=np.uint8)
        buf = np.reshape(buf, (h, w, 3))
        return buf

    def compute_grid_layout(self, obs_space, grid_layout = None):
        # We overload to specify the scale
        # Also we expect obs_space has a grid_layout
        return layout_obs_sub_load_and_gen(obs_space, self._scale, True)

    def _draw_substation_txt(self, pos_x, pos_y, text):
        self.ax.text(pos_x, pos_y, text,
                     color=self._sub_txt_color,
                     horizontalalignment='center',
                     verticalalignment='center')
    
    def _draw_substation_circle(self, pos_x, pos_y):
        patch = patches.Circle((pos_x, pos_y),
                               radius=self._sub_radius,
                               facecolor=self._sub_face_color,
                               edgecolor=self._sub_edge_color)
        self.ax.add_patch(patch)

    def draw_substation(self, figure, observation,
                        sub_id, sub_name,
                        pos_x, pos_y):
        self.xlim[0] = min(self.xlim[0], pos_x)
        self.xlim[1] = max(self.xlim[1], pos_x)
        self.ylim[0] = min(self.ylim[0], pos_y)
        self.ylim[1] = max(self.ylim[1], pos_y)

        self._draw_substation_circle(pos_x, pos_y)
        self._draw_substation_txt(pos_x, pos_y, str(sub_id))
    
    def _draw_load_txt(self, pos_x, pos_y, sub_x, sub_y, text):
        dir_x, dir_y = pltu.vec_from_points(sub_x, sub_y, pos_x, pos_y)
        off_x, off_y = pltu.norm_from_points(sub_x, sub_y, pos_x, pos_y)
        txt_x = pos_x + off_x * self._gen_radius
        txt_y = pos_y + off_y * self._gen_radius
        ha = self._h_textpos_from_dir(dir_x, dir_y)
        va = self._v_textpos_from_dir(dir_x, dir_y)
        self.ax.text(txt_x, txt_y, text,
                     color=self._load_txt_color,
                     horizontalalignment=ha,
                     verticalalignment=va)
    
    def _draw_load_name(self, pos_x, pos_y, txt):
        self.ax.text(pos_x, pos_y, txt,
                     color=self._load_txt_color,
                     va='center', ha='center',
                     fontsize='x-small')

    def _draw_load_circle(self, pos_x, pos_y):
        patch = patches.Circle((pos_x, pos_y),
                               radius=self._load_radius,
                               facecolor=self._load_face_color,
                               edgecolor=self._load_edge_color)
        self.ax.add_patch(patch)
    
    def _draw_load_line(self, pos_x, pos_y, sub_x, sub_y):
        codes = [
            Path.MOVETO,
            Path.LINETO
        ]
        verts = [
            (pos_x, pos_y),
            (sub_x, sub_y)
        ]
        path = Path(verts, codes)
        patch = patches.PathPatch(path,
                                  color=self._load_line_color,
                                  lw=self._load_line_width)
        self.ax.add_patch(patch)
    
    def _draw_load_bus(self,
                       pos_x, pos_y,
                       norm_dir_x, norm_dir_y,
                       bus_id):
        center_x = pos_x + norm_dir_x * self._sub_radius
        center_y = pos_y + norm_dir_y * self._sub_radius
        face_color = self._line_bus_face_colors[bus_id]
        patch = patches.Circle((center_x, center_y),
                               radius=self._line_bus_radius,
                               facecolor=face_color)
        self.ax.add_patch(patch)

    def draw_load(self, figure, observation,
                  load_id, load_name, load_bus,
                  load_value, load_unit,
                  pos_x, pos_y,
                  sub_x, sub_y):
        self.xlim[0] = min(self.xlim[0], pos_x)
        self.xlim[1] = max(self.xlim[1], pos_x)
        self.ylim[0] = min(self.ylim[0], pos_y)
        self.ylim[1] = max(self.ylim[1], pos_y)
        self._draw_load_line(pos_x, pos_y, sub_x, sub_y)
        self._draw_load_circle(pos_x, pos_y)
        load_txt = load_name + ":\n"
        load_txt += pltu.format_value_unit(load_value, load_unit)
        self._draw_load_txt(pos_x, pos_y, sub_x, sub_y, load_txt)
        self._draw_load_name(pos_x, pos_y, str(load_id))
        load_dir_x, load_dir_y = pltu.norm_from_points(sub_x, sub_y, pos_x, pos_y)
        self._draw_load_bus(sub_x, sub_y, load_dir_x, load_dir_y, load_bus)
    
    def update_load(self, figure, observation,
                    load_id, load_name, load_bus,
                    load_value, load_unit,
                    pos_x, pos_y,
                    sub_x, sub_y):
        pass
    
    def _draw_gen_txt(self, pos_x, pos_y, sub_x, sub_y, text):
        dir_x, dir_y = pltu.vec_from_points(sub_x, sub_y, pos_x, pos_y)
        off_x, off_y = pltu.norm_from_points(sub_x, sub_y, pos_x, pos_y)
        txt_x = pos_x + off_x * self._gen_radius
        txt_y = pos_y + off_y * self._gen_radius
        ha = self._h_textpos_from_dir(dir_x, dir_y)
        va = self._v_textpos_from_dir(dir_x, dir_y)
        self.ax.text(txt_x, txt_y, text,
                     color=self._gen_txt_color,
                     wrap=True,
                     horizontalalignment=ha,
                     verticalalignment=va)

    def _draw_gen_circle(self, pos_x, pos_y):
        patch = patches.Circle((pos_x, pos_y),
                               radius=self._gen_radius,
                               edgecolor=self._gen_edge_color,
                               facecolor=self._gen_face_color)
        self.ax.add_patch(patch)
    
    def _draw_gen_line(self, pos_x, pos_y, sub_x, sub_y):
        codes = [
            Path.MOVETO,
            Path.LINETO
        ]
        verts = [
            (pos_x, pos_y),
            (sub_x, sub_y)
        ]
        path = Path(verts, codes)
        patch = patches.PathPatch(path,
                                  color=self._gen_line_color,
                                  lw=self._load_line_width)
        self.ax.add_patch(patch)

    def _draw_gen_name(self, pos_x, pos_y, txt):
        self.ax.text(pos_x, pos_y, txt,
                     color=self._gen_txt_color,
                     va='center', ha='center',
                     fontsize='x-small')
        
    def _draw_gen_bus(self,
                      pos_x, pos_y,
                      norm_dir_x, norm_dir_y,
                      bus_id):
        center_x = pos_x + norm_dir_x * self._sub_radius
        center_y = pos_y + norm_dir_y * self._sub_radius
        face_color = self._line_bus_face_colors[bus_id]
        patch = patches.Circle((center_x, center_y),
                               radius=self._line_bus_radius,
                               facecolor=face_color)
        self.ax.add_patch(patch)
        
    def draw_gen(self, figure, observation,
                 gen_id, gen_name, gen_bus,
                 gen_value, gen_unit,
                 pos_x, pos_y,
                 sub_x, sub_y):
        self.xlim[0] = min(self.xlim[0], pos_x)
        self.xlim[1] = max(self.xlim[1], pos_x)
        self.ylim[0] = min(self.ylim[0], pos_y)
        self.ylim[1] = max(self.ylim[1], pos_y)
        self._draw_gen_line(pos_x, pos_y, sub_x, sub_y)
        self._draw_gen_circle(pos_x, pos_y)
        gen_txt = gen_name + ":\n"
        gen_txt += pltu.format_value_unit(gen_value, gen_unit)
        self._draw_gen_name(pos_x, pos_y, str(gen_id))
        self._draw_gen_txt(pos_x, pos_y, sub_x, sub_y, gen_txt)
        gen_dir_x, gen_dir_y = pltu.norm_from_points(sub_x, sub_y, pos_x, pos_y)
        self._draw_gen_bus(sub_x, sub_y, gen_dir_x, gen_dir_y, gen_bus)

    def update_gen(self, figure, observation,
                   gen_id, gen_name, gen_bus,
                   gen_value, gen_unit,
                   pos_x, pos_y,
                   sub_x, sub_y):
        pass

    def _draw_powerline_txt(self, 
                            pos_or_x, pos_or_y,
                            pos_ex_x, pos_ex_y,
                            text):
        pos_x, pos_y = pltu.middle_from_points(pos_or_x, pos_or_y, pos_ex_x, pos_ex_y)
        off_x, off_y = pltu.orth_norm_from_points(pos_or_x, pos_or_y, pos_ex_x, pos_ex_y)
        txt_x = pos_x + off_x * self._load_radius
        txt_y = pos_y + off_y * self._load_radius
        ha = self._h_textpos_from_dir(off_x, off_y)
        va = self._v_textpos_from_dir(off_x, off_y)
        self.ax.text(txt_x, txt_y, text,
                     color=self._gen_txt_color,
                     horizontalalignment=ha,
                     verticalalignment=va)
    
    def _draw_powerline_line(self,
                             pos_or_x, pos_or_y,
                             pos_ex_x, pos_ex_y,
                             color, line_style):
        codes = [
            Path.MOVETO,
            Path.LINETO
        ]
        verts = [
            (pos_or_x, pos_or_y),
            (pos_ex_x, pos_ex_y)
        ]
        path = Path(verts, codes)
        patch = patches.PathPatch(path,
                                  color=color,
                                  lw=self._line_color_width,
                                  ls=line_style)
        self.ax.add_patch(patch)

    def _draw_powerline_bus(self,
                            pos_x, pos_y,
                            norm_dir_x, norm_dir_y,
                            bus_id):
        center_x = pos_x + norm_dir_x * self._sub_radius
        center_y = pos_y + norm_dir_y * self._sub_radius
        face_color = self._line_bus_face_colors[bus_id]
        patch = patches.Circle((center_x, center_y),
                               radius=self._line_bus_radius,
                               facecolor=face_color)
        self.ax.add_patch(patch)

    def _draw_powerline_arrow(self,
                              pos_or_x, pos_or_y,
                              pos_ex_x, pos_ex_y,
                              color, watt_value):
        sign = 1.0 if watt_value > 0.0 else -1.0
        off = 1.0 if watt_value > 0.0 else 2.0
        dx, dy = pltu.norm_from_points(pos_or_x, pos_or_y, pos_ex_x, pos_ex_y)
        lx = dx * self._line_arrow_len
        ly = dy * self._line_arrow_len
        arr_x = pos_or_x + dx * self._sub_radius + off * lx
        arr_y = pos_or_y + dy * self._sub_radius + off * ly
        patch = patches.FancyArrow(arr_x, arr_y,
                                   sign * lx,
                                   sign * ly,
                                   length_includes_head=True,
                                   head_length=self._line_arrow_len,
                                   head_width=self._line_arrow_width,
                                   edgecolor=color,
                                   facecolor=color)
        self.ax.add_patch(patch)
    
    def draw_powerline(self, figure, observation,
                       line_id, line_name, connected,
                       line_value, line_unit,
                       or_bus, pos_or_x, pos_or_y,
                       ex_bus, pos_ex_x, pos_ex_y):
        rho = observation.rho[line_id]
        color_idx = int(rho * len(self._line_color_scheme[:-1]))
        color = self._line_color_scheme[color_idx] if connected else "black"
        line_style = "-" if connected else "--"
        self._draw_powerline_line(pos_or_x, pos_or_y,
                                  pos_ex_x, pos_ex_y,
                                  color, line_style)
        txt = pltu.format_value_unit(line_value, line_unit)
        self._draw_powerline_txt(pos_or_x, pos_or_y,
                                 pos_ex_x, pos_ex_y,
                                 txt)

        or_dir_x, or_dir_y = pltu.norm_from_points(pos_or_x, pos_or_y, pos_ex_x, pos_ex_y)
        self._draw_powerline_bus(pos_or_x, pos_or_y,
                                 or_dir_x, or_dir_y,
                                 or_bus)
        ex_dir_x, ex_dir_y = pltu.norm_from_points(pos_ex_x, pos_ex_y, pos_or_x, pos_or_y)
        self._draw_powerline_bus(pos_ex_x, pos_ex_y,
                                 ex_dir_x, ex_dir_y,
                                 ex_bus)
        watt_value = observation.p_or[line_id]
        if rho > 0.0 and watt_value != 0.0:
            self._draw_powerline_arrow(pos_or_x, pos_or_y,
                                       pos_ex_x, pos_ex_y,
                                       color, watt_value)
        
    def update_powerline(self, figure, observation,
                         line_id, line_name, connected,
                         line_value, line_unit,
                         or_bus, pos_or_x, pos_or_y,
                         ex_bus, pos_ex_x, pos_ex_y):
        pass

    def draw_legend(self, figure, observation):
        legend_help = [
            Line2D([0], [0], color="black", lw=1),
            Line2D([0], [0], color=self._sub_edge_color, lw=3),
            Line2D([0], [0], color=self._load_edge_color, lw=3),
            Line2D([0], [0], color=self._gen_edge_color, lw=3),
            Line2D([0], [0], marker='o', color=self._line_bus_face_colors[0]),
            Line2D([0], [0], marker='o', color=self._line_bus_face_colors[1]),
            Line2D([0], [0], marker='o', color=self._line_bus_face_colors[2])
        ]
        self.ax.legend(legend_help, [
            "powerline",
            "substation",
            "load",
            "generator",
            "no bus",
            "bus 1",
            "bus 2"
        ])
        # Hide axis
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        # Hide frame
        self.ax.set(frame_on=False)

    def plot_postprocess(self, figure, observation, update):
        self.ax.set_xlim(self.xlim[0] - self.xpad, self.xlim[1] + self.xpad)
        self.ax.set_ylim(self.ylim[0] - self.ypad, self.ylim[1] + self.ypad)
