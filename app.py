import streamlit as st
import anthropic

st.set_page_config(
    page_title="Smit — Financial + ESG Diagnostic",
    page_icon="📊",
    layout="centered"
)

# ── DARK MODE DETECTION + TOGGLE ─────────────────────────────
if 'colour_mode' not in st.session_state:
    st.session_state.colour_mode = 'light'

# Popup only fires once, before anything else
if 'mode_confirmed' not in st.session_state:
    st.session_state.mode_confirmed = False

if not st.session_state.mode_confirmed:
    st.markdown("""
    <style>
    .mode-popup-overlay {
        position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.7); z-index: 9999;
        display: flex; align-items: center; justify-content: center;
    }
    .mode-popup {
        background: #1C1C1A; border: 2px solid #8B0000;
        padding: 2.5rem; max-width: 420px; width: 90%; text-align: center;
    }
    .mode-popup h3 {
        font-family: Georgia, serif; font-size: 1.3rem;
        color: white; margin-bottom: 0.75rem;
    }
    .mode-popup p {
        font-size: 0.85rem; color: rgba(255,255,255,0.55);
        margin-bottom: 1.5rem; line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#fff8f0;border:1px solid #8B0000;padding:1.25rem;margin-bottom:1rem;text-align:center;">
        <p style="font-size:0.9rem;color:#1C1C1A;font-weight:600;margin-bottom:0.25rem;">
            One quick question before we start
        </p>
        <p style="font-size:0.82rem;color:#6b6b6b;">
            Smit uses a light-mode design. If your device is in dark mode, colours may not display correctly.
            Choose your preference below so everything displays as intended.
        </p>
    </div>
    """, unsafe_allow_html=True)

    mode_choice = st.radio(
        "How are you viewing this?",
        ["Light mode (white background)", "Dark mode (dark background)"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if st.button("Continue to Smit →", type="primary"):
        st.session_state.colour_mode = 'dark' if 'Dark' in mode_choice else 'light'
        st.session_state.mode_confirmed = True
        st.rerun()

    st.stop()

# ── CSS — ADAPTS TO MODE ──────────────────────────────────────
is_dark = st.session_state.colour_mode == 'dark'

BG = "#1C1C1A" if is_dark else "#FAFAF8"
BG2 = "#2A2A27" if is_dark else "#F5F5EF"
TEXT = "#F5F5EF" if is_dark else "#1C1C1A"
TEXT2 = "#B0B0A8" if is_dark else "#6B6B63"
BORDER = "#3A3A37" if is_dark else "#D4D4CC"
CARD = "#2A2A27" if is_dark else "#FFFFFF"
RED = "#8B0000"
GREEN_TEXT = "#4ade80" if is_dark else "#1a5c2e"
GREEN_BG = "rgba(74,222,128,0.1)" if is_dark else "#e8f5ee"
AMBER_TEXT = "#fbbf24" if is_dark else "#7a4a0a"
AMBER_BG = "rgba(251,191,36,0.1)" if is_dark else "#fdf3e3"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {BG};
    color: {TEXT};
}}
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}
h1, h2, h3 {{ font-family: 'Playfair Display', serif; color: {TEXT}; }}
.block-container {{ padding: 2rem 1.5rem; max-width: 820px; }}

/* Masthead */
.masthead {{ border-bottom: 3px solid {TEXT}; padding-bottom: 0.85rem; margin-bottom: 0.5rem; }}
.masthead-row {{ display: flex; justify-content: space-between; align-items: baseline; }}
.masthead-name {{ font-family: 'Playfair Display', serif; font-size: 2.8rem; font-weight: 700; color: {TEXT}; letter-spacing: -1px; line-height: 1; }}
.masthead-name span {{ color: {RED}; }}
.masthead-sub {{ font-size: 0.7rem; color: {TEXT2}; border-top: 1px solid {BORDER}; padding-top: 0.4rem; margin-top: 0.35rem; letter-spacing: 0.3px; }}

/* Rules */
.rule {{ height: 1px; background: {BORDER}; margin: 1.5rem 0; }}
.rule-thick {{ height: 2px; background: {TEXT}; margin: 2rem 0; }}

/* Kicker labels */
.kicker {{ font-size: 0.68rem; font-weight: 600; color: {RED}; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.25rem; }}

/* Combined score */
.smit-score-hero {{
    background: #1C1C1A;
    padding: 2rem 1.75rem; margin: 1rem 0; text-align: center;
}}
.ssh-label {{ font-size: 0.62rem; font-weight: 600; color: rgba(255,255,255,0.35); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.5rem; }}
.ssh-number {{ font-family: 'Playfair Display', serif; font-size: 4.5rem; font-weight: 700; line-height: 1; margin-bottom: 0.4rem; }}
.ssh-label-status {{ font-size: 0.85rem; font-weight: 600; margin-bottom: 0.25rem; }}
.ssh-sub {{ font-size: 0.72rem; color: rgba(255,255,255,0.3); }}
.ssh-breakdown {{ display: flex; justify-content: center; gap: 2.5rem; margin-top: 1.25rem; padding-top: 1.25rem; border-top: 1px solid rgba(255,255,255,0.08); }}
.ssh-b-item {{ text-align: center; }}
.ssh-b-val {{ font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; }}
.ssh-b-lbl {{ font-size: 0.58rem; font-weight: 600; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem; }}

/* Three score row */
.score-row {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: {BORDER}; border: 1px solid {BORDER}; margin: 1rem 0; }}
.score-cell {{ background: {BG}; padding: 1.25rem 1rem; text-align: center; }}
.score-cell-label {{ font-size: 0.62rem; font-weight: 600; color: {TEXT2}; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.5rem; }}
.score-cell-number {{ font-family: 'Playfair Display', serif; font-size: 2.6rem; font-weight: 700; line-height: 1; margin-bottom: 0.35rem; }}
.score-cell-status {{ font-size: 0.7rem; font-weight: 600; padding: 0.2rem 0.6rem; display: inline-block; }}
.s-green {{ color: {GREEN_TEXT}; background: {GREEN_BG}; }}
.s-amber {{ color: {AMBER_TEXT}; background: {AMBER_BG}; }}
.s-red {{ color: {RED}; background: {"rgba(139,0,0,0.12)" if is_dark else "#fdecea"}; }}

/* Ratio table */
.ratio-table {{ width: 100%; border-collapse: collapse; font-size: 0.875rem; margin: 1rem 0; }}
.ratio-table th {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; color: {TEXT2}; padding: 0.5rem 0.75rem; border-bottom: 2px solid {TEXT}; text-align: left; }}
.ratio-table td {{ padding: 0.7rem 0.75rem; border-bottom: 1px solid {BORDER}; color: {TEXT}; vertical-align: top; }}
.ratio-table tr:hover td {{ background: {BG2}; }}
.ratio-val {{ font-weight: 600; font-size: 1rem; }}
.ratio-explain {{ font-size: 0.7rem; color: {TEXT2}; display: block; margin-top: 0.2rem; font-style: italic; line-height: 1.4; }}
.r-good {{ color: {GREEN_TEXT}; }}
.r-warn {{ color: {AMBER_TEXT}; }}
.r-bad {{ color: {RED}; }}

/* Flags */
.flag {{ padding: 0.75rem 1rem; margin: 0.4rem 0; border-left: 3px solid; font-size: 0.875rem; line-height: 1.5; }}
.flag-crit {{ border-color: {RED}; background: {"rgba(139,0,0,0.12)" if is_dark else "#fdecea"}; color: {"#f87171" if is_dark else "#5a1010"}; }}
.flag-warn {{ border-color: #C17A2A; background: {"rgba(193,122,42,0.12)" if is_dark else "#fdf3e3"}; color: {"#fbbf24" if is_dark else "#6b4010"}; }}
.flag-ok {{ border-color: {"#4ade80" if is_dark else "#1a5c2e"}; background: {GREEN_BG}; color: {GREEN_TEXT}; }}

/* Actions */
.action-item {{ display: flex; gap: 0.75rem; align-items: flex-start; padding: 0.85rem 1rem; margin: 0.4rem 0; background: {BG2}; border: 1px solid {BORDER}; font-size: 0.875rem; line-height: 1.5; color: {TEXT}; }}
.action-num {{ font-family: 'Playfair Display', serif; font-size: 1.3rem; font-weight: 700; color: {RED}; line-height: 1; flex-shrink: 0; min-width: 20px; }}

/* ESG upgrade plan */
.esg-plan-wrap {{ margin: 0.4rem 0; border: 1px solid {"rgba(74,222,128,0.2)" if is_dark else "#d1fae5"}; }}
.esg-plan-header {{ background: {"rgba(26,92,46,0.3)" if is_dark else "#1a5c2e"}; color: {"#4ade80" if is_dark else "white"}; padding: 0.6rem 1rem; font-size: 0.68rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; display: flex; justify-content: space-between; }}
.esg-plan-item {{ padding: 0.85rem 1rem; background: {GREEN_BG}; font-size: 0.875rem; line-height: 1.6; color: {TEXT}; }}
.esg-plan-item strong {{ color: {GREEN_TEXT}; }}

/* ESG grid */
.esg-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0.4rem; margin: 0.75rem 0; }}
.esg-item {{ display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0.75rem; background: {BG2}; border: 1px solid {BORDER}; font-size: 0.8rem; color: {TEXT}; }}
.esg-pass {{ border-left: 3px solid {GREEN_TEXT}; }}
.esg-fail {{ border-left: 3px solid {RED}; opacity: 0.6; }}

/* Summary */
.summary-box {{ background: #1C1C1A; color: #F5F5EF; padding: 1.5rem; margin: 1rem 0; font-size: 0.9rem; line-height: 1.7; }}
.summary-kicker {{ font-size: 0.62rem; font-weight: 600; color: #C17A2A; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.5rem; }}

/* Stress test */
.stress-row {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: {BORDER}; border: 1px solid {BORDER}; margin: 1rem 0; }}
.stress-cell {{ background: {BG}; padding: 1rem; text-align: center; }}
.stress-cell-label {{ font-size: 0.62rem; font-weight: 600; color: {TEXT2}; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.4rem; }}
.stress-cell-value {{ font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 700; color: {TEXT}; }}
.stress-cell-delta {{ font-size: 0.75rem; margin-top: 0.2rem; }}
.d-neg {{ color: {RED}; }}
.d-pos {{ color: {GREEN_TEXT}; }}

/* Pro gate */
.pro-gate {{ background: #1C1C1A; padding: 1.5rem; text-align: center; }}
.pro-gate p {{ color: rgba(255,255,255,0.6); font-size: 0.875rem; margin-bottom: 0.75rem; line-height: 1.6; }}
.pro-gate strong {{ color: white; }}

/* Chat */
.chat-wrap {{ border: 1px solid {BORDER}; background: {CARD}; margin: 1rem 0; }}
.chat-header {{ background: #1C1C1A; color: #F5F5EF; padding: 0.75rem 1rem; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; display: flex; justify-content: space-between; align-items: center; }}
.chat-badge {{ font-size: 0.62rem; background: {RED}; color: white; padding: 0.15rem 0.5rem; }}
.chat-user {{ background: {BG2}; border-left: 3px solid {TEXT}; padding: 0.75rem 1rem; margin: 0.5rem; font-size: 0.875rem; color: {TEXT}; }}
.chat-assistant {{ background: {CARD}; border-left: 3px solid {RED}; padding: 0.75rem 1rem; margin: 0.5rem; font-size: 0.875rem; line-height: 1.6; color: {TEXT}; }}
.chat-lbl {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.35rem; }}
.chat-user .chat-lbl {{ color: {TEXT2}; }}
.chat-assistant .chat-lbl {{ color: {RED}; }}

/* Step indicator */
.step-wrap {{ display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; }}
.step-dot {{ width: 24px; height: 24px; background: {RED}; color: white; font-size: 0.75rem; font-weight: 600; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }}
.step-lbl {{ font-size: 0.72rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; color: {TEXT}; }}

/* Legal warning */
.legal-warn {{ background: {"rgba(193,122,42,0.15)" if is_dark else "#fff8e1"}; border: 1px solid {"#c17a2a" if is_dark else "#f59e0b"}; padding: 0.75rem 1rem; font-size: 0.8rem; color: {"#fbbf24" if is_dark else "#78350f"}; line-height: 1.6; margin: 0.5rem 0; }}

/* Disclaimer */
.disclaimer {{ border-top: 1px solid {BORDER}; padding-top: 1rem; margin-top: 2rem; font-size: 0.72rem; color: {TEXT2}; line-height: 1.6; }}

/* Buttons */
.stButton > button {{ background: #1C1C1A !important; color: #F5F5EF !important; border: 1px solid #1C1C1A !important; border-radius: 0 !important; padding: 0.65rem 1.5rem !important; font-size: 0.85rem !important; font-weight: 500 !important; letter-spacing: 0.5px !important; font-family: 'DM Sans', sans-serif !important; transition: all 0.2s !important; width: 100% !important; }}
.stButton > button:hover {{ background: {RED} !important; border-color: {RED} !important; }}
.stButton > button:disabled {{ background: {BORDER} !important; border-color: {BORDER} !important; color: {TEXT2} !important; }}

/* Inputs */
.stTextInput > div > div > input {{ border-radius: 0 !important; border: 1px solid {BORDER} !important; background: {CARD} !important; color: {TEXT} !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.9rem !important; }}
.stTextInput > div > div > input:focus {{ border-color: {TEXT} !important; box-shadow: none !important; }}
.stNumberInput > div > div > input {{ border-radius: 0 !important; border: 1px solid {BORDER} !important; background: {CARD} !important; color: {TEXT} !important; }}
.stSelectbox > div > div {{ border-radius: 0 !important; border: 1px solid {BORDER} !important; background: {CARD} !important; color: {TEXT} !important; }}
.stCheckbox > label {{ font-size: 0.875rem !important; color: {TEXT} !important; }}
.stRadio > label {{ font-size: 0.875rem !important; color: {TEXT} !important; }}
.stSlider > div > div > div {{ background: {RED} !important; }}
label {{ color: {TEXT} !important; }}
p, span, div {{ color: inherit; }}
</style>
""", unsafe_allow_html=True)

# ── MASTHEAD ──────────────────────────────────────────────────
st.markdown(f"""
<div class="masthead">
    <div class="masthead-row">
        <div class="masthead-name">Smit<span>.</span></div>
        <div style="font-size:0.72rem;color:{RED};font-weight:600;letter-spacing:1px;text-transform:uppercase;">
            Financial + ESG Diagnostic
        </div>
    </div>
    <div class="masthead-sub">
        UK &amp; India &nbsp;·&nbsp; HMRC · RBI · Bank of England · World Bank benchmarks
        &nbsp;·&nbsp; Not regulated financial advice
        &nbsp;·&nbsp; <span style="cursor:pointer;text-decoration:underline;" onclick="document.querySelector('[data-testid=stButton]').click()">Switch to {'light' if is_dark else 'dark'} mode</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Mode toggle button (hidden, triggered by masthead link)
if st.button("Toggle colour mode", key="mode_toggle"):
    st.session_state.colour_mode = 'light' if is_dark else 'dark'
    st.rerun()

# ── SESSION STATE ─────────────────────────────────────────────
for k, v in [
    ('signed_up', False), ('user_info', {}),
    ('results_ready', False), ('financial_data', {}),
    ('chat_messages', [])
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── SIGNUP GATE ───────────────────────────────────────────────
if not st.session_state.signed_up:
    st.markdown(f"""
    <div style="padding: 2rem 0 1rem;">
        <div class="kicker">Free access — no credit card required</div>
        <h1 style="font-size: 2.2rem; letter-spacing: -1px; margin-bottom: 0.5rem; line-height: 1.2; color: {TEXT};">
            Your business deserves a financial expert.
        </h1>
        <p style="font-family: 'Playfair Display', serif; font-size: 1.1rem; font-style: italic; color: {RED}; margin-bottom: 1rem;">
            Now it has one.
        </p>
        <p style="font-size: 0.9rem; color: {TEXT2}; max-width: 560px; line-height: 1.8; margin-bottom: 1.5rem;">
            Enter 7 numbers. Get the same financial and ESG analysis that banks and CAs run
            on businesses — benchmarked against official HMRC, RBI, Bank of England, and World Bank data.
            In plain English. On demand.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full name", placeholder="Your name")
        email = st.text_input("Email address", placeholder="your@email.com")
    with col2:
        region = st.selectbox("Your region", [
            "", "🇬🇧 United Kingdom", "🇮🇳 India", "🌍 Other"
        ])
        biz_type = st.selectbox("Business type", [
            "", "Freelancer / Sole trader", "Small business (1–10 people)",
            "Early-stage startup", "Limited company director", "Other"
        ])

    consent = st.checkbox(
        "I agree to Smit storing my name, email, and business type for product communications. "
        "I understand I can request deletion at any time. "
        "Smit does not sell or share this data. "
        "Financial data I enter is not stored without additional consent."
    )

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    if st.button("Access Smit free — no credit card required"):
        if not name or not email or not region or not biz_type:
            st.error("Please fill in all fields to continue.")
        elif "@" not in email:
            st.error("Please enter a valid email address.")
        elif not consent:
            st.error("Please agree to the data terms to continue.")
        else:
            st.session_state.signed_up = True
            st.session_state.user_info = {
                "name": name, "email": email,
                "region": region, "biz_type": biz_type
            }
            st.rerun()

    st.markdown(f"""
    <div class="rule" style="margin-top:1.5rem;"></div>
    <p style="font-size:0.75rem;color:{TEXT2};line-height:1.7;">
        <strong style="color:{TEXT}">Privacy:</strong> Smit collects your name, email, and business type
        for product communications only, with your consent. Financial data you enter is processed
        in-session and is not stored on our servers. Smit operates under UK GDPR and India DPDP Act 2023.
        Deletion requests: hello@getsmit.co<br><br>
        <strong style="color:{TEXT}">Important:</strong> Smit is a financial intelligence tool.
        It does not provide regulated financial, tax, or legal advice.
        Always consult a qualified professional for regulated decisions.
    </p>
    """, unsafe_allow_html=True)
    st.stop()

# ── MAIN TOOL ─────────────────────────────────────────────────
user = st.session_state.user_info
is_uk = "United Kingdom" in user.get("region", "")
currency = "£" if is_uk else "₹"
step = 1000.0 if is_uk else 10000.0

st.markdown(f"""
<div style="padding:0.5rem 0 1rem;">
    <span style="font-size:0.78rem;color:{TEXT2};">
        Welcome, {user.get('name','')} &nbsp;·&nbsp;
        {user.get('biz_type','')} &nbsp;·&nbsp;
        {user.get('region','')}
    </span>
</div>
""", unsafe_allow_html=True)

# ── STEP 1: FINANCIAL INPUTS ──────────────────────────────────
st.markdown("""
<div class="rule-thick"></div>
<div class="step-wrap"><div class="step-dot">1</div><div class="step-lbl">Your 7 financial inputs</div></div>
""", unsafe_allow_html=True)
st.markdown(f'<p style="font-size:0.85rem;color:{TEXT2};margin-bottom:1.25rem;">Enter your most recent figures. These are the exact numbers Smit uses for every calculation and every Smit AI response.</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<p style="font-weight:600;margin-bottom:0.5rem;color:{TEXT};">Revenue & costs ({currency})</p>', unsafe_allow_html=True)
    revenue = st.number_input("Annual revenue", min_value=0.0, step=step, key="rev",
        help="Total income for the past 12 months, before any deductions")
    expenses = st.number_input("Annual expenses", min_value=0.0, step=step, key="exp",
        help="All business operating costs for the year — staff, rent, software, everything")
    cash = st.number_input("Cash in bank", min_value=0.0, step=step/2, key="cash",
        help="Liquid cash across all business accounts right now")
with col2:
    st.markdown(f'<p style="font-weight:600;margin-bottom:0.5rem;color:{TEXT};">Debt & obligations ({currency})</p>', unsafe_allow_html=True)
    debt = st.number_input("Total debt / liabilities", min_value=0.0, step=step/2, key="debt",
        help="All outstanding loans, credit cards, overdrafts, and financial obligations")
    fixed_costs = st.number_input("Monthly fixed costs", min_value=0.0, step=100.0, key="fc",
        help="Costs that stay constant regardless of revenue — rent, salaries, subscriptions")
    receivables = st.number_input("Money owed to you", min_value=0.0, step=100.0, key="rec",
        help="Outstanding invoices and payments due to you that you haven't received yet")

# ── STEP 2: COMPLIANCE CHECKLIST ─────────────────────────────
st.markdown(f"""
<div class="rule"></div>
<div class="step-wrap"><div class="step-dot">2</div><div class="step-lbl">Compliance checklist</div></div>
<p style="font-size:0.85rem;color:{TEXT2};margin-bottom:1rem;">
    These are the first things any regulatory review, loan application, or formal audit checks.
    Answer honestly — your answers directly affect your audit readiness and ESG governance scores.
</p>
""", unsafe_allow_html=True)

if is_uk:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)",
        help="HMRC requires companies to keep records for 6 years, sole traders for 22 months from the tax year end (Finance Act 1998 / HMRC record-keeping guidance). No records = no defence in any tax enquiry.")
    q2 = st.checkbox("I have a dedicated business bank account",
        help="Legally mandatory for limited companies under Companies Act 2006. Strongly required for sole traders under HMRC guidance. Mixing personal and business finances is the #1 finding in SME audits and makes accurate profit calculation impossible.")
    q3 = st.checkbox("I know my VAT registration status and whether I am above the £85,000 threshold",
        help="HMRC requires registration within 30 days of exceeding £85,000 annual taxable turnover. Non-registration above threshold is a criminal offence under Value Added Tax Act 1994, Section 67. Penalty: up to 15% of VAT owed.")
    q4 = st.checkbox("I file self-assessment or company accounts on time every year",
        help="Late self-assessment filing: £100 immediate penalty, £10/day after 3 months (up to £900), then 5% surcharges (HMRC). Late company accounts: £150–£1,500 penalty from Companies House depending on delay.")
    q5 = st.checkbox("I have financial records going back at least 2 years",
        help="HMRC requires 5 years post-submission for self-assessment; 6 years for companies. 2 years is Smit's practical minimum — below this, any financial review would immediately identify a gap.")
else:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)",
        help="GST Rules 2017 require records to be maintained for 72 months (6 years) from the end of the relevant financial year. Tax invoices are mandatory for GST-registered businesses under CGST Act 2017 Section 31.")
    q2 = st.checkbox("I have a dedicated business bank account",
        help="Required for GST-registered businesses to track input tax credits accurately. For companies, Companies Act 2013 Section 128 requires proper books of account. Mixing finances is the most common reason for CA audit qualifications.")
    q3 = st.checkbox("I know my GST registration status and whether I am above the ₹20 Lakh threshold",
        help="CGST Act 2017, Section 22: mandatory registration for service providers above ₹20 Lakhs annual turnover (₹40 Lakhs for goods suppliers). Penalty for non-registration: 10% of tax amount due or ₹10,000, whichever is higher.")
    q4 = st.checkbox("I file GST returns quarterly and on time",
        help="Late GSTR-3B filing: ₹50/day (₹20 for nil returns) plus interest at 18% per annum on outstanding tax (CGST Act 2017 Section 47). Consistent filing history is required for bank loans and government contracts.")
    q5 = st.checkbox("I maintain records that could be reviewed immediately",
        help="Companies Act 2013 Section 128: books of account must be kept at the registered office and made available for inspection. Income Tax Act 1961 Section 44AA: mandatory account maintenance for specified professionals and businesses above threshold.")

# ── STEP 3: ESG ASSESSMENT ────────────────────────────────────
st.markdown(f"""
<div class="rule"></div>
<div class="step-wrap"><div class="step-dot">3</div><div class="step-lbl">ESG governance assessment</div></div>
<p style="font-size:0.85rem;color:{TEXT2};margin-bottom:0.5rem;">
    ESG governance is increasingly required by banks, large clients, and supply chains — even for small businesses.
    These questions assess your current position across all three pillars.
</p>
<p style="font-size:0.75rem;color:{TEXT2};margin-bottom:1rem;">
    Sources: UK DBT SME ESG Guidance 2023 · SEBI BRSR Lite Framework (India) · ISO 26000 · FRC Corporate Governance Code · IoD India SME Guidelines
</p>
""", unsafe_allow_html=True)

st.markdown(f'<p style="font-size:0.8rem;font-weight:600;color:{TEXT};margin-bottom:0.5rem;">G — Governance</p>', unsafe_allow_html=True)
esg1 = st.checkbox("I review my finances monthly or quarterly",
    help="Regular financial review is a core governance indicator. Source: FRC Corporate Governance Code (UK), SEBI BRSR Lite Principle 1 (India). Governance pillar — weighted 40% of ESG score.")
esg2 = st.checkbox("I am aware of my key legal and compliance obligations",
    help="Compliance awareness is the governance foundation. Source: UK DBT SME ESG Guidance 2023, SEBI BRSR Lite. Businesses that cannot identify their own obligations have a structural governance gap.")

st.markdown(f'<p style="font-size:0.8rem;font-weight:600;color:{TEXT};margin-top:0.75rem;margin-bottom:0.5rem;">S — Social and Fair Practices</p>', unsafe_allow_html=True)
esg3 = st.checkbox("I have written contracts or terms of service with clients",
    help="Source: ISO 26000 Section 6.6 (fair operating practices). Written contracts reduce dispute risk, protect payment rights under Late Payment of Commercial Debts Act 1998 (UK) and MSME Development Act 2006 (India). Social pillar — weighted 30% of ESG score.")
esg4 = st.checkbox("I treat all clients and suppliers fairly and do not engage in discriminatory practices",
    help="Source: ISO 26000 Section 6.3 (human rights) and Section 6.6 (fair operating practices). Minimum social baseline for ESG compliance.")

st.markdown(f'<p style="font-size:0.8rem;font-weight:600;color:{TEXT};margin-top:0.75rem;margin-bottom:0.5rem;">E — Environmental</p>', unsafe_allow_html=True)
esg5 = st.checkbox("I track or consider the environmental impact of my business operations",
    help="Source: SEBI BRSR Lite Principle 6 (India) · UK DBT SME ESG Guidance 2023 · BSI BS 8001:2017. Basic environmental awareness is the entry-level E indicator for SMEs. Environmental pillar — weighted 30% of ESG score.")
esg6 = st.checkbox("I have taken or am considering steps to reduce energy use, waste, or carbon footprint",
    help="Source: UK DBT SME ESG Guidance 2023 — identifies energy efficiency as the most actionable and cost-saving E action for SMEs. Often reduces costs by 8–15%.")

# ── RUN ───────────────────────────────────────────────────────
st.markdown(f'<div class="rule"></div>', unsafe_allow_html=True)

if st.button("Run Smit Diagnostic →"):
    if revenue == 0:
        st.error("Please enter your annual revenue to continue.")
        st.stop()

    # ── CALCULATIONS ──────────────────────────────────────────
    profit = revenue - expenses
    profit_margin = (profit / revenue) * 100 if revenue > 0 else 0
    expense_ratio = (expenses / revenue) * 100 if revenue > 0 else 0
    debt_to_revenue = (debt / revenue) * 100 if revenue > 0 else 0
    current_ratio = (cash + receivables) / (debt if debt > 0 else 1)

    # Audit readiness score
    audit_items = [q1, q2, q3, q4, q5]
    audit_score = (sum(audit_items) / 5) * 100

    # ESG score — three pillars
    g_items = [esg1, esg2]
    s_items = [esg3, esg4]
    e_items = [esg5, esg6]
    g_score = (sum(g_items) / len(g_items)) * 100
    s_score = (sum(s_items) / len(s_items)) * 100
    e_score = (sum(e_items) / len(e_items)) * 100
    # Governance also incorporates audit compliance items
    g_score_weighted = min((g_score * 0.5) + (audit_score * 0.3) + (20 if q2 else 0) + (10 if q1 else 0), 100)
    esg_score = round((g_score_weighted * 0.4) + (s_score * 0.3) + (e_score * 0.3))

    # Financial risk scoring
    risk_points = 0
    if is_uk:
        if profit_margin >= 20: risk_points += 0
        elif profit_margin >= 10: risk_points += 15
        else: risk_points += 30
    else:
        if profit_margin >= 15: risk_points += 0
        elif profit_margin >= 8: risk_points += 15
        else: risk_points += 30

    if current_ratio >= 2: risk_points += 0
    elif current_ratio >= 1: risk_points += 15
    else: risk_points += 30

    if debt_to_revenue <= 30: risk_points += 0
    elif debt_to_revenue <= 60: risk_points += 20
    else: risk_points += 40

    financial_score = max(0, 100 - risk_points)

    # Combined Smit Score
    combined_score = round((financial_score * 0.6) + (esg_score * 0.4))

    # Status helpers
    def fin_status(s):
        if s >= 70: return "Low risk", "s-green"
        elif s >= 45: return "Moderate", "s-amber"
        return "High risk", "s-red"

    def audit_st(s):
        if s >= 80: return "Prepared", "s-green"
        elif s >= 50: return "Partial", "s-amber"
        return "Not ready", "s-red"

    def esg_st(s):
        if s >= 70: return "Strong", "s-green"
        elif s >= 40: return "Developing", "s-amber"
        return "Needs work", "s-red"

    def combined_st(s):
        if s >= 70: return "Strong position", "#4ade80" if is_dark else "#1a5c2e"
        elif s >= 50: return "Developing", "#fbbf24" if is_dark else "#7a4a0a"
        return "Needs attention", RED

    fs_lbl, fs_cls = fin_status(financial_score)
    as_lbl, as_cls = audit_st(audit_score)
    es_lbl, es_cls = esg_st(esg_score)
    cs_lbl, cs_col = combined_st(combined_score)

    # Compliance flags
    flags = []
    if profit_margin < 0:
        flags.append(("crit", "Operating at a loss — expenses exceed revenue. Every month without correction deepens the deficit."))
    if expense_ratio > 85:
        flags.append(("warn", f"Expense ratio {expense_ratio:.1f}% — above the 85% warning threshold (HMRC Business Population Estimates). Under 15p of every £1 remains after costs."))
    if cash < (fixed_costs * 2):
        flags.append(("warn", f"Cash reserves below 2 months of fixed costs ({currency}{fixed_costs*2:,.0f}). Bank of England SME resilience guidance recommends a minimum 3-month buffer."))
    if debt_to_revenue > 60:
        flags.append(("crit", f"Debt-to-revenue {debt_to_revenue:.1f}% — above the 60% high-risk threshold (World Bank MSME Finance Gap Report). Significant income committed to debt obligations."))
    if current_ratio < 1:
        flags.append(("crit", f"Current ratio {current_ratio:.2f} — below 1.0. Cannot meet short-term obligations from liquid assets. This is a going concern indicator under ISA 570 (Bank of England SME lending criteria)."))
    if is_uk and revenue > 85000 and not q3:
        flags.append(("crit", "Revenue above VAT registration threshold (£85,000). Non-registration is a criminal offence under Value Added Tax Act 1994, Section 67."))
    if not is_uk and revenue > 2000000 and not q3:
        flags.append(("crit", "Revenue above GST threshold (₹20 Lakhs). Mandatory registration required under CGST Act 2017. Penalty: 10% of tax or ₹10,000, whichever is higher."))

    # Financial priority actions
    actions = []
    if profit_margin < 0:
        actions.append(f"Your business is operating at a loss. Review your 3 largest costs and identify what can be reduced immediately. Returning to break-even requires cutting {currency}{abs(profit):,.0f} from annual costs or increasing revenue by the same amount.")
    if expense_ratio > 85:
        actions.append(f"Reduce expense ratio from {expense_ratio:.1f}% toward 80%. On your revenue of {currency}{revenue:,.0f}, a 5-point improvement adds {currency}{revenue*0.05:,.0f} to annual profit.")
    if cash < fixed_costs * 2:
        actions.append(f"Build cash reserves to {currency}{fixed_costs*2:,.0f} before new commitments. You have {currency}{receivables:,.0f} in outstanding receivables — prioritise collection. Each month of reserves buys you time to adapt to any revenue disruption.")
    if debt_to_revenue > 60:
        actions.append(f"Prioritise debt reduction before new borrowing. At {debt_to_revenue:.1f}% debt-to-revenue, a revenue decline of 20% would leave debt obligations consuming {(debt_to_revenue/0.8):.0f}% of reduced revenue.")
    if audit_score < 60:
        actions.append("Address compliance checklist gaps. These are the first items surfaced in any regulatory review, loan application, or formal business assessment. Each unticked item represents a specific legal or regulatory requirement.")
    if current_ratio < 1:
        actions.append(f"Accelerate receivables collection ({currency}{receivables:,.0f} outstanding). Your current ratio of {current_ratio:.2f} is the most immediate operational risk — below 1.0 means you cannot meet short-term obligations from liquid assets.")
    if not actions:
        actions.append("Your financial position is stable. Run this diagnostic quarterly to monitor trends. Focus next on improving your ESG governance score above 70% — this strengthens your position for contracts, loans, and client relationships.")

    # ESG upgrade plan — tied to actual numbers
    esg_actions = []

    if not esg1:
        saving_estimate = revenue * 0.05
        esg_actions.append({
            "pillar": "G — Governance",
            "action": "Start a monthly 30-minute financial review",
            "detail": f"Set a recurring calendar event on the last day of each month. Review your actual vs expected revenue, expense ratio, and cash position. At your scale ({currency}{revenue:,.0f}/year), one month of unnoticed drift costs an average of {currency}{saving_estimate/12:,.0f}. Zero cost to implement.",
            "impact": "+15 pts Governance",
            "cost": "Zero cost"
        })

    if expense_ratio > 75:
        if is_uk:
            potential_saving = expenses * 0.05
            esg_actions.append({
                "pillar": "E — Environmental",
                "action": "Audit supplier and subscription costs for sustainable alternatives",
                "detail": f"Your expense base of {currency}{expenses:,.0f}/year includes costs that may have greener, cheaper alternatives. Switching to a renewable energy tariff alone typically saves £200–800/year. Reviewing and replacing 10% of costs with certified sustainable alternatives qualifies you for UK DBT Green Business support and lifts your ESG score. Source: UK DBT SME ESG Guidance 2023.",
                "impact": "+12 pts Environmental",
                "cost": f"Potential saving: {currency}{potential_saving:,.0f}/year"
            })
        else:
            esg_actions.append({
                "pillar": "E — Environmental",
                "action": "Track energy and operational costs as an ESG baseline",
                "detail": f"With expenses of {currency}{expenses:,.0f}/year, tracking energy and waste costs takes one spreadsheet and an hour per month. This creates the baseline required for SEBI BRSR Lite Principle 6 compliance. Businesses that track operational costs typically identify 8–15% savings. Source: SEBI BRSR Lite Framework.",
                "impact": "+12 pts Environmental",
                "cost": "Zero cost"
            })

    if not esg3:
        esg_actions.append({
            "pillar": "S — Social",
            "action": "Create a standard written contract or terms of service",
            "detail": f"A one-page written agreement for every client engagement protects your payment rights under {'Late Payment of Commercial Debts Act 1998 (UK)' if is_uk else 'MSME Development Act 2006 (India)'}. It also demonstrates social governance (ISO 26000 Section 6.6). Free templates available from {'gov.uk/business-support' if is_uk else 'msme.gov.in'}. Takes 2 hours to create, protects indefinitely.",
            "impact": "+10 pts Social",
            "cost": "Zero cost"
        })

    if not esg2:
        esg_actions.append({
            "pillar": "G — Governance",
            "action": "Map your key legal and compliance obligations",
            "detail": f"Create a one-page compliance calendar covering {'VAT filing, self-assessment, Companies House (if applicable)' if is_uk else 'GST quarterly filing, ROC compliance, TDS obligations'}. This is the governance foundation required by UK DBT SME ESG Guidance 2023 and SEBI BRSR Lite Principle 1. Zero cost — one afternoon to complete.",
            "impact": "+10 pts Governance",
            "cost": "Zero cost"
        })

    if not esg5 and not esg6:
        esg_actions.append({
            "pillar": "E — Environmental",
            "action": "Start tracking your business's environmental footprint",
            "detail": f"The minimum E requirement under {'UK DBT SME ESG Guidance 2023' if is_uk else 'SEBI BRSR Lite Principle 6'} is demonstrated awareness of your environmental impact. A simple monthly log of energy bills and travel costs takes 20 minutes and is the first step. UK businesses doing this report 8–15% cost savings within 12 months as they identify inefficiencies.",
            "impact": "+8 pts Environmental",
            "cost": "Zero cost"
        })

    if not esg_actions:
        esg_actions.append({
            "pillar": "All pillars",
            "action": "Formalise and document your existing ESG practices",
            "detail": "Your governance indicators are strong. The next step is creating a simple one-page ESG statement documenting your practices. Banks and large clients increasingly request this from SME suppliers. A documented ESG position costs nothing to create and strengthens every commercial relationship you have.",
            "impact": "Consolidates existing position",
            "cost": "Zero cost"
        })

    # ESG checklist items
    esg_items = [
        ("Monthly or quarterly financial review (G)", esg1),
        ("Compliance obligations awareness (G)", esg2),
        ("Written contracts with clients (S)", esg3),
        ("Fair and non-discriminatory practices (S)", esg4),
        ("Environmental impact awareness (E)", esg5),
        ("Active environmental reduction steps (E)", esg6),
        ("Dedicated business bank account (G)", q2),
        ("Consistent record keeping (G)", q1),
    ]

    # Overall summary
    if financial_score >= 70:
        summary = f"Your business presents a broadly stable position — financial risk score {financial_score:.0f}/100, Combined Smit Score {combined_score}/100. Profitability and liquidity are within acceptable ranges. ESG governance at {esg_score:.0f}% — {'address the gaps in the ESG upgrade plan to strengthen your position with lenders and clients.' if esg_score < 70 else 'strong governance foundations in place.'}"
    elif financial_score >= 45:
        weak = "cash reserves" if cash < fixed_costs * 2 else "leverage position" if debt_to_revenue > 60 else "profit margins"
        summary = f"Moderate financial risk — score {financial_score:.0f}/100, Combined Smit Score {combined_score}/100. The principal concern is your {weak}. This is manageable now but requires attention before it compounds. ESG governance at {esg_score:.0f}% — improving governance practices now strengthens your access to credit and contracts."
    else:
        summary = f"High-risk signals across multiple dimensions — financial score {financial_score:.0f}/100, Combined Smit Score {combined_score}/100. Immediate attention needed. The ESG upgrade plan below includes zero-cost actions that simultaneously improve operational resilience and sustainability position."

    # Store all results
    st.session_state.results_ready = True
    st.session_state.financial_data = {
        "revenue": revenue, "expenses": expenses, "cash": cash,
        "debt": debt, "fixed_costs": fixed_costs, "receivables": receivables,
        "profit": profit, "profit_margin": profit_margin,
        "expense_ratio": expense_ratio, "debt_to_revenue": debt_to_revenue,
        "current_ratio": current_ratio, "financial_score": financial_score,
        "audit_score": audit_score, "esg_score": esg_score,
        "g_score": g_score_weighted, "s_score": s_score, "e_score": e_score,
        "combined_score": combined_score, "cs_lbl": cs_lbl, "cs_col": cs_col,
        "flags": flags, "actions": actions,
        "esg_items": esg_items, "esg_actions": esg_actions,
        "summary": summary, "currency": currency, "is_uk": is_uk,
        "fs_lbl": fs_lbl, "fs_cls": fs_cls,
        "as_lbl": as_lbl, "as_cls": as_cls,
        "es_lbl": es_lbl, "es_cls": es_cls,
        "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5,
        "esg1": esg1, "esg2": esg2, "esg3": esg3,
        "esg4": esg4, "esg5": esg5, "esg6": esg6,
    }
    st.rerun()

# ── RESULTS ───────────────────────────────────────────────────
if st.session_state.results_ready:
    d = st.session_state.financial_data

    st.markdown(f"""
    <div class="rule-thick"></div>
    <div class="kicker">Your Smit diagnostic results</div>
    """, unsafe_allow_html=True)

    # ── COMBINED SCORE HERO ───────────────────────────────────
    st.markdown(f"""
    <div class="smit-score-hero">
        <div class="ssh-label">Combined Smit Score — Financial + ESG</div>
        <div class="ssh-number" style="color:{d['cs_col']}">{d['combined_score']}</div>
        <div class="ssh-label-status" style="color:{d['cs_col']}">{d['cs_lbl']}</div>
        <div class="ssh-sub">60% financial risk weighting · 40% ESG governance weighting</div>
        <div class="ssh-breakdown">
            <div class="ssh-b-item">
                <div class="ssh-b-val" style="color:{'#4ade80' if d['financial_score']>=70 else '#fbbf24' if d['financial_score']>=45 else '#f87171'}">{d['financial_score']:.0f}</div>
                <div class="ssh-b-lbl">Financial risk</div>
            </div>
            <div class="ssh-b-item">
                <div class="ssh-b-val" style="color:{'#4ade80' if d['audit_score']>=80 else '#fbbf24' if d['audit_score']>=50 else '#f87171'}">{d['audit_score']:.0f}%</div>
                <div class="ssh-b-lbl">Audit readiness</div>
            </div>
            <div class="ssh-b-item">
                <div class="ssh-b-val" style="color:{'#4ade80' if d['esg_score']>=70 else '#fbbf24' if d['esg_score']>=40 else '#f87171'}">{d['esg_score']:.0f}%</div>
                <div class="ssh-b-lbl">ESG governance</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── THREE SCORE CELLS ────────────────────────────────────
    st.markdown(f"""
    <div class="score-row">
        <div class="score-cell">
            <div class="score-cell-label">Financial risk score</div>
            <div class="score-cell-number" style="color:{'#1a5c2e' if d['financial_score']>=70 else '#7a4a0a' if d['financial_score']>=45 else '#8B0000'}">
                {d['financial_score']:.0f}<span style="font-size:1.1rem;color:{TEXT2};font-weight:400">/100</span>
            </div>
            <span class="score-cell-status {d['fs_cls']}">{d['fs_lbl']}</span>
        </div>
        <div class="score-cell">
            <div class="score-cell-label">Audit readiness</div>
            <div class="score-cell-number" style="color:{'#1a5c2e' if d['audit_score']>=80 else '#7a4a0a' if d['audit_score']>=50 else '#8B0000'}">
                {d['audit_score']:.0f}<span style="font-size:1.1rem;color:{TEXT2};font-weight:400">%</span>
            </div>
            <span class="score-cell-status {d['as_cls']}">{d['as_lbl']}</span>
        </div>
        <div class="score-cell">
            <div class="score-cell-label">ESG governance score</div>
            <div class="score-cell-number" style="color:{'#1a5c2e' if d['esg_score']>=70 else '#7a4a0a' if d['esg_score']>=40 else '#8B0000'}">
                {d['esg_score']:.0f}<span style="font-size:1.1rem;color:{TEXT2};font-weight:400">%</span>
            </div>
            <span class="score-cell-status {d['es_cls']}">{d['es_lbl']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── RATIOS ───────────────────────────────────────────────
    st.markdown(f'<div class="kicker" style="margin-top:1.5rem">Key financial ratios</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.75rem;color:{TEXT2};margin-bottom:0.75rem;">Benchmarks: HMRC Business Population Estimates (UK) · RBI MSME Lending Data (India) · Bank of England SME criteria · World Bank MSME Finance Gap Report</p>', unsafe_allow_html=True)

    def rc(m, v, uk):
        if m == "margin": t, w = (20,10) if uk else (15,8); return "r-good" if v>=t else "r-warn" if v>=w else "r-bad"
        if m == "expense": return "r-good" if v<80 else "r-warn" if v<85 else "r-bad"
        if m == "dtr": return "r-good" if v<=30 else "r-warn" if v<=60 else "r-bad"
        if m == "cr": return "r-good" if v>=2 else "r-warn" if v>=1 else "r-bad"

    mc=rc("margin",d['profit_margin'],d['is_uk']); ec=rc("expense",d['expense_ratio'],d['is_uk'])
    dc=rc("dtr",d['debt_to_revenue'],d['is_uk']); cc=rc("cr",d['current_ratio'],d['is_uk'])
    def st_txt(c): return "✓ Healthy" if c=="r-good" else "⚠ Watch" if c=="r-warn" else "✗ At risk"
    bm = "≥20% (HMRC)" if d['is_uk'] else "≥15% (RBI)"

    st.markdown(f"""
    <table class="ratio-table">
        <thead><tr>
            <th>Ratio</th><th>What it measures</th>
            <th>Your figure</th><th>Benchmark</th><th>Status</th>
        </tr></thead>
        <tbody>
        <tr>
            <td>
                <strong style="color:{TEXT}">Net profit margin</strong>
                <span class="ratio-explain">Revenue minus all costs as % of revenue. How much you actually keep from each {d['currency']} earned.</span>
            </td>
            <td style="font-size:0.75rem;color:{TEXT2}">Profitability</td>
            <td class="ratio-val {mc}">{d['profit_margin']:.1f}%</td>
            <td style="font-size:0.75rem;color:{TEXT2}">{bm}</td>
            <td class="{mc}">{st_txt(mc)}</td>
        </tr>
        <tr>
            <td>
                <strong style="color:{TEXT}">Expense ratio</strong>
                <span class="ratio-explain">Total expenses as % of revenue. Higher means less buffer against cost shocks or revenue dips.</span>
            </td>
            <td style="font-size:0.75rem;color:{TEXT2}">Cost efficiency</td>
            <td class="ratio-val {ec}">{d['expense_ratio']:.1f}%</td>
            <td style="font-size:0.75rem;color:{TEXT2}">Below 80% healthy (HMRC)</td>
            <td class="{ec}">{st_txt(ec)}</td>
        </tr>
        <tr>
            <td>
                <strong style="color:{TEXT}">Debt-to-revenue</strong>
                <span class="ratio-explain">Total debt as % of annual revenue. Above 60% is high risk — a large portion of income is committed to obligations before operating costs.</span>
            </td>
            <td style="font-size:0.75rem;color:{TEXT2}">Leverage</td>
            <td class="ratio-val {dc}">{d['debt_to_revenue']:.1f}%</td>
            <td style="font-size:0.75rem;color:{TEXT2}">Below 30% low risk (World Bank)</td>
            <td class="{dc}">{'✓ Low risk' if dc=='r-good' else '⚠ Moderate' if dc=='r-warn' else '✗ High risk'}</td>
        </tr>
        <tr>
            <td>
                <strong style="color:{TEXT}">Current ratio</strong>
                <span class="ratio-explain">(Cash + receivables) ÷ debt. Below 1.0 means you cannot meet short-term obligations from liquid assets — a going concern indicator (ISA 570).</span>
            </td>
            <td style="font-size:0.75rem;color:{TEXT2}">Liquidity</td>
            <td class="ratio-val {cc}">{d['current_ratio']:.2f}</td>
            <td style="font-size:0.75rem;color:{TEXT2}">Above 2.0 (Bank of England)</td>
            <td class="{cc}">{st_txt(cc)}</td>
        </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # ── COMPLIANCE FLAGS ─────────────────────────────────────
    st.markdown(f'<div class="rule"></div><div class="kicker">Compliance flags</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.75rem;color:{TEXT2};margin-bottom:0.75rem;">Issues a regulatory review, loan assessment, or formal audit would identify immediately. Each flag cites the specific legislation or regulatory standard.</p>', unsafe_allow_html=True)
    if d['flags']:
        for severity, msg in d['flags']:
            css = "flag-crit" if severity == "crit" else "flag-warn"
            icon = "●" if severity == "crit" else "◐"
            st.markdown(f'<div class="flag {css}"><strong>{icon}</strong> {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="flag flag-ok">✓ No compliance flags detected. Your numbers present cleanly against regulatory thresholds.</div>', unsafe_allow_html=True)

    # ── FINANCIAL PRIORITY ACTIONS ───────────────────────────
    st.markdown(f'<div class="rule"></div><div class="kicker">Financial priority actions</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.75rem;color:{TEXT2};margin-bottom:0.75rem;">The 3 most important steps based on your specific numbers — in priority order.</p>', unsafe_allow_html=True)
    for i, action in enumerate(d['actions'][:3], 1):
        st.markdown(f'<div class="action-item"><div class="action-num">{i}.</div><div style="color:{TEXT}">{action}</div></div>', unsafe_allow_html=True)

    # ── ESG UPGRADE PLAN ─────────────────────────────────────
    st.markdown(f'<div class="rule"></div><div class="kicker">ESG upgrade plan</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.75rem;color:{TEXT2};margin-bottom:0.75rem;">Concrete, zero or low-cost actions calculated from your specific numbers. Each shows the estimated ESG score improvement and where relevant the financial saving. Sources: UK DBT SME ESG Guidance 2023 · SEBI BRSR Lite · ISO 26000.</p>', unsafe_allow_html=True)

    for item in d['esg_actions'][:4]:
        st.markdown(f"""
        <div class="esg-plan-wrap">
            <div class="esg-plan-header">
                <span>{item['pillar']}</span>
                <span>{item['impact']} &nbsp;·&nbsp; {item['cost']}</span>
            </div>
            <div class="esg-plan-item">
                <strong>{item['action']}</strong><br>
                {item['detail']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── ESG INDICATORS ───────────────────────────────────────
    st.markdown(f'<div class="kicker" style="margin-top:1rem">ESG governance indicators</div>', unsafe_allow_html=True)
    esg_html = ""
    for item, passed in d['esg_items']:
        css = "esg-pass" if passed else "esg-fail"
        icon = "✓" if passed else "✗"
        esg_html += f'<div class="esg-item {css}" style="color:{TEXT}"><strong style="color:{"inherit"}">{icon}</strong>&nbsp; {item}</div>'
    st.markdown(f'<div class="esg-grid">{esg_html}</div>', unsafe_allow_html=True)

    # ── OVERALL ASSESSMENT ───────────────────────────────────
    st.markdown(f'<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="summary-box">
        <div class="summary-kicker">Overall assessment</div>
        {d['summary']}
    </div>
    """, unsafe_allow_html=True)

    # ── STRESS TEST ──────────────────────────────────────────
    st.markdown(f'<div class="kicker" style="margin-top:1.5rem">Stress test — what happens if revenue declines?</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.78rem;color:{TEXT2};margin-bottom:0.75rem;">Expenses held constant — the conservative assumption used in Bank of England SME stress testing. Smit also shows which ESG actions would reduce the damage.</p>', unsafe_allow_html=True)

    drop = st.slider("Revenue declines by:", 0, 50, 20, format="%d%%")
    nr = d['revenue'] * (1 - drop/100)
    np_ = nr - d['expenses']
    nm = (np_/nr*100) if nr > 0 else 0
    esg_buffer = d['expenses'] * 0.05

    st.markdown(f"""
    <div class="stress-row">
        <div class="stress-cell">
            <div class="stress-cell-label">Revenue after decline</div>
            <div class="stress-cell-value">{d['currency']}{nr:,.0f}</div>
            <div class="stress-cell-delta d-neg">−{drop}%</div>
        </div>
        <div class="stress-cell">
            <div class="stress-cell-label">Profit / loss</div>
            <div class="stress-cell-value" style="color:{'#1a5c2e' if np_>=0 else RED}">{d['currency']}{np_:,.0f}</div>
            <div class="stress-cell-delta {'d-pos' if np_>=0 else 'd-neg'}">{d['currency']}{np_-d['profit']:,.0f}</div>
        </div>
        <div class="stress-cell">
            <div class="stress-cell-label">New profit margin</div>
            <div class="stress-cell-value" style="color:{'#1a5c2e' if nm>=10 else RED}">{nm:.1f}%</div>
            <div class="stress-cell-delta d-neg">{nm-d['profit_margin']:+.1f}pp</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if np_ < 0:
        st.markdown(f'<div class="flag flag-crit">A {drop}% revenue decline pushes your business into loss. ESG action: reducing your expense ratio by 5% through sustainable cost review would add {d["currency"]}{esg_buffer:,.0f}/year — enough to {'stay profitable' if (nr - d["expenses"] + esg_buffer) > 0 else 'meaningfully reduce the loss'} under this scenario.</div>', unsafe_allow_html=True)
    elif nm < 10:
        st.markdown(f'<div class="flag flag-warn">Margin compresses to {nm:.1f}% — dangerously thin. ESG action: a monthly financial review (zero cost) gives you 30 days earlier warning to respond to revenue decline before it becomes critical.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="flag flag-ok">Business remains profitable under a {drop}% revenue decline. Margin holds at {nm:.1f}%. Your ESG governance practices support resilience — businesses with strong governance typically access emergency credit faster in downturns.</div>', unsafe_allow_html=True)

    # ── SMIT AI — PRO GATE ───────────────────────────────────
    st.markdown(f"""
    <div class="rule-thick" style="margin-top:2rem"></div>
    <div class="kicker">Smit AI — financial + ESG assistant</div>
    <h3 style="font-size:1.3rem;margin-bottom:0.4rem;color:{TEXT}">Ask Smit about your numbers</h3>
    <p style="font-size:0.82rem;color:{TEXT2};margin-bottom:1rem;line-height:1.6;">
        Smit AI knows your exact 7 inputs. Every answer is constrained to your data and official benchmarks — not generic advice.
        This is a Pro feature.
    </p>
    """, unsafe_allow_html=True)

    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        has_api = bool(api_key)
    except Exception:
        has_api = False

    if not has_api:
        st.markdown(f"""
        <div class="pro-gate">
            <p><strong>Smit AI — Pro feature</strong></p>
            <p>Ask any question about your specific numbers. Answers are constrained to your 7 inputs and official Smit benchmarks only. Max 250 words. Every answer cites its source. Always ends with a legal disclaimer.</p>
            <p>Not generic financial advice — specific to your actual data.</p>
            <p style="font-size:0.75rem;margin-top:0.5rem;color:rgba(255,255,255,0.35);">Pro access coming soon. Join early access at getsmit.co</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-wrap">
            <div class="chat-header">
                <span>Smit AI</span>
                <span class="chat-badge">Pro · Your data loaded · Constrained to official benchmarks</span>
            </div>
        </div>
        <p style="font-size:0.78rem;color:{TEXT2};margin:0.5rem 0 0.75rem;line-height:1.6;">
            Every answer uses only your 7 inputs + Smit's official benchmarks (HMRC, RBI, Bank of England, World Bank, ISA 570, SEBI BRSR Lite, ISO 26000). Not regulated financial advice.
        </p>
        """, unsafe_allow_html=True)

        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user"><div class="chat-lbl">You</div>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-assistant"><div class="chat-lbl">Smit AI</div>{msg["content"]}</div>', unsafe_allow_html=True)

        user_q = st.text_input(
            "Ask Smit",
            placeholder="e.g. Why is my risk score low? Which ESG action saves the most money? What would a bank see?",
            label_visibility="collapsed",
            key="chat_input"
        )

        if st.button("Send →", key="send_chat"):
            if user_q.strip():
                d = st.session_state.financial_data
                cur = d['currency']

                system_prompt = f"""You are Smit AI — the financial and ESG diagnostic assistant built into the Smit platform.

STRICT IDENTITY: You ONLY use the user's exact 7 financial inputs, their checklist answers, their region, and the official Smit methodology v2.0 benchmarks listed below. You do NOT use any outside knowledge, general financial advice, or information not provided in this prompt.

USER'S 7 FINANCIAL INPUTS:
1. Annual revenue: {cur}{d['revenue']:,.0f}
2. Annual expenses: {cur}{d['expenses']:,.0f}
3. Cash in bank: {cur}{d['cash']:,.0f}
4. Total debt / liabilities: {cur}{d['debt']:,.0f}
5. Monthly fixed costs: {cur}{d['fixed_costs']:,.0f}
6. Receivables: {cur}{d['receivables']:,.0f}
7. Region: {'United Kingdom' if d['is_uk'] else 'India'} | Business: {st.session_state.user_info.get('biz_type','SME')}

CALCULATED METRICS:
- Net profit margin: {d['profit_margin']:.1f}%
- Expense ratio: {d['expense_ratio']:.1f}%
- Debt-to-revenue: {d['debt_to_revenue']:.1f}%
- Current ratio: {d['current_ratio']:.2f}
- Financial risk score: {d['financial_score']:.0f}/100
- Audit readiness: {d['audit_score']:.0f}%
- ESG governance score: {d['esg_score']:.0f}%
- G pillar score: {d['g_score']:.0f}%
- S pillar score: {d['s_score']:.0f}%
- E pillar score: {d['e_score']:.0f}%
- Combined Smit Score: {d['combined_score']}/100

CHECKLIST ANSWERS:
- Receipts/invoices kept: {'Yes' if d['q1'] else 'No'}
- Dedicated business bank account: {'Yes' if d['q2'] else 'No'}
- VAT/GST registration known: {'Yes' if d['q3'] else 'No'}
- Files returns on time: {'Yes' if d['q4'] else 'No'}
- Records available: {'Yes' if d['q5'] else 'No'}
- Monthly/quarterly financial review: {'Yes' if d['esg1'] else 'No'}
- Compliance awareness: {'Yes' if d['esg2'] else 'No'}
- Written client contracts: {'Yes' if d['esg3'] else 'No'}
- Fair practices: {'Yes' if d['esg4'] else 'No'}
- Environmental awareness: {'Yes' if d['esg5'] else 'No'}
- Active environmental steps: {'Yes' if d['esg6'] else 'No'}

OFFICIAL SMIT METHODOLOGY v2.0 BENCHMARKS (always cite source):
Financial:
- UK profit margin healthy ≥20% — source: HMRC Business Population Estimates
- India profit margin healthy ≥15% — source: RBI Annual Report MSME Lending Data
- Expense ratio warning >85% — source: HMRC SME benchmarks
- Current ratio healthy ≥2.0; below 1.0 = going concern indicator — source: Bank of England SME lending criteria; ISA 570 (IAASB)
- Debt-to-revenue low risk ≤30%; high risk >60% — source: World Bank MSME Finance Gap Report
- Cash buffer recommended ≥2 months fixed costs — source: Bank of England SME resilience guidance
- UK VAT threshold: £85,000 — source: HMRC, Value Added Tax Act 1994
- India GST threshold: ₹20 Lakhs services — source: CGST Act 2017

ESG:
- Governance baseline: FRC Corporate Governance Code (UK); SEBI BRSR Lite Principle 1 (India)
- Social practices: ISO 26000 Section 6.6; Late Payment Act 1998 (UK); MSME Development Act 2006 (India)
- Environmental baseline: UK DBT SME ESG Guidance 2023; SEBI BRSR Lite Principle 6; BSI BS 8001:2017
- ESG score weighting: Governance 40%, Social 30%, Environmental 30%
- Combined Smit Score: Financial 60%, ESG 40%

NON-NEGOTIABLE RULES:
1. EVERY answer MUST reference the user's actual numbers AND the specific official threshold with source.
2. ESG suggestions MUST be zero or low-cost, directly linked to their numbers, with estimated score impact and financial saving where calculable.
3. You MUST end EVERY single response with exactly: "⚠ Not regulated financial, tax or legal advice. For decisions affecting your tax or legal position, consult a qualified professional."
4. If a question cannot be answered from the 7 inputs + benchmarks, respond ONLY with: "I can only answer using your provided figures and Smit's official benchmarks. Please clarify your question."
5. Maximum 250 words. Plain English. One concrete next step. Always actionable.
6. Never speculate. Never use outside knowledge. Never fabricate numbers."""

                msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_messages]
                msgs.append({"role": "user", "content": user_q})
                st.session_state.chat_messages.append({"role": "user", "content": user_q})

                try:
                    client = anthropic.Anthropic(api_key=api_key)
                    resp = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=400,
                        system=system_prompt,
                        messages=msgs
                    )
                    answer = resp.content[0].text
                    st.session_state.chat_messages.append({"role": "assistant", "content": answer})
                except Exception:
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": "Connection error — please try again.\n\n⚠ Not regulated financial, tax or legal advice. For decisions affecting your tax or legal position, consult a qualified professional."
                    })
                st.rerun()

    # ── DOWNLOAD ─────────────────────────────────────────────
    st.markdown(f'<div class="rule"></div>', unsafe_allow_html=True)
    st.button("📄 Download full report (PDF) — Pro feature · Coming soon", disabled=True)

    # ── DISCLAIMER ───────────────────────────────────────────
    st.markdown(f"""
    <div class="disclaimer">
        <strong style="color:{TEXT}">⚠ Important — please read.</strong>
        Smit is a financial intelligence and ESG diagnostic tool. It calculates and interprets your data
        using published benchmarks from HMRC, Companies House, Bank of England, Reserve Bank of India,
        Ministry of MSME India, World Bank MSME Finance Gap Report, UK DBT SME ESG Guidance 2023,
        SEBI BRSR Lite Framework, ISO 26000, and ISA 570.<br><br>
        <strong style="color:{TEXT}">Smit does not provide regulated financial, tax, investment, or legal advice.</strong>
        Benchmarks are indicative — your specific sector, circumstances, and business model may differ
        from general SME averages. For decisions affecting your tax position, compliance obligations,
        or legal standing, always consult a qualified professional (CA, accountant, or solicitor).<br><br>
        <strong style="color:{TEXT}">Privacy:</strong> Financial data you enter is processed in-session only
        and is not stored on Smit's servers. Your name and email (collected at signup with your consent)
        are used only for product communications. You can request deletion at any time:
        hello@getsmit.co. Smit operates under UK GDPR and India DPDP Act 2023.
    </div>
    """, unsafe_allow_html=True)
