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


class LoadData:

    def __init__(self, nload, nbus, ntime=1):
        """

        :param nload:
        :param nbus:
        :param ntime:
        """
        self.nload = nload
        self.ntime = ntime

        self.load_names = np.empty(nload, dtype=object)

        self.load_active = np.zeros((nload, ntime), dtype=bool)
        self.load_s = np.zeros((nload, ntime), dtype=complex)
        self.load_i = np.zeros((nload, ntime), dtype=complex)
        self.load_y = np.zeros((nload, ntime), dtype=complex)

        self.C_bus_load = sp.lil_matrix((nbus, nload), dtype=int)

    def slice(self, elm_idx, bus_idx, time_idx=None):
        """

        :param elm_idx:
        :param bus_idx:
        :param time_idx:
        :return:
        """

        if time_idx is None:
            tidx = elm_idx
        else:
            tidx = np.ix_(elm_idx, time_idx)

        data = LoadData(nload=len(elm_idx), nbus=len(bus_idx))

        data.load_names = self.load_names[elm_idx]

        data.load_active = self.load_active[tidx]
        data.load_s = self.load_s[tidx]
        data.load_i = self.load_i[tidx]
        data.load_y = self.load_y[tidx]

        data.C_bus_load = self.C_bus_load[np.ix_(bus_idx, elm_idx)]

        return data

    def get_island(self, bus_idx, t_idx=0):
        if self.nload:
            return tp.get_elements_of_the_island(self.C_bus_load.T, bus_idx,
                                                 active=self.load_active[t_idx])
        else:
            return np.zeros(0, dtype=int)

    def get_effective_load(self):
        return self.load_s * self.load_active

    def get_injections_per_bus(self):
        return - self.C_bus_load * self.get_effective_load()

    def get_current_injections_per_bus(self):
        return - self.C_bus_load * (self.load_i * self.load_active)

    def get_admittance_injections_per_bus(self):
        return - self.C_bus_load * (self.load_y * self.load_active)

    def __len__(self):
        return self.nload


class LoadOpfData(LoadData):

    def __init__(self, nload, nbus, ntime=1):
        """

        :param nload:
        :param nbus:
        :param ntime:
        """
        LoadData.__init__(self, nload, nbus, ntime)

        self.load_cost = np.zeros((nload, ntime))

    def slice(self, elm_idx, bus_idx, time_idx=None):
        """

        :param elm_idx:
        :param bus_idx:
        :param time_idx:
        :return:
        """

        if time_idx is None:
            tidx = elm_idx
        else:
            tidx = np.ix_(elm_idx, time_idx)

        data = LoadData(nload=len(elm_idx), nbus=len(bus_idx))

        data.load_names = self.load_names[elm_idx]

        data.load_active = self.load_active[tidx]
        data.load_s = self.load_s[tidx]
        data.load_cost = self.load_cost[tidx]

        data.C_bus_load = self.C_bus_load[np.ix_(bus_idx, elm_idx)]

        return data
