# vari_overlay.py – compute and save VARI overlays
import numpy as np
import cv2
import os

# VARI: (G - R) / (G + R - B + 1e-6)
def compute_vari(rgb_image_uint8: np.ndarray) -> np.ndarray:
    img = rgb_image_uint8.astype(np.float32) / 255.0
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    vari = (g - r) / (g + r - b + 1e-6)
    return np.clip(vari, -1.0, 1.0)

# Save heatmap overlay (using OpenCV colormap for controller-side light deps)
def save_vari_overlay(rgb_image_uint8: np.ndarray, vari_map: np.ndarray, out_path: str, alpha: float = 0.4):
    mn, mx = float(vari_map.min()), float(vari_map.max())
    norm = (vari_map - mn) / (mx - mn + 1e-6)
    heat = (norm * 255.0).astype(np.uint8)
    heat = cv2.applyColorMap(heat, cv2.COLORMAP_JET)  # BGR
    base = cv2.cvtColor(rgb_image_uint8, cv2.COLOR_RGB2BGR)
    overlay = cv2.addWeighted(heat, alpha, base, 1.0 - alpha, 0)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cv2.imwrite(out_path, overlay)