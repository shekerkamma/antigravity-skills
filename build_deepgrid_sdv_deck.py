import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_sdv_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    DARK_BG = RGBColor(10, 15, 29)         # Deep Space Navy
    SLATE_BG = RGBColor(248, 250, 252)     # Clean Light Surface
    CARD_BG = RGBColor(255, 255, 255)      # White Card
    CARD_BORDER = RGBColor(226, 232, 240)  # Slate Border
    TEXT_DARK = RGBColor(15, 23, 42)       # Slate 900
    TEXT_MUTED = RGBColor(71, 85, 105)     # Slate 600
    PRIMARY_CYAN = RGBColor(6, 182, 212)   # Cyan 500
    ACCENT_TEAL = RGBColor(14, 116, 144)   # Teal 700
    ACCENT_PURPLE = RGBColor(124, 58, 237) # Purple 600
    ACCENT_RED = RGBColor(220, 38, 38)     # Red 600
    ACCENT_GREEN = RGBColor(22, 163, 74)   # Green 600
    ACCENT_GOLD = RGBColor(217, 119, 6)    # Amber 600

    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, tag, title, subtitle):
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.3))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_TEAL

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_DARK

        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.4))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
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

        tb = slide.shapes.add_textbox(left + Inches(0.22), top + Inches(0.16), width - Inches(0.44), height - Inches(0.32))
        tf = tb.text_frame
        tf.word_wrap = True

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = TEXT_DARK
        p0.space_after = Pt(6)

        if badge:
            p_badge = tf.add_paragraph()
            p_badge.text = f"STANDARD: {badge}"
            p_badge.font.size = Pt(9)
            p_badge.font.bold = True
            p_badge.font.color.rgb = accent_color if accent_color else ACCENT_TEAL
            p_badge.space_after = Pt(6)

        for b in body_bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(9.5)
            p.font.color.rgb = TEXT_MUTED
            p.space_after = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark)
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, DARK_BG)

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True

    p_badge = tf.paragraphs[0]
    p_badge.text = "DEEPGRID SEMI · AUTOMOTIVE & DEFENCE SILICON REFERENCE ARCHITECTURE"
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = PRIMARY_CYAN
    p_badge.space_after = Pt(12)

    p_title = tf.add_paragraph()
    p_title.text = "DG Software-Defined Vehicle (SDV)\nZonal Compute Platform"
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)
    p_title.space_after = Pt(16)

    p_sub = tf.add_paragraph()
    p_sub.text = "Triple-Lockstep ASIL-D Safety, EVITA-Full HSM, 64-bit Coherent AXI4 Matrix, and 16x Smart Electronic Fuses."
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(148, 163, 184)

    meta_cols = [
        ("SAFETY INTEGRITY", "ISO 26262 ASIL-D\nTriple-Core Lockstep (TMR)"),
        ("SECURITY ENCLAVE", "EVITA-Full / EAL5+\nIsolated Hardware Crypto HSM"),
        ("SYSTEM INTERCONNECT", "64-bit AXI4 Crossbar\nAXI-REALM QoS Bandwidth Shaper"),
        ("ZONAL SMART POWER", "16x Smart e-Fuses\n4x CAN-XL (20 Mbps) + Gigabit TSN")
    ]
    for i, (m_title, m_val) in enumerate(meta_cols):
        left = Inches(1.0 + i * 2.88)
        top = Inches(5.2)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.68), Inches(1.3))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(15, 23, 42)
        card.line.color.rgb = RGBColor(30, 58, 100)
        tb_m = s1.shapes.add_textbox(left + Inches(0.15), top + Inches(0.15), Inches(2.38), Inches(1.0))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        p0 = tf_m.paragraphs[0]
        p0.text = m_title
        p0.font.size = Pt(9)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY_CYAN
        p1 = tf_m.add_paragraph()
        p1.text = m_val
        p1.font.size = Pt(10)
        p1.font.color.rgb = RGBColor(241, 245, 249)

    # -------------------------------------------------------------
    # SLIDE 2: The Zonal Paradigm Shift
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, SLATE_BG)
    add_header(s2, "Automotive Paradigm Shift",
               "Consolidating 80+ Legacy ECUs Into High-Density Sovereign Zonal Controllers",
               "Modern vehicles replace kilometers of heavy copper wiring harnesses with 4 zonal nodes and a central SDV compute spine.")

    add_card(s2, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "1. The Legacy ECU Crisis", [
                 "Traditional vehicles carry 70–100 discrete ECUs from different vendors.",
                 "Harness weight exceeds 50 kg; massive assembly labor and point-to-point wiring.",
                 "Incompatible proprietary software stacks prevent over-the-air (OTA) feature upgrades.",
                 "Chassis reliability suffers from electromechanical relay and physical fuse failures."
             ], ACCENT_RED)

    add_card(s2, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "2. The Zonal Compute Vision", [
                 "Vehicle partitioned into 4 physical zones (Front-Left, Front-Right, Rear-Left, Rear-Right).",
                 "Each zone aggregates local sensors, smart power switching, and motor control.",
                 "Backbone connected via deterministic Gigabit Time-Sensitive Networking (TSN).",
                 "Harness weight reduced by >40%, cutting vehicle manufacturing cost significantly."
             ], ACCENT_GOLD)

    add_card(s2, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "3. The DeepGrid Sovereign Solution", [
                 "Unified RISC-V compute platform replacing imported NXP S32G and Infineon Aurix TC4x.",
                 "Integrates ASIL-D safety, Linux host, hardware HSM, and zonal I/O on one platform.",
                 "100% auditable open-source RTL eliminates foreign intellectual property royalties.",
                 "Compliant with Indian MoRTH AIS-140 and military DAP-2020 IDDM procurement."
             ], ACCENT_TEAL)

    # -------------------------------------------------------------
    # SLIDE 3: Multi-Domain Architecture Breakdown
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, SLATE_BG)
    add_header(s3, "Unified Multi-Domain Architecture",
               "Hardware-Isolated Enclaves Guarantee Safe Coexistence Of Linux And Real-Time Control",
               "Physical firewalls and memory protection units prevent non-critical software panics from impacting chassis safety.")

    add_card(s3, Inches(0.8), Inches(1.9), Inches(2.75), Inches(5.0),
             "DG Secure Domain", [
                 "Dual-lockstep DGI-RV32 security cores.",
                 "EVITA-Full & Common Criteria EAL5+.",
                 "Hardware Crypto: AES-256, SHA-3, SM4.",
                 "Secure OTP eFuse array for key vault.",
                 "Always-On power island with anti-tamper."
             ], ACCENT_GOLD, "EVITA-FULL")

    add_card(s3, Inches(3.75), Inches(1.9), Inches(2.75), Inches(5.0),
             "DG Safe Domain", [
                 "Triple-Core Lockstep (TMR) DGCV32-RT.",
                 "ISO 26262 ASIL-D & IEC 61508 SIL-3.",
                 "Hardware majority voting in <=2 cycles.",
                 "Private ISPM & DSPM with SECDED ECC.",
                 "Controls steering, braking, and chassis."
             ], ACCENT_RED, "ASIL-D / SIL-3")

    add_card(s3, Inches(6.7), Inches(1.9), Inches(2.75), Inches(5.0),
             "DG Host Domain", [
                 "Multi-Core 64-bit RV64GCH Linux host.",
                 "POSIX-compliant OS execution environment.",
                 "Coherent 1 MB shared L2 cache.",
                 "Hardware MMU, FPU, and virtualization.",
                 "Manages cloud telemetry, OTA, and fleet UX."
             ], PRIMARY_CYAN, "POSIX / LINUX")

    add_card(s3, Inches(9.65), Inches(1.9), Inches(2.85), Inches(5.0),
             "DG Accelerators", [
                 "Vector Multi-Core (DG RVV 1.0, 512-bit).",
                 "Integer Cluster: 4x DGCV32 tiny cores.",
                 "Interleaved TCDM scratchpad SRAM banks.",
                 "2D DMA engine for zero-copy streaming.",
                 "Real-time sensor fusion & radar perception."
             ], ACCENT_GREEN, "HARDWARE ACCEL")

    # -------------------------------------------------------------
    # SLIDE 4: Safe Domain (Triple-Modular Redundancy)
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, SLATE_BG)
    add_header(s4, "Chassis Safety Core: ASIL-D TMR",
               "Triple-Core Lockstep With 2-Cycle Skew Eliminates Single-Event Upset Failures",
               "Hardware majority voter masks transient bit-flips instantly without stopping vehicle braking or steer-by-wire loops.")

    add_card(s4, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "1. Temporal 2-Cycle Skew Execution", [
                 "Three identical DGCV32-RT cores execute with temporal stagger: Core 0 (T), Core 1 (T+1), Core 2 (T+2).",
                 "Prevents common-mode substrate voltage dips or EMI bursts from corrupting all cores simultaneously.",
                 "Zero performance penalty: deterministic execution clocked at 300 MHz.",
                 "Each core has private instruction/data scratchpad SRAM with ECC."
             ], ACCENT_RED)

    add_card(s4, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "2. Hardware Majority Voter", [
                 "Combinational majority voting circuit samples output buses on every clock cycle.",
                 "If 1 core deviates due to an alpha particle or voltage dip, voter outputs 2-out-of-3 majority value.",
                 "Zero execution stall: critical steer-by-wire and braking commands proceed without delay.",
                 "Voting logic latches disagreement state in under 2 clock cycles."
             ], ACCENT_GOLD)

    add_card(s4, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "3. Fault Collection & Control Unit (FCCU)", [
                 "Captures core discrepancy telemetry and logs precise cycle and instruction counter.",
                 "Autonomous hardware reset of corrupted core without interrupting vehicle operation.",
                 "Directly drives external hardware safety pin (FAULTn) to trigger secondary safe-state if needed.",
                 "Full compliance with ISO 26262 ASIL-D and IEC 61508 SIL-3 automotive standards."
             ], ACCENT_TEAL)

    # -------------------------------------------------------------
    # SLIDE 5: Interconnect & AXI-REALM QoS
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, SLATE_BG)
    add_header(s5, "Central Fabric & AXI-REALM QoS",
               "64-Bit Coherent AXI4 Crossbar Delivers Bounded Latency For Chassis Control",
               "AXI-REALM bandwidth regulator guarantees that high-volume Linux data streams never starve critical ASIL-D safety packets.")

    add_card(s5, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "1. 64-bit Non-Blocking Crossbar", [
                 "Clocked at 400 MHz providing aggregate interconnect bandwidth exceeding 50 GB/s.",
                 "Full multi-master / multi-slave non-blocking crossbar topology.",
                 "Hardware-enforced memory protection units (MPUs) isolate security and safety address spaces.",
                 "Zero-wait-state access to tightly coupled scratchpad memories."
             ], PRIMARY_CYAN)

    add_card(s5, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "2. AXI-REALM QoS Shaper", [
                 "Monitors bus credit allocation across all bus masters in real time.",
                 "Throttles Linux host memory thrashing during heavy cloud logging or video streaming.",
                 "Grants preemptive, zero-arbitration priority to ASIL-D chassis safety frames (<2.5 ns latency).",
                 "Mathematical Worst-Case Response Time (WCRT) bounded to <=12.5 ns across the crossbar."
             ], ACCENT_GREEN)

    add_card(s5, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "3. Hardware Domain Firewall", [
                 "Enforces ARM TrustZone-equivalent isolation across open RISC-V bus transactions.",
                 "Malicious or compromised Linux driver cannot read or overwrite safety SRAM registers.",
                 "Direct hardware fault trap asserted if non-secure master attempts secure enclave access.",
                 "Enables mixed-criticality workload consolidation on a single physical SoC."
             ], ACCENT_TEAL)

    # -------------------------------------------------------------
    # SLIDE 6: Zonal I/O & 16x Smart Electronic Fuses
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, SLATE_BG)
    add_header(s6, "Zonal Actuation & Smart Solid-State Power",
               "16 Integrated Electronic Fuses Eliminate Mechanical Relays And Copper Bulk",
               "DeepGrid's 180nm BCD power switches deliver sub-microsecond short-circuit protection and intelligent current monitoring.")

    add_card(s6, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "1. 16x Smart e-Fuses (48V / 12V)", [
                 "Integrated 180nm BCD power switches handling up to 25A continuous per channel.",
                 "Sub-microsecond (<1 µs) short-circuit trip eliminates wiring harness thermal damage.",
                 "Programmable digital I²t thermal profiling replaces physical sacrificial melting fuses.",
                 "Real-time digital current sensing enables predictive failure diagnostics on motors/heaters."
             ], ACCENT_PURPLE)

    add_card(s6, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "2. Gigabit TSN Automotive Ethernet", [
                 "4-port Ethernet switch complying with IEEE 802.1Qbv Time-Aware Traffic Shapers.",
                 "Deterministic time slots guaranteed for raw radar/camera perception streams.",
                 "Ultra-low latency audio/video bridging (AVB) for zonal infotainment and speakers.",
                 "Immune to Ethernet network congestion under intense vehicle sensor traffic."
             ], PRIMARY_CYAN)

    add_card(s6, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "3. CAN-XL & Legacy Bus Support", [
                 "4 dedicated CAN-XL controllers delivering up to 20 Mbps with 2048-byte payloads.",
                 "Backward compatible with CAN-FD and classic CAN on all vehicle body networks.",
                 "Integrated LIN transceivers for smart mirrors, window lifters, and ambient lighting.",
                 "Thick-oxide LDMOS I/O buffers rated for ±15 kV HBM electrostatic discharge."
             ], ACCENT_TEAL)

    # -------------------------------------------------------------
    # SLIDE 7: Accelerators & Sensor Fusion
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, SLATE_BG)
    add_header(s7, "Vector DSP & Heterogeneous Accelerators",
               "Hardware Vector Extensions Accelerate Real-Time 4D Radar & Vision Sensor Fusion",
               "RISC-V Vector 1.0 architecture with 512-bit ALUs processes point-clouds with zero cache-miss latency.")

    add_card(s7, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "1. DG RVV Vector Compute Core", [
                 "RISC-V Vector Extension 1.0 compliant microarchitecture with 512-bit vector registers.",
                 "Optimized for FFT and matrix transforms used in 77 GHz 4D imaging radar signal processing.",
                 "Achieves 8x throughput advantage over scalar DSPs at equivalent clock frequency.",
                 "Dedicated hardware pipeline for point-cloud clustering and Doppler velocity extraction."
             ], ACCENT_GREEN)

    add_card(s7, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "2. TCDM Scratchpad Memory (SPM)", [
                 "512 KB multi-bank interleaved tightly coupled data memory (TCDM).",
                 "Logarithmic interconnect allows simultaneous zero-contention access across cores.",
                 "Eliminates cache invalidation and flushing overhead during multi-sensor data fusion.",
                 "2D DMA engine automatically stages sensor tensors from host DRAM into SPM."
             ], PRIMARY_CYAN)

    add_card(s7, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "3. Real-Time Perception Pipeline", [
                 "Fuses front 77 GHz radar (SKU-7) with surround ultrasonic and camera streams in <10 ms.",
                 "Executes automated emergency braking (AEB) and blind-spot detection with zero false triggers.",
                 "Operates within a strict 6W thermal power envelope suitable for passive zonal enclosures.",
                 "Proven resilience against dirty sensor lenses and harsh monsoon weather conditions."
             ], ACCENT_TEAL)

    # -------------------------------------------------------------
    # SLIDE 8: Multi-Die Organic Packaging
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, SLATE_BG)
    add_header(s8, "System-in-Package Composition",
               "Multi-Die Organic Substrate Packaging Eliminates Advanced Packaging NRE",
               "Heterogeneous integration of 28nm high-speed compute with 130nm/180nm BCD mature dies in a 25x25 mm BGA.")

    specs = [
        ("PACKAGE FORMAT", "25 x 25 mm BGA Substrate", "4-layer high-reliability organic laminate with 1.0 mm ball pitch for robust automotive soldering"),
        ("COMPUTE DIE (FLIP-CHIP)", "28nm CMOS @ 1.2 GHz", "Houses RV64 Linux host, coherent L2 cache, and AXI4 crossbar attached via copper pillars"),
        ("SAFETY & POWER DIES", "130nm / 180nm BCD Wire-Bonded", "ASIL-D TMR safety island and 16x smart e-Fuses fabricated on proven, cost-effective mature nodes"),
        ("INTER-DIE INTERCONNECT", "Substrate Trace Routing", "Standardized on-substrate SPI, differential UART, and parallel buses — Deliberately avoiding expensive UCIe"),
        ("AUTOMOTIVE RATING", "AEC-Q100 Grade 0 (-40°C to +150°C)", "Engineered for harsh under-hood and chassis environments with high thermal tolerance"),
        ("NRE & YIELD ADVANTAGE", "90% Cost Reduction", "Packaging tooling cost under $45,000 vs >$1.5M for TSMC CoWoS / Intel EMIB silicon interposers")
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
        p0.font.color.rgb = ACCENT_TEAL
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
    # SLIDE 9: Sovereign Supply Chain & Fab Migration
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9, SLATE_BG)
    add_header(s9, "Sovereign Supply Chain Roadmap",
               "Three-Factory Manufacturing Topology Insulates Indian Automotive Tier-1s",
               "Initial commercial foundry runs on open-PDK shuttles transition directly to SCL Mohali domestic defence lines.")

    add_card(s9, Inches(0.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "Phase 1: Open-Source EDA & MPWs", [
                 "Digital implementation executed entirely on OpenLane, Yosys, and OpenROAD toolchains.",
                 "Eliminates multi-million-dollar Synopsys/Cadence EDA license taxes.",
                 "Rapid MPW prototyping on SkyWater 130nm ($14.3K shuttle runs).",
                 "77 GHz radar AFE verified on IHP SG13G2 SiGe BiCMOS (Germany)."
             ], PRIMARY_CYAN, "PROVEN")

    add_card(s9, Inches(4.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "Phase 2: SCL Mohali Domestic Fab", [
                 "Retargets BCD power switches, supervisor ICs, and ASIL-D safe cores to SCL Mohali 180nm.",
                 "Establishes 100% domestic silicon manufacturing immune to international export controls.",
                 "Fully satisfies Indian Ministry of Defence DAP-2020 Make-II indigenization rules.",
                 "In-house automated test equipment (ATE) screening line established in Hyderabad."
             ], ACCENT_GOLD, "TRANSFER")

    add_card(s9, Inches(8.8), Inches(1.9), Inches(3.7), Inches(5.0),
             "Phase 3: Automotive Tier-1 Rollout", [
                 "Integration testing with Indian commercial vehicle leaders (Tata Motors, Ashok Leyland).",
                 "Drop-in zonal controller kits for electric buses and heavy-duty commercial haulage.",
                 "Full ISO 26262 functional safety and ARAI automotive homologation.",
                 "Long-term 15-year automotive lifecycle availability guarantee."
             ], ACCENT_GREEN, "QUALIFIED")

    # -------------------------------------------------------------
    # SLIDE 10: Commercial Impact & Economics (Dark)
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10, DARK_BG)

    tag_box = s10.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.3))
    tf_tag = tag_box.text_frame
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "FINANCIAL MODEL & COMMERCIAL IMPACT".upper()
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = PRIMARY_CYAN

    title_box = s10.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = "Capturing The Indian Automotive Zonal Revolution At 1/10th The Silicon Cost"
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)

    sub_box = s10.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.7), Inches(0.4))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Open-source EDA, mature foundry nodes, and organic packaging compound into 68%+ gross margins."
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = RGBColor(148, 163, 184)

    fin_cols = [
        ("TARGET MARKET", "₹4,200 Cr / Year", [
            "Indian commercial and passenger vehicle market migrating to zonal architectures by 2028.",
            "MoRTH regulatory mandates for ADAS and electronic safety on commercial vehicles.",
            "Average silicon BOM content expanding from $180 to $650 per vehicle chassis."
        ], PRIMARY_CYAN),
        ("UNIT ECONOMICS", "$38 BOM / $140 ASP", [
            "Mature-node silicon and organic packaging keep unit manufacturing cost under $38.",
            "Target average selling price (ASP) of $120–$160 delivers >68% gross margin.",
            "Replaces over $400 worth of fragmented foreign ECUs and electromechanical fuse boxes."
        ], ACCENT_GOLD),
        ("CAPITAL EFFICIENCY", "10x Advantage", [
            "Zero Synopsys/Cadence license costs ($1.5M saved per tapeout).",
            "Shuttle-based rapid iteration loop every 198 days across 3 domestic/international fabs.",
            "₹10 Cr use of funds buys complete silicon qualification and commercial production."
        ], ACCENT_GREEN),
        ("SOVEREIGN MOAT", "Zero Foreign Lock-in", [
            "100% domestic IP ownership protected under Indian patent and semiconductor layout acts.",
            "Permanent immunity from foreign export bans, ITAR restrictions, or kill-switches.",
            "Scalable architectural platform powering 10 SKUs toward ₹1,000 Cr FY31 revenue."
        ], ACCENT_TEAL)
    ]

    for idx, (col_title, col_stat, bullets, accent) in enumerate(fin_cols):
        left = Inches(0.8 + idx * 2.95)
        top = Inches(1.9)
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.75), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(15, 23, 42)
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

    out_path = "deepgrid-sdv-architecture.pptx"
    prs.save(out_path)
    print(f"Successfully generated {out_path}")

if __name__ == "__main__":
    build_sdv_deck()
