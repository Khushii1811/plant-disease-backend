"""
src/models/gradcam.py — Grad-CAM Heatmap Extraction for ConvNeXt-Tiny DualHead.

Generates activation heatmaps from the final convolutional stage (features[7])
to explain disease localization on foliar pathology images.

Adheres strictly to:
1. Running within torch.enable_grad().
2. Model zero_grad(set_to_none=True) post-computation.
3. try...finally cleanup of forward and backward hooks.
4. Bilinear interpolation computed at model input resolution (256x256).
5. Output capped at 512 px on the longer side, preserving aspect ratio.
6. Encoded as WebP (format="WEBP", quality=85) to minimize payload size.
"""

import base64
import io
from typing import Optional, Tuple

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image


def generate_gradcam(
    model: torch.nn.Module,
    tensor: torch.Tensor,
    target_class_idx: int,
    target_size: Optional[Tuple[int, int]] = None,
) -> str:
    """
    Generate a base64-encoded WebP Grad-CAM heatmap for ConvNeXt-Tiny.

    Parameters:
        model: Evaluated DualHeadConvNeXt PyTorch model.
        tensor: Normalized input tensor of shape [1, 3, 256, 256].
        target_class_idx: Predicted disease class index for gradient targeting.
        target_size: Optional (width, height) of the original uploaded image.

    Returns:
        Data URL string 'data:image/webp;base64,...' representing the RGB heatmap,
        capped to at most 512 px on the longer side.
    """
    if not hasattr(model, "features") or len(model.features) < 8:
        return ""

    target_layer = model.features[7]
    activations = []
    gradients = []

    def _forward_hook(module, inp, out):
        activations.append(out)

    def _backward_hook(module, grad_in, grad_out):
        gradients.append(grad_out[0])

    f_handle = target_layer.register_forward_hook(_forward_hook)
    b_handle = target_layer.register_full_backward_hook(_backward_hook)

    try:
        model.eval()
        with torch.enable_grad():
            inp = tensor.clone().detach().requires_grad_(True)
            _, d_logits = model(inp)
            score = d_logits[0, target_class_idx]
            model.zero_grad(set_to_none=True)
            score.backward(retain_graph=False)

        if not activations or not gradients:
            return ""

        act = activations[0]  # [1, 768, 8, 8]
        grad = gradients[0]   # [1, 768, 8, 8]

        # Channel-wise spatial mean of gradients
        weights = grad.mean(dim=(2, 3), keepdim=True)
        cam = (weights * act).sum(dim=1, keepdim=True)
        cam = F.relu(cam)

        cam_min = cam.min()
        cam_max = cam.max()
        if cam_max > cam_min:
            cam = (cam - cam_min) / (cam_max - cam_min)
        else:
            cam = torch.zeros_like(cam)

        # 1. Compute at model input resolution (256x256)
        cam = F.interpolate(cam, size=(256, 256), mode="bilinear", align_corners=False)
        cam_np = cam[0, 0].detach().cpu().numpy()

        # Pure NumPy Jet Colormap mapping: [0, 1] -> RGB
        v = np.clip(cam_np, 0.0, 1.0)
        r = np.clip(1.5 - np.abs(4.0 * v - 3.0), 0.0, 1.0)
        g = np.clip(1.5 - np.abs(4.0 * v - 2.0), 0.0, 1.0)
        b = np.clip(1.5 - np.abs(4.0 * v - 1.0), 0.0, 1.0)
        rgb = (np.stack([r, g, b], axis=-1) * 255).astype(np.uint8)

        img = Image.fromarray(rgb, mode="RGB")

        # 2. Cap returned image to at most 512 px on longer side, matching target aspect ratio
        if target_size is not None and len(target_size) == 2:
            orig_w, orig_h = target_size
            max_side = max(orig_w, orig_h)
            if max_side > 512:
                scale = 512.0 / max_side
                out_w = max(1, int(round(orig_w * scale)))
                out_h = max(1, int(round(orig_h * scale)))
            else:
                out_w, out_h = orig_w, orig_h
            if (out_w, out_h) != (256, 256):
                img = img.resize((out_w, out_h), Image.Resampling.BILINEAR)

        # 3. Encode as WebP (capped quality to minimize bandwidth and memory)
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=85)
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/webp;base64,{b64}"
    except Exception:
        return ""
    finally:
        f_handle.remove()
        b_handle.remove()
        model.zero_grad(set_to_none=True)
