# Webots (R2023b) – AgriSwarmRL

This project uses the Webots DJI Mavic 2 Pro robot and a custom Python controller
(`ashu_drone_controller`) to hover, follow simple waypoints, and save camera frames
into your project `data/` folder for NDVI/VARI processing.

## Prereqs
- Webots R2023b installed
- Python venv at: `D:\Solo-projects\AgriSwarmRL\.venv`
- In Webots: **Tools → Preferences → Python →** set to
  `D:\Solo-projects\AgriSwarmRL\.venv\Scripts\python.exe`

## How to run
1. Open world: `webots_sim/worlds/dji_mavic_2_agri.wbt`
2. In Scene Tree, select `DJIMavic2Pro` and confirm its `controller` is `ashu_drone_controller`.
3. Make sure your venv is active in CMD:
   ```cmd
   cd D:\Solo-projects\AgriSwarmRL
   .\.venv\Scripts\activate
   ```
4. Hit **Run ▶** in Webots. The drone will lift to ~5 m and save frames at `data/webots_frame_*.png`.

## Tuning
- If the drone rises too fast or too slow: edit `BASE_THRUST` in `ashu_drone_controller.py`.
- To fly to multiple points: set `USE_WAYPOINTS = True` and edit `WAYPOINTS` in the same file.
- To save NDVI/VARI overlays for each frame: set `SAVE_VARI_OVERLAY = True`.

## Paths
- Data output: `D:\Solo-projects\AgriSwarmRL\data`
- Results (from notebooks): `D:\Solo-projects\AgriSwarmRL\results`

## Troubleshooting
- `ModuleNotFoundError: cv2/numpy` → Preferences → Python path must point to your venv; restart Webots.
- Wobbly hover → reduce `KP_ALT`, increase `KD_ALT`, and/or adjust clamps.
- No images saved → check that `data/` exists; the controller creates it if missing.