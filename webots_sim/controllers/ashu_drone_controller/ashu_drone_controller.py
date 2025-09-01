"""
ashu_drone_controller.py – Minimal DJI Mavic 2 control (Webots R2023b)
- Hovers at target altitude
- Optional 2D waypoints
- Saves camera frames to <project>/data
- Optional VARI overlay saved alongside frames
"""
from controller import Robot
import os
import numpy as np
import cv2

# Flags
USE_WAYPOINTS = False
WAYPOINTS = [(0.0, 0.0, 5.0), (3.0, 0.0, 5.0), (3.0, 3.0, 5.0), (0.0, 0.0, 5.0)]
SAVE_VARI_OVERLAY = False

def clamp(x, lo, hi):
    return max(lo, min(hi, x))

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, os.pardir, os.pardir, os.pardir))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

if SAVE_VARI_OVERLAY:
    from .vari_overlay import compute_vari, save_vari_overlay

robot = Robot()
TIME_STEP = int(robot.getBasicTimeStep())

imu  = robot.getDevice('inertial unit'); imu.enable(TIME_STEP)
gps  = robot.getDevice('gps');           gps.enable(TIME_STEP)
cam  = robot.getDevice('camera');        cam.enable(TIME_STEP)

fl = robot.getDevice('front left propeller')
fr = robot.getDevice('front right propeller')
rl = robot.getDevice('rear left propeller')
rr = robot.getDevice('rear right propeller')
for m in (fl, fr, rl, rr):
    m.setPosition(float('inf'))
    m.setVelocity(0.0)

BASE_THRUST = 68.0
KP_ALT, KD_ALT = 60.0, 15.0
KP_XZ = 0.8
MAX_RPM = 110.0
prev_alt_err = 0.0

if USE_WAYPOINTS:
    wp_i = 0
    tx, tz, target_alt = WAYPOINTS[wp_i]
else:
    tx, tz, target_alt = 0.0, 0.0, 5.0

step = 0
while robot.step(TIME_STEP) != -1:
    x, y, z = gps.getValues()

    alt_err = (target_alt - y)
    alt_der = alt_err - prev_alt_err
    prev_alt_err = alt_err
    thrust = BASE_THRUST + KP_ALT * alt_err + KD_ALT * alt_der

    ex = (tx - x)
    ez = (tz - z)
    cmd_pitch = clamp(+KP_XZ * ex, -0.3, 0.3)
    cmd_roll  = clamp(-KP_XZ * ez, -0.3, 0.3)

    pitch_mix = cmd_pitch * 25.0
    roll_mix  = cmd_roll  * 25.0

    fl_rpm = clamp(thrust - pitch_mix - roll_mix, 0, MAX_RPM)
    rr_rpm = clamp(thrust + pitch_mix + roll_mix, 0, MAX_RPM)
    fr_rpm = clamp(thrust - pitch_mix + roll_mix, 0, MAX_RPM)
    rl_rpm = clamp(thrust + pitch_mix - roll_mix, 0, MAX_RPM)

    fl.setVelocity(fl_rpm); fr.setVelocity(fr_rpm)
    rl.setVelocity(rl_rpm); rr.setVelocity(rr_rpm)

    if step % 30 == 0:
        w, h = cam.getWidth(), cam.getHeight()
        bgra = np.frombuffer(cam.getImage(), dtype=np.uint8).reshape((h, w, 4))
        bgr = bgra[:, :, :3]
        rgb = bgr[:, :, ::-1]
        frame_path = os.path.join(DATA_DIR, f'webots_frame_{step:05d}.png')
        cv2.imwrite(frame_path, bgr)

        if SAVE_VARI_OVERLAY:
            vari = compute_vari(rgb)
            overlay_path = os.path.join(DATA_DIR, f'webots_frame_{step:05d}_vari.png')
            save_vari_overlay(rgb, vari, overlay_path, alpha=0.4)

    if USE_WAYPOINTS:
        if abs(x - tx) < 0.3 and abs(z - tz) < 0.3 and abs(y - target_alt) < 0.3:
            wp_i = (wp_i + 1) % len(WAYPOINTS)
            tx, tz, target_alt = WAYPOINTS[wp_i]

    step += 1