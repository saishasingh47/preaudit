import streamlit as st
import anthropic

st.set_page_config(
    page_title="Smit — Financial + ESG Diagnostic",
    page_icon="smit_icon.png",
    layout="centered"
)

# ── SESSION DEFAULTS ──────────────────────────────────────────
for k, v in [
    ('colour_mode', 'light'), ('mode_confirmed', False),
    ('signed_up', False), ('user_info', {}),
    ('results_ready', False), ('financial_data', {}),
    ('chat_messages', [])
]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── TINY MODE POPUP — fires once ──────────────────────────────
if not st.session_state.mode_confirmed:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&family=Playfair+Display:wght@700;900&display=swap');
    html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background:#F4F5F7;color:#111214}
    #MainMenu{visibility:hidden}footer{visibility:hidden}header{visibility:hidden}
    .block-container{padding:3rem 1.5rem;max-width:400px;margin:0 auto}
    .popup-logo{font-family:'Playfair Display',serif;font-size:2rem;font-weight:900;color:#111214;letter-spacing:-0.03em;margin-bottom:0.25rem}
    .popup-logo em{font-style:normal;color:#8B0000}
    .popup-q{font-size:0.75rem;font-weight:500;color:#72757E;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:1.5rem}
    .stButton>button{background:#111214!important;color:#F4F5F7!important;border:none!important;border-radius:0!important;font-family:'DM Sans',sans-serif!important;font-size:0.82rem!important;font-weight:500!important;letter-spacing:0.04em!important;padding:0.75rem 1.5rem!important;width:100%!important;transition:background .2s!important}
    .stButton>button:hover{background:#8B0000!important}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="popup-logo">Smit<em>.</em></div>', unsafe_allow_html=True)
    st.markdown('<div class="popup-q">Display preference</div>', unsafe_allow_html=True)

    mode_choice = st.radio(
        "Select mode",
        ["Light", "Dark"],
        horizontal=True,
        label_visibility="collapsed"
    )

    if st.button("Continue →"):
        st.session_state.colour_mode = 'dark' if mode_choice == "Dark" else 'light'
        st.session_state.mode_confirmed = True
        st.rerun()
    st.stop()

# ── COLOUR TOKENS ─────────────────────────────────────────────
dk = st.session_state.colour_mode == 'dark'

BG    = "#111214" if dk else "#F4F5F7"
BG2   = "#1C1E22" if dk else "#E8EAEE"
CARD  = "#1C1E22" if dk else "#FFFFFF"
TEXT  = "#F0F1F3" if dk else "#111214"
TEXT2 = "#888A93" if dk else "#72757E"
RULE  = "#2E3038" if dk else "#CACDD5"
RED   = "#8B0000"
ACCENT = "#D6E6F2"
# Pastel status colours — for technical result displays only
GR_T  = "#B8D9C2" if dk else "#1C5E30"
GR_BG = "rgba(184,217,194,0.1)" if dk else "#EAF5EF"
AM_T  = "#F5E0A8" if dk else "#7A5910"
AM_BG = "rgba(245,224,168,0.1)" if dk else "#FBF4E0"
RD_T  = "#F4BBBB" if dk else "#8B0000"
RD_BG = "rgba(244,187,187,0.1)" if dk else "#FDECEC"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

html,body,[class*="css"]{{font-family:'DM Sans',sans-serif;background:{BG};color:{TEXT}}}
#MainMenu{{visibility:hidden}}footer{{visibility:hidden}}header{{visibility:hidden}}
h1,h2,h3{{font-family:'Playfair Display',serif;color:{TEXT}}}
.block-container{{padding:2rem 1.5rem;max-width:840px}}

/* Masthead */
.mast{{border-bottom:2px solid {TEXT};padding-bottom:0.85rem;margin-bottom:0.5rem}}
.mast-row{{display:flex;justify-content:space-between;align-items:baseline}}
.mast-logo{{font-family:'Playfair Display',serif;font-size:2.6rem;font-weight:900;color:{TEXT};letter-spacing:-0.03em;line-height:1}}
.mast-logo em{{font-style:normal;color:{RED}}}
.mast-tag{{font-size:0.7rem;font-weight:500;color:{RED};text-transform:uppercase;letter-spacing:0.1em}}
.mast-sub{{font-size:0.7rem;color:{TEXT2};border-top:1px solid {RULE};padding-top:0.4rem;margin-top:0.4rem}}

/* Mode toggle link */
.mode-link{{font-size:0.7rem;color:{TEXT2};cursor:pointer;text-decoration:underline;text-underline-offset:2px}}

/* Rules */
.rule{{height:1px;background:{RULE};margin:1.5rem 0}}
.rule-heavy{{height:2px;background:{TEXT};margin:2rem 0}}
.kicker{{font-size:0.7rem;font-weight:500;color:{RED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.3rem}}

/* Steps */
.step-row{{display:flex;align-items:center;gap:0.6rem;margin-bottom:1rem}}
.step-dot{{width:22px;height:22px;background:{RED};color:white;font-size:0.75rem;font-weight:600;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.step-lbl{{font-size:0.78rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:{TEXT}}}

/* Combined score hero */
.score-hero{{background:#111214;padding:2rem 1.75rem;text-align:center;margin:1rem 0}}
.sh-lbl{{font-size:0.65rem;font-weight:500;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:0.14em;margin-bottom:0.5rem}}
.sh-num{{font-family:'Playfair Display',serif;font-size:4.5rem;font-weight:900;line-height:1;margin-bottom:0.3rem}}
.sh-status{{font-size:0.88rem;font-weight:600;margin-bottom:0.25rem}}
.sh-sub{{font-size:0.68rem;color:rgba(255,255,255,0.28)}}
.sh-breakdown{{display:flex;justify-content:center;gap:2.5rem;margin-top:1.25rem;padding-top:1.25rem;border-top:1px solid rgba(255,255,255,0.08)}}
.sh-b{{text-align:center}}
.sh-b-v{{font-family:'Playfair Display',serif;font-size:1.5rem;font-weight:700}}
.sh-b-l{{font-size:0.62rem;font-weight:500;color:rgba(255,255,255,0.28);text-transform:uppercase;letter-spacing:0.08em;margin-top:0.15rem}}

/* Score summary table */
.score-summary-table{{width:100%;border-collapse:collapse;margin:1rem 0;font-size:0.875rem}}
.score-summary-table th{{font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:{TEXT2};padding:0.5rem 0.75rem;border-bottom:2px solid {TEXT};text-align:left}}
.score-summary-table td{{padding:0.65rem 0.75rem;border-bottom:1px solid {RULE};color:{TEXT};vertical-align:middle}}
.score-summary-table tr:hover td{{background:{BG2}}}
.sst-score{{font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700}}
.sst-badge{{display:inline-block;font-size:0.7rem;font-weight:500;padding:0.18rem 0.55rem}}

/* Score row */
.score-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:{RULE};border:1px solid {RULE};margin:1rem 0}}
.score-cell{{background:{BG};padding:1.25rem 1rem;text-align:center}}
.score-cell-lbl{{font-size:0.65rem;font-weight:500;color:{TEXT2};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem}}
.score-cell-num{{font-family:'Playfair Display',serif;font-size:2.6rem;font-weight:900;line-height:1;margin-bottom:0.35rem}}
.score-cell-status{{font-size:0.7rem;font-weight:500;padding:0.2rem 0.6rem;display:inline-block}}
.s-green{{color:{GR_T};background:{GR_BG}}}
.s-amber{{color:{AM_T};background:{AM_BG}}}
.s-red{{color:{RD_T};background:{RD_BG}}}

/* Ratio table */
.ratio-table{{width:100%;border-collapse:collapse;font-size:0.875rem;margin:1rem 0}}
.ratio-table th{{font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:{TEXT2};padding:0.5rem 0.75rem;border-bottom:2px solid {TEXT};text-align:left}}
.ratio-table td{{padding:0.7rem 0.75rem;border-bottom:1px solid {RULE};color:{TEXT};vertical-align:top}}
.ratio-table tr:hover td{{background:{BG2}}}
.r-val{{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700}}
.r-explain{{font-size:0.7rem;color:{TEXT2};display:block;margin-top:0.2rem;font-style:italic;line-height:1.45}}
.r-good{{color:{GR_T}}}.r-warn{{color:{AM_T}}}.r-bad{{color:{RD_T}}}

/* Flags — pastel colours */
.flag{{padding:0.75rem 1rem;margin:0.4rem 0;border-left:3px solid;font-size:0.875rem;line-height:1.5}}
.flag-crit{{border-color:{RD_T};background:{RD_BG};color:{RD_T}}}
.flag-warn{{border-color:{AM_T};background:{AM_BG};color:{AM_T}}}
.flag-ok{{border-color:{GR_T};background:{GR_BG};color:{GR_T}}}

/* Actions */
.action-item{{display:flex;gap:0.75rem;align-items:flex-start;padding:0.85rem 1rem;margin:0.4rem 0;background:{BG2};border:1px solid {RULE};font-size:0.875rem;line-height:1.5;color:{TEXT}}}
.action-num{{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:{RED};line-height:1;flex-shrink:0;min-width:20px}}

/* ESG plan */
.esg-plan{{margin:0.4rem 0;border:1px solid {"rgba(184,217,194,0.2)" if dk else "#C8E6D0"}}}
.esg-plan-header{{background:{"rgba(28,94,48,0.25)" if dk else "#1C5E30"};color:{"#B8D9C2" if dk else "white"};padding:0.6rem 1rem;font-size:0.7rem;font-weight:500;text-transform:uppercase;letter-spacing:0.08em;display:flex;justify-content:space-between}}
.esg-plan-body{{padding:0.85rem 1rem;background:{GR_BG};font-size:0.875rem;line-height:1.65;color:{TEXT}}}
.esg-plan-body strong{{color:{GR_T}}}

/* ESG indicators grid */
.esg-grid{{display:grid;grid-template-columns:1fr 1fr;gap:0.4rem;margin:0.75rem 0}}
.esg-item{{display:flex;align-items:center;gap:0.5rem;padding:0.5rem 0.75rem;background:{BG2};border:1px solid {RULE};font-size:0.8rem;color:{TEXT}}}
.esg-pass{{border-left:3px solid {GR_T}}}
.esg-fail{{border-left:3px solid {RD_T};opacity:0.55}}

/* Summary */
.summary{{background:#111214;color:#F0F1F3;padding:1.5rem;margin:1rem 0;font-size:0.9rem;line-height:1.7}}
.summary-kicker{{font-size:0.68rem;font-weight:500;color:#F5E0A8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.5rem}}

/* Stress */
.stress-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:{RULE};border:1px solid {RULE};margin:1rem 0}}
.stress-cell{{background:{BG};padding:1rem;text-align:center}}
.stress-cell-l{{font-size:0.65rem;font-weight:500;color:{TEXT2};text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.4rem}}
.stress-cell-v{{font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:700;color:{TEXT}}}
.stress-cell-d{{font-size:0.72rem;margin-top:0.2rem}}
.d-neg{{color:{RD_T}}}.d-pos{{color:{GR_T}}}

/* Pro gate */
.pro-gate{{background:#111214;padding:1.75rem;text-align:center}}
.pro-gate-lbl{{font-size:0.7rem;font-weight:500;text-transform:uppercase;letter-spacing:0.1em;color:{RED};margin-bottom:0.5rem}}
.pro-gate p{{font-size:0.875rem;color:rgba(255,255,255,0.55);line-height:1.65;margin-bottom:0.5rem}}
.pro-gate strong{{color:white}}

/* Chat */
.chat-wrap{{border:1px solid {RULE};background:{CARD};margin:1rem 0}}
.chat-header{{background:#111214;color:#F0F1F3;padding:0.75rem 1rem;font-size:0.72rem;font-weight:500;text-transform:uppercase;letter-spacing:0.06em;display:flex;justify-content:space-between;align-items:center}}
.chat-badge{{font-size:0.65rem;background:{RED};color:white;padding:0.14rem 0.5rem}}
.chat-user{{background:{BG2};border-left:3px solid {TEXT};padding:0.75rem 1rem;margin:0.5rem;font-size:0.875rem;color:{TEXT}}}
.chat-assistant{{background:{CARD};border-left:3px solid {RED};padding:0.75rem 1rem;margin:0.5rem;font-size:0.875rem;line-height:1.65;color:{TEXT}}}
.chat-lbl{{font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.35rem}}
.chat-user .chat-lbl{{color:{TEXT2}}}
.chat-assistant .chat-lbl{{color:{RED}}}

/* Legal */
.legal-disclaimer{{border-top:1px solid {RULE};padding-top:1rem;margin-top:2rem;font-size:0.72rem;color:{TEXT2};line-height:1.65}}

/* Buttons — red primary, matches website */
.stButton>button{{background:{RED}!important;color:white!important;border:none!important;border-radius:0!important;padding:0.7rem 1.5rem!important;font-family:'DM Sans',sans-serif!important;font-size:0.85rem!important;font-weight:500!important;letter-spacing:0.04em!important;transition:all .2s!important;width:100%!important}}
.stButton>button:hover{{background:#A50000!important}}
.stButton>button:disabled{{background:{RULE}!important;color:{TEXT2}!important}}

/* Inputs */
.stTextInput>div>div>input{{border-radius:0!important;border:1px solid {RULE}!important;background:{CARD}!important;color:{TEXT}!important;font-family:'DM Sans',sans-serif!important;font-size:0.9rem!important}}
.stTextInput>div>div>input:focus{{border-color:{TEXT}!important;box-shadow:none!important}}
.stNumberInput>div>div>input{{border-radius:0!important;border:1px solid {RULE}!important;background:{CARD}!important;color:{TEXT}!important}}
.stSelectbox>div>div{{border-radius:0!important;border:1px solid {RULE}!important;background:{CARD}!important}}
.stCheckbox>label,.stRadio>label,label{{font-family:'DM Sans',sans-serif!important;font-size:0.875rem!important;color:{TEXT}!important}}
.stSlider>div>div>div{{background:{RED}!important}}
</style>
""", unsafe_allow_html=True)

# ── MASTHEAD ──────────────────────────────────────────────────
mode_label = "Switch to light mode" if dk else "Switch to dark mode"
st.markdown(f"""
<div class="mast">
    <div class="mast-row">
        <div class="mast-logo">Smit<em>.</em></div>
        <div class="mast-tag">Financial + ESG Diagnostic</div>
    </div>
    <div class="mast-sub">
        UK &amp; India &nbsp;·&nbsp; HMRC · RBI · Bank of England · World Bank &nbsp;·&nbsp; Not regulated financial advice
    </div>
</div>
""", unsafe_allow_html=True)

if st.button(mode_label, key="mode_toggle"):
    st.session_state.colour_mode = 'light' if dk else 'dark'
    st.rerun()

# ── SIGNUP ────────────────────────────────────────────────────
if not st.session_state.signed_up:
    st.markdown(f"""
    <div style="padding:2rem 0 1rem">
        <div class="kicker">Free access — no credit card</div>
        <h1 style="font-size:2.1rem;letter-spacing:-0.03em;margin-bottom:0.5rem;line-height:1.1">
            Your business deserves a financial expert.
        </h1>
        <p style="font-family:'Playfair Display',serif;font-size:1.1rem;font-style:italic;color:{RED};margin-bottom:1rem">Now it has one.</p>
        <p style="font-size:0.9rem;color:{TEXT2};max-width:540px;line-height:1.8;margin-bottom:1.5rem">
            Enter 7 numbers. Receive the same financial and ESG analysis benchmarked against HMRC, RBI, Bank of England, and World Bank data. In plain English.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full name", placeholder="Your name")
        email = st.text_input("Email address", placeholder="your@email.com")
    with col2:
        region = st.selectbox("Region", ["", "🇬🇧 United Kingdom", "🇮🇳 India", "🌍 Other"])
        biz_type = st.selectbox("Business type", [
            "", "Freelancer / Sole trader", "Small business", "Early-stage startup",
            "Limited company director", "Other"
        ])

    consent = st.checkbox(
        "I agree to Smit storing my name, email, and business type for product communications. "
        "I can request deletion at any time at hello@getsmit.co. "
        "Smit does not sell or share this data. Financial data I enter is not stored without additional consent."
    )

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    if st.button("Access Smit free"):
        if not name or not email or not region or not biz_type:
            st.error("Please complete all fields.")
        elif "@" not in email:
            st.error("Please enter a valid email address.")
        elif not consent:
            st.error("Please agree to the data terms to continue.")
        else:
            st.session_state.signed_up = True
            st.session_state.user_info = {"name": name, "email": email, "region": region, "biz_type": biz_type}
            st.rerun()

    st.markdown(f"""
    <div class="rule" style="margin-top:1.5rem"></div>
    <p style="font-family:'DM Mono',monospace;font-size:0.65rem;color:{TEXT2};line-height:1.75">
        Privacy: name and email are stored with consent for communications only. Financial inputs are processed in-session and not stored. UK GDPR &amp; India DPDP Act 2023. Deletion: hello@getsmit.co<br><br>
        Smit does not provide regulated financial, tax, or legal advice. Consult a qualified professional for regulated decisions.
    </p>
    """, unsafe_allow_html=True)
    st.stop()

# ── MAIN TOOL ─────────────────────────────────────────────────
user = st.session_state.user_info
is_uk = "United Kingdom" in user.get("region", "")
currency = "£" if is_uk else "₹"
step = 1000.0 if is_uk else 10000.0

st.markdown(f'<p style="font-family:\'DM Mono\',monospace;font-size:0.68rem;color:{TEXT2};padding:0.5rem 0 1rem">Welcome, {user.get("name","")} &nbsp;·&nbsp; {user.get("biz_type","")} &nbsp;·&nbsp; {user.get("region","")}</p>', unsafe_allow_html=True)

# ── STEP 1 ────────────────────────────────────────────────────
st.markdown('<div class="rule-heavy"></div>', unsafe_allow_html=True)
st.markdown('<div class="step-row"><div class="step-dot">1</div><div class="step-lbl">Your 7 financial inputs</div></div>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:0.85rem;color:{TEXT2};margin-bottom:1.25rem">These exact figures are used for every calculation and every Smit AI response.</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<p style="font-weight:600;margin-bottom:0.4rem;color:{TEXT}">Revenue & costs ({currency})</p>', unsafe_allow_html=True)
    revenue = st.number_input("Annual revenue", min_value=0.0, step=step, key="rev",
        help="Total income for the past 12 months before any deductions")
    expenses = st.number_input("Annual expenses", min_value=0.0, step=step, key="exp",
        help="All business costs for the year — staff, rent, software, materials")
    cash = st.number_input("Cash in bank", min_value=0.0, step=step/2, key="cash",
        help="Liquid cash across all business accounts right now")
with col2:
    st.markdown(f'<p style="font-weight:600;margin-bottom:0.4rem;color:{TEXT}">Debt & obligations ({currency})</p>', unsafe_allow_html=True)
    debt = st.number_input("Total debt / liabilities", min_value=0.0, step=step/2, key="debt",
        help="All outstanding loans, credit, overdrafts, and financial obligations")
    fixed_costs = st.number_input("Monthly fixed costs", min_value=0.0, step=100.0, key="fc",
        help="Costs that stay constant regardless of revenue — rent, salaries, subscriptions")
    receivables = st.number_input("Money owed to you", min_value=0.0, step=100.0, key="rec",
        help="Outstanding invoices and payments due that haven't been received yet")

# ── STEP 2 ────────────────────────────────────────────────────
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="step-row"><div class="step-dot">2</div><div class="step-lbl">Compliance checklist</div></div>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:0.85rem;color:{TEXT2};margin-bottom:1rem">These are the first items any regulatory review, loan application, or formal audit checks.</p>', unsafe_allow_html=True)

if is_uk:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)",
        help="HMRC record-keeping requirement. Companies: 6 years. Sole traders: 22 months from tax year end. No records = no defence in any tax enquiry.")
    q2 = st.checkbox("I have a dedicated business bank account",
        help="Legally required for limited companies (Companies Act 2006). For sole traders, HMRC guidance strongly recommends separation. Mixing finances is the most common finding in SME audits.")
    q3 = st.checkbox("I know my VAT position relative to the £85,000 registration threshold",
        help="HMRC requires registration within 30 days of exceeding £85,000 annual taxable turnover. Source: Value Added Tax Act 1994, Section 67.")
    q4 = st.checkbox("I file self-assessment or company accounts on time each year",
        help="Late self-assessment: £100 immediate penalty, then £10/day up to £900. Late company accounts: £150–£1,500 (Companies House). Source: HMRC, Finance Act 1994.")
    q5 = st.checkbox("I have financial records going back at least 2 years",
        help="HMRC requires 5 years post-submission for self-assessment; 6 years for companies. Two years is Smit's practical minimum baseline.")
else:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)",
        help="GST Rules 2017 require records for 72 months (6 years) from the end of the relevant financial year. Tax invoices mandatory under CGST Act 2017, Section 31.")
    q2 = st.checkbox("I have a dedicated business bank account",
        help="Required for GST-registered businesses to track input tax credits. For companies: Companies Act 2013, Section 128 requires books of account at registered office.")
    q3 = st.checkbox("I know my GST position relative to the ₹20 Lakh registration threshold",
        help="CGST Act 2017, Section 22: mandatory registration above ₹20 Lakhs (services) or ₹40 Lakhs (goods). Penalty for non-registration: 10% of tax or ₹10,000, whichever is higher.")
    q4 = st.checkbox("I file GST returns quarterly and on time",
        help="Late GSTR-3B: ₹50/day plus 18% per annum interest on outstanding tax (CGST Act 2017, Section 47). Filing history is required for bank loans and government contracts.")
    q5 = st.checkbox("I maintain records available for immediate review",
        help="Companies Act 2013, Section 128: books must be at registered office and available for inspection. Income Tax Act 1961, Section 44AA: mandatory for specified professionals.")

# ── STEP 3 ────────────────────────────────────────────────────
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
st.markdown('<div class="step-row"><div class="step-dot">3</div><div class="step-lbl">ESG governance assessment</div></div>', unsafe_allow_html=True)
st.markdown(f'<p style="font-size:0.85rem;color:{TEXT2};margin-bottom:0.5rem">ESG requirements are filtering down to SMEs from banks, large clients, and supply chains. These questions assess your current position across the three pillars.</p>', unsafe_allow_html=True)
st.markdown(f'<p style="font-family:\'DM Mono\',monospace;font-size:0.62rem;color:{TEXT2};margin-bottom:1rem">Sources: UK DBT SME ESG Guidance 2023 · SEBI BRSR Lite · ISO 26000 · FRC Corporate Governance Code</p>', unsafe_allow_html=True)

st.markdown(f'<p style="font-size:0.78rem;font-weight:600;color:{TEXT};margin-bottom:0.5rem">G — Governance</p>', unsafe_allow_html=True)
esg1 = st.checkbox("I review my finances monthly or quarterly",
    help="Regular review is a core governance indicator. FRC Corporate Governance Code (UK) · SEBI BRSR Lite Principle 1 (India).")
esg2 = st.checkbox("I am aware of my key legal and compliance obligations",
    help="Compliance awareness is the governance foundation. Source: UK DBT SME ESG Guidance 2023 · SEBI BRSR Lite.")

st.markdown(f'<p style="font-size:0.78rem;font-weight:600;color:{TEXT};margin-top:0.75rem;margin-bottom:0.5rem">S — Social</p>', unsafe_allow_html=True)
esg3 = st.checkbox("I use written contracts or terms of service with clients",
    help="ISO 26000, Section 6.6 (fair operating practices). Protects payment rights under Late Payment Act 1998 (UK) / MSME Development Act 2006 (India).")
esg4 = st.checkbox("I deal fairly and consistently with clients and suppliers",
    help="ISO 26000, Sections 6.3 and 6.6. Social baseline for ESG compliance.")

st.markdown(f'<p style="font-size:0.78rem;font-weight:600;color:{TEXT};margin-top:0.75rem;margin-bottom:0.5rem">E — Environmental</p>', unsafe_allow_html=True)
esg5 = st.checkbox("I track or consider the environmental impact of my business",
    help="SEBI BRSR Lite Principle 6 (India) · UK DBT SME ESG Guidance 2023 · BSI BS 8001:2017. Entry-level E indicator for SMEs.")
esg6 = st.checkbox("I have taken or am considering steps to reduce energy use, waste, or carbon footprint",
    help="UK DBT SME ESG Guidance 2023: energy efficiency is the most actionable E action for SMEs. Typically reduces costs 8–15%.")

# ── RUN ───────────────────────────────────────────────────────
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

if st.button("Run Smit Diagnostic →"):
    if revenue == 0:
        st.error("Please enter your annual revenue to continue.")
        st.stop()

    # Calculations
    profit = revenue - expenses
    profit_margin = (profit / revenue) * 100
    expense_ratio = (expenses / revenue) * 100
    debt_to_revenue = (debt / revenue) * 100 if revenue > 0 else 0
    current_ratio = (cash + receivables) / (debt if debt > 0 else 1)

    audit_items = [q1, q2, q3, q4, q5]
    audit_score = (sum(audit_items) / 5) * 100

    g_items = [esg1, esg2]; s_items = [esg3, esg4]; e_items = [esg5, esg6]
    g_raw = (sum(g_items) / 2) * 100; s_raw = (sum(s_items) / 2) * 100; e_raw = (sum(e_items) / 2) * 100
    g_weighted = min((g_raw * 0.5) + (audit_score * 0.3) + (20 if q2 else 0) + (10 if q1 else 0), 100)
    esg_score = round((g_weighted * 0.4) + (s_raw * 0.3) + (e_raw * 0.3))

    rp = 0
    if is_uk:
        if profit_margin >= 20: rp += 0
        elif profit_margin >= 10: rp += 15
        else: rp += 30
    else:
        if profit_margin >= 15: rp += 0
        elif profit_margin >= 8: rp += 15
        else: rp += 30
    if current_ratio >= 2: rp += 0
    elif current_ratio >= 1: rp += 15
    else: rp += 30
    if debt_to_revenue <= 30: rp += 0
    elif debt_to_revenue <= 60: rp += 20
    else: rp += 40

    financial_score = max(0, 100 - rp)
    combined_score = round((financial_score * 0.6) + (esg_score * 0.4))

    def fin_st(s): return ("Low risk","s-green") if s>=70 else ("Moderate","s-amber") if s>=45 else ("High risk","s-red")
    def aud_st(s): return ("Prepared","s-green") if s>=80 else ("Partial","s-amber") if s>=50 else ("Not ready","s-red")
    def esg_st(s): return ("Strong","s-green") if s>=70 else ("Developing","s-amber") if s>=40 else ("Needs work","s-red")
    def comb_col(s): return ("#4ade80" if dk else GR_T) if s>=70 else ("#fbbf24" if dk else AM_T) if s>=50 else RED
    def comb_lbl(s): return "Strong position" if s>=70 else "Developing" if s>=50 else "Needs attention"

    fs_lbl, fs_cls = fin_st(financial_score)
    as_lbl, as_cls = aud_st(audit_score)
    es_lbl, es_cls = esg_st(esg_score)

    # Flags
    flags = []
    if profit_margin < 0:
        flags.append(("crit", "Operating at a loss — expenses exceed revenue."))
    if expense_ratio > 85:
        flags.append(("warn", f"Expense ratio {expense_ratio:.1f}% — above the 85% threshold. This may indicate limited buffer against cost or revenue changes. (Based on HMRC Business Population Estimates)"))
    if cash < (fixed_costs * 2):
        flags.append(("warn", f"Cash below 2 months of fixed costs ({currency}{fixed_costs*2:,.0f}). Consider building reserves before new commitments. (Bank of England SME resilience guidance)"))
    if debt_to_revenue > 60:
        flags.append(("crit", f"Debt-to-revenue {debt_to_revenue:.1f}% — above the 60% elevated-risk threshold. (Based on World Bank MSME Finance Gap Report)"))
    if current_ratio < 1:
        flags.append(("crit", f"Current ratio {current_ratio:.2f} — below 1.0. This may indicate difficulty meeting short-term obligations from liquid assets. This is a going concern indicator under ISA 570."))
    if is_uk and revenue > 85000 and not q3:
        flags.append(("crit", "Revenue may be above the VAT registration threshold (£85,000). Source: Value Added Tax Act 1994, Section 67."))
    if not is_uk and revenue > 2000000 and not q3:
        flags.append(("crit", "Revenue may be above the GST registration threshold (₹20 Lakhs). Source: CGST Act 2017, Section 22."))

    # Financial actions
    actions = []
    if profit_margin < 0:
        actions.append(f"Your business is currently operating at a loss ({currency}{abs(profit):,.0f}/year). Consider reviewing your three largest cost categories and assessing whether each is generating proportional value. Returning to break-even may require reducing costs or growing revenue by this amount.")
    if expense_ratio > 85:
        actions.append(f"An expense ratio of {expense_ratio:.1f}% leaves limited buffer. A 5-point reduction on your current revenue of {currency}{revenue:,.0f} could add approximately {currency}{revenue*0.05:,.0f} to annual profit. Consider which costs are discretionary and which are essential.")
    if cash < fixed_costs * 2:
        actions.append(f"Building cash reserves toward {currency}{fixed_costs*2:,.0f} (2 months of fixed costs) may reduce vulnerability to revenue interruption. Your {currency}{receivables:,.0f} in outstanding receivables is worth prioritising for collection.")
    if debt_to_revenue > 60:
        actions.append(f"At {debt_to_revenue:.1f}% debt-to-revenue, taking on additional borrowing may increase financial vulnerability. Consider whether existing debt can be reduced before any new financial commitments.")
    if audit_score < 60:
        actions.append("Several compliance checklist items are unconfirmed. These are typically the first areas reviewed in any loan application, regulatory enquiry, or formal business assessment. Addressing each item systematically reduces exposure.")
    if current_ratio < 1:
        actions.append(f"Your current ratio of {current_ratio:.2f} suggests short-term liquidity may be tight. Collecting outstanding receivables ({currency}{receivables:,.0f}) could meaningfully improve this position.")
    if not actions:
        actions.append("Your financial position is broadly stable. Running this diagnostic quarterly and tracking your Combined Smit Score over time may help you identify trends early.")

    # ESG actions — meaningful and specific
    esg_actions = []

    if not esg1:
        esg_actions.append({
            "pillar": "G — Governance",
            "action": "Schedule a recurring 30-minute monthly financial review",
            "detail": f"Block the last Friday of each month. Review three things: revenue vs last month, whether your expense ratio is trending up or down, and your cash vs fixed cost ratio. At your revenue of {currency}{revenue:,.0f}/year, catching a 5% expense drift early could protect {currency}{revenue*0.05:,.0f} in annual profit. This is the single most impactful governance action you can take — and it costs nothing.",
            "impact": "+15 pts Governance",
            "cost": "Zero cost — 30 min/month"
        })

    if expense_ratio > 75:
        saving = expenses * 0.05
        if is_uk:
            esg_actions.append({
                "pillar": "E — Environmental + Cost",
                "action": "Audit your supplier costs for greener, cheaper alternatives",
                "detail": f"With annual expenses of {currency}{expenses:,.0f}, even replacing 10% of costs with verified sustainable alternatives may reduce spend by {currency}{saving:,.0f}/year. Start with energy (switching to a renewable tariff typically saves £200–800/year for small businesses) and your most-used consumables. This also qualifies you for UK DBT Green Business support. Source: UK DBT SME ESG Guidance 2023.",
                "impact": "+12 pts Environmental",
                "cost": f"Potential saving: ~{currency}{saving:,.0f}/year"
            })
        else:
            esg_actions.append({
                "pillar": "E — Environmental + Cost",
                "action": "Track energy and operational costs monthly to identify savings",
                "detail": f"Create a simple monthly log of electricity, fuel, and material costs. At your expense base of {currency}{expenses:,.0f}/year, identifying and reducing 5% of operational costs could save {currency}{saving:,.0f}/year. This also creates the baseline required for SEBI BRSR Lite Principle 6 compliance. Source: SEBI BRSR Lite Framework.",
                "impact": "+12 pts Environmental",
                "cost": f"Zero cost — potential saving {currency}{saving:,.0f}/year"
            })

    if not esg3:
        esg_actions.append({
            "pillar": "S — Social",
            "action": "Introduce a one-page standard client agreement",
            "detail": f"A written agreement for every client engagement protects your payment rights under {'the Late Payment of Commercial Debts Act 1998' if is_uk else 'the MSME Development Act 2006'}. It also signals governance quality to banks and larger clients who increasingly assess suppliers. Free templates are available from {'gov.uk' if is_uk else 'msme.gov.in'}. This takes a few hours to set up and protects every future engagement.",
            "impact": "+10 pts Social",
            "cost": "Zero cost"
        })

    if not esg2:
        esg_actions.append({
            "pillar": "G — Governance",
            "action": "Create a one-page compliance calendar for your business",
            "detail": f"List your key obligations and their dates — {'self-assessment deadline (31 Jan), VAT quarters, Companies House confirmation statement' if is_uk else 'GST quarterly deadlines, ROC annual filing, TDS deposit dates'}. Add them to your calendar. Knowing what is due and when is the governance foundation referenced by UK DBT SME ESG Guidance 2023 and SEBI BRSR Lite Principle 1. Takes one afternoon to create; reduces risk of late filing penalties indefinitely.",
            "impact": "+10 pts Governance",
            "cost": "Zero cost — one-time setup"
        })

    if not esg5 and not esg6:
        esg_actions.append({
            "pillar": "E — Environmental",
            "action": "Start a simple monthly energy and travel log",
            "detail": f"Track electricity bills, business travel, and any material waste in a spreadsheet — 10 minutes a month. This creates the environmental baseline required by {'UK DBT SME ESG Guidance 2023' if is_uk else 'SEBI BRSR Lite Principle 6'}. Businesses that start tracking typically find 8–15% in operational cost reductions within 12 months by identifying what they hadn't noticed before.",
            "impact": "+8 pts Environmental",
            "cost": "Zero cost — 10 min/month"
        })

    if not esg_actions:
        esg_actions.append({
            "pillar": "All pillars",
            "action": "Document your existing ESG practices in a one-page statement",
            "detail": "Your governance indicators are already strong. The next step is writing down what you already do — a one-page ESG statement you can share with banks, clients, and supply chain partners. Large corporate clients increasingly request this from SME suppliers, and having it prepared positions you ahead of the requirement. Takes 2–3 hours to write; strengthens every commercial relationship going forward.",
            "impact": "Consolidates and signals existing position",
            "cost": "Zero cost — one-time"
        })

    # ESG indicators list
    esg_items = [
        ("Monthly/quarterly financial review (G)", esg1),
        ("Compliance awareness (G)", esg2),
        ("Written client contracts (S)", esg3),
        ("Fair practices with clients and suppliers (S)", esg4),
        ("Environmental impact awareness (E)", esg5),
        ("Active environmental reduction steps (E)", esg6),
        ("Dedicated business bank account (G)", q2),
        ("Consistent record keeping (G)", q1),
    ]

    # Summary
    if financial_score >= 70:
        summary = f"Broadly stable financial position — financial risk score {financial_score:.0f}/100, Combined Smit Score {combined_score}/100. Profitability and liquidity are within acceptable ranges. ESG governance at {esg_score:.0f}% — {'addressing the gaps in the upgrade plan below may strengthen your position with lenders and clients.' if esg_score < 70 else 'governance foundations are solid.'}"
    elif financial_score >= 45:
        weak = "cash reserves" if cash < fixed_costs * 2 else "leverage" if debt_to_revenue > 60 else "profit margins"
        summary = f"Moderate financial risk — score {financial_score:.0f}/100, Combined Smit Score {combined_score}/100. The primary area for attention is your {weak}. ESG governance at {esg_score:.0f}% — improving governance practices may also strengthen your access to credit and contracts."
    else:
        summary = f"Financial risk signals across multiple areas — score {financial_score:.0f}/100, Combined Smit Score {combined_score}/100. The priority actions and ESG upgrade plan below include zero-cost steps that may simultaneously improve financial resilience and sustainability position."

    st.session_state.results_ready = True
    st.session_state.financial_data = {
        "revenue": revenue, "expenses": expenses, "cash": cash,
        "debt": debt, "fixed_costs": fixed_costs, "receivables": receivables,
        "profit": profit, "profit_margin": profit_margin,
        "expense_ratio": expense_ratio, "debt_to_revenue": debt_to_revenue,
        "current_ratio": current_ratio, "financial_score": financial_score,
        "audit_score": audit_score, "esg_score": esg_score,
        "combined_score": combined_score,
        "comb_col": comb_col(combined_score), "comb_lbl": comb_lbl(combined_score),
        "flags": flags, "actions": actions,
        "esg_items": esg_items, "esg_actions": esg_actions,
        "g_score": g_weighted, "s_score": s_raw, "e_score": e_raw,
        "summary": summary, "currency": currency, "is_uk": is_uk,
        "fs_lbl": fs_lbl, "fs_cls": fs_cls,
        "as_lbl": as_lbl, "as_cls": as_cls,
        "es_lbl": es_lbl, "es_cls": es_cls,
        "q1":q1,"q2":q2,"q3":q3,"q4":q4,"q5":q5,
        "esg1":esg1,"esg2":esg2,"esg3":esg3,"esg4":esg4,"esg5":esg5,"esg6":esg6,
    }
    st.rerun()

# ── RESULTS ───────────────────────────────────────────────────
if st.session_state.results_ready:
    d = st.session_state.financial_data

    st.markdown('<div class="rule-heavy"></div>', unsafe_allow_html=True)
    st.markdown('<div class="kicker">Your Smit diagnostic</div>', unsafe_allow_html=True)

    # Combined score
    st.markdown(f"""
    <div class="score-hero">
        <div class="sh-lbl">Combined Smit Score — Financial + ESG</div>
        <div class="sh-num" style="color:{d['comb_col']}">{d['combined_score']}</div>
        <div class="sh-status" style="color:{d['comb_col']}">{d['comb_lbl']}</div>
        <div class="sh-sub">60% financial · 40% ESG</div>
        <div class="sh-breakdown">
            <div class="sh-b"><div class="sh-b-v" style="color:{'#4ade80' if d['financial_score']>=70 else '#fbbf24' if d['financial_score']>=45 else '#f87171'}">{d['financial_score']:.0f}</div><div class="sh-b-l">Financial risk</div></div>
            <div class="sh-b"><div class="sh-b-v" style="color:{'#4ade80' if d['audit_score']>=80 else '#fbbf24' if d['audit_score']>=50 else '#f87171'}">{d['audit_score']:.0f}%</div><div class="sh-b-l">Compliance</div></div>
            <div class="sh-b"><div class="sh-b-v" style="color:{'#4ade80' if d['esg_score']>=70 else '#fbbf24' if d['esg_score']>=40 else '#f87171'}">{d['esg_score']:.0f}%</div><div class="sh-b-l">ESG</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Three scores
    st.markdown(f"""
    <div class="score-row">
        <div class="score-cell">
            <div class="score-cell-lbl">Financial risk</div>
            <div class="score-cell-num" style="color:{GR_T if d['financial_score']>=70 else AM_T if d['financial_score']>=45 else RD_T}">{d['financial_score']:.0f}<span style="font-size:1.1rem;color:{TEXT2};font-weight:400">/100</span></div>
            <span class="score-cell-status {d['fs_cls']}">{d['fs_lbl']}</span>
        </div>
        <div class="score-cell">
            <div class="score-cell-lbl">Compliance readiness</div>
            <div class="score-cell-num" style="color:{GR_T if d['audit_score']>=80 else AM_T if d['audit_score']>=50 else RD_T}">{d['audit_score']:.0f}<span style="font-size:1.1rem;color:{TEXT2};font-weight:400">%</span></div>
            <span class="score-cell-status {d['as_cls']}">{d['as_lbl']}</span>
        </div>
        <div class="score-cell">
            <div class="score-cell-lbl">ESG governance</div>
            <div class="score-cell-num" style="color:{GR_T if d['esg_score']>=70 else AM_T if d['esg_score']>=40 else RD_T}">{d['esg_score']:.0f}<span style="font-size:1.1rem;color:{TEXT2};font-weight:400">%</span></div>
            <span class="score-cell-status {d['es_cls']}">{d['es_lbl']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Score summary table — full breakdown at a glance
    st.markdown(f'<div class="kicker" style="margin-top:1.5rem">Full score breakdown</div>', unsafe_allow_html=True)

    def score_colour(val, t1, t2):
        return GR_T if val >= t1 else AM_T if val >= t2 else RD_T
    def score_bg(val, t1, t2):
        return GR_BG if val >= t1 else AM_BG if val >= t2 else RD_BG
    def score_lbl_map(val, t1, t2, labels):
        return labels[0] if val >= t1 else labels[1] if val >= t2 else labels[2]

    table_rows = f"""
    <tr style="border-bottom:2px solid {TEXT}">
        <td style="font-size:0.88rem;font-weight:700;color:{TEXT};padding:0.7rem 0.75rem">Combined Smit Score</td>
        <td style="padding:0.7rem 0.75rem"><span style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:{d['comb_col']}">{d['combined_score']}/100</span></td>
        <td style="padding:0.7rem 0.75rem"><span class="sst-badge" style="color:{d['comb_col']};background:{'rgba(214,230,242,0.15)' if dk else '#EEF4FA'}">{d['comb_lbl']}</span></td>
    </tr>
    <tr>
        <td style="font-size:0.85rem;color:{TEXT};padding:0.65rem 0.75rem;padding-left:1.5rem">Financial risk score</td>
        <td style="padding:0.65rem 0.75rem"><span style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:{score_colour(d['financial_score'],70,45)}">{d['financial_score']:.0f}/100</span></td>
        <td style="padding:0.65rem 0.75rem"><span class="sst-badge" style="color:{score_colour(d['financial_score'],70,45)};background:{score_bg(d['financial_score'],70,45)}">{score_lbl_map(d['financial_score'],70,45,['Low risk','Moderate','High risk'])}</span></td>
    </tr>
    <tr>
        <td style="font-size:0.85rem;color:{TEXT};padding:0.65rem 0.75rem;padding-left:1.5rem">Compliance readiness</td>
        <td style="padding:0.65rem 0.75rem"><span style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:{score_colour(d['audit_score'],80,50)}">{d['audit_score']:.0f}%</span></td>
        <td style="padding:0.65rem 0.75rem"><span class="sst-badge" style="color:{score_colour(d['audit_score'],80,50)};background:{score_bg(d['audit_score'],80,50)}">{score_lbl_map(d['audit_score'],80,50,['Prepared','Partial','Not ready'])}</span></td>
    </tr>
    <tr style="border-bottom:2px solid {TEXT}">
        <td style="font-size:0.85rem;color:{TEXT};padding:0.65rem 0.75rem;padding-left:1.5rem">ESG governance (overall)</td>
        <td style="padding:0.65rem 0.75rem"><span style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:{score_colour(d['esg_score'],70,40)}">{d['esg_score']:.0f}%</span></td>
        <td style="padding:0.65rem 0.75rem"><span class="sst-badge" style="color:{score_colour(d['esg_score'],70,40)};background:{score_bg(d['esg_score'],70,40)}">{score_lbl_map(d['esg_score'],70,40,['Strong','Developing','Needs work'])}</span></td>
    </tr>
    <tr>
        <td style="font-size:0.82rem;color:{TEXT2};padding:0.6rem 0.75rem;padding-left:2.5rem;font-style:italic">G — Governance pillar</td>
        <td style="padding:0.6rem 0.75rem;font-size:0.85rem;color:{score_colour(d['g_score'],70,40)}">{d['g_score']:.0f}%</td>
        <td style="padding:0.6rem 0.75rem;font-size:0.8rem;color:{score_colour(d['g_score'],70,40)}">{score_lbl_map(d['g_score'],70,40,['Strong','Developing','Weak'])}</td>
    </tr>
    <tr>
        <td style="font-size:0.82rem;color:{TEXT2};padding:0.6rem 0.75rem;padding-left:2.5rem;font-style:italic">S — Social pillar</td>
        <td style="padding:0.6rem 0.75rem;font-size:0.85rem;color:{score_colour(d['s_score'],70,40)}">{d['s_score']:.0f}%</td>
        <td style="padding:0.6rem 0.75rem;font-size:0.8rem;color:{score_colour(d['s_score'],70,40)}">{score_lbl_map(d['s_score'],70,40,['Strong','Developing','Weak'])}</td>
    </tr>
    <tr>
        <td style="font-size:0.82rem;color:{TEXT2};padding:0.6rem 0.75rem;padding-left:2.5rem;font-style:italic">E — Environmental pillar</td>
        <td style="padding:0.6rem 0.75rem;font-size:0.85rem;color:{score_colour(d['e_score'],70,40)}">{d['e_score']:.0f}%</td>
        <td style="padding:0.6rem 0.75rem;font-size:0.8rem;color:{score_colour(d['e_score'],70,40)}">{score_lbl_map(d['e_score'],70,40,['Strong','Developing','Weak'])}</td>
    </tr>
    """

    st.markdown(f"""
    <table class="score-summary-table">
        <thead><tr>
            <th>Category</th>
            <th>Score</th>
            <th>Status</th>
        </tr></thead>
        <tbody>{table_rows}</tbody>
    </table>
    """, unsafe_allow_html=True)

    # Ratios
    st.markdown(f'<div class="kicker" style="margin-top:1.5rem">Key financial ratios</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.72rem;color:{TEXT2};margin-bottom:0.75rem">Benchmarked against HMRC (UK) · RBI (India) · Bank of England · World Bank data</p>', unsafe_allow_html=True)

    def rc(m,v,uk):
        if m=="margin": t,w=(20,10) if uk else (15,8); return "r-good" if v>=t else "r-warn" if v>=w else "r-bad"
        if m=="expense": return "r-good" if v<80 else "r-warn" if v<85 else "r-bad"
        if m=="dtr": return "r-good" if v<=30 else "r-warn" if v<=60 else "r-bad"
        if m=="cr": return "r-good" if v>=2 else "r-warn" if v>=1 else "r-bad"

    mc=rc("margin",d['profit_margin'],d['is_uk']); ec=rc("expense",d['expense_ratio'],d['is_uk'])
    dc=rc("dtr",d['debt_to_revenue'],d['is_uk']); cc=rc("cr",d['current_ratio'],d['is_uk'])
    def st_(c): return "Healthy" if c=="r-good" else "Watch" if c=="r-warn" else "At risk"
    bm = "≥20% (HMRC)" if d['is_uk'] else "≥15% (RBI)"

    st.markdown(f"""
    <table class="ratio-table">
        <thead><tr><th>Ratio</th><th>What it measures</th><th>Your figure</th><th>Benchmark</th><th>Status</th></tr></thead>
        <tbody>
        <tr>
            <td><strong style="color:{TEXT}">Net profit margin</strong><span class="r-explain">Revenue minus costs, as % of revenue. How much remains from each {d['currency']} earned after all expenses.</span></td>
            <td style="font-size:0.72rem;color:{TEXT2}">Profitability</td>
            <td class="r-val {mc}">{d['profit_margin']:.1f}%</td>
            <td style="font-size:0.72rem;color:{TEXT2}">{bm}</td>
            <td class="{mc}" style="font-size:0.8rem">{st_(mc)}</td>
        </tr>
        <tr>
            <td><strong style="color:{TEXT}">Expense ratio</strong><span class="r-explain">Total expenses as % of revenue. Higher values may indicate limited resilience to cost or revenue changes.</span></td>
            <td style="font-size:0.72rem;color:{TEXT2}">Cost efficiency</td>
            <td class="r-val {ec}">{d['expense_ratio']:.1f}%</td>
            <td style="font-family:'DM Mono',monospace;font-size:0.68rem;color:{TEXT2}">Below 80% (HMRC)</td>
            <td class="{ec}" style="font-family:'DM Mono',monospace;font-size:0.72rem">{st_(ec)}</td>
        </tr>
        <tr>
            <td><strong style="color:{TEXT}">Debt-to-revenue</strong><span class="r-explain">Total debt as % of annual revenue. Above 60% may indicate significant income committed to debt obligations before operating costs.</span></td>
            <td style="font-size:0.72rem;color:{TEXT2}">Leverage</td>
            <td class="r-val {dc}">{d['debt_to_revenue']:.1f}%</td>
            <td style="font-family:'DM Mono',monospace;font-size:0.68rem;color:{TEXT2}">Below 30% (World Bank)</td>
            <td class="{dc}" style="font-family:'DM Mono',monospace;font-size:0.72rem">{'Low risk' if dc=='r-good' else 'Moderate' if dc=='r-warn' else 'Elevated risk'}</td>
        </tr>
        <tr>
            <td><strong style="color:{TEXT}">Current ratio</strong><span class="r-explain">(Cash + receivables) ÷ debt. Below 1.0 may indicate difficulty meeting short-term obligations from liquid assets — a going concern indicator under ISA 570.</span></td>
            <td style="font-size:0.72rem;color:{TEXT2}">Liquidity</td>
            <td class="r-val {cc}">{d['current_ratio']:.2f}</td>
            <td style="font-family:'DM Mono',monospace;font-size:0.68rem;color:{TEXT2}">Above 2.0 (Bank of England)</td>
            <td class="{cc}" style="font-family:'DM Mono',monospace;font-size:0.72rem">{st_(cc)}</td>
        </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # Flags
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="kicker">Compliance flags</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.75rem;color:{TEXT2};margin-bottom:0.75rem">Issues a regulatory review, loan assessment, or formal audit may identify. Each flag references the relevant source.</p>', unsafe_allow_html=True)
    if d['flags']:
        for sev, msg in d['flags']:
            css = "flag-crit" if sev=="crit" else "flag-warn"
            st.markdown(f'<div class="flag {css}">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="flag flag-ok">No compliance flags detected based on the information provided.</div>', unsafe_allow_html=True)

    # Actions
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="kicker">Priority actions</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.75rem;color:{TEXT2};margin-bottom:0.75rem">Based on your specific figures — in priority order.</p>', unsafe_allow_html=True)
    for i, action in enumerate(d['actions'][:3], 1):
        st.markdown(f'<div class="action-item"><div class="action-num">{i}.</div><div style="color:{TEXT}">{action}</div></div>', unsafe_allow_html=True)

    # ESG plan
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown('<div class="kicker">ESG upgrade plan</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.75rem;color:{TEXT2};margin-bottom:0.75rem">Zero or low-cost actions calculated from your numbers. Financial saving estimate included where applicable.</p>', unsafe_allow_html=True)
    for item in d['esg_actions'][:4]:
        st.markdown(f"""
        <div class="esg-plan">
            <div class="esg-plan-header">
                <span>{item['pillar']}</span>
                <span>{item['impact']} &nbsp;·&nbsp; {item['cost']}</span>
            </div>
            <div class="esg-plan-body">
                <strong>{item['action']}</strong><br>
                {item['detail']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ESG indicators
    st.markdown(f'<div class="kicker" style="margin-top:1rem">ESG indicators</div>', unsafe_allow_html=True)
    html = ""
    for item, passed in d['esg_items']:
        css = "esg-pass" if passed else "esg-fail"
        icon = "✓" if passed else "○"
        html += f'<div class="esg-item {css}"><strong>{icon}</strong>&nbsp; {item}</div>'
    st.markdown(f'<div class="esg-grid">{html}</div>', unsafe_allow_html=True)

    # Summary
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="summary">
        <div class="summary-kicker">Overall assessment</div>
        {d['summary']}
    </div>
    """, unsafe_allow_html=True)

    # Stress test
    st.markdown(f'<div class="kicker" style="margin-top:1.5rem">Stress test — what if revenue declines?</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-family:\'DM Mono\',monospace;font-size:0.62rem;color:{TEXT2};margin-bottom:0.75rem">Expenses held constant — the conservative assumption in Bank of England SME stress testing.</p>', unsafe_allow_html=True)

    drop = st.slider("Revenue declines by:", 0, 50, 20, format="%d%%")
    nr = d['revenue'] * (1 - drop/100)
    np_ = nr - d['expenses']
    nm = (np_/nr*100) if nr > 0 else 0
    buf = d['expenses'] * 0.05

    st.markdown(f"""
    <div class="stress-row">
        <div class="stress-cell">
            <div class="stress-cell-l">Revenue after decline</div>
            <div class="stress-cell-v">{d['currency']}{nr:,.0f}</div>
            <div class="stress-cell-d d-neg">−{drop}%</div>
        </div>
        <div class="stress-cell">
            <div class="stress-cell-l">Profit / loss</div>
            <div class="stress-cell-v" style="color:{'#1C5E30' if np_>=0 else RED}">{d['currency']}{np_:,.0f}</div>
            <div class="stress-cell-d {'d-pos' if np_>=0 else 'd-neg'}">{d['currency']}{np_-d['profit']:,.0f}</div>
        </div>
        <div class="stress-cell">
            <div class="stress-cell-l">New profit margin</div>
            <div class="stress-cell-v" style="color:{'#1C5E30' if nm>=10 else RED}">{nm:.1f}%</div>
            <div class="stress-cell-d d-neg">{nm-d['profit_margin']:+.1f}pp</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if np_ < 0:
        st.markdown(f'<div class="flag flag-crit">A {drop}% revenue decline may push your business into loss under this model. Reviewing your expense base could add {d["currency"]}{buf:,.0f}/year in buffer. ESG action: a supplier cost review may help reduce expenses while improving your ESG score.</div>', unsafe_allow_html=True)
    elif nm < 10:
        st.markdown(f'<div class="flag flag-warn">Margin compresses to {nm:.1f}% under this scenario — limited buffer for unexpected costs. A monthly financial review (zero cost) may provide earlier warning of revenue pressure.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="flag flag-ok">Business appears profitable under a {drop}% revenue decline in this model. Margin holds at {nm:.1f}%.</div>', unsafe_allow_html=True)

    # AI — Pro gate or active
    st.markdown('<div class="rule-heavy" style="margin-top:2rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="kicker">Smit AI assistant</div>', unsafe_allow_html=True)

    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        has_api = bool(api_key)
    except Exception:
        has_api = False

    if not has_api:
        st.markdown(f"""
        <div class="pro-gate">
            <div class="pro-gate-lbl">Pro feature</div>
            <p><strong>Smit AI — constrained to your data and official benchmarks.</strong></p>
            <p>Ask any question about your specific numbers. Every answer references your inputs and the relevant benchmark source, and ends with the required legal disclaimer. Not general financial advice — specific to your figures.</p>
            <p style="font-family:'DM Mono',monospace;font-size:0.65rem;opacity:0.4">Pro access at getsmit.co</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-wrap">
            <div class="chat-header">
                <span>Smit AI</span>
                <span class="chat-badge">Pro · Constrained to your data + official benchmarks</span>
            </div>
        </div>
        <p style="font-family:'DM Mono',monospace;font-size:0.62rem;color:{TEXT2};margin:0.5rem 0 0.75rem;line-height:1.6">Every answer uses your 7 inputs and official benchmarks only. Not regulated financial advice — see disclaimer below.</p>
        """, unsafe_allow_html=True)

        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user"><div class="chat-lbl">You</div>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-assistant"><div class="chat-lbl">Smit AI</div>{msg["content"]}</div>', unsafe_allow_html=True)

        user_q = st.text_input("Ask Smit", placeholder="e.g. What does my current ratio mean for my business? Which ESG action is most cost-effective?", label_visibility="collapsed", key="chat_input")

        if st.button("Send →", key="send_chat"):
            if user_q.strip():
                d = st.session_state.financial_data
                cur = d['currency']

                system_prompt = f"""You are Smit AI — the financial and ESG assistant built into the Smit platform.

STRICT CONSTRAINTS: You ONLY use the user's 7 financial inputs, checklist answers, region, and the official Smit methodology v2.0 benchmarks below. Do not use outside knowledge or general financial advice.

USER'S 7 INPUTS:
1. Annual revenue: {cur}{d['revenue']:,.0f}
2. Annual expenses: {cur}{d['expenses']:,.0f}
3. Cash in bank: {cur}{d['cash']:,.0f}
4. Total debt: {cur}{d['debt']:,.0f}
5. Monthly fixed costs: {cur}{d['fixed_costs']:,.0f}
6. Receivables: {cur}{d['receivables']:,.0f}
7. Region: {'United Kingdom' if d['is_uk'] else 'India'} | Business: {st.session_state.user_info.get('biz_type','SME')}

CALCULATED:
- Profit margin: {d['profit_margin']:.1f}% | Expense ratio: {d['expense_ratio']:.1f}%
- Debt-to-revenue: {d['debt_to_revenue']:.1f}% | Current ratio: {d['current_ratio']:.2f}
- Financial score: {d['financial_score']:.0f}/100 | Audit readiness: {d['audit_score']:.0f}%
- ESG score: {d['esg_score']:.0f}% | Combined Smit Score: {d['combined_score']}/100
- G: {d['g_score']:.0f}% | S: {d['s_score']:.0f}% | E: {d['e_score']:.0f}%

CHECKLIST: Receipts: {'Y' if d['q1'] else 'N'} | Business bank: {'Y' if d['q2'] else 'N'} | VAT/GST known: {'Y' if d['q3'] else 'N'} | Files on time: {'Y' if d['q4'] else 'N'} | Records available: {'Y' if d['q5'] else 'N'} | Monthly review: {'Y' if d['esg1'] else 'N'} | Compliance aware: {'Y' if d['esg2'] else 'N'} | Written contracts: {'Y' if d['esg3'] else 'N'} | Fair practices: {'Y' if d['esg4'] else 'N'} | Env. awareness: {'Y' if d['esg5'] else 'N'} | Active env. steps: {'Y' if d['esg6'] else 'N'}

OFFICIAL BENCHMARKS (always cite source):
UK margin ≥20% — HMRC Business Population Estimates
India margin ≥15% — RBI Annual Report MSME Lending
Expense ratio warning >85% — HMRC benchmarks
Current ratio ≥2.0; <1.0 going concern indicator — Bank of England SME criteria; ISA 570
Debt-to-revenue <30% low risk; >60% elevated risk — World Bank MSME Finance Gap Report
Cash buffer ≥2 months fixed costs — Bank of England SME resilience guidance
UK VAT threshold £85,000 — Value Added Tax Act 1994
India GST threshold ₹20L services — CGST Act 2017
ESG: UK DBT SME ESG Guidance 2023 · SEBI BRSR Lite · ISO 26000
Combined score: Financial 60%, ESG 40%

RULES (non-negotiable):
1. Every answer MUST reference the user's actual numbers and the specific benchmark with source.
2. ESG suggestions must be zero or low-cost, tied to their numbers, with estimated impact where calculable.
3. Use neutral language — "this may indicate", "consider", "based on" — not directive commands.
4. Do NOT imply endorsement by HMRC, RBI, or any regulatory body. Use "benchmarked against" or "based on data from".
5. End EVERY response with exactly: "/ Not regulated financial, tax or legal advice. For decisions affecting your tax or legal position, consult a qualified professional."
6. If a question cannot be answered from these inputs and benchmarks, reply: "I can only answer based on the figures and benchmarks provided. Please clarify."
7. Maximum 250 words. Plain English. One concrete next step."""

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
                    st.session_state.chat_messages.append({"role": "assistant", "content": resp.content[0].text})
                except Exception:
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": "Connection issue — please try again.\n\n/ Not regulated financial, tax or legal advice. For decisions affecting your tax or legal position, consult a qualified professional."
                    })
                st.rerun()

    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.button("Download full report (PDF) — Pro feature · Coming soon", disabled=True)

    st.markdown(f"""
    <div class="legal-disclaimer">
        <strong style="color:{TEXT}">Not regulated financial, tax, investment, or legal advice.</strong>
        Smit is a financial intelligence and ESG diagnostic tool. It calculates and interprets your data
        using published benchmarks from HMRC, Companies House, Bank of England, Reserve Bank of India,
        Ministry of MSME India, World Bank MSME Finance Gap Report, UK DBT SME ESG Guidance 2023,
        SEBI BRSR Lite Framework, ISO 26000, and ISA 570. Smit is not endorsed by any of these bodies.
        Benchmarks are indicative — your specific circumstances, sector, and business model may differ.
        For decisions affecting your tax position, compliance obligations, or legal standing,
        consult a qualified professional (CA, accountant, or solicitor).<br><br>
        <strong style="color:{TEXT}">Privacy:</strong> Financial data is processed in-session only and not stored on our servers.
        Your signup details are held with consent for product communications.
        UK GDPR and India DPDP Act 2023. Deletion: hello@getsmit.co
    </div>
    """, unsafe_allow_html=True)
