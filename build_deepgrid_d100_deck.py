import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_d100_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank

    # Color Palette: Deep Consulting Aerospace
    DARK_BG = RGBColor(10, 25, 47)        # #0A192F (Navy Base)
    SLATE_BG = RGBColor(248, 250, 252)    # #F8FAFC (Clean Light Surface)
    CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF (White Card)
    CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0
    TEXT_DARK = RGBColor(15, 23, 42)      # #0F172A (Slate 900)
    TEXT_MUTED = RGBColor(71, 85, 105)    # #475569 (Slate 600)
    PRIMARY_TEAL = RGBColor(14, 116, 144) # #0E7490 (Cyan/Teal 700)
    ACCENT_CYAN = RGBColor(6, 182, 212)   # #06B6D4 (Cyan 500)
    ACCENT_GOLD = RGBColor(217, 119, 6)   # #D97706 (Amber 600)
    ACCENT_RED = RGBColor(220, 38, 38)    # #DC2626 (Red 600)
    ACCENT_GREEN = RGBColor(22, 163, 74)  # #16A34A (Green 600)
    HEADER_BLUE = RGBColor(30, 58, 138)   # #1E3A8A (Blue 900)

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, tag, title, subtitle):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.3))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = PRIMARY_TEAL

        # Slide Title (Assertion Claim)
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_DARK

        # Subtitle / Strategic takeaway
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.4))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=None, badge=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        if accent_color:
            bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.08))
            bar.fill.solid()
            bar.fill.fore_color.rgb = accent_color
            bar.line.fill.background()

        tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.18), width - Inches(0.5), height - Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = TEXT_DARK
        p0.space_after = Pt(8)

        if badge:
            p_badge = tf.add_paragraph()
            p_badge.text = f"STATUS: {badge}"
            p_badge.font.size = Pt(9)
            p_badge.font.bold = True
            p_badge.font.color.rgb = accent_color if accent_color else PRIMARY_TEAL
            p_badge.space_after = Pt(6)

        for b in body_bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MUTED
            p.space_after = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme)
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, DARK_BG)

    # Title box
    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p_badge = tf.paragraphs[0]
    p_badge.text = "DEEPGRID SEMI · ARCHITECTURAL SPECIFICATION & DEFENCE DOSSIER"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = ACCENT_CYAN
    p_badge.space_after = Pt(12)

    p_title = tf.add_paragraph()
    p_title.text = "D100 Tactical UAV Drone SoC\nMulti-Die System-in-Package (SiP)"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    p_title.space_after = Pt(16)

    p_sub = tf.add_paragraph()
    p_sub.text = "Sovereign Flight Control, 30 Hz Optical EKF VIO, and Hardware Failsafe Recovery for Contested Airspaces"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(148, 163, 184)

    # Bottom Meta Cards
    meta_cols = [
        ("PROCESS NODE", "130nm CMOS + BCD 180nm\n+ 28nm Compute Flip-Chip"),
        ("PACKAGING FORMAT", "15x15 mm 4-Layer Organic BGA\nDeliberately NOT UCIe"),
        ("SOVEREIGN STANDARDS", "MIL-STD-810H / DAP-2020\nDGCA Type Certification Path"),
        ("FOUNDRY SUPPLY CHAIN", "SkyWater 130nm -> IHP SiGe\n-> SCL Mohali 180nm")
    ]
    for i, (m_title, m_val) in enumerate(meta_cols):
        left = Inches(1.0 + i * 2.88)
        top = Inches(5.2)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.68), Inches(1.3))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(15, 30, 56)
        card.line.color.rgb = RGBColor(30, 58, 100)
        tb_m = s1.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), Inches(2.38), Inches(1.0))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        p0 = tf_m.paragraphs[0]
        p0.text = m_title
        p0.font.size = Pt(9)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_CYAN
        p1 = tf_m.add_paragraph()
        p1.text = m_val
        p1.font.size = Pt(10)
        p1.font.color.rgb = RGBColor(241, 245, 249)

    # -------------------------------------------------------------
    # SLIDE 2: Strategic Context & The $9B Problem
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, SLATE_BG)
    add_header(s2, "Sovereign Context & Threat Vector", 
               "Foreign Silicon In Indian Tactical UAVs Represents A Single-Point Kill Switch",
               "95%+ of Indian defence drone flight controllers rely on commercial STM32/TI microcontrollers vulnerable to GPS jamming and supply embargoes.")

    add_card(s2, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "1. Electronic Warfare Vulnerability", [
                 "Contested borders (LoC / LAC) experience aggressive GPS spoofing and multi-band RF denial.",
                 "Commercial flight controllers experience catastrophic navigational drift within 60 seconds of GPS denial.",
                 "Firmware-level failsafes often lock up during intense RF jamming or bus overload.",
                 "Airframe recovery fails when flight software threads deadlock in RTOS."
             ], ACCENT_RED)

    add_card(s2, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "2. The $9B Import Reality", [
                 "India imports $23.4B in electronics annually, with $9B concentrated in mature nodes (130nm–180nm).",
                 "Drone avionics, ESC drivers, and power regulators are entirely sourced from Western or Chinese vendors.",
                 "DAP-2020 Buy (Indian-IDDM) mandates 50%+ Indigenous Content (IC), impossible with imported chips.",
                 "ideaForge, BEL, and Indian military integrators urgently require drop-in sovereign silicon."
             ], ACCENT_GOLD)

    add_card(s2, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "3. The DeepGrid D100 Mandate", [
                 "100% sovereign RTL, GDSII, and packaging layout fully owned and auditable in India.",
                 "Hardware-isolated Failsafe Island completely decouples recovery logic from the main CPU.",
                 "Geometric 30 Hz EKF VIO provides autonomous zero-GPS navigation with <1% drift/km.",
                 "Drop-in 15x15 mm BGA replacement that consolidates 4 discrete PCBs into 1 sovereign package."
             ], PRIMARY_TEAL)

    # -------------------------------------------------------------
    # SLIDE 3: Architectural Breakthrough - Multi-Die SiP
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, SLATE_BG)
    add_header(s3, "System-in-Package Innovation",
               "Heterogeneous Multi-Die SiP Combines 6 Mature Dies With 1 Compute Die",
               "DeepGrid deliberately rejects expensive UCIe and silicon interposers in favor of 4-layer organic BGA packaging.")

    add_card(s3, Inches(0.8), Inches(1.9), Inches(5.6), Inches(2.4),
             "6 Mature Dies Wire-Bonded (130nm / 180nm)", [
                 "SKU-3 Hi-Rel PMIC: Direct 5V–120V battery rail down-conversion to 1.2V/1.8V/3.3V.",
                 "SKU-6 Supervisor: Chopper-stabilized voltage monitoring with 8 µs deglitch protection.",
                 "SKU-5 Tactical Transceiver: CAN-FD (5 Mbps) & RS-485 with ±15 kV HBM ESD protection.",
                 "Analog Front-End (AFE): High-precision sensor digitization for avionics."
             ], PRIMARY_TEAL)

    add_card(s3, Inches(6.9), Inches(1.9), Inches(5.6), Inches(2.4),
             "1 High-Speed Compute Die Flip-Chip Attached", [
                 "Fabricated in high-density digital node (28nm CMOS flip-chip attached via copper pillars).",
                 "Contains Dual DGridRiscV cores, Hardware 30 Hz EKF VIO, and optional 10-TOPS NPU.",
                 "128-bit AXI4 crossbar interconnect running at 200 MHz non-blocking throughput.",
                 "Tightly coupled to 512 KB zero-wait-state ECC SRAM."
             ], HEADER_BLUE)

    add_card(s3, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.4),
             "Why 'Deliberately Not UCIe': The Mature-Node Cost Advantage", [
                 "UCIe & TSMC CoWoS require sub-micron silicon interposers, micro-bumps, and offshore foundries (Taiwan/USA).",
                 "Organic 4-layer laminate substrate (FR4/BT core) slashes packaging NRE from >$1.5M down to <$35,000.",
                 "Substrate-level trace routing (high-speed SPI, differential UART, GPIO power trees) achieves >99% assembly yield.",
                 "Enables rapid assembly across domestic Indian ATMP facilities without foreign export licenses or ITAR restrictions."
             ], ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 4: Flight Control Engine (Dual DGridRiscV)
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, SLATE_BG)
    add_header(s4, "Deterministic Flight Computer",
               "Dual DGridRiscV Cores Deliver Zero-Jitter Real-Time Flight Control",
               "Cacheless Harvard microarchitecture eliminates branch prediction vulnerabilities and non-deterministic cache miss latency.")

    add_card(s4, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "1. Cacheless Execution Determinism", [
                 "RV32IM_Safety ISA (Integer arithmetic + hardware multiply/divide).",
                 "2-stage fetch, 6-stage execute strictly deterministic pipeline.",
                 "Zero instruction or data cache: code runs directly from 512 KB ECC SRAM.",
                 "Eliminates worst-case execution time (WCET) jitter in PX4 attitude control loops."
             ], PRIMARY_TEAL)

    add_card(s4, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "2. Dual-Core Lockstep Safety", [
                 "Two identical DGridRiscV cores execute simultaneously with 2-cycle temporal skew.",
                 "Temporal skew prevents common-mode EMI and power rail transient corruptions.",
                 "Hardware comparator inspects output buses on every cycle.",
                 "Latches FAULTn output within ≤2 clock cycles upon divergence."
             ], ACCENT_GOLD)

    add_card(s4, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "3. Avionics Interface Engine", [
                 "Dedicated hardware timer blocks generating up to 8x DShot600 / PWM ESC signals.",
                 "High-speed SPI buses polling dual IMUs, magnetometer, and barometer at 1 kHz.",
                 "Zero-copy DMA transfers flight telemetry into SRAM without CPU intervention.",
                 "Direct interrupt vectoring with sub-50ns interrupt service latency."
             ], HEADER_BLUE)

    # -------------------------------------------------------------
    # SLIDE 5: Geometric VIO Engine (GPS-Denied Ops)
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, SLATE_BG)
    add_header(s5, "Electronic Warfare Resilient Navigation",
               "30 Hz Hardware EKF VIO Maintains <1% Drift/km In Total GPS Blackouts",
               "Fuses MIPI CSI-2 optical feature tracking with high-rate IMU telemetry completely in dedicated digital RTL.")

    add_card(s5, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "1. Hardware ISP & Feature Pipeline", [
                 "Direct 2-lane MIPI CSI-2 receiver handling 1080p60 downward/forward optical streams.",
                 "Hardware debayering, tone-mapping, and high-frequency edge enhancement.",
                 "FAST corner detector engine extracts up to 500 optical keypoints per frame.",
                 "KLT optical flow hardware engine tracks feature vectors across frames in real time."
             ], PRIMARY_TEAL)

    add_card(s5, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "2. 6-DoF Extended Kalman Filter", [
                 "Dedicated matrix math accelerator computing state propagation and covariance updates.",
                 "Tight-coupling with 1 kHz IMU gyro and accelerometer measurements.",
                 "Delivers 30 Hz full 6-DoF vehicle pose vector (position, velocity, attitude).",
                 "Bounded error drift: <0.8% of total distance traversed without satellite lock."
             ], ACCENT_GREEN)

    add_card(s5, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "3. Operational Advantage at the Border", [
                 "Immune to Russian/Chinese GPS spoofing pods deployed along active borders.",
                 "Eliminates dependency on magnetic compasses that fail near heavy metal bridges or power lines.",
                 "Guarantees autonomous return-to-launch (RTL) navigation under zero-RF conditions.",
                 "Zero cloud or pre-loaded satellite map dependency: purely local geometric odometry."
             ], ACCENT_RED)

    # -------------------------------------------------------------
    # SLIDE 6: The Hardware Failsafe Wedge
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, SLATE_BG)
    add_header(s6, "The Hardware Failsafe Wedge",
               "Dedicated Hardware Island Guarantees Airframe Recovery During System Lockup",
               "Completely bypasses main processors, VIO, and AI to directly control motor ESCs during critical command link loss.")

    add_card(s6, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "1. 100% Isolated Hardware Island", [
                 "Fabricated with dedicated internal LDO regulator and independent on-chip ring oscillator.",
                 "Zero firmware or software execution: implemented strictly as pure combinational/synchronous RTL.",
                 "Independent watchdog counter resets automatically on verified telemetry heartbeat.",
                 "Survives full main processor lockup, memory fault, or firmware panic."
             ], ACCENT_RED)

    add_card(s6, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "2. Multi-Threat Link Loss Detection", [
                 "Continuously samples RF telemetry signal quality, SBUS/CRSF links, and GNSS integrity.",
                 "Detects RF desensitization and electronic jamming within 200 ms.",
                 "Monitors core rail voltages through SKU-6 supervisor for brownout precursors.",
                 "Triggers automated emergency mode if control commands cease for >500 ms."
             ], ACCENT_GOLD)

    add_card(s6, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "3. Hardwired Actuator Multiplexer", [
                 "Physical silicon MUX located directly adjacent to the output pad ring.",
                 "Instantly severs main flight controller outputs upon fault confirmation.",
                 "Drives pre-programmed safe rotor RPM profile directly to motor ESCs.",
                 "Executes steady-state hover and controlled descent to prevent catastrophic airframe crash."
             ], PRIMARY_TEAL)

    # -------------------------------------------------------------
    # SLIDE 7: Edge AI Perception & Sensor Ingestion
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, SLATE_BG)
    add_header(s7, "Tactical Edge AI Perception",
               "Optional 10-TOPS NPU Accelerates Real-Time Object Tracking & Guidance",
               "128-bit AXI4 crossbar connects high-throughput sensor streams without starving flight control cycles.")

    add_card(s7, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "1. 10-TOPS INT8/INT4 NPU Core", [
                 "Massive 2D systolic MAC array optimized for convolution and matrix multiplication.",
                 "2 MB on-chip ultra-low-power SRAM eliminates high-frequency external DRAM access.",
                 "Runs YOLOv8-Nano at >60 FPS for target detection, perimeter defense, and convoy tracking.",
                 "Energy efficiency: >2.5 TOPS/Watt within an ultra-low 4W thermal envelope."
             ], HEADER_BLUE)

    add_card(s7, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "2. 128-bit Non-Blocking AXI4 Crossbar", [
                 "High-speed crossbar matrix clocked at 200 MHz providing >25 GB/s aggregate bandwidth.",
                 "Strict quality-of-service (AXI-QoS) prioritizes flight control traffic over AI data.",
                 "Zero-copy DMA channels stream camera frames directly from ISP to NPU SRAM.",
                 "LPDDR4 memory controller interface supports up to 2 GB external DRAM."
             ], PRIMARY_TEAL)

    add_card(s7, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "3. Multi-Sensor Tactical Ingestion", [
                 "SKU-7 mmWave Radar fusion via high-speed SPI for micro-Doppler moving object detection.",
                 "Thermal FLIR camera ingestion over secondary MIPI CSI-2 channel.",
                 "Secure Enclave provides hardware Root-of-Trust (RoT) for encrypted video transmission.",
                 "Automated terminal homing and GPS-independent precision landing marker detection."
             ], ACCENT_GREEN)

    # -------------------------------------------------------------
    # SLIDE 8: Electrical, Thermal & Mechanical Specifications
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, SLATE_BG)
    add_header(s8, "Physical & Electrical Envelope",
               "Engineered For Harsh Aerospace Environments: -55°C to +125°C Operation",
               "Consolidates discrete power supplies, supervisor ICs, and compute into a ruggedized 15x15 mm package.")

    specs = [
        ("PACKAGE DIMENSIONS", "15 x 15 mm BGA", "0.8 mm ball pitch, 324-ball grid array, 4-layer organic laminate substrate"),
        ("INPUT POWER RAIL", "5V to 120V Raw Battery", "Direct connection to drone LiPo packs via SKU-3 BCD PMIC without bulky external buck converters"),
        ("INTERNAL POWER TREE", "1.2V / 1.8V / 3.3V", "Low-noise rails for core digital logic, high-speed MIPI, and rugged 3.3V tactical I/O"),
        ("THERMAL DISSIPATION", "4.8W Nominal / 7.2W Peak", "Integrated top copper slug allows direct thermal conduction to drone carbon-fiber chassis"),
        ("OPERATING RANGE", "-55°C to +125°C", "Full military temperature range compliance; tested under extreme desert heat (+55°C ambient)"),
        ("ESD & TRANSIENT MOAT", "±15 kV HBM ESD", "Thick-oxide LDMOS I/O buffers protect against tactical lightning and high-altitude static discharge")
    ]

    for idx, (param, val, desc) in enumerate(specs):
        r = idx // 2
        c = idx % 2
        left = Inches(0.8 + c * 5.95)
        top = Inches(1.9 + r * 1.65)
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.75), Inches(1.45))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        tb_s = s8.shapes.add_textbox(left + Inches(0.2), top + Inches(0.12), Inches(5.35), Inches(1.2))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        p0 = tf_s.paragraphs[0]
        p0.text = param
        p0.font.size = Pt(9)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY_TEAL
        p1 = tf_s.add_paragraph()
        p1.text = val
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_DARK
        p2 = tf_s.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_MUTED

    # -------------------------------------------------------------
    # SLIDE 9: Production & Qualification Roadmap
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9, SLATE_BG)
    add_header(s9, "Qualification & Sovereign Fab Migration",
               "Three-Factory Sovereignty Roadmap Ensures Zero Foreign Supply Disruption",
               "Initial fabrication on commercial open-source shuttles transitions directly to SCL Mohali domestic foundry lines.")

    add_card(s9, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "Phase 1: SkyWater 130nm & IHP", [
                 "OpenLane / Yosys / OpenROAD automated physical design flow eliminates $1M EDA license fees.",
                 "Prototyping on SkyWater 130nm (MPW shuttles at $14,300 per run).",
                 "77 GHz mmWave front-end validated on IHP SG13G2 BiCMOS (Germany).",
                 "Pre-ASIC FPGA validation complete on Xilinx Artix-7 at 81.25 MHz."
             ], PRIMARY_TEAL, "PROVEN TRACTION")

    add_card(s9, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "Phase 2: SCL Mohali 180nm Transfer", [
                 "Direct retargeting of DGridRiscV and BCD power IP to Semi-Conductor Laboratory (SCL) Mohali.",
                 "Secures 100% sovereign domestic fabrication immune to US ITAR or European export restrictions.",
                 "Meets DAP-2020 Make-II and Buy (Indian-IDDM) domestic procurement rules.",
                 "Dedicated ₹1.2 Cr automated test equipment (ATE) production line established in Hyderabad."
             ], ACCENT_GOLD, "MIGRATION PATH")

    add_card(s9, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "Phase 3: Military Qualification", [
                 "MIL-STD-810H environmental testing (altitude, shock, propeller vibration profile).",
                 "MIL-STD-461G compliance for electromagnetic compatibility and EW resistance.",
                 "DGCA Type Certification path for commercial and dual-use aerospace deployment.",
                 "Approved Vendor List (AVL) inclusion with DRDO, BEL, and Indian Army MCEME."
             ], ACCENT_GREEN, "DEFENCE READY")

    # -------------------------------------------------------------
    # SLIDE 10: Economics, Deployment & Capital Plan
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10, DARK_BG)

    # Header for dark slide
    tag_box = s10.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.3))
    tf_tag = tag_box.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "FINANCIAL MODEL & COMMERCIAL DEPLOYMENT".upper()
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_CYAN

    title_box = s10.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = "Transforming A $1.2B Indian Drone Market Into A ₹1,000 Cr Silicon Business"
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)

    sub_box = s10.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.4))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "₹10 Cr use of funds buys complete silicon qualification, ATE lines, and commercial scale to FY31."
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = RGBColor(148, 163, 184)

    # 4 Columns on Dark Slide
    fin_cols = [
        ("CONTRACTED TRACTION", "₹2.88 Cr Pre-ASIC", [
            "Live contracted revenue with Indian Army MCEME (₹1.01 Cr order).",
            "Infinis and Axitech commercial validation partners.",
            "Replaces multi-board STM32/TI imports in active tactical drones."
        ], ACCENT_CYAN),
        ("MARKET EXPANSION", "$1.2B -> $3.2B", [
            "Indian UAV hardware market expanding at 22%+ CAGR toward 2032.",
            "SoC ASP band ranges from $100 (basic UAV) to $800 (tactical autonomous drone).",
            "ideaForge alone guides 340–450 units/quarter in target classes."
        ], ACCENT_GOLD),
        ("USE OF ₹10 CR FUNDS", "10x Capital Moat", [
            "₹3.6 Cr: Foundry fabrication and MPW shuttles.",
            "₹2.4 Cr: Core engineering and physical design team.",
            "₹1.8 Cr: MIL-883 / DGCA testing and certification.",
            "₹1.2 Cr: Dedicated high-throughput ATE screening line."
        ], ACCENT_GREEN),
        ("FY31 REVENUE TARGET", "₹1,000 Cr Scale", [
            "Scale-up driven by 50 mature-node building blocks across 10 SKUs.",
            "Gross margins >68% enabled by open-source EDA and mature fab nodes.",
            "High switching costs once integrated into sovereign defence programs.",
            "Protected by DAP-2020 Make-II and Positive Indigenisation Lists."
        ], PRIMARY_TEAL)
    ]

    for idx, (col_title, col_stat, bullets, accent) in enumerate(fin_cols):
        left = Inches(0.8 + idx * 2.95)
        top = Inches(1.9)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.75), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(15, 30, 56)
        card.line.color.rgb = RGBColor(30, 58, 100)

        bar = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(2.75), Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = accent
        bar.line.fill.background()

        tb_f = s10.shapes.add_textbox(left + Inches(0.18), top + Inches(0.2), Inches(2.39), Inches(4.6))
        tf_f = tb_f.text_frame
        tf_f.word_wrap = True

        p0 = tf_f.paragraphs[0]
        p0.text = col_title
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = accent
        p0.space_after = Pt(4)

        p1 = tf_f.add_paragraph()
        p1.text = col_stat
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(255, 255, 255)
        p1.space_after = Pt(12)

        for b in bullets:
            p = tf_f.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = RGBColor(203, 213, 225)
            p.space_after = Pt(6)

    out_path = "deepgrid-d100-architecture.pptx"
    prs.save(out_path)
    print(f"Successfully generated {out_path}")

if __name__ == "__main__":
    build_d100_deck()
