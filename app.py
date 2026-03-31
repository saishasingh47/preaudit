import streamlit as st
import anthropic
import json

st.set_page_config(
    page_title="Smit — Financial Intelligence for Independent Businesses",
    page_icon="📊",
    layout="centered"
)

# --- DESIGN SYSTEM ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #FAFAF8;
    color: #1a1a1a;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Typography */
h1, h2, h3 { font-family: 'Playfair Display', serif; color: #1a1a1a; }

/* Main container */
.block-container { padding: 2rem 1.5rem; max-width: 780px; }

/* Masthead */
.masthead {
    border-bottom: 3px solid #1a1a1a;
    padding-bottom: 1rem;
    margin-bottom: 0.5rem;
}
.masthead-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.25rem;
}
.masthead-name {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #1a1a1a;
    letter-spacing: -1px;
    line-height: 1;
}
.masthead-tagline {
    font-size: 0.8rem;
    color: #6b6b6b;
    font-style: italic;
    letter-spacing: 0.5px;
}
.masthead-sub {
    font-size: 0.75rem;
    color: #6b6b6b;
    border-top: 1px solid #d4d4d4;
    padding-top: 0.4rem;
    margin-top: 0.4rem;
    letter-spacing: 0.3px;
}

/* Thin rule */
.rule { height: 1px; background: #d4d4d4; margin: 1.5rem 0; }
.rule-thick { height: 2px; background: #1a1a1a; margin: 2rem 0; }

/* Section label — like FT section headers */
.section-kicker {
    font-size: 0.7rem;
    font-weight: 600;
    color: #8B1A1A;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.25rem;
}

/* Score cards — Bloomberg terminal aesthetic */
.score-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: #d4d4d4;
    border: 1px solid #d4d4d4;
    margin: 1rem 0;
}
.score-cell {
    background: #FAFAF8;
    padding: 1.25rem 1rem;
    text-align: center;
}
.score-cell-label {
    font-size: 0.65rem;
    font-weight: 600;
    color: #6b6b6b;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.5rem;
}
.score-cell-number {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.score-cell-status {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    padding: 0.2rem 0.6rem;
    display: inline-block;
}
.status-green { color: #1a5c2e; background: #e8f5ee; }
.status-amber { color: #7a4a0a; background: #fdf3e3; }
.status-red { color: #8B1A1A; background: #fdecea; }

/* Ratio table */
.ratio-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    margin: 1rem 0;
}
.ratio-table th {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #6b6b6b;
    padding: 0.5rem 0.75rem;
    border-bottom: 2px solid #1a1a1a;
    text-align: left;
}
.ratio-table td {
    padding: 0.7rem 0.75rem;
    border-bottom: 1px solid #e8e8e4;
    color: #1a1a1a;
    vertical-align: middle;
}
.ratio-table tr:hover td { background: #f5f5f0; }
.ratio-val { font-weight: 600; font-size: 1rem; }
.ratio-good { color: #1a5c2e; }
.ratio-warn { color: #7a4a0a; }
.ratio-bad { color: #8B1A1A; }

/* Flag items */
.flag-item {
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
    border-left: 3px solid;
    font-size: 0.875rem;
    line-height: 1.5;
}
.flag-critical { border-color: #8B1A1A; background: #fdecea; color: #5a1010; }
.flag-warning { border-color: #C17A2A; background: #fdf3e3; color: #6b4010; }
.flag-ok { border-color: #1a5c2e; background: #e8f5ee; color: #1a5c2e; }

/* Action items */
.action-item {
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
    padding: 0.85rem 1rem;
    margin: 0.4rem 0;
    background: #f5f5f0;
    border: 1px solid #e8e8e4;
    font-size: 0.875rem;
    line-height: 1.5;
}
.action-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #8B1A1A;
    line-height: 1;
    flex-shrink: 0;
    min-width: 20px;
}

/* Summary box */
.summary-box {
    background: #1a1a1a;
    color: #FAFAF8;
    padding: 1.5rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    line-height: 1.7;
}
.summary-box .summary-kicker {
    font-size: 0.65rem;
    font-weight: 600;
    color: #C17A2A;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 0.5rem;
}

/* Chat */
.chat-container {
    border: 1px solid #d4d4d4;
    background: #ffffff;
    margin: 1rem 0;
}
.chat-header {
    background: #1a1a1a;
    color: #FAFAF8;
    padding: 0.75rem 1rem;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.chat-header-badge {
    font-size: 0.65rem;
    background: #8B1A1A;
    color: white;
    padding: 0.15rem 0.5rem;
    letter-spacing: 0.5px;
}
.chat-msg-user {
    background: #f5f5f0;
    border-left: 3px solid #1a1a1a;
    padding: 0.75rem 1rem;
    margin: 0.5rem;
    font-size: 0.875rem;
}
.chat-msg-assistant {
    background: #ffffff;
    border-left: 3px solid #8B1A1A;
    padding: 0.75rem 1rem;
    margin: 0.5rem;
    font-size: 0.875rem;
    line-height: 1.6;
}
.chat-msg-label {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.35rem;
}
.chat-msg-user .chat-msg-label { color: #1a1a1a; }
.chat-msg-assistant .chat-msg-label { color: #8B1A1A; }

/* Signup form */
.signup-box {
    background: #1a1a1a;
    padding: 2rem;
    margin: 2rem 0;
    color: #FAFAF8;
}
.signup-box h2 {
    color: #FAFAF8;
    font-size: 1.6rem;
    margin-bottom: 0.5rem;
}
.signup-box p {
    color: #a0a0a0;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
    line-height: 1.6;
}

/* Buttons */
.stButton > button {
    background: #1a1a1a !important;
    color: #FAFAF8 !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 0 !important;
    padding: 0.65rem 1.5rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #8B1A1A !important;
    border-color: #8B1A1A !important;
}
.stButton > button:disabled {
    background: #d4d4d4 !important;
    border-color: #d4d4d4 !important;
    color: #6b6b6b !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stSelectbox > div > div > div {
    border-radius: 0 !important;
    border: 1px solid #d4d4d4 !important;
    background: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #1a1a1a !important;
    box-shadow: none !important;
}
.stNumberInput > div > div > input {
    border-radius: 0 !important;
    border: 1px solid #d4d4d4 !important;
    background: #ffffff !important;
}
.stCheckbox > label { font-size: 0.875rem !important; }
.stRadio > label { font-size: 0.875rem !important; }

/* Step indicator */
.step-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}
.step-dot {
    width: 24px; height: 24px;
    background: #8B1A1A;
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.step-text {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #1a1a1a;
}

/* Stress test */
.stress-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: #d4d4d4;
    border: 1px solid #d4d4d4;
    margin: 1rem 0;
}
.stress-cell {
    background: #FAFAF8;
    padding: 1rem;
    text-align: center;
}
.stress-cell-label {
    font-size: 0.65rem;
    font-weight: 600;
    color: #6b6b6b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.4rem;
}
.stress-cell-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #1a1a1a;
}
.stress-cell-delta {
    font-size: 0.75rem;
    margin-top: 0.2rem;
}
.delta-neg { color: #8B1A1A; }
.delta-pos { color: #1a5c2e; }

/* ESG grid */
.esg-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.4rem;
    margin: 0.75rem 0;
}
.esg-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 0.75rem;
    background: #f5f5f0;
    border: 1px solid #e8e8e4;
    font-size: 0.8rem;
    color: #1a1a1a;
}
.esg-pass { border-left: 3px solid #1a5c2e; }
.esg-fail { border-left: 3px solid #8B1A1A; opacity: 0.6; }

/* Disclaimer */
.disclaimer {
    border-top: 1px solid #d4d4d4;
    padding-top: 1rem;
    margin-top: 2rem;
    font-size: 0.75rem;
    color: #6b6b6b;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ── MASTHEAD ──────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div class="masthead-top">
        <div class="masthead-name">Smit.</div>
        <div class="masthead-tagline">Financial intelligence for independent businesses</div>
    </div>
    <div class="masthead-sub">
        UK & India frameworks &nbsp;·&nbsp; HMRC, ICAEW, RBI & ICAI benchmarks &nbsp;·&nbsp; Built by Saisha Singh Dhankar · BSc Business Economics (UK) · ACCA in progress
    </div>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────
if 'signed_up' not in st.session_state:
    st.session_state.signed_up = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'results_ready' not in st.session_state:
    st.session_state.results_ready = False
if 'financial_data' not in st.session_state:
    st.session_state.financial_data = {}
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# ── SIGNUP GATE ───────────────────────────────────────────────
if not st.session_state.signed_up:
    st.markdown("""
    <div style="padding: 2rem 0 1rem;">
        <div class="section-kicker">Free access</div>
        <h1 style="font-size: 2.2rem; letter-spacing: -1px; margin-bottom: 0.75rem; line-height: 1.2;">
            Your business deserves a financial expert.<br>Now it has one.
        </h1>
        <p style="font-size: 1rem; color: #4a4a4a; max-width: 560px; line-height: 1.7; margin-bottom: 2rem;">
            Smit gives small businesses and freelancers the financial intelligence 
            that used to require a CA on retainer — on demand, in plain English, 
            grounded in real benchmarks.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full name", placeholder="Your name")
        email = st.text_input("Email address", placeholder="your@email.com")
    with col2:
        region = st.selectbox("Your region", ["", "🇬🇧 United Kingdom", "🇮🇳 India", "🌍 Other"])
        biz_type = st.selectbox("Business type", [
            "",
            "Freelancer / Sole trader",
            "Small business (1–10 people)",
            "Early-stage startup",
            "Limited company director",
            "Other"
        ])

    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)

    if st.button("Access Smit free — no credit card required"):
        if not name or not email or not region or not biz_type:
            st.error("Please fill in all fields to continue.")
        elif "@" not in email:
            st.error("Please enter a valid email address.")
        else:
            st.session_state.signed_up = True
            st.session_state.user_info = {
                "name": name,
                "email": email,
                "region": region,
                "biz_type": biz_type
            }
            st.rerun()

    st.markdown("""
    <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid #d4d4d4;">
        <p style="font-size: 0.78rem; color: #6b6b6b; line-height: 1.7;">
            No credit card. No spam. Your data is used only to personalise your diagnostic.<br>
            Smit is a financial intelligence tool — it does not provide regulated financial or tax advice.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ── SIGNED IN — SHOW TOOL ─────────────────────────────────────
user = st.session_state.user_info
region = user.get("region", "")
is_uk = "United Kingdom" in region

st.markdown(f"""
<div style="padding: 0.5rem 0 1rem;">
    <span style="font-size:0.78rem; color:#6b6b6b;">
        Welcome, {user.get('name', '')} &nbsp;·&nbsp; 
        {user.get('biz_type', '')} &nbsp;·&nbsp; 
        {region}
    </span>
</div>
""", unsafe_allow_html=True)

# ── STEP 1: INPUTS ────────────────────────────────────────────
st.markdown("""
<div class="rule-thick"></div>
<div class="step-indicator">
    <div class="step-dot">1</div>
    <div class="step-text">Your financial data</div>
</div>
<p style="font-size:0.85rem; color:#4a4a4a; margin-bottom:1.25rem;">
    Enter your most recent figures. These are the numbers any CA or bank would ask for first.
</p>
""", unsafe_allow_html=True)

currency = "£" if is_uk else "₹"
step = 1000.0 if is_uk else 10000.0

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Revenue & costs** _{currency}_")
    revenue = st.number_input(f"Annual revenue", min_value=0.0, step=step, key="rev")
    expenses = st.number_input(f"Annual expenses", min_value=0.0, step=step, key="exp")
    cash = st.number_input(f"Cash in bank", min_value=0.0, step=step/2, key="cash")
with col2:
    st.markdown(f"**Debt & obligations** _{currency}_")
    debt = st.number_input(f"Total debt / liabilities", min_value=0.0, step=step/2, key="debt")
    fixed_costs = st.number_input(f"Monthly fixed costs", min_value=0.0, step=100.0, key="fc")
    receivables = st.number_input(f"Money owed to you", min_value=0.0, step=100.0, key="rec")

# ── STEP 2: AUDIT CHECKLIST ───────────────────────────────────
st.markdown("""
<div class="rule"></div>
<div class="step-indicator">
    <div class="step-dot">2</div>
    <div class="step-text">Compliance checklist</div>
</div>
<p style="font-size:0.85rem; color:#4a4a4a; margin-bottom:1rem;">
    Answer honestly. These are the first five things a CA checks.
</p>
""", unsafe_allow_html=True)

if is_uk:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)")
    q2 = st.checkbox("I have a dedicated business bank account")
    q3 = st.checkbox("I know my VAT registration status and whether I'm above the £85,000 threshold")
    q4 = st.checkbox("I file self-assessment or company accounts on time every year")
    q5 = st.checkbox("I have financial records going back at least 2 years")
else:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)")
    q2 = st.checkbox("I have a dedicated business bank account")
    q3 = st.checkbox("I know my GST registration status and whether I'm above the ₹20 Lakh threshold")
    q4 = st.checkbox("I file GST returns quarterly and on time")
    q5 = st.checkbox("I maintain records a CA could review immediately")

# ── STEP 3: ESG ───────────────────────────────────────────────
st.markdown("""
<div class="rule"></div>
<div class="step-indicator">
    <div class="step-dot">3</div>
    <div class="step-text">Governance & ESG</div>
</div>
""", unsafe_allow_html=True)

esg1 = st.checkbox("I review my finances monthly or quarterly")
esg2 = st.checkbox("I have clear contracts or terms of service with clients")
esg3 = st.checkbox("I am aware of my key legal and compliance obligations")
esg4 = st.checkbox("I track or am aware of the environmental or social impact of my business")

# ── RUN ───────────────────────────────────────────────────────
st.markdown('<div class="rule"></div>', unsafe_allow_html=True)

if st.button("Run financial diagnostic →"):
    if revenue == 0:
        st.error("Please enter your annual revenue to continue.")
        st.stop()

    # ── CALCULATIONS ─────────────────────────────────────────
    profit = revenue - expenses
    profit_margin = (profit / revenue) * 100
    expense_ratio = (expenses / revenue) * 100
    debt_to_revenue = (debt / revenue) * 100 if revenue > 0 else 0
    current_ratio = (cash + receivables) / (debt if debt > 0 else 1)

    checklist = [q1, q2, q3, q4, q5]
    audit_score = (sum(checklist) / 5) * 100
    esg_checklist = [esg1, esg2, esg3, esg4]
    esg_raw = (sum(esg_checklist) / 4) * 100
    governance_score = min((audit_score * 0.5) + (esg_raw * 0.3) + (20 if q2 else 0) + (10 if q1 else 0), 100)

    # Risk scoring
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

    overall_risk = max(0, 100 - risk_points)

    # Status helpers
    def risk_status(s):
        if s >= 70: return "Low risk", "status-green"
        elif s >= 45: return "Moderate", "status-amber"
        else: return "High risk", "status-red"

    def audit_status(s):
        if s >= 80: return "Prepared", "status-green"
        elif s >= 50: return "Partial", "status-amber"
        else: return "Not ready", "status-red"

    def gov_status(s):
        if s >= 70: return "Strong", "status-green"
        elif s >= 40: return "Developing", "status-amber"
        else: return "Weak", "status-red"

    rs_label, rs_class = risk_status(overall_risk)
    as_label, as_class = audit_status(audit_score)
    gs_label, gs_class = gov_status(governance_score)

    # Red flags
    red_flags = []
    if profit_margin < 0:
        red_flags.append(("critical", "Operating at a loss — expenses exceed revenue. Every month of operation deepens the deficit."))
    if expense_ratio > 85:
        red_flags.append(("warning", f"Expense ratio at {expense_ratio:.1f}% — above the 85% warning threshold. Less than 15p of every £1 earned remains after costs."))
    if cash < (fixed_costs * 2):
        red_flags.append(("warning", "Cash reserves below 2 months of fixed costs. Vulnerability to any revenue interruption."))
    if debt_to_revenue > 60:
        red_flags.append(("critical", f"Debt-to-revenue at {debt_to_revenue:.1f}% — above the 60% high-risk threshold. Significant portion of annual income committed to debt obligations."))
    if current_ratio < 1:
        red_flags.append(("critical", f"Current ratio {current_ratio:.2f} — below 1.0. Cannot meet short-term obligations from liquid assets. Going concern indicator."))
    if is_uk and revenue > 85000 and not q3:
        red_flags.append(("critical", "Revenue above VAT registration threshold (£85,000). Non-registration above this threshold is a criminal offence under the Value Added Tax Act 1994."))
    if not is_uk and revenue > 2000000 and not q3:
        red_flags.append(("critical", "Revenue above GST registration threshold (₹20 Lakhs). Mandatory registration required under CGST Act 2017."))

    # Actions
    actions = []
    if profit_margin < 0:
        actions.append("Review your full expense structure immediately. Identify your three largest costs and assess whether each is generating proportional value.")
    if expense_ratio > 85:
        actions.append(f"Reduce expense ratio from {expense_ratio:.1f}% toward 80%. A 5-point improvement on your current revenue base would add {currency}{(revenue * 0.05):,.0f} to annual profit.")
    if cash < fixed_costs * 2:
        actions.append(f"Build cash reserves to at least {currency}{(fixed_costs * 2):,.0f} (2 months fixed costs) before taking on new financial commitments.")
    if debt_to_revenue > 60:
        actions.append("Prioritise debt reduction before any new borrowing. Your current leverage ratio increases vulnerability to revenue volatility significantly.")
    if audit_score < 60:
        actions.append("Address compliance checklist gaps — particularly records and registration status. These are the first items any formal review would surface.")
    if current_ratio < 1:
        actions.append(f"Accelerate conversion of receivables ({currency}{receivables:,.0f}) to cash. Your liquidity position is the most immediate operational risk.")
    if not actions:
        actions.append("Your financial position is stable. Maintain current discipline, review quarterly, and focus on improving audit readiness to 100%.")

    # ESG items
    esg_items = [
        ("Monthly or quarterly financial review", esg1),
        ("Client contracts and terms of service", esg2),
        ("Compliance obligations awareness", esg3),
        ("Environmental and social impact awareness", esg4),
        ("Dedicated business banking", q2),
        ("Consistent record keeping", q1),
    ]

    # Overall summary
    if overall_risk >= 70:
        summary_text = f"Your business presents a broadly stable financial profile with a risk score of {overall_risk:.0f}/100. Profitability and liquidity are within acceptable ranges for your category. The primary area for improvement is audit readiness at {audit_score:.0f}% — addressing the outstanding compliance items would materially reduce your exposure in any formal review."
    elif overall_risk >= 45:
        weak = "cash reserves" if cash < fixed_costs * 2 else "leverage position" if debt_to_revenue > 60 else "profit margins"
        summary_text = f"Your business shows moderate risk at {overall_risk:.0f}/100. The principal concern is your {weak}, which requires attention before it compounds. Audit readiness at {audit_score:.0f}% suggests compliance gaps that should be addressed systematically over the next 60–90 days."
    else:
        summary_text = f"Your business is showing high-risk signals across multiple dimensions — score {overall_risk:.0f}/100. This warrants immediate attention. The combination of {('loss-making operations, ' if profit_margin < 0 else '')}{('insufficient liquidity, ' if current_ratio < 1 else '')}{('high leverage' if debt_to_revenue > 60 else 'compliance gaps')} creates compounding vulnerability. Address the priority actions below in sequence."

    # Store results
    st.session_state.results_ready = True
    st.session_state.financial_data = {
        "revenue": revenue, "expenses": expenses, "cash": cash,
        "debt": debt, "fixed_costs": fixed_costs, "receivables": receivables,
        "profit": profit, "profit_margin": profit_margin,
        "expense_ratio": expense_ratio, "debt_to_revenue": debt_to_revenue,
        "current_ratio": current_ratio, "overall_risk": overall_risk,
        "audit_score": audit_score, "governance_score": governance_score,
        "red_flags": red_flags, "actions": actions,
        "esg_items": esg_items, "summary_text": summary_text,
        "currency": currency, "is_uk": is_uk,
        "rs_label": rs_label, "rs_class": rs_class,
        "as_label": as_label, "as_class": as_class,
        "gs_label": gs_label, "gs_class": gs_class,
    }
    st.rerun()

# ── RESULTS ───────────────────────────────────────────────────
if st.session_state.results_ready:
    d = st.session_state.financial_data

    st.markdown("""
    <div class="rule-thick"></div>
    <div class="section-kicker">Diagnostic results</div>
    <h2 style="font-size:1.8rem; letter-spacing:-0.5px; margin-bottom:0.25rem;">
        Financial Health Report
    </h2>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="score-row">
        <div class="score-cell">
            <div class="score-cell-label">Financial risk</div>
            <div class="score-cell-number" style="color:{'#1a5c2e' if d['overall_risk']>=70 else '#7a4a0a' if d['overall_risk']>=45 else '#8B1A1A'}">
                {d['overall_risk']:.0f}<span style="font-size:1.2rem;color:#6b6b6b;font-weight:400">/100</span>
            </div>
            <span class="score-cell-status {d['rs_class']}">{d['rs_label']}</span>
        </div>
        <div class="score-cell">
            <div class="score-cell-label">Audit readiness</div>
            <div class="score-cell-number" style="color:{'#1a5c2e' if d['audit_score']>=80 else '#7a4a0a' if d['audit_score']>=50 else '#8B1A1A'}">
                {d['audit_score']:.0f}<span style="font-size:1.2rem;color:#6b6b6b;font-weight:400">%</span>
            </div>
            <span class="score-cell-status {d['as_class']}">{d['as_label']}</span>
        </div>
        <div class="score-cell">
            <div class="score-cell-label">Governance</div>
            <div class="score-cell-number" style="color:{'#1a5c2e' if d['governance_score']>=70 else '#7a4a0a' if d['governance_score']>=40 else '#8B1A1A'}">
                {d['governance_score']:.0f}<span style="font-size:1.2rem;color:#6b6b6b;font-weight:400">%</span>
            </div>
            <span class="score-cell-status {d['gs_class']}">{d['gs_label']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Ratios
    st.markdown('<div class="section-kicker" style="margin-top:1.5rem">Key financial ratios</div>', unsafe_allow_html=True)

    def ratio_class(metric, value, is_uk):
        if metric == "margin":
            t = 20 if is_uk else 15
            w = 10 if is_uk else 8
            return "ratio-good" if value >= t else "ratio-warn" if value >= w else "ratio-bad"
        elif metric == "expense":
            return "ratio-good" if value < 80 else "ratio-warn" if value < 85 else "ratio-bad"
        elif metric == "dtr":
            return "ratio-good" if value <= 30 else "ratio-warn" if value <= 60 else "ratio-bad"
        elif metric == "cr":
            return "ratio-good" if value >= 2 else "ratio-warn" if value >= 1 else "ratio-bad"

    m_class = ratio_class("margin", d['profit_margin'], d['is_uk'])
    e_class = ratio_class("expense", d['expense_ratio'], d['is_uk'])
    dtr_class = ratio_class("dtr", d['debt_to_revenue'], d['is_uk'])
    cr_class = ratio_class("cr", d['current_ratio'], d['is_uk'])

    st.markdown(f"""
    <table class="ratio-table">
        <thead>
            <tr>
                <th>Ratio</th>
                <th>Your figure</th>
                <th>Benchmark</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Net profit margin</td>
                <td class="ratio-val {m_class}">{d['profit_margin']:.1f}%</td>
                <td>≥{'20' if d['is_uk'] else '15'}% healthy</td>
                <td class="{m_class}">{'✓ Healthy' if m_class=='ratio-good' else '⚠ Watch' if m_class=='ratio-warn' else '✗ At risk'}</td>
            </tr>
            <tr>
                <td>Expense ratio</td>
                <td class="ratio-val {e_class}">{d['expense_ratio']:.1f}%</td>
                <td>Below 80% healthy</td>
                <td class="{e_class}">{'✓ Healthy' if e_class=='ratio-good' else '⚠ Watch' if e_class=='ratio-warn' else '✗ At risk'}</td>
            </tr>
            <tr>
                <td>Debt-to-revenue</td>
                <td class="ratio-val {dtr_class}">{d['debt_to_revenue']:.1f}%</td>
                <td>Below 30% low risk</td>
                <td class="{dtr_class}">{'✓ Low risk' if dtr_class=='ratio-good' else '⚠ Moderate' if dtr_class=='ratio-warn' else '✗ High risk'}</td>
            </tr>
            <tr>
                <td>Current ratio</td>
                <td class="ratio-val {cr_class}">{d['current_ratio']:.2f}</td>
                <td>Above 2.0 healthy</td>
                <td class="{cr_class}">{'✓ Healthy' if cr_class=='ratio-good' else '⚠ Watch' if cr_class=='ratio-warn' else '✗ At risk'}</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    # Flags
    st.markdown('<div class="rule"></div><div class="section-kicker">Audit flags</div>', unsafe_allow_html=True)
    if d['red_flags']:
        for severity, msg in d['red_flags']:
            css = "flag-critical" if severity == "critical" else "flag-warning"
            icon = "●" if severity == "critical" else "◐"
            st.markdown(f'<div class="flag-item {css}"><strong>{icon}</strong> {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="flag-item flag-ok">✓ No audit flags detected. Your numbers present cleanly.</div>', unsafe_allow_html=True)

    # Actions
    st.markdown('<div class="rule"></div><div class="section-kicker">Priority actions</div>', unsafe_allow_html=True)
    for i, action in enumerate(d['actions'][:3], 1):
        st.markdown(f"""
        <div class="action-item">
            <div class="action-number">{i}.</div>
            <div>{action}</div>
        </div>
        """, unsafe_allow_html=True)

    # ESG
    st.markdown('<div class="rule"></div><div class="section-kicker">Governance & ESG</div>', unsafe_allow_html=True)
    esg_grid = ""
    for item, passed in d['esg_items']:
        css = "esg-pass" if passed else "esg-fail"
        icon = "✓" if passed else "✗"
        esg_grid += f'<div class="esg-item {css}"><span>{"<strong>" if passed else ""}{icon}{"</strong>" if passed else ""}</span> {item}</div>'
    st.markdown(f'<div class="esg-grid">{esg_grid}</div>', unsafe_allow_html=True)

    # Summary
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="summary-box">
        <div class="summary-kicker">Overall assessment</div>
        {d['summary_text']}
    </div>
    """, unsafe_allow_html=True)

    # Stress test
    st.markdown('<div class="section-kicker" style="margin-top:1.5rem">Stress test</div>', unsafe_allow_html=True)
    st.caption("Model a revenue decline. Expenses held constant — the conservative assumption used in bank and investor stress testing.")
    drop = st.slider("Revenue decline:", 0, 50, 20, format="%d%%")
    new_rev = d['revenue'] * (1 - drop/100)
    new_profit = new_rev - d['expenses']
    new_margin = (new_profit / new_rev * 100) if new_rev > 0 else 0
    rev_delta = f"−{drop}%"
    profit_delta = f"{d['currency']}{new_profit - d['profit']:,.0f}"
    margin_delta = f"{new_margin - d['profit_margin']:+.1f}pp"

    st.markdown(f"""
    <div class="stress-row">
        <div class="stress-cell">
            <div class="stress-cell-label">Revenue after decline</div>
            <div class="stress-cell-value">{d['currency']}{new_rev:,.0f}</div>
            <div class="stress-cell-delta delta-neg">{rev_delta}</div>
        </div>
        <div class="stress-cell">
            <div class="stress-cell-label">Profit / loss</div>
            <div class="stress-cell-value" style="color:{'#1a5c2e' if new_profit>=0 else '#8B1A1A'}">{d['currency']}{new_profit:,.0f}</div>
            <div class="stress-cell-delta {'delta-pos' if new_profit>=0 else 'delta-neg'}">{profit_delta}</div>
        </div>
        <div class="stress-cell">
            <div class="stress-cell-label">New profit margin</div>
            <div class="stress-cell-value" style="color:{'#1a5c2e' if new_margin>=10 else '#8B1A1A'}">{new_margin:.1f}%</div>
            <div class="stress-cell-delta delta-neg">{margin_delta}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if new_profit < 0:
        st.markdown(f'<div class="flag-item flag-critical">A {drop}% revenue decline pushes your business into loss. Fixed cost base of {d["currency"]}{d["fixed_costs"]*12:,.0f}/year is not sustainable at this revenue level.</div>', unsafe_allow_html=True)
    elif new_margin < 10:
        st.markdown(f'<div class="flag-item flag-warning">Margin compresses to {new_margin:.1f}% under this scenario — dangerously thin. Limited capacity to absorb unexpected costs.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="flag-item flag-ok">Business remains profitable under a {drop}% revenue decline. Margin holds at {new_margin:.1f}%.</div>', unsafe_allow_html=True)

    # ── AI CHAT ───────────────────────────────────────────────
    st.markdown("""
    <div class="rule-thick" style="margin-top:2rem"></div>
    <div class="section-kicker">Financial intelligence</div>
    <h3 style="font-size:1.3rem; margin-bottom:0.25rem;">Ask Smit about your results</h3>
    <p style="font-size:0.85rem; color:#4a4a4a; margin-bottom:1rem; line-height:1.6;">
        Your financial data is loaded. Ask anything about your specific numbers — 
        what they mean, what to prioritise, what a bank or investor would think, 
        or what steps to take next.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="chat-container">
        <div class="chat-header">
            <span>Smit financial assistant</span>
            <span class="chat-header-badge">Powered by Claude · Your data loaded</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-msg-user">
                <div class="chat-msg-label">You</div>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-msg-assistant">
                <div class="chat-msg-label">Smit</div>
                {msg["content"]}
            </div>
            """, unsafe_allow_html=True)

    # Chat input
    user_question = st.text_input(
        "Your question",
        placeholder="e.g. Why is my risk score low? What should I fix first? What would a bank think of my numbers?",
        label_visibility="collapsed",
        key="chat_input"
    )

    if st.button("Send →", key="send_chat"):
        if user_question.strip():
            d = st.session_state.financial_data
            currency = d['currency']

            system_prompt = f"""You are Smit, a financial intelligence assistant built for small businesses and freelancers. You have access to this user's complete financial diagnostic results and answer questions about their specific situation.

USER FINANCIAL DATA:
- Region: {"UK" if d['is_uk'] else "India"} | Business type: {st.session_state.user_info.get('biz_type', 'SME')}
- Annual revenue: {currency}{d['revenue']:,.0f}
- Annual expenses: {currency}{d['expenses']:,.0f}
- Cash in bank: {currency}{d['cash']:,.0f}
- Total debt: {currency}{d['debt']:,.0f}
- Monthly fixed costs: {currency}{d['fixed_costs']:,.0f}
- Receivables: {currency}{d['receivables']:,.0f}

CALCULATED METRICS:
- Net profit margin: {d['profit_margin']:.1f}%
- Expense ratio: {d['expense_ratio']:.1f}%
- Debt-to-revenue: {d['debt_to_revenue']:.1f}%
- Current ratio: {d['current_ratio']:.2f}
- Overall risk score: {d['overall_risk']:.0f}/100
- Audit readiness: {d['audit_score']:.0f}%
- Governance score: {d['governance_score']:.0f}%

FLAGS: {[f[1] for f in d['red_flags']] if d['red_flags'] else ['None']}
PRIORITY ACTIONS: {d['actions'][:3]}

INSTRUCTIONS:
- Answer specifically using their actual numbers, not generic advice
- Be direct, clear, and honest — do not sugarcoat serious issues
- Use plain English — no unnecessary jargon
- Keep responses concise but complete
- Always end with one specific next step they can take this week
- Add this disclaimer ONLY when giving compliance-specific advice: "Note: for regulated tax or legal decisions, always confirm with a qualified professional."
- Do NOT add the disclaimer to general financial questions
- Benchmarks: UK profit margin healthy ≥20%, India ≥15%. Current ratio healthy ≥2.0. Debt-to-revenue low risk ≤30%, high risk >60%. These are sourced from HMRC, ICAEW, RBI, and ICAI frameworks."""

            messages_for_api = []
            for msg in st.session_state.chat_messages:
                messages_for_api.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            messages_for_api.append({
                "role": "user",
                "content": user_question
            })

            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_question
            })

            try:
                client = anthropic.Anthropic()
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=600,
                    system=system_prompt,
                    messages=messages_for_api
                )
                answer = response.content[0].text
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": answer
                })
            except Exception as e:
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": "I'm having trouble connecting right now. Please try again in a moment."
                })

            st.rerun()

    # Download button
    st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
    st.button("Download full report (PDF) — Pro feature · Coming soon", disabled=True)

    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        <strong>Important.</strong> Smit is a financial intelligence tool. It calculates, interprets, 
        and explains your financial data using published benchmarks from HMRC, ICAEW, RBI, and ICAI. 
        It does not provide regulated financial, tax, or legal advice. Benchmarks are indicative — 
        your specific circumstances may differ. For decisions affecting your tax position, compliance 
        obligations, or legal standing, always consult a qualified professional.
        <br><br>
        Benchmarks: HMRC Business Population Estimates · ICAEW SME Financial Health · 
        RBI Annual Report MSME Lending · ICAI SME Audit Manual · ACCA F3/F7 · ISA 570 Going Concern
    </div>
    """, unsafe_allow_html=True)
```

---
