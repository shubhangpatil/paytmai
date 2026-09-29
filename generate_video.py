import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio

def get_fonts():
    try:
        font_title = ImageFont.truetype("segoeuib.ttf", 38)
        font_sub = ImageFont.truetype("segoeuib.ttf", 24)
        font_body = ImageFont.truetype("segoeui.ttf", 20)
        font_badge = ImageFont.truetype("segoeuib.ttf", 16)
        font_hud_title = ImageFont.truetype("segoeuib.ttf", 22)
        font_hud_desc = ImageFont.truetype("segoeui.ttf", 18)
        font_big = ImageFont.truetype("segoeuib.ttf", 52)
    except:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_body = font_title
        font_badge = font_title
        font_hud_title = font_title
        font_hud_desc = font_title
        font_big = font_title
    return {
        "title": font_title,
        "sub": font_sub,
        "body": font_body,
        "badge": font_badge,
        "hud_title": font_hud_title,
        "hud_desc": font_hud_desc,
        "big": font_big
    }

def ease_in_out(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)

def create_gradient_background(w, h, color_top=(5, 18, 42), color_bot=(10, 30, 68)):
    base = Image.new("RGB", (w, h), color_top)
    top = np.array(color_top, dtype=np.float32)
    bot = np.array(color_bot, dtype=np.float32)
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        ratio = y / float(h)
        col = (top * (1.0 - ratio) + bot * ratio).astype(np.uint8)
        arr[y, :] = col
    return Image.fromarray(arr)

def draw_hud(canvas, fonts, top_badge, track_name, feature_tag, feature_title, feature_desc, progress, frame_num):
    draw = ImageDraw.Draw(canvas)
    w, h = canvas.size

    # --- TOP HUD BAR ---
    top_h = 75
    # Semi-transparent dark overlay
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.rectangle([0, 0, w, top_h], fill=(8, 20, 45, 235))
    ov_draw.line([0, top_h, w, top_h], fill=(0, 186, 242, 220), width=2)

    # Top Left: Event Badge
    badge_text = top_badge.upper()
    ov_draw.rounded_rectangle([25, 18, 560, 56], radius=6, fill=(0, 41, 110, 200), outline=(0, 186, 242, 255), width=1)
    
    # Top Right: Track Name Badge
    ov_draw.rounded_rectangle([w - 480, 18, w - 25, 56], radius=6, fill=(18, 38, 70, 220), outline=(255, 184, 0, 255), width=1)

    # --- BOTTOM HUD BANNER ---
    bot_h = 135
    bot_y = h - bot_h
    ov_draw.rectangle([0, bot_y, w, h], fill=(6, 16, 38, 245))
    ov_draw.line([0, bot_y, w, bot_y], fill=(0, 186, 242, 220), width=2)

    # Feature Tag Badge
    ov_draw.rounded_rectangle([35, bot_y + 18, 330, bot_y + 54], radius=6, fill=(0, 186, 242, 230), outline=(255, 255, 255, 255), width=1)

    # Timeline progress bar at very bottom
    prog_w = int(w * max(0.0, min(1.0, progress)))
    ov_draw.rectangle([0, h - 6, w, h], fill=(20, 35, 60, 255))
    ov_draw.rectangle([0, h - 6, prog_w, h], fill=(0, 186, 242, 255))

    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB"))
    draw = ImageDraw.Draw(canvas)

    # Text rendering
    draw.text((38, 25), badge_text, fill=(255, 255, 255), font=fonts["badge"])
    draw.text((w - 460, 25), track_name, fill=(255, 200, 50), font=fonts["badge"])

    # Bottom Banner Text
    draw.text((45, bot_y + 24), feature_tag, fill=(10, 25, 47), font=fonts["badge"])
    draw.text((350, bot_y + 20), feature_title, fill=(255, 255, 255), font=fonts["hud_title"])
    draw.text((35, bot_y + 68), feature_desc, fill=(200, 220, 245), font=fonts["hud_desc"])

    # Animated recording / live indicator
    pulse = (frame_num // 15) % 2 == 0
    dot_color = (0, 230, 130) if pulse else (0, 160, 90)
    draw.ellipse([w - 180, bot_y + 28, w - 164, bot_y + 44], fill=dot_color)
    draw.text((w - 155, bot_y + 25), "LIVE DEMO", fill=(255, 255, 255), font=fonts["badge"])

def draw_focus_bracket(canvas, box_coords, label="FOCUS FEATURE", pulse_val=1.0):
    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x1, y1, x2, y2 = box_coords
    pad = 8
    x1, y1, x2, y2 = x1 - pad, y1 - pad, x2 + pad, y2 + pad

    col_box = (0, 186, 242, int(200 * pulse_val))
    col_glow = (0, 186, 242, int(45 * pulse_val))
    
    # Glow fill
    draw.rectangle([x1, y1, x2, y2], fill=col_glow)

    # Corner brackets
    corner_len = min(35, (x2 - x1) // 4, (y2 - y1) // 4)
    thick = 3
    # Top-Left
    draw.line([x1, y1, x1 + corner_len, y1], fill=col_box, width=thick)
    draw.line([x1, y1, x1, y1 + corner_len], fill=col_box, width=thick)
    # Top-Right
    draw.line([x2, y1, x2 - corner_len, y1], fill=col_box, width=thick)
    draw.line([x2, y1, x2, y1 + corner_len], fill=col_box, width=thick)
    # Bottom-Left
    draw.line([x1, y2, x1 + corner_len, y2], fill=col_box, width=thick)
    draw.line([x1, y2, x1, y2 - corner_len], fill=col_box, width=thick)
    # Bottom-Right
    draw.line([x2, y2, x2 - corner_len, y2], fill=col_box, width=thick)
    draw.line([x2, y2, x2, y2 - corner_len], fill=col_box, width=thick)

    # Badge on top of bracket
    tag_bg = (0, 186, 242, int(230 * pulse_val))
    draw.rectangle([x1, max(76, y1 - 24), x1 + 180, y1], fill=tag_bg)
    
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB"))
    draw_top = ImageDraw.Draw(canvas)
    f = ImageFont.truetype("segoeuib.ttf", 13) if os.path.exists("C:/Windows/Fonts/segoeuib.ttf") else ImageFont.load_default()
    draw_top.text((x1 + 8, max(78, y1 - 22)), f"🎯 {label}", fill=(10, 25, 47), font=f)

def render_scene_title(fonts, frame_idx, total_frames):
    # Scene 1: Opening Vision & Hackathon Badge
    w, h = 1920, 1080
    canvas = create_gradient_background(w, h, (4, 15, 35), (8, 25, 55))
    draw = ImageDraw.Draw(canvas)

    t = frame_idx / float(total_frames)
    scale = 0.96 + 0.08 * t

    # Center card with zoom
    card_w, card_h = int(1400 * scale), int(680 * scale)
    cx, cy = w // 2, h // 2 - 20
    x1, y1 = cx - card_w // 2, cy - card_h // 2
    x2, y2 = cx + card_w // 2, cy + card_h // 2

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ov = ImageDraw.Draw(overlay)
    ov.rounded_rectangle([x1, y1, x2, y2], radius=24, fill=(12, 28, 60, 220), outline=(0, 186, 242, 255), width=3)
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB"))
    draw = ImageDraw.Draw(canvas)

    # Top Tag
    draw.text((cx - 360, y1 + 55), "PAYTM BUILD FOR INDIA AI HACKATHON • MUMBAI EDITION (OCT 3)", fill=(0, 186, 242), font=fonts["badge"])
    
    # Title
    t_text = "Paytm AI: Voice & Memory"
    draw.text((cx - 360, y1 + 95), t_text, fill=(255, 255, 255), font=fonts["big"])
    
    sub1 = "For 30 Million Bharat Shopkeepers"
    draw.text((cx - 360, y1 + 175), sub1, fill=(255, 184, 0), font=fonts["title"])

    sub2 = "Autonomous Multi-Agent AI System across 3 Core Tracks"
    draw.text((cx - 360, y1 + 240), sub2, fill=(190, 210, 235), font=fonts["sub"])

    # 4 Tech Stack Pills
    pills = [
        ("SARVAM AI", "Indic Voice STT/TTS", (0, 186, 242)),
        ("COGNEE", "Graph Memory Engine", (255, 184, 0)),
        ("N8N", "Autonomous Agent Router", (40, 210, 130)),
        ("PAYTM ECOSYSTEM", "Soundbox & UPI Gateway", (0, 186, 242))
    ]
    pill_w = 260
    pill_start_x = cx - (len(pills) * pill_w + (len(pills)-1)*20) // 2
    py = y1 + 320
    for i, (p_title, p_desc, col) in enumerate(pills):
        px = pill_start_x + i * (pill_w + 20)
        draw.rounded_rectangle([px, py, px + pill_w, py + 110], radius=12, fill=(18, 40, 80), outline=col, width=2)
        draw.text((px + 18, py + 22), p_title, fill=col, font=fonts["sub"])
        draw.text((px + 18, py + 62), p_desc, fill=(220, 230, 245), font=fonts["badge"])

    # 3 Track Badges at bottom of card
    t_badges = [
        "Track 1: VyaparDost (Voice Store Copilot)",
        "Track 2: JanSuraksha (60s Micro-Claims)",
        "Track 3: OpsGuard (Dispute Teammate)"
    ]
    draw.text((cx - 430, y1 + 475), " • ".join(t_badges), fill=(160, 190, 225), font=fonts["body"])

    draw_hud(canvas, fonts,
             "PAYTM AI HACKATHON • MUMBAI EDITION",
             "SUBMISSION DECK • OCT 3, 2026",
             "EXECUTIVE STRATEGY",
             "Voice & Memory for 30 Million Shopkeepers",
             "Combining Sarvam AI, Cognee Graph & n8n Workflows with Paytm Soundbox & UPI Disbursal.",
             t * 0.15, frame_idx)
    return canvas

def render_scene_architecture(fonts, frame_idx, total_frames):
    # Scene 2: Unified Architecture with Zoom
    w, h = 1920, 1080
    canvas = create_gradient_background(w, h, (5, 16, 38), (10, 28, 62))
    t = frame_idx / float(total_frames)

    # Base diagram dimensions
    diag_w, diag_h = 1600, 720
    base_diag = Image.new("RGB", (diag_w, diag_h), (12, 28, 58))
    bd_draw = ImageDraw.Draw(base_diag)

    # Draw Architecture Layers
    layers = [
        ("LAYER 1: PAYTM CLIENT & HARDWARE LAYER",
         "Paytm Soundbox 4.0 (Audio Mic/Speaker)  •  Paytm Merchant Mobile App  •  QR Scanner / POS Transaction Stream",
         (0, 186, 242)),
        ("LAYER 2: INDIC VOICE INTELLIGENCE (SARVAM AI)",
         "Real-time STT / TTS Gateway  •  10+ Indian Regional Languages (Hindi, Marathi, Gujarati, Telugu, Tamil, Kannada)",
         (0, 186, 242)),
        ("LAYER 3: CONTEXTUAL MEMORY GRAPH (COGNEE)",
         "Merchant Cashflow Ledger Graph  •  Risk & Fraud Geolocation Nodes  •  Customer Visit Frequency Knowledge Graph",
         (255, 184, 0)),
        ("LAYER 4: AUTONOMOUS MULTI-AGENT ORCHESTRATOR (N8N)",
         "Event Router  •  Automated WhatsApp Retargeting  •  Instant Claim Evaluation Engine  •  UPI Disbursal Webhook",
         (40, 210, 130)),
        ("LAYER 5: PAYTM CORE INFRASTRUCTURE & SETTLEMENT",
         "Paytm UPI Instant Disbursal API  •  Postpaid Micro-Credit Rails  •  Paytm Merchant Wallet Settlement",
         (0, 186, 242))
    ]

    ly = 20
    layer_rects = []
    for l_title, l_desc, col in layers:
        rect = [30, ly, diag_w - 30, ly + 115]
        layer_rects.append(rect)
        bd_draw.rounded_rectangle(rect, radius=12, fill=(18, 42, 85), outline=col, width=2)
        bd_draw.text((55, ly + 18), l_title, fill=col, font=fonts["sub"])
        bd_draw.text((55, ly + 58), l_desc, fill=(230, 240, 255), font=fonts["body"])
        ly += 140

    # Determine Camera Pan & Zoom based on phase
    # Phase A (0.0 - 0.35): Overview
    # Phase B (0.35 - 0.70): Zoom into Layers 2 & 3 (Sarvam + Cognee)
    # Phase C (0.70 - 1.0): Pan/Zoom into Layer 4 & 5 (n8n + UPI)
    if t < 0.35:
        sub_t = ease_in_out(t / 0.35)
        zoom = 1.0 + 0.1 * sub_t
        focus_center = (diag_w / 2, diag_h / 2)
        target_box = None
        f_tag = "ARCHITECTURE OVERVIEW"
        f_title = "5-Layer End-to-End Enterprise Architecture"
        f_desc = "Unifying edge hardware (Soundbox) with AI models, graph memory, and payment settlement."
    elif t < 0.70:
        sub_t = ease_in_out((t - 0.35) / 0.35)
        zoom = 1.1 + 0.45 * sub_t
        focus_center = (diag_w / 2, 280) # Layer 2 & 3
        target_box = (150, 200, 1770, 520)
        f_tag = "INTELLIGENCE CORE: SARVAM + COGNEE"
        f_title = "Indic Voice Understanding + Graph Memory Engine"
        f_desc = "Sarvam converts regional speech into text; Cognee grounds queries in live merchant cashflow graphs."
    else:
        sub_t = ease_in_out((t - 0.70) / 0.30)
        zoom = 1.55 - 0.1 * sub_t
        focus_center = (diag_w / 2, 530) # Layer 4 & 5
        target_box = (150, 480, 1770, 780)
        f_tag = "ACTION ENGINE: N8N + PAYTM UPI"
        f_title = "Multi-Agent Autonomous Orchestration & Instant Settlement"
        f_desc = "n8n decision router triggers automated WhatsApp vouchers, micro-claims, and <60s UPI payouts."

    # Render Zoomed View of base_diag onto canvas
    cw, ch = int(diag_w / zoom), int((h - 220) / zoom)
    cx, cy = focus_center
    x1 = max(0, min(diag_w - cw, int(cx - cw / 2)))
    y1 = max(0, min(diag_h - ch, int(cy - ch / 2)))
    crop = base_diag.crop((x1, y1, x1 + cw, y1 + ch)).resize((1800, h - 220), Image.Resampling.BICUBIC)
    canvas.paste(crop, (60, 85))

    if target_box:
        pulse = 0.8 + 0.2 * math.sin(frame_idx * 0.2)
        draw_focus_bracket(canvas, target_box, f_tag, pulse)

    draw_hud(canvas, fonts,
             "PAYTM AI ARCHITECTURE • MUMBAI HACKATHON",
             "SYSTEM BLUEPRINT • TRIPLE-TRACK UNIFIED",
             f_tag, f_title, f_desc,
             0.15 + t * 0.15, frame_idx)
    return canvas

def render_ui_showcase(fonts, img_path, frame_idx, total_frames, track_name, track_badge, features_timeline):
    # Dynamic Ken Burns Zoom on UI Screenshots
    w, h = 1920, 1080
    canvas = create_gradient_background(w, h, (4, 14, 34), (8, 22, 50))
    t = frame_idx / float(total_frames)

    base_ui = Image.open(img_path).convert("RGB")
    ui_w, ui_h = base_ui.size

    # Find which feature we are currently demonstrating
    # features_timeline is list of: (start_t, end_t, center_norm, zoom_level, box_norm, tag, title, desc)
    cur_feat = features_timeline[0]
    for feat in features_timeline:
        if feat[0] <= t <= feat[1]:
            cur_feat = feat
            break

    start_t, end_t, center_norm, zoom_level, box_norm, tag, title, desc = cur_feat
    local_t = (t - start_t) / max(0.001, (end_t - start_t))
    local_t = ease_in_out(local_t)

    # Smooth zoom interpolation
    base_zoom = 1.05
    target_zoom = base_zoom + (zoom_level - base_zoom) * local_t
    focus_cx = ui_w * center_norm[0]
    focus_cy = ui_h * center_norm[1]

    # Crop and scale UI
    view_h = h - 220
    aspect = 1.33 if ui_w > ui_h else 0.58
    dest_w = int(view_h * aspect)
    dest_h = view_h

    # Zoom window on original image
    zw = int(ui_w / target_zoom)
    zh = int(ui_h / target_zoom)
    zx1 = max(0, min(ui_w - zw, int(focus_cx - zw / 2)))
    zy1 = max(0, min(ui_h - zh, int(focus_cy - zh / 2)))
    crop_ui = base_ui.crop((zx1, zy1, zx1 + zw, zy1 + zh)).resize((dest_w, dest_h), Image.Resampling.BICUBIC)

    # Center placement or left placement with right feature card
    ui_x = (w - dest_w) // 2
    ui_y = 85
    canvas.paste(crop_ui, (ui_x, ui_y))

    # Border around UI mockup
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([ui_x - 3, ui_y - 3, ui_x + dest_w + 3, ui_y + dest_h + 3], outline=(0, 186, 242), width=3)

    # Transform box_norm to screen coordinates
    if box_norm:
        bx1_norm, by1_norm, bx2_norm, by2_norm = box_norm
        # Map from original coords to crop coords to screen coords
        box_px_x1 = (bx1_norm * ui_w - zx1) / zw * dest_w + ui_x
        box_px_y1 = (by1_norm * ui_h - zy1) / zh * dest_h + ui_y
        box_px_x2 = (bx2_norm * ui_w - zx1) / zw * dest_w + ui_x
        box_px_y2 = (by2_norm * ui_h - zy1) / zh * dest_h + ui_y

        box_screen = (int(box_px_x1), int(box_px_y1), int(box_px_x2), int(box_px_y2))
        pulse = 0.8 + 0.2 * math.sin(frame_idx * 0.2)
        draw_focus_bracket(canvas, box_screen, tag, pulse)

    draw_hud(canvas, fonts,
             track_badge,
             track_name,
             tag, title, desc,
             0.30 + t * 0.55, frame_idx)
    return canvas

def render_scene_finale(fonts, frame_idx, total_frames):
    # Scene 6: Closing Pitch & Jury Evaluation Blueprint
    w, h = 1920, 1080
    canvas = create_gradient_background(w, h, (4, 12, 30), (8, 24, 55))
    t = frame_idx / float(total_frames)

    scale = 0.98 + 0.04 * ease_in_out(t)
    cx, cy = w // 2, h // 2 - 15

    # Center panel
    pw, ph = int(1550 * scale), int(700 * scale)
    x1, y1 = cx - pw // 2, cy - ph // 2
    x2, y2 = cx + pw // 2, cy + ph // 2

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ov = ImageDraw.Draw(overlay)
    ov.rounded_rectangle([x1, y1, x2, y2], radius=24, fill=(12, 28, 62, 235), outline=(0, 186, 242, 255), width=3)
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB"))
    draw = ImageDraw.Draw(canvas)

    draw.text((cx - 400, y1 + 45), "PAYTM BUILD FOR INDIA AI HACKATHON • MUMBAI FINALE", fill=(0, 186, 242), font=fonts["badge"])
    draw.text((cx - 400, y1 + 80), "The Winning Pitch Formula", fill=(255, 255, 255), font=fonts["big"])
    draw.text((cx - 400, y1 + 160), "Why Paytm AI Wins 1st Place on October 3rd in Mumbai", fill=(255, 184, 0), font=fonts["title"])

    # 4 Judging Criteria Pillars
    pillars = [
        ("AI INNOVATION", "Sarvam Indic Voice + Cognee Graph Memory", "10+ Regional Languages, zero app friction", (0, 186, 242)),
        ("AUTONOMOUS ACTION", "n8n Multi-Agent Workflow Automation", "<60s end-to-end claim and refund disbursal", (255, 184, 0)),
        ("PAYTM ECOSYSTEM", "100% Fit for Soundbox, App & UPI Rails", "Immediately scalable to 30M+ merchants", (40, 210, 130)),
        ("STAGE 'WOW' FACTOR", "Live Soundbox Hindi Audio Interaction", "Real-time WhatsApp alert firing on phones", (0, 186, 242))
    ]

    col_w = 340
    start_px = cx - (4 * col_w + 3 * 20) // 2
    py = y1 + 240
    for i, (title, sub, metric, col) in enumerate(pillars):
        px = start_px + i * (col_w + 20)
        draw.rounded_rectangle([px, py, px + col_w, py + 190], radius=12, fill=(18, 42, 85), outline=col, width=2)
        draw.text((px + 16, py + 20), title, fill=col, font=fonts["sub"])
        draw.text((px + 16, py + 65), sub, fill=(255, 255, 255), font=fonts["hud_desc"])
        draw.text((px + 16, py + 125), "Impact: " + metric, fill=(200, 220, 245), font=fonts["badge"])

    # Pro-tip banner
    draw.rounded_rectangle([cx - 650, y1 + 465, cx + 650, y1 + 555], radius=10, fill=(0, 41, 110), outline=(255, 184, 0), width=2)
    draw.text((cx - 620, y1 + 482), "🎤 ON-STAGE DEMO HOOK FOR JURY (OCT 3):", fill=(255, 184, 0), font=fonts["badge"])
    draw.text((cx - 620, y1 + 510), "Speak Hindi directly into Paytm Soundbox mic -> Soundbox answers back in Hindi -> n8n graph fires live on stage!", fill=(255, 255, 255), font=fonts["body"])

    draw.text((cx - 320, y1 + 585), "Project: Paytm AI Voice & Memory  •  Participant: Shubhang Patil  •  October 3, 2026", fill=(170, 195, 230), font=fonts["body"])

    draw_hud(canvas, fonts,
             "PAYTM AI MUMBAI HACKATHON",
             "FINAL JURY BLUEPRINT",
             "WINNING SUMMARY", "Ready for Stage Demo & Evaluation",
             "Complete autonomous voice AI stack addressing 30M shopkeepers across India.",
             0.85 + t * 0.15, frame_idx)
    return canvas

def generate_video(output_mp4_path):
    print("Initializing video rendering pipeline...")
    fonts = get_fonts()
    fps = 30

    assets_dir = r"C:\Users\shubh\paytmai\assets"
    img_vyapar = os.path.join(assets_dir, "vyapardost_merchant_ui_1790517076186.jpg")
    img_suraksha = os.path.join(assets_dir, "jansuraksha_claim_ui_1790517104424.jpg")
    img_opsguard = os.path.join(assets_dir, "opsguard_dashboard_ui_1790517130036.jpg")

    # Features timeline configurations
    vyapar_features = [
        # (start_t, end_t, center_norm, zoom_level, box_norm, tag, title, desc)
        (0.0, 0.25, (0.5, 0.5), 1.05, None,
         "TRACK 1: OVERVIEW", "Paytm VyaparDost Merchant Copilot",
         "Autonomous voice-first store manager living directly inside Paytm Soundbox and Merchant App."),
        (0.25, 0.60, (0.5, 0.28), 1.65, (0.1, 0.18, 0.9, 0.38),
         "FEATURE: SARVAM VOICE COPILOT", "Conversational Regional Voice Insights",
         "Merchant asks in Hindi: 'Aaj kitna dhandha hua?' AI queries Cognee graphs and speaks audio answer via Soundbox."),
        (0.60, 1.0, (0.5, 0.72), 1.60, (0.1, 0.58, 0.9, 0.86),
         "FEATURE: N8N WHATSAPP RETENTION", "Autonomous Repeat Customer Retention",
         "Tracks QR scan inactivity (14 days) and automatically triggers localized WhatsApp discount vouchers via n8n.")
    ]

    suraksha_features = [
        (0.0, 0.25, (0.5, 0.5), 1.05, None,
         "TRACK 2: OVERVIEW", "Paytm JanSuraksha Micro-Claims & Lending",
         "60-second micro-insurance claims and micro-lending copilot for street vendors and small merchants."),
        (0.25, 0.60, (0.5, 0.30), 1.65, (0.1, 0.18, 0.9, 0.42),
         "FEATURE: ZERO-PAPERWORK CLAIM", "15-Second Voice Note + Damage Photo",
         "Street vendors submit flood/fire insurance claims via quick voice notes in native tongue. No tedious paper forms."),
        (0.60, 1.0, (0.5, 0.75), 1.65, (0.1, 0.60, 0.9, 0.90),
         "FEATURE: COGNEE GRAPH FRAUD & UPI", "Contextual Fraud Audit & <60s Disbursal",
         "Audits claim against Soundbox history and flood data. n8n triggers instant claim payout to Paytm Wallet in 60s.")
    ]

    opsguard_features = [
        (0.0, 0.25, (0.5, 0.5), 1.05, None,
         "TRACK 3: OVERVIEW", "Paytm OpsGuard Autonomous Teammate",
         "Autonomous operations teammate for payment disputes, failed UPI transactions, and Soundbox hardware diagnostics."),
        (0.25, 0.60, (0.35, 0.40), 1.55, (0.08, 0.22, 0.62, 0.65),
         "FEATURE: DISPUTE AUTO-TRIAGE", "Multi-Agent UPI Dispute Ingestion",
         "Failed UPI transfers and chargebacks are ingested instantly and analyzed by autonomous n8n agent routers."),
        (0.60, 1.0, (0.75, 0.55), 1.60, (0.55, 0.30, 0.95, 0.78),
         "FEATURE: SARVAM OUTBOUND CALL", "Autonomous Outbound Voice Verification & Refund",
         "AI calls merchant in native dialect to verify transaction context and issues instant Paytm wallet refund.")
    ]

    # Scene durations (in seconds):
    # Scene 1: Title (8s = 240 frames)
    # Scene 2: Architecture (14s = 420 frames)
    # Scene 3: Track 1 VyaparDost (16s = 480 frames)
    # Scene 4: Track 2 JanSuraksha (16s = 480 frames)
    # Scene 5: Track 3 OpsGuard (16s = 480 frames)
    # Scene 6: Finale / Pitch Blueprint (10s = 300 frames)
    # Total = 80 seconds = 2400 frames
    scene_defs = [
        ("title", 240),
        ("arch", 420),
        ("vyapar", 480),
        ("suraksha", 480),
        ("opsguard", 480),
        ("finale", 300)
    ]
    total_video_frames = sum(count for _, count in scene_defs)
    print(f"Total video duration: {total_video_frames / fps:.1f}s ({total_video_frames} frames @ {fps}fps)")

    writer = imageio.get_writer(
        output_mp4_path,
        fps=fps,
        codec="libx264",
        pixelformat="yuv420p",
        macro_block_size=1,
        ffmpeg_params=["-preset", "fast", "-crf", "20"]
    )

    frame_counter = 0

    # 1. Title Scene
    print("Rendering Scene 1: Executive Title & Vision...")
    n_frames = 240
    for i in range(n_frames):
        frame = render_scene_title(fonts, i, n_frames)
        writer.append_data(np.array(frame))
        frame_counter += 1

    # 2. Architecture Scene
    print("Rendering Scene 2: Unified System Architecture...")
    n_frames = 420
    for i in range(n_frames):
        frame = render_scene_architecture(fonts, i, n_frames)
        writer.append_data(np.array(frame))
        frame_counter += 1

    # 3. Track 1 VyaparDost
    print("Rendering Scene 3: Track 1 VyaparDost...")
    n_frames = 480
    for i in range(n_frames):
        frame = render_ui_showcase(fonts, img_vyapar, i, n_frames,
                                   "TRACK 1: VYAPARDOST",
                                   "PAYTM BUILD FOR INDIA • MUMBAI",
                                   vyapar_features)
        writer.append_data(np.array(frame))
        frame_counter += 1

    # 4. Track 2 JanSuraksha
    print("Rendering Scene 4: Track 2 JanSuraksha...")
    n_frames = 480
    for i in range(n_frames):
        frame = render_ui_showcase(fonts, img_suraksha, i, n_frames,
                                   "TRACK 2: JANSURAKSHA AI",
                                   "PAYTM BUILD FOR INDIA • MUMBAI",
                                   suraksha_features)
        writer.append_data(np.array(frame))
        frame_counter += 1

    # 5. Track 3 OpsGuard
    print("Rendering Scene 5: Track 3 OpsGuard...")
    n_frames = 480
    for i in range(n_frames):
        frame = render_ui_showcase(fonts, img_opsguard, i, n_frames,
                                   "TRACK 3: OPSGUARD AI",
                                   "PAYTM BUILD FOR INDIA • MUMBAI",
                                   opsguard_features)
        writer.append_data(np.array(frame))
        frame_counter += 1

    # 6. Finale
    print("Rendering Scene 6: Finale & Pitch Blueprint...")
    n_frames = 300
    for i in range(n_frames):
        frame = render_scene_finale(fonts, i, n_frames)
        writer.append_data(np.array(frame))
        frame_counter += 1

    writer.close()
    print(f"Video saved successfully to: {output_mp4_path}")

if __name__ == "__main__":
    out_video = r"C:\Users\shubh\paytmai\Paytm_AI_Hackathon_Presentation_Video.mp4"
    generate_video(out_video)
