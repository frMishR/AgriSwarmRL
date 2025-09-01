# AgriSwarmRL – Drone Vision & Reinforcement Learning for Precision Farming

## 📌 Overview
AgriSwarmRL is a research-driven project exploring how semantic segmentation of satellite/drone imagery and reinforcement learning (RL) can enable intelligent agricultural drone swarms. The current progress focuses on vegetation index computation (NDVI/VARI) from Sentinel Playground satellite images and simulated drone images (Webots). These indices provide the foundation for RL-based navigation and area coverage.

## 🌱 Vision Module (Completed)
**NDVI/VARI Segmentation:**
- NDVI (Normalized Difference Vegetation Index) – requires NIR band.
- VARI (Visible Atmospherically Resistant Index) – proxy for RGB-only data (Sentinel images).

**Implemented Features:**
- Loaded sample field images (synthetic, Sentinel satellite, Webots drone exports).
- Computed NDVI/VARI per pixel, generated vegetation heatmaps.
- Produced binary vegetation masks (vegetation=1, barren=0).
- Calculated area statistics (% vegetation per image).
- Saved masks and overlays to `/results/` for downstream RL use.
- Modular pipeline: any new image dropped into `/data/` is auto-processed.

## 🗂️ Folder Structure
AgriSwarmRL/
├── data/                     # Input Sentinel/Drone images (RGB)
├── ndvi_seg/
│   ├── ndvi_demo.ipynb                   # NDVI/VARI explainer (single image)
│   └── ndvi_segmentation_satellite.ipynb # Batch pipeline (finalized)
├── webots_sim/                # Drone simulation (future)
├── rl_agent/
│   └── ppo_agent.ipynb        # PPO integration (future)
├── results/                   # Masks, overlays, visualizations
├── utils/                     # Helper functions (future expansion)
├── README.md
├── requirements.txt
└── .gitignore

## 📅 Project Roadmap
1. ✅ Phase 1 – Vision (DONE): NDVI/VARI segmentation module finalized.
2. 🔜 Phase 2 – Rule-Based Drone Control (NEXT): Waypoint navigation, NDVI-driven rules in Webots.
3. 🔜 Phase 3 – RL Agent (PPO): Custom Gym env, RL reward shaping from masks, PPO training.
4. 🔜 Phase 4 – Multi-Drone Swarm: Collision avoidance, coordination, vegetation coverage.
5. 🔜 Phase 5 – Demo & GitHub Polish: MP4 demo, final README, recruiter-ready docs.

## ⚙️ Requirements
- Python 3.10+
- OpenCV
- numpy
- matplotlib
- tqdm
- stable-baselines3 (for PPO, later phase)
- Webots (drone simulation)
- moviepy (for MP4 demos, later phase)

Install all dependencies:
pip install -r requirements.txt

## 🚩 Status
- ✅ Vegetation segmentation pipeline **complete & tested**
- ✅ Outputs saved for RL integration
- ⏸️ Project paused (next: Webots rule-based drone control)

## 🚧 Under Construction
This project is actively being developed.
Stay tuned for updates as reinforcement learning and multi-agent drone swarms are added in the next phases!