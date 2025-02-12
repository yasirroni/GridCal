# GridCal
# Copyright (C) 2022 Santiago Peñate Vera
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import numpy as np
import scipy.sparse as sp
import GridCal.Engine.Core.topology as tp


class TransformerData:

    def __init__(self, ntr, nbus, ntime=1):
        """

        :param ntr:
        :param nbus:
        """
        self.ntr = ntr
        self.ntime = ntime

        self.tr_names = np.zeros(ntr, dtype=object)
        self.tr_active = np.zeros((ntr, ntime), dtype=int)
        self.tr_R = np.zeros(ntr, dtype=float)
        self.tr_X = np.zeros(ntr, dtype=float)
        self.tr_G = np.zeros(ntr, dtype=float)
        self.tr_B = np.zeros(ntr)

        self.tr_tap_f = np.ones(ntr)  # tap generated by the difference in nominal voltage at the form side
        self.tr_tap_t = np.ones(ntr)  # tap generated by the difference in nominal voltage at the to side
        self.tr_tap_mod = np.ones(ntr)  # normal tap module
        self.tr_tap_ang = np.zeros(ntr)  # normal tap angle
        self.tr_is_bus_to_regulated = np.zeros(ntr, dtype=bool)
        self.tr_bus_to_regulated_idx = np.zeros(ntr, dtype=int)
        self.tr_tap_position = np.zeros(ntr, dtype=int)
        self.tr_min_tap = np.zeros(ntr, dtype=int)
        self.tr_max_tap = np.zeros(ntr, dtype=int)
        self.tr_tap_inc_reg_up = np.zeros(ntr)
        self.tr_tap_inc_reg_down = np.zeros(ntr)
        self.tr_vset = np.ones(ntr)
        self.tr_control_mode = np.zeros(ntr, dtype=object)

        self.C_tr_bus = sp.lil_matrix((ntr, nbus), dtype=int)  # this ons is just for splitting islands

    def slice(self, tr_idx, bus_idx, time_idx=None):
        """

        :param tr_idx:
        :param bus_idx:
        :param time_idx
        :return:
        """
        if time_idx is None:
            idx = tr_idx
        else:
            idx = np.ix_(tr_idx, time_idx)

        data = TransformerData(ntr=len(tr_idx), nbus=len(bus_idx))

        data.tr_active = self.tr_active[idx]

        data.tr_names = self.tr_names[tr_idx]
        data.tr_R = self.tr_R[tr_idx]
        data.tr_X = self.tr_X[tr_idx]
        data.tr_G = self.tr_G[tr_idx]
        data.tr_B = self.tr_B[tr_idx]

        data.tr_tap_f = self.tr_tap_f[tr_idx]
        data.tr_tap_t = self.tr_tap_t[tr_idx]
        data.tr_tap_mod = self.tr_tap_mod[tr_idx]
        data.tr_tap_ang = self.tr_tap_ang[tr_idx]
        data.tr_is_bus_to_regulated = self.tr_is_bus_to_regulated[tr_idx]
        data.tr_tap_position = self.tr_tap_position[tr_idx]
        data.tr_min_tap = self.tr_min_tap[tr_idx]
        data.tr_max_tap = self.tr_max_tap[tr_idx]
        data.tr_tap_inc_reg_up = self.tr_tap_inc_reg_up[tr_idx]
        data.tr_tap_inc_reg_down = self.tr_tap_inc_reg_down[tr_idx]
        data.tr_vset = self.tr_vset[tr_idx]

        data.C_tr_bus = self.C_tr_bus[np.ix_(tr_idx, bus_idx)]

        return data

    def get_island(self, bus_idx, t_idx=0):
        """
        Get the elements of the island given the bus indices
        :param bus_idx: list of bus indices
        :return: list of line indices of the island
        """
        if self.ntr:
            return tp.get_elements_of_the_island(self.C_tr_bus, bus_idx, active=self.tr_active[:, t_idx])
        else:
            return np.zeros(0, dtype=int)

    def __len__(self):
        return self.ntr
