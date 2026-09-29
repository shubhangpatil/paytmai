import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path):
    prs = Presentation()
    # 16:9 Widescreen slides
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide layout

    # Colors
    c_bg_dark = RGBColor(10, 25, 47)      # Deep Navy
    c_card_bg = RGBColor(18, 38, 70)      # Lighter Card Navy
    c_paytm_cyan = RGBColor(0, 186, 242)  # Paytm Cyan
    c_paytm_blue = RGBColor(0, 41, 112)   # Paytm Deep Blue
    c_gold = RGBColor(255, 184, 0)        # Accent Gold
    c_white = RGBColor(255, 255, 255)
    c_gray = RGBColor(180, 195, 215)
    c_green = RGBColor(40, 200, 120)

    assets_dir = r"C:\Users\shubh\paytmai\assets"
    img_vyapar = os.path.join(assets_dir, "vyapardost_merchant_ui_1790517076186.jpg")
    img_suraksha = os.path.join(assets_dir, "jansuraksha_claim_ui_1790517104424.jpg")
    img_opsguard = os.path.join(assets_dir, "opsguard_dashboard_ui_1790517130036.jpg")

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.color.rgb = color
        return bg

    def add_header(slide, title_text, category_text="PAYTM BUILD FOR INDIA AI HACKATHON • MUMBAI EDITION (OCT 3)"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = c_paytm_cyan

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = c_white

    # ============================================================
    # SLIDE 1: Title Slide
    # ============================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, c_bg_dark)

    # Accent bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.15), Inches(5.0))
    bar.fill.solid()
    bar.fill.fore_color.rgb = c_paytm_cyan
    bar.line.fill.background()

    # Title box
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(5.0))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "PAYTM BUILD FOR INDIA AI HACKATHON • MUMBAI EDITION"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = c_paytm_cyan

    p1 = tf1.add_paragraph()
    p1.text = "Paytm AI: Voice & Contextual Memory\nfor 30 Million Bharat Merchants"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = c_white
    p1.space_before = Pt(14)
    p1.space_after = Pt(14)

    p2 = tf1.add_paragraph()
    p2.text = "Triple-Track Autonomous AI Solution | Powered by Sarvam AI + Cognee + n8n"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = c_gold
    p2.space_after = Pt(20)

    p3 = tf1.add_paragraph()
    p3.text = "Track 1: VyaparDost (Voice Store Copilot)  |  Track 2: JanSuraksha (60s Micro-Claims)  |  Track 3: OpsGuard (Dispute Teammate)\nEvent Date: 3rd October 2026 • Mumbai, India • Team Submission Deck"
    p3.font.size = Pt(13)
    p3.font.color.rgb = c_gray

    # ============================================================
    # SLIDE 2: Problem & Bharat-First Vision
    # ============================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, c_bg_dark)
    add_header(s2, "The Problem in Bharat: 30M Shopkeepers Left Behind by Text AI")

    cards_data = [
        ("1. Linguistic & Literacy Barrier",
         "• 80%+ shopkeepers in Tier 2/3/4 operate exclusively in regional languages (Hindi, Marathi, Gujarati).\n• Complex fintech apps and keyboards create severe operational friction.\n• Shopkeepers want to talk to their business, not type numbers into spreadsheets.",
         c_paytm_cyan),
        ("2. Cashflow & Working Capital Blindspots",
         "• Merchants lack formal bookkeeping and real-time cashflow visibility.\n• Seasonal sales spikes and festival inventory runs lead to sudden stockouts.\n• Micro-insurance & working capital loans require weeks of tedious paperwork.",
         c_gold),
        ("3. Payment Disputes & Downtime Frustration",
         "• Failed UPI transfers or chargebacks leave merchants feeling helpless.\n• Calling customer care wastes hours of peak business time.\n• Hardware soundbox issues disrupt daily shopkeeper trust and revenue.",
         c_green),
    ]

    left_positions = [Inches(0.8), Inches(4.8), Inches(8.8)]
    for i, (ctitle, cdesc, accent_c) in enumerate(cards_data):
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_positions[i], Inches(1.8), Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = accent_c
        card.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(left_positions[i] + Inches(0.2), Inches(2.0), Inches(3.3), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = ctitle
        pt.font.size = Pt(17)
        pt.font.bold = True
        pt.font.color.rgb = accent_c

        pd = tf.add_paragraph()
        pd.text = cdesc
        pd.font.size = Pt(13)
        pd.font.color.rgb = c_white
        pd.space_before = Pt(14)

    # ============================================================
    # SLIDE 3: The Winning Formula & Partner Tech Stack
    # ============================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, c_bg_dark)
    add_header(s3, "The Winning Formula: 100% Partner Tech Stack Synergy")

    partners = [
        ("SARVAM AI", "Indic Voice Intelligence",
         "• High-fidelity Indian English, Hindi, Marathi, Gujarati STT/TTS\n• Seamless voice streaming with authentic regional accents\n• Zero app friction: Merchants speak and listen via Paytm Soundbox",
         c_paytm_cyan),
        ("COGNEE", "Contextual Memory Graph",
         "• Dynamic knowledge graphs mapping merchant cashflow history\n• Transaction stability, fraud geolocation maps, and vendor relationships\n• Instant context recall for zero-hallucination decisions",
         c_gold),
        ("N8N", "Autonomous Agent Orchestrator",
         "• Multi-agent event router executing real-world financial actions\n• Automated WhatsApp coupon dispatch & customer retention\n• Instant UPI refund & claims payout triggers (<60 seconds)",
         c_green),
        ("PAYTM ECOSYSTEM", "Hardware & Core APIs",
         "• Soundbox 4.0 / Voicebox live audio output & mic hardware\n• Paytm Merchant POS & QR dynamic transaction feed\n• Paytm Postpaid, Wallet & Instant UPI Disbursal Gateway",
         c_paytm_cyan),
    ]

    p_lefts = [Inches(0.8), Inches(3.8), Inches(6.8), Inches(9.8)]
    for i, (pname, psub, pdesc, pc) in enumerate(partners):
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, p_lefts[i], Inches(1.8), Inches(2.75), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = pc
        card.line.width = Pt(1.5)

        tb = s3.shapes.add_textbox(p_lefts[i] + Inches(0.15), Inches(2.0), Inches(2.45), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = pname
        pt.font.size = Pt(16)
        pt.font.bold = True
        pt.font.color.rgb = pc

        ps = tf.add_paragraph()
        ps.text = psub
        ps.font.size = Pt(12)
        ps.font.bold = True
        ps.font.color.rgb = c_white
        ps.space_before = Pt(4)

        pd = tf.add_paragraph()
        pd.text = pdesc
        pd.font.size = Pt(11)
        pd.font.color.rgb = c_gray
        pd.space_before = Pt(12)

    # ============================================================
    # SLIDE 4: End-to-End System Architecture
    # ============================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, c_bg_dark)
    add_header(s4, "System Architecture: From Soundbox Voice to Real-World Settlement")

    arch_layers = [
        ("Layer 1: Edge & Client Layer", "Paytm Soundbox Mic/Speaker  •  Paytm Merchant Mobile App  •  QR Scanner & POS Telemetry", c_paytm_cyan),
        ("Layer 2: Indic Voice Gateway", "Sarvam AI Multilingual Speech-to-Text & Text-to-Speech (Hindi, Marathi, Gujarati, Telugu)", c_paytm_cyan),
        ("Layer 3: Contextual Memory Graph", "Cognee Graph Engine: Merchant Ledger Graph, Geo-Risk Nodes, Customer Visit Frequency Graph", c_gold),
        ("Layer 4: Multi-Agent Orchestration", "n8n Autonomous Decision Workflows: Disbursal Engine, WhatsApp Campaigner, Dispute Arbiter", c_green),
        ("Layer 5: Paytm Core Infrastructure", "Paytm UPI Instant Settlement Gateway  •  Postpaid Micro-Credit  •  Merchant Wallet API", c_paytm_cyan)
    ]

    top_y = Inches(1.8)
    for title, desc, col in arch_layers:
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), top_y, Inches(11.33), Inches(0.9))
        box.fill.solid()
        box.fill.fore_color.rgb = c_card_bg
        box.line.color.rgb = col
        box.line.width = Pt(1.5)

        tb = s4.shapes.add_textbox(Inches(1.2), top_y + Inches(0.08), Inches(10.9), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = title.upper()
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = col

        pd = tf.add_paragraph()
        pd.text = desc
        pd.font.size = Pt(12)
        pd.font.color.rgb = c_white
        pd.space_before = Pt(2)

        top_y += Inches(1.05)

    # ============================================================
    # SLIDE 5: Track 1 - Paytm VyaparDost
    # ============================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, c_bg_dark)
    add_header(s5, "Track 1: Paytm VyaparDost — Autonomous Voice Store Copilot")

    if os.path.exists(img_vyapar):
        s5.shapes.add_picture(img_vyapar, Inches(0.8), Inches(1.8), Inches(3.2), Inches(5.1))

    card_t1 = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.3), Inches(1.8), Inches(8.2), Inches(5.1))
    card_t1.fill.solid()
    card_t1.fill.fore_color.rgb = c_card_bg
    card_t1.line.color.rgb = c_paytm_cyan
    card_t1.line.width = Pt(1.5)

    tb_t1 = s5.shapes.add_textbox(Inches(4.6), Inches(2.0), Inches(7.6), Inches(4.6))
    tf_t1 = tb_t1.text_frame
    tf_t1.word_wrap = True

    p_t1_0 = tf_t1.paragraphs[0]
    p_t1_0.text = "CORE INNOVATIONS FOR 30M SHOPKEEPERS"
    p_t1_0.font.size = Pt(14)
    p_t1_0.font.bold = True
    p_t1_0.font.color.rgb = c_paytm_cyan

    items_t1 = [
        ("1. Conversational Voice Financial Insights", "Merchant asks in Hindi: 'Aaj kitna dhandha hua? Kal ka kya plan hai?' Sarvam AI transcribes speech, Cognee queries the merchant's financial knowledge graph, and Paytm Soundbox vocalizes concise Hindi audio analysis."),
        ("2. Autonomous Customer Retention via n8n", "n8n tracks repeat customer QR scans. If a regular customer hasn't visited in 14 days, the AI orchestrator automatically creates and dispatches a personalized WhatsApp discount coupon in their native language."),
        ("3. Predictive Inventory & Festival Purchasing", "Graph memory detects festival surges (Diwali, Eid, Ganesh Utsav) and warns of stockouts 5 days in advance, providing automated supplier price comparisons and post-paid credit recommendations.")
    ]

    for title, body in items_t1:
        pt = tf_t1.add_paragraph()
        pt.text = title
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = c_gold
        pt.space_before = Pt(12)

        pb = tf_t1.add_paragraph()
        pb.text = body
        pb.font.size = Pt(12)
        pb.font.color.rgb = c_white
        pb.space_before = Pt(3)

    # ============================================================
    # SLIDE 6: Track 2 - Paytm JanSuraksha AI
    # ============================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, c_bg_dark)
    add_header(s6, "Track 2: Paytm JanSuraksha AI — 60-Second Micro-Claims & Micro-Lending")

    if os.path.exists(img_suraksha):
        s6.shapes.add_picture(img_suraksha, Inches(0.8), Inches(1.8), Inches(3.2), Inches(5.1))

    card_t2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.3), Inches(1.8), Inches(8.2), Inches(5.1))
    card_t2.fill.solid()
    card_t2.fill.fore_color.rgb = c_card_bg
    card_t2.line.color.rgb = c_gold
    card_t2.line.width = Pt(1.5)

    tb_t2 = s6.shapes.add_textbox(Inches(4.6), Inches(2.0), Inches(7.6), Inches(4.6))
    tf_t2 = tb_t2.text_frame
    tf_t2.word_wrap = True

    p_t2_0 = tf_t2.paragraphs[0]
    p_t2_0.text = "ZERO-PAPERWORK FINANCIAL SECURITY FOR BHARAT"
    p_t2_0.font.size = Pt(14)
    p_t2_0.font.bold = True
    p_t2_0.font.color.rgb = c_gold

    items_t2 = [
        ("1. 15-Second Voice Claim Submission", "Street vendors and stall owners file weather/flood damage claims using a quick voice note in their native tongue + a single camera snap. Zero forms, zero bureaucratic delay."),
        ("2. Cognee Multi-Graph Fraud Engine", "Instead of slow manual assessors, Cognee validates the claim against historical Soundbox activity patterns, local meteorological flood feeds, and shop geolocation consistency scores."),
        ("3. Instant 60-Second Claim Payout via UPI", "Upon AI verification, n8n executes the automated disbursal webhook to Paytm UPI / Wallet in under 60 seconds, restoring merchant business continuity on the exact same day.")
    ]

    for title, body in items_t2:
        pt = tf_t2.add_paragraph()
        pt.text = title
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = c_paytm_cyan
        pt.space_before = Pt(12)

        pb = tf_t2.add_paragraph()
        pb.text = body
        pb.font.size = Pt(12)
        pb.font.color.rgb = c_white
        pb.space_before = Pt(3)

    # ============================================================
    # SLIDE 7: Track 3 - Paytm OpsGuard AI
    # ============================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, c_bg_dark)
    add_header(s7, "Track 3: Paytm OpsGuard AI — Autonomous AI Operations Teammate")

    if os.path.exists(img_opsguard):
        s7.shapes.add_picture(img_opsguard, Inches(0.8), Inches(1.8), Inches(6.0), Inches(5.1))

    card_t3 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.8), Inches(5.4), Inches(5.1))
    card_t3.fill.solid()
    card_t3.fill.fore_color.rgb = c_card_bg
    card_t3.line.color.rgb = c_green
    card_t3.line.width = Pt(1.5)

    tb_t3 = s7.shapes.add_textbox(Inches(7.3), Inches(2.0), Inches(5.0), Inches(4.6))
    tf_t3 = tb_t3.text_frame
    tf_t3.word_wrap = True

    p_t3_0 = tf_t3.paragraphs[0]
    p_t3_0.text = "AUTONOMOUS RESOLUTION FOR HARDWARE & DISPUTES"
    p_t3_0.font.size = Pt(14)
    p_t3_0.font.bold = True
    p_t3_0.font.color.rgb = c_green

    items_t3 = [
        ("1. Multi-Agent UPI Dispute Ingestion", "Failed UPI debits or merchant chargebacks are ingested instantly by n8n and categorized with sub-second accuracy."),
        ("2. Outbound Native Voice Verification", "When transaction status is ambiguous between banking rails, Sarvam AI triggers an autonomous outbound phone call to the customer/merchant in their regional dialect to confirm transaction context."),
        ("3. Self-Healing Hardware Logistics", "Identifies faulty Soundbox battery or SIM errors via IoT diagnostics and automatically dispatches replacement units via logistics webhooks.")
    ]

    for title, body in items_t3:
        pt = tf_t3.add_paragraph()
        pt.text = title
        pt.font.size = Pt(13)
        pt.font.bold = True
        pt.font.color.rgb = c_paytm_cyan
        pt.space_before = Pt(10)

        pb = tf_t3.add_paragraph()
        pb.text = body
        pb.font.size = Pt(11.5)
        pb.font.color.rgb = c_white
        pb.space_before = Pt(3)

    # ============================================================
    # SLIDE 8: 36-Hour Hackathon Roadmap (Oct 3rd Mumbai)
    # ============================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, c_bg_dark)
    add_header(s8, "36-Hour Hackathon Execution Roadmap & Milestones")

    phases = [
        ("Hours 00 – 12", "Foundation & Pipeline",
         "• Sarvam AI Speech STT/TTS pipeline setup\n• Simulated Paytm Soundbox & POS telemetry stream\n• Schema ingestion into Cognee Knowledge Graph\n• Initial Hindi/Marathi voice loop verification",
         c_paytm_cyan),
        ("Hours 12 – 24", "Intelligence & Orchestration",
         "• Connect Cognee memory graph to decision agent\n• Build n8n multi-agent routers & triggers\n• Wire WhatsApp Cloud API for automated coupons\n• Implement <60s micro-claim validation pipeline",
         c_gold),
        ("Hours 24 – 36", "Polish & Live Pitch Readiness",
         "• Live Soundbox hardware audio output test\n• Full end-to-end voice scenario stress testing\n• Edge case validation on dialect variations\n• Pitch deck rehearsal & live jury QA setup",
         c_green),
    ]

    r_lefts = [Inches(0.8), Inches(4.8), Inches(8.8)]
    for i, (ph_name, ph_sub, ph_desc, pc) in enumerate(phases):
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, r_lefts[i], Inches(1.8), Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = c_card_bg
        card.line.color.rgb = pc
        card.line.width = Pt(1.5)

        tb = s8.shapes.add_textbox(r_lefts[i] + Inches(0.2), Inches(2.0), Inches(3.3), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = ph_name
        pt.font.size = Pt(18)
        pt.font.bold = True
        pt.font.color.rgb = pc

        ps = tf.add_paragraph()
        ps.text = ph_sub
        ps.font.size = Pt(14)
        ps.font.bold = True
        ps.font.color.rgb = c_white
        ps.space_before = Pt(4)

        pd = tf.add_paragraph()
        pd.text = ph_desc
        pd.font.size = Pt(12)
        pd.font.color.rgb = c_gray
        pd.space_before = Pt(14)

    # ============================================================
    # SLIDE 9: Jury Evaluation Criteria & The Stage Demo Hook
    # ============================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, c_bg_dark)
    add_header(s9, "Jury Evaluation Criteria & The On-Stage Demo Strategy")

    criteria = [
        ("AI Innovation", "Integrated Sarvam Voice + Cognee Graph Memory", "10+ Indic languages supported with sub-second voice latency"),
        ("Autonomous Action", "n8n multi-agent workflows executing real financial APIs", "<60s end-to-end claim and refund disbursal time"),
        ("Paytm Synergy", "Direct fit for Soundbox, Merchant App, QR and Postpaid", "Addresses 30M+ active Paytm merchants immediately"),
        ("Stage 'Wow' Factor", "Live voice conversation through actual Soundbox speaker", "Real-time WhatsApp alert firing on audience phone")
    ]

    t_top = Inches(1.8)
    for crit, approach, metric in criteria:
        box = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), t_top, Inches(11.33), Inches(0.95))
        box.fill.solid()
        box.fill.fore_color.rgb = c_card_bg
        box.line.color.rgb = c_paytm_cyan
        box.line.width = Pt(1.5)

        tb = s9.shapes.add_textbox(Inches(1.2), t_top + Inches(0.08), Inches(10.9), Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        pt = tf.paragraphs[0]
        pt.text = crit.upper() + "  —  " + approach
        pt.font.size = Pt(14)
        pt.font.bold = True
        pt.font.color.rgb = c_gold

        pd = tf.add_paragraph()
        pd.text = "Key Metric / Impact: " + metric
        pd.font.size = Pt(12)
        pd.font.color.rgb = c_white
        pd.space_before = Pt(3)

        t_top += Inches(1.1)

    # Pro-tip banner
    protip = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(6.3), Inches(11.33), Inches(0.8))
    protip.fill.solid()
    protip.fill.fore_color.rgb = c_paytm_blue
    protip.line.color.rgb = c_gold
    protip.line.width = Pt(1.5)

    tb_p = s9.shapes.add_textbox(Inches(1.2), Inches(6.35), Inches(10.9), Inches(0.7))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    pp = tf_p.paragraphs[0]
    pp.text = "PRO-TIP FOR MUMBAI STAGE: Start the demo by speaking a live Hindi question to the Soundbox. Let the judges hear the Soundbox speak back in Hindi while showing the n8n execution graph live on the projector screen!"
    pp.font.size = Pt(12)
    pp.font.bold = True
    pp.font.color.rgb = c_white

    # Save presentation
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out = r"C:\Users\shubh\paytmai\Paytm_AI_Hackathon_Winning_Presentation.pptx"
    create_presentation(out)
