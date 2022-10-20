import os, sys
import time

import traci
import ccparams as cc
import random
from utils import add_vehicle, set_par, change_lane, communicate, \
    get_distance, get_par, start_sumo, running

# from plexe import Plexe

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = os.path.join(os.environ['SUMO_HOME'], 'bin', 'sumo-gui')

SUMO_PARAMS = ["--lateral-resolution", "0.8",
               "--quit-on-end"]

print(sumoBinary)
sumocfg = "cfg/freeway_test.sumocfg"

sumoCmd = [sumoBinary] + SUMO_PARAMS + ["-c", sumocfg]

traci.start(sumoCmd)
step = 0

INTER_VEHICLE_DISTANCE = 5
XI = 1.0
OMEGA_N = 0.2
C1 = 0.5
ACC_HEADWAY = 1.0
INTER_VEHICLE_DISTANCE = 5
PLATOON_LENGTH = 3


class Platoon:
    vehicle_ids = list()
    # plexe = Plexe()

    def __init__(self, platoon_length=1, prefix='Platoon_1_', start_pos=20, start_speed=30.55, start_lane=0,
                 color=(255, 255, 255, 255)):

        # traci.addStepListener(self.plexe)

        for i in range(platoon_length):
            vid = f'{prefix}{i}'

            self.vehicle_ids.append(vid)

            vehicle_length = traci.vehicletype.getLength('PlatoonCar')

            pos = (platoon_length - i + 1) * (INTER_VEHICLE_DISTANCE + vehicle_length) + start_pos

            traci.vehicle.add(vehID=vid, routeID='freeway', departPos=str(pos), departSpeed=str(start_speed),
                              departLane=str(start_lane), typeID='PlatoonCar')
            traci.vehicle.setColor(vid, color)

            traci.vehicle.setSpeedMode(vid, 0)
            traci.vehicle.setLaneChangeMode(vid, 0b0000000000)

            set_par(vid, cc.CC_PAR_CACC_C1, C1)
            set_par(vid, cc.CC_PAR_CACC_XI, XI)
            set_par(vid, cc.CC_PAR_CACC_OMEGA_N, OMEGA_N)
            set_par(vid, cc.PAR_CACC_SPACING, INTER_VEHICLE_DISTANCE)
            set_par(vid, cc.PAR_CC_DESIRED_SPEED, start_speed)

            if i == 0:
                set_par(vid, cc.PAR_ACTIVE_CONTROLLER, cc.ACC)
            else:
                set_par(vid, cc.PAR_ACTIVE_CONTROLLER, cc.CACC)

            # self.plexe.set_path_cacc_parameters(vid, INTER_VEHICLE_DISTANCE, XI, OMEGA_N, C1)
            # self.plexe.set_cc_desired_speed(vid, start_speed)
            # self.plexe.set_acc_headway_time(vid, ACC_HEADWAY)
            # # # keep platoon members in specified lane
            # # self.plexe.set_fixed_lane(vid, 0, safe=False)
            # # # all speed checks off (https://sumo.dlr.de/docs/TraCI/Change_Vehicle_State.html#speed_mode_0xb3)
            #
            # if i == 0:
            #     self.plexe.set_active_controller(vid, 1)
            #     # if par.PLEXE_OVERTAKING_ON:
            #     # plexe.enable_auto_lane_changing(vid, True)
            # else:
            #     self.plexe.set_active_controller(vid, 2)
            #     self.plexe.enable_auto_feed(vid, True, self.vehicle_ids[0], f'{prefix}{i - 1}')
            #     self.plexe.add_member(self.vehicle_ids[0], vid, i)

    def track_with_gui(self):
        traci.gui.trackVehicle('View #0', self.vehicle_ids[0])

    def get_leader_vehicle_id(self):
        return self.vehicle_ids[0]

    def change_lane(self):
        for vid in self.vehicle_ids:
            # vid = f'Platoon_{i}'
            lane_id = traci.vehicle.getLaneID(vid)
            lat_dist = traci.lane.getWidth(lane_id)
            traci.vehicle.setLaneChangeMode(vid, 0b000000000000)
            traci.vehicle.changeSublane(vid, lat_dist)

    def slow_down(self, speed, duration_secs):
        traci.vehicle.slowDown(self.vehicle_ids[0], speed, duration_secs)

    def set_desired_speed(self, speed):
        for vid in self.vehicle_ids:
            self.plexe.set_cc_desired_speed(vid, speed)


my_platoon = Platoon(platoon_length=10, prefix='Platoon_1_', start_pos=20, start_speed=30.55)
my_platoon_2 = Platoon(platoon_length=10, prefix='Platoon_2_', start_pos=20, start_speed=20.55, start_lane=1)
my_platoon.track_with_gui()

traci.simulationStep()

while True:
    step += 1

    if step == 25:
        # my_platoon.change_lane()
        pass
    if step == 200:
        pass
        # my_platoon.slow_down(10.55, 2)
        # my_platoon.set_desired_speed(1.55)

        # plexe.set_cc_desired_speed(vid, 30.55)
    # elif step == 400:
    #     # Lane crossed
    #     # if abs(curr_offset) > 0.5 and lane_offset_last_step * curr_offset < 0:
    #     traci.vehicle.changeSublane('Platoon_0', -1 * curr_offset)

    # lane_offset_last_step = curr_offset
    # print('in else')
    # print(lat_dist)
    # offset = traci.vehicle.getLateralLanePosition('Platoon_0')
    # if abs(offset) <= 0.01 and abs(lat_speed) == 0:
    #     return True
    # traci.vehicle.getLateralSpeed()
    # traci.vehicle.getLateralAlignment()
    # print(traci.vehicle.getLaneIndex('Platoon_0'), traci.vehicle.getLateralLanePosition('Platoon_0'),
    #       traci.vehicle.getLateralAlignment('Platoon_0'))
    traci.simulationStep()
    # print(traci.simulation.getTime())
    # time.sleep(0.010)

traci.close()
# traci.start(sumo_cmd, numRetries=1)
# print(f'TraCI version: {traci.getVersion()}')
# self.plexe = Plexe()
# if use_plexe:
#     print('Adding Plexe to step listener')
#     traci.addStepListener(self.plexe)
