#!/usr/bin/env python
#
# Copyright (c) 2022 Abhishek Bharambe <abhishek.bharambe@sjsu.edu>
# Copyright (c) 2022 Eugene Clewlow <eugene.clewlow@sjsu.edu>
# Copyright (c) 2022 Kanak Kshirsagar <kanak.kshirsagar@sjsu.edu>
# Copyright (c) 2022 Spoorthi Devanand <spoorthi.devanand@sjsu.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

import pytest
from Simulation import Simulation
from Vehicle import Vehicle, vehicle_counter
from Platoon import Platoon
from PlatoonManager import platoon_manager
from VehicleManager import vehicle_manager
import traci


# Arrange
@pytest.fixture(autouse=True, params=[4])
def before_after(request):
    request.config.sim = Simulation()
    yield
    platoon_manager.reset()
    vehicle_counter.reset()
    vehicle_manager.reset()
    assert True


# @pytest.mark.skip(reason="uncomment this to skip this test")
def test_add_slow_vehicle_and_track_platoon(request):
    simulation = request.config.sim

    platoon = simulation.add_platoon(platoon_length=6, platoon_start_position=50,
                                     platoon_start_lane=Platoon.DEFAULT_LANE,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(vehicle_start_position=6 * (platoon.vehicle_length + platoon.min_gap),
                                            vehicle_start_lane=1, vehicle_start_speed=30)
    slow_vehicle_2 = simulation.add_vehicle(vehicle_start_position=15 * (platoon.vehicle_length + platoon.min_gap),
                                            vehicle_start_lane=0, vehicle_start_speed=30)

    simulation.set_simulation_time_length(10)  # end simulation after 10 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


# @pytest.mark.skip(reason="uncomment this to skip this test")
def test_add_slow_vehicle_and_require_overtake(request):
    simulation = request.config.sim

    platoon = simulation.add_platoon(platoon_length=6, platoon_start_position=50,
                                     platoon_start_lane=Platoon.DEFAULT_LANE,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(vehicle_start_position=6 * (platoon.vehicle_length + platoon.min_gap),
                                            vehicle_start_lane=2, vehicle_start_speed=30)
    slow_vehicle_2 = simulation.add_vehicle(vehicle_start_position=10 * (platoon.vehicle_length + platoon.min_gap),
                                            vehicle_start_lane=1, vehicle_start_speed=10)

    simulation.set_simulation_time_length(60)  # end simulation after 25 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


@pytest.mark.skip(reason="uncomment this to skip this test")
def test_unable_to_split(request):
    simulation = request.config.sim

    platoon = simulation.add_platoon(platoon_length=6, platoon_start_position=50,
                                     platoon_start_lane=Platoon.DEFAULT_LANE,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(vehicle_start_position=15 * (platoon.vehicle_length + platoon.min_gap),
                                            vehicle_start_lane=1, vehicle_start_speed=30)
    slow_vehicle_2 = simulation.add_vehicle(vehicle_start_position=18 * (platoon.vehicle_length + platoon.min_gap),
                                            vehicle_start_lane=2, vehicle_start_speed=30)

    simulation.set_simulation_time_length(40)  # end simulation after 40 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


# @pytest.mark.skip(reason="uncomment this to skip this test")
def test_four_vehicle_split(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 7 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6, platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=Platoon.DEFAULT_LANE,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 13 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=0, vehicle_start_speed=30)
    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 13 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 19 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=2, vehicle_start_speed=30)
    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 13 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=3, vehicle_start_speed=30)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(slow_vehicle_2)

    simulation.run()


# @pytest.mark.skip(reason="uncomment this to skip this test")
def test_three_vehicle_split(request):
    simulation = request.config.sim

    platoon = simulation.add_platoon(platoon_length=6, platoon_start_position=50,
                                     platoon_start_lane=Platoon.DEFAULT_LANE,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(vehicle_start_position=14 * (platoon.vehicle_length + platoon.min_gap),
                                            vehicle_start_lane=1, vehicle_start_speed=30)
    slow_vehicle_2 = simulation.add_vehicle(vehicle_start_position=19 * (platoon.vehicle_length + platoon.min_gap),
                                            vehicle_start_lane=2, vehicle_start_speed=30)

    simulation.set_simulation_time_length(30)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(slow_vehicle_2)

    simulation.run()


# @pytest.mark.skip(reason="uncomment this to skip this test")
def test_dangerous_situation(request):
    simulation = request.config.sim

    platoon = simulation.add_platoon(platoon_length=6, platoon_start_position=50,
                                     platoon_start_lane=Platoon.DEFAULT_LANE,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(vehicle_start_position=6 * (platoon.vehicle_length + platoon.min_gap),
                                            vehicle_start_lane=1, vehicle_start_speed=30)
    slow_vehicle_2 = simulation.add_vehicle(vehicle_start_position=15 * (platoon.vehicle_length + platoon.min_gap),
                                            vehicle_start_lane=2, vehicle_start_speed=30)
    merging_vehicle = simulation.add_vehicle(vehicle_start_position=12 * (platoon.vehicle_length + platoon.min_gap),
                                             vehicle_start_lane=0, vehicle_start_speed=30,
                                             commands={
                                                 1000: Vehicle.CMD_CHANGE_LANE_LEFT})  # at 10 seconds change lanes

    simulation.set_simulation_time_length(10)  # end simulation after 10 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


# @pytest.mark.skip(reason="uncomment this to skip this test")
def test_requires_v2v_change_lanes_right(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 6 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=2,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 12 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=False)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + (12 - 3) * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=2, vehicle_start_speed=30, v2v=True)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


def test_requires_platoon_overtake_left(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 7 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=1,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=0, vehicle_start_speed=30, v2v=True)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 14 * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=False)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


def test_requires_platoon_overtake_right(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 7 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=1,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=2, vehicle_start_speed=30, v2v=True)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 9 * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=False)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


def test_platoon_signals_neighbor_v2v(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 7 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=2,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=3, vehicle_start_speed=30, v2v=False)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 9 * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=2, vehicle_start_speed=30, v2v=False)
    slow_vehicle_3 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=True)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


def test_platoon_signals_multiple_neighbor_v2v(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 7 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=2,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=3, vehicle_start_speed=30, v2v=False)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 9 * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=2, vehicle_start_speed=30, v2v=False)
    slow_vehicle_3 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=True)
    slow_vehicle_4 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 4 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=True)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


def test_platoon_signals_multiple_neighbor_v2v_one_car_not_v2v(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 7 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=2,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=3, vehicle_start_speed=30, v2v=False)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 9 * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=2, vehicle_start_speed=30, v2v=False)
    slow_vehicle_3 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=True)
    slow_vehicle_4 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 4 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=False)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


def test_platoon_signals_multiple_neighbor_v2v_one_car_not_v2v_but_split_possible(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 7 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=2,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=3, vehicle_start_speed=30, v2v=False)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 9 * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=2, vehicle_start_speed=30, v2v=False)
    slow_vehicle_3 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 7 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=True)
    slow_vehicle_4 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 3 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=False)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


##########################################################################################
# Start Demo Here
##########################################################################################

def test_platoon_signals_multiple_neighbor_v2v_left_car_request(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 7 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=2,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=3, vehicle_start_speed=30, v2v=True)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 9 * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=2, vehicle_start_speed=30, v2v=False)
    slow_vehicle_3 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=True)
    slow_vehicle_4 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 4 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=False)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


def test_platoon_requires_split(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 7 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=2,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=3, vehicle_start_speed=30, v2v=False)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 11 * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=2, vehicle_start_speed=30, v2v=False)
    slow_vehicle_3 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=False)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


def test_requires_v2v_change_lanes_left(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 6 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=1,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 12 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=0, vehicle_start_speed=30, v2v=True)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 13 * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=30, v2v=True)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


def test_platoon_requires_double_lane_change(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 7 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=2,
                                     platoon_desired_speed=50)

    slow_vehicle_1 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=3, vehicle_start_speed=35, v2v=False)
    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 11 * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=2, vehicle_start_speed=30, v2v=False)
    slow_vehicle_3 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 6 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=35, v2v=False)
    slow_vehicle_4 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 4 * (platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=1, vehicle_start_speed=40, v2v=False)

    simulation.set_simulation_time_length(60)  # end simulation after 30 seconds

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()


def test_platoon_with_random_traffic(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 7 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=2,
                                     platoon_desired_speed=27.8)

    car_vehicle_length = traci.vehicletype.getLength('V2V_Car')
    car_min_gap = traci.vehicletype.getMinGap('V2V_Car')

    lane_count = 3
    how_many_cars_long = 100

    import random
    from datetime import datetime

    # Random number with system time
    random.seed(datetime.now())

    new_list = [(x, y) for x in range(lane_count) for y in range(how_many_cars_long)]
    random.shuffle(new_list)

    for i in range(0, 50):
        start_lane, start_position = new_list[i]
        simulation.add_vehicle(
            vehicle_start_position=platoon_start_pos + 6 * (
                    platoon.vehicle_length + platoon.min_gap) + start_position * 2 * (
                                           car_vehicle_length + car_min_gap),
            vehicle_start_lane=start_lane, vehicle_start_speed=22.2, v2v=random.choice([True, False]))

    # simulation.set_simulation_time_length(60)  # end simulation after 30 seconds
    simulation.set_simulation_platoon_run_distance(3200)

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    total_simulation_time = simulation.run()

    print(total_simulation_time)


def test_platoon_with_random_traffic_non_v2v(request):
    simulation = request.config.sim

    platoon_vehicle_length = traci.vehicletype.getLength('PlatoonCar')
    platoon_min_gap = traci.vehicletype.getMinGap('PlatoonCar')
    platoon_start_pos = 10 * (platoon_vehicle_length + platoon_min_gap)

    platoon = simulation.add_platoon(platoon_length=6,
                                     platoon_start_position=platoon_start_pos,
                                     platoon_start_lane=2,
                                     platoon_desired_speed=50)

    slow_vehicle_2 = simulation.add_vehicle(
        vehicle_start_position=platoon_start_pos + 15 * (
                platoon.vehicle_length + platoon.min_gap),
        vehicle_start_lane=2, vehicle_start_speed=30, v2v=False)

    import random

    for y in range(1, 600):
        slow_vehicle_y = simulation.add_vehicle(
            vehicle_start_position=20 + (3 * y) * (platoon.vehicle_length + platoon.min_gap),
            vehicle_start_lane=0, vehicle_start_speed=random.randint(25, 45), v2v=False)
        slow_vehicle_y = simulation.add_vehicle(
            vehicle_start_position=20 + (5 * y) * (platoon.vehicle_length + platoon.min_gap),
            vehicle_start_lane=0, vehicle_start_speed=random.randint(25, 45), v2v=False)
        slow_vehicle_3y = simulation.add_vehicle(
            vehicle_start_position=20 + (2 * y) * (platoon.vehicle_length + platoon.min_gap),
            vehicle_start_lane=1, vehicle_start_speed=random.randint(30, 45), v2v=False)
        slow_vehicle_y = simulation.add_vehicle(
            vehicle_start_position=20 + (5 * y) * (platoon.vehicle_length + platoon.min_gap),
            vehicle_start_lane=1, vehicle_start_speed=random.randint(25, 40), v2v=False)
        slow_vehicle_3y = simulation.add_vehicle(
            vehicle_start_position=20 + (6 * y) * (platoon.vehicle_length + platoon.min_gap),
            vehicle_start_lane=3, vehicle_start_speed=random.randint(30, 40), v2v=False)
        """slow_vehicle_y = simulation.add_vehicle(
            vehicle_start_position=20 + (3 * y) * (platoon.vehicle_length + platoon.min_gap),
            vehicle_start_lane=3, vehicle_start_speed=random.randint(25, 40), v2v=False)"""
        slow_vehicle_3y = simulation.add_vehicle(
            vehicle_start_position=20 + (4 * y) * (platoon.vehicle_length + platoon.min_gap),
            vehicle_start_lane=4, vehicle_start_speed=random.randint(30, 40), v2v=False)
        """slow_vehicle_y = simulation.add_vehicle(
            vehicle_start_position=platoon_start_pos + ( 17* y) * (platoon.vehicle_length + platoon.min_gap),
            vehicle_start_lane=2, vehicle_start_speed=random.randint(25, 40), v2v=False)"""
        slow_vehicle_3y = simulation.add_vehicle(
            vehicle_start_position=platoon_start_pos + (12 * y) * (platoon.vehicle_length + platoon.min_gap),
            vehicle_start_lane=0, vehicle_start_speed=random.randint(30, 35), v2v=False)

    simulation.set_simulation_platoon_run_distance(10000)

    simulation.set_zoom(20000)
    simulation.track_vehicle(platoon.vehicles[0])

    simulation.run()
