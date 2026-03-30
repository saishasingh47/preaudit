import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PreAudit — Know What Your Auditor Would Flag",
    page_icon="📊",
    layout="centered"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 3rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero h1 {
        color: #ffffff;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .hero p {
        color: #a0aec0;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .hero .tagline {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 600;
        font-style: italic;
        margin: 1rem 0;
        padding: 0.8rem 1.5rem;
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        border-left: 4px solid #667eea;
        display: inline-block;
    }
    .hero .pill {
        display: inline-block;
        background: rgba(102, 126, 234, 0.3);
        color: #a78bfa;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.2rem;
        border: 1px solid rgba(102, 126, 234, 0.4);
    }

    /* Score cards */
    .score-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #f0f0f0;
        margin-bottom: 1rem;
    }
    .score-card .score-number {
        font-size: 3rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.3rem;
    }
    .score-card .score-label {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    .score-card .score-status {
        font-size: 1rem;
        font-weight: 600;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        display: inline-block;
    }
    .green { color: #22c55e; }
    .amber { color: #f59e0b; }
    .red { color: #ef4444; }
    .green-badge { background: #f0fdf4; color: #16a34a; }
    .amber-badge { background: #fffbeb; color: #d97706; }
    .red-badge { background: #fef2f2; color: #dc2626; }

    /* Section headers */
    .section-header {
        background: #f8fafc;
        border-left: 4px solid #667eea;
        padding: 0.8rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 1.5rem 0 1rem 0;
        font-weight: 600;
        font-size: 1.1rem;
        color: #1a1a2e;
    }

    /* Flag cards */
    .flag-red {
        background: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 0.8rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        color: #991b1b;
        font-size: 0.95rem;
    }
    .flag-amber {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 0.8rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        color: #92400e;
        font-size: 0.95rem;
    }
    .flag-green {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 0.8rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        color: #166534;
        font-size: 0.95rem;
    }

    /* Action cards */
    .action-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    /* Ratio cards */
    .ratio-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .ratio-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a2e;
    }
    .ratio-label {
        font-size: 0.8rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    .ratio-benchmark {
        font-size: 0.78rem;
        color: #aaa;
        margin-top: 0.3rem;
    }

    /* ESG card */
    .esg-card {
        background: linear-gradient(135deg, #134e4a, #065f46);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        margin: 0.5rem 0;
    }
    .esg-card h4 {
        color: #6ee7b7;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
    }
    .esg-card .esg-score {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
    }
    .esg-card p {
        color: #a7f3d0;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* Summary box */
    .summary-box {
        background: linear-gradient(135deg, #667eea15, #764ba215);
        border: 1px solid #667eea40;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    /* Step badge */
    .step-badge {
        background: #667eea;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }

    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #f0f0f0;
        margin: 2rem 0;
    }

    /* Input styling */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div class="hero">
    <h1>📊 PreAudit</h1>
    <p>Pre-audit diagnostic tool for small businesses and freelancers</p>
    <div class="tagline">
        "Know what your auditor would flag — before you're in that room."
    </div>
    <br/>
    <span class="pill">🔍 Financial Risk Scoring</span>
    <span class="pill">📋 Audit Readiness</span>
    <span class="pill">🌱 ESG & Governance</span>
    <span class="pill">⚡ Stress Testing</span>
    <br/><br/>
    <p style="color: #718096; font-size: 0.9rem;">
        Built using SME financial benchmarks from HMRC, ICAEW, RBI, and ICAI frameworks
    </p>
</div>
""", unsafe_allow_html=True)

# --- MODULE SELECTION ---
st.markdown('<div class="section-header">🌍 Select Your Region</div>', unsafe_allow_html=True)
module = st.radio(
    "Get the right compliance framework for your location:",
    ["🇬🇧 UK — Freelancer / Small Business", "🇮🇳 India — SME / Startup"],
    horizontal=True
)
st.divider()

# --- STEP 1 ---
st.markdown('<span class="step-badge">Step 1</span> **Enter Your Financial Details**', unsafe_allow_html=True)
st.caption("These are the numbers a CA or auditor asks for first. You should know them.")

col1, col2 = st.columns(2)
with col1:
    if "🇬🇧" in module:
        st.markdown("**💰 Revenue & Profitability**")
        revenue = st.number_input("Annual Revenue (£)", min_value=0.0, step=1000.0)
        expenses = st.number_input("Annual Expenses (£)", min_value=0.0, step=1000.0)
        cash = st.number_input("Cash in Bank (£)", min_value=0.0, step=500.0)
    else:
        st.markdown("**💰 Revenue & Profitability**")
        revenue = st.number_input("Annual Revenue (₹)", min_value=0.0, step=10000.0)
        expenses = st.number_input("Annual Expenses (₹)", min_value=0.0, step=10000.0)
        cash = st.number_input("Cash in Bank (₹)", min_value=0.0, step=5000.0)

with col2:
    if "🇬🇧" in module:
        st.markdown("**🏦 Debt & Obligations**")
        debt = st.number_input("Total Debt / Liabilities (£)", min_value=0.0, step=500.0)
        fixed_costs = st.number_input("Monthly Fixed Costs (£)", min_value=0.0, step=100.0)
        receivables = st.number_input("Money Owed to You (£)", min_value=0.0, step=100.0)
    else:
        st.markdown("**🏦 Debt & Obligations**")
        debt = st.number_input("Total Debt / Liabilities (₹)", min_value=0.0, step=5000.0)
        fixed_costs = st.number_input("Monthly Fixed Costs (₹)", min_value=0.0, step=1000.0)
        receivables = st.number_input("Money Owed to You (₹)", min_value=0.0, step=1000.0)

st.divider()

# --- STEP 2 ---
st.markdown('<span class="step-badge">Step 2</span> **Audit Readiness Check**', unsafe_allow_html=True)
st.caption("Answer honestly — a CA asks exactly these questions in the first ten minutes.")

if "🇬🇧" in module:
    q1 = st.checkbox("📁 I keep all receipts and invoices (digital or physical)")
    q2 = st.checkbox("🏦 I have a separate business bank account")
    q3 = st.checkbox("📋 I am registered for VAT — or I know exactly where I stand on the threshold")
    q4 = st.checkbox("✅ I file my self-assessment or company accounts on time, every year")
    q5 = st.checkbox("📂 I have financial records going back at least 2 years")
else:
    q1 = st.checkbox("📁 I keep all receipts and invoices (digital or physical)")
    q2 = st.checkbox("🏦 I have a separate business bank account")
    q3 = st.checkbox("📋 I am registered for GST — or I know exactly where I stand on the threshold")
    q4 = st.checkbox("✅ I file GST returns quarterly, consistently and on time")
    q5 = st.checkbox("📂 I maintain records that a CA could review without preparation")

# --- ESG QUESTIONS ---
st.markdown("**🌱 Governance & ESG Check**")
st.caption("A lightweight governance assessment — increasingly relevant as businesses grow.")
esg1 = st.checkbox("📊 I produce or review a monthly/quarterly financial summary")
esg2 = st.checkbox("⚖️ I am aware of my key legal and compliance obligations")
esg3 = st.checkbox("🤝 I have clear terms of service or contracts with clients")
esg4 = st.checkbox("♻️ I am aware of any environmental or social impact of my business operations")

st.divider()

# --- RUN BUTTON ---
if st.button("🔍 Run My Pre-Audit Diagnostic", type="primary", use_container_width=True):

    if revenue == 0:
        st.error("Please enter your annual revenue to run the diagnostic.")
    else:
        # --- CALCULATIONS ---
        currency = "£" if "🇬🇧" in module else "₹"
        profit = revenue - expenses
        profit_margin = (profit / revenue) * 100 if revenue > 0 else 0
        expense_ratio = (expenses / revenue) * 100 if revenue > 0 else 0
        debt_to_revenue = (debt / revenue) * 100 if revenue > 0 else 0
        current_ratio = (cash + receivables) / (debt if debt > 0 else 1)

        checklist = [q1, q2, q3, q4, q5]
        audit_score = (sum(checklist) / len(checklist)) * 100

        esg_checklist = [esg1, esg2, esg3, esg4]
        esg_raw = (sum(esg_checklist) / len(esg_checklist)) * 100
        governance_score = min(
            (audit_score * 0.5) + (esg_raw * 0.3) + (20 if q2 else 0) + (10 if q1 else 0),
            100
        )

        # --- RISK SCORING ---
        risk_points = 0
        if "🇬🇧" in module:
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

        # --- RED FLAGS ---
        red_flags = []
        if profit_margin < 0:
            red_flags.append(("red", "🚨 Operating at a loss — expenses exceed revenue."))
        if expense_ratio > 85:
            red_flags.append(("amber", "⚠️ Expenses consuming more than 85% of revenue — very little financial buffer."))
        if cash < (fixed_costs * 2):
            red_flags.append(("amber", "⚠️ Cash reserves below 2 months of fixed costs — liquidity risk."))
        if debt_to_revenue > 60:
            red_flags.append(("red", "🚨 Debt is high relative to revenue — significant leverage risk."))
        if current_ratio < 1:
            red_flags.append(("red", "🚨 Current ratio below 1 — may struggle to meet short-term obligations."))
        if "🇬🇧" in module and revenue > 85000 and not q3:
            red_flags.append(("amber", "⚠️ Revenue above VAT threshold (£85,000). Verify registration status immediately."))
        if "🇮🇳" in module and revenue > 2000000 and not q3:
            red_flags.append(("amber", "⚠️ Revenue above GST threshold (₹20 Lakhs). Verify registration status immediately."))

        # --- TOP ACTIONS ---
        actions = []
        if profit_margin < 0:
            actions.append("🔴 Review your expense structure immediately — identify what can be cut without impacting revenue.")
        if expense_ratio > 85:
            actions.append("🔴 Reduce expense ratio below 80% — audit your top 3 costs and assess each one critically.")
        if cash < fixed_costs * 2:
            actions.append("🟠 Build at least 2 months of fixed cost coverage in cash reserves before new commitments.")
        if debt_to_revenue > 60:
            actions.append("🟠 Reduce debt exposure before taking on further financial commitments or credit.")
        if audit_score < 60:
            actions.append("🟡 Address compliance checklist gaps before any CA or audit review.")
        if current_ratio < 1:
            actions.append("🔴 Liquidity is critical — prioritise converting receivables to cash immediately.")
        if not actions:
            actions.append("✅ No immediate corrective action required. Review quarterly to maintain this position.")

        # --- ESG NARRATIVE ---
        if governance_score >= 75:
            esg_narrative = "Strong governance foundations. Your business demonstrates good financial transparency and compliance awareness."
        elif governance_score >= 50:
            esg_narrative = "Moderate governance. Some controls are in place but gaps remain — particularly around reporting consistency and compliance awareness."
        else:
            esg_narrative = "Governance needs significant attention. Focus first on financial record separation, compliance awareness, and regular reporting."

        # ── RESULTS ──────────────────────────────────────────
        st.markdown('<span class="step-badge">Step 3</span> **Your Pre-Audit Diagnostic Results**', unsafe_allow_html=True)
        st.caption("Here is how your business looks through an auditor's lens.")
        st.divider()

        # SCORE CARDS
        col1, col2, col3 = st.columns(3)

        def score_color(score, thresholds):
            if score >= thresholds[0]: return "green", "green-badge", "✅"
            elif score >= thresholds[1]: return "amber", "amber-badge", "⚠️"
            else: return "red", "red-badge", "🚨"

        risk_col, risk_badge, risk_icon = score_color(overall_risk, [70, 45])
        audit_col, audit_badge, audit_icon = score_color(audit_score, [80, 50])
        gov_col, gov_badge, gov_icon = score_color(governance_score, [70, 40])

        risk_label = "Low Risk" if overall_risk >= 70 else "Moderate Risk" if overall_risk >= 45 else "High Risk"
        audit_label = "Well Prepared" if audit_score >= 80 else "Partially Prepared" if audit_score >= 50 else "Not Audit Ready"
        gov_label = "Strong Controls" if governance_score >= 70 else "Needs Attention" if governance_score >= 40 else "Weak Governance"

        with col1:
            st.markdown(f"""
            <div class="score-card">
                <div class="score-label">Financial Risk Score</div>
                <div class="score-number {risk_col}">{overall_risk:.0f}<span style="font-size:1.2rem;color:#888">/100</span></div>
                <span class="score-status {risk_badge}">{risk_icon} {risk_label}</span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="score-card">
                <div class="score-label">Audit Readiness</div>
                <div class="score-number {audit_col}">{audit_score:.0f}<span style="font-size:1.2rem;color:#888">%</span></div>
                <span class="score-status {audit_badge}">{audit_icon} {audit_label}</span>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="score-card">
                <div class="score-label">Governance Score</div>
                <div class="score-number {gov_col}">{governance_score:.0f}<span style="font-size:1.2rem;color:#888">%</span></div>
                <span class="score-status {gov_badge}">{gov_icon} {gov_label}</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # RATIOS
        st.markdown('<div class="section-header">📈 Key Financial Ratios</div>', unsafe_allow_html=True)
        st.caption("Benchmarked against published SME standards from HMRC, ICAEW, RBI, and ICAI.")

        col1, col2, col3, col4 = st.columns(4)
        ratios = [
            ("Net Profit Margin", f"{profit_margin:.1f}%", "≥20% healthy (UK) / ≥15% (India)"),
            ("Expense Ratio", f"{expense_ratio:.1f}%", "Below 80% healthy. Above 85% = warning."),
            ("Debt-to-Revenue", f"{debt_to_revenue:.1f}%", "Below 30% low risk. Above 60% high risk."),
            ("Current Ratio", f"{current_ratio:.2f}", "Above 2.0 healthy. Below 1.0 = risk signal.")
        ]
        for col, (label, value, benchmark) in zip([col1, col2, col3, col4], ratios):
            with col:
                st.markdown(f"""
                <div class="ratio-card">
                    <div class="ratio-label">{label}</div>
                    <div class="ratio-value">{value}</div>
                    <div class="ratio-benchmark">{benchmark}</div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # AUDIT FLAGS
        st.markdown('<div class="section-header">🚩 Audit Flags</div>', unsafe_allow_html=True)
        st.caption("Issues a CA would flag immediately in an initial review.")
        if red_flags:
            for severity, flag in red_flags:
                st.markdown(f'<div class="flag-{severity}">{flag}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="flag-green">✅ No audit flags detected. Your numbers are telling a clean story.</div>', unsafe_allow_html=True)

        st.divider()

        # TOP ACTIONS
        st.markdown('<div class="section-header">⚡ Top Priority Actions</div>', unsafe_allow_html=True)
        st.caption("The most important steps to take based on your results.")
        for action in actions[:3]:
            st.markdown(f'<div class="action-card">{action}</div>', unsafe_allow_html=True)

        st.divider()

        # ESG SECTION
        st.markdown('<div class="section-header">🌱 ESG & Governance Assessment</div>', unsafe_allow_html=True)
        st.caption("A lightweight governance and sustainability indicator — increasingly relevant for businesses of all sizes.")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div class="esg-card">
                <h4>Governance Score</h4>
                <div class="esg-score">{governance_score:.0f}%</div>
                <p>{gov_label}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            esg_items = [
                ("Monthly/quarterly financial review", esg1),
                ("Compliance obligations awareness", esg2),
                ("Client contracts / terms of service", esg3),
                ("Environmental & social impact awareness", esg4),
                ("Separate business banking", q2),
                ("Consistent record keeping", q1),
            ]
            for item, passed in esg_items:
                icon = "✅" if passed else "❌"
                color = "#166534" if passed else "#991b1b"
                bg = "#f0fdf4" if passed else "#fef2f2"
                st.markdown(f"""
                <div style="background:{bg};padding:0.4rem 0.8rem;border-radius:6px;
                margin:0.3rem 0;font-size:0.9rem;color:{color};">
                    {icon} {item}
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#f0fdf4;border-left:4px solid #22c55e;
        padding:1rem 1.2rem;border-radius:0 8px 8px 0;margin-top:1rem;color:#166534;">
            💡 {esg_narrative}
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # SUMMARY
        st.markdown('<div class="section-header">📋 Overall Assessment</div>', unsafe_allow_html=True)
        if overall_risk >= 70:
            summary = f"Your business is in a healthy position — risk score {overall_risk:.0f}/100. Profit margins and liquidity look stable. Audit readiness at {audit_score:.0f}% — {'address the checklist gaps before your next CA review.' if audit_score < 100 else 'well prepared for a CA review.'}"
        elif overall_risk >= 45:
            weak = "cash reserves" if cash < fixed_costs * 2 else "debt levels" if debt_to_revenue > 60 else "profit margins"
            summary = f"Moderate risk — score {overall_risk:.0f}/100. Main concern: {weak}. Manageable now but needs attention before it becomes critical. Audit readiness at {audit_score:.0f}%."
        else:
            summary = f"High risk signals detected — score {overall_risk:.0f}/100. Immediate attention needed across your financial position. Use this as a starting point for an urgent conversation with your CA or accountant."

        st.markdown(f'<div class="summary-box">💡 {summary}</div>', unsafe_allow_html=True)

        st.divider()

        # STRESS TEST
        st.markdown('<div class="section-header">📉 Stress Test — What If?</div>', unsafe_allow_html=True)
        st.caption("Model a revenue decline to see how your business holds up. Expenses held constant — the conservative assumption.")

        scenario_drop = st.slider("Revenue drops by:", 0, 50, 20, format="%d%%")
        new_revenue = revenue * (1 - scenario_drop / 100)
        new_profit = new_revenue - expenses
        new_margin = (new_profit / new_revenue) * 100 if new_revenue > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Revenue After Drop", f"{currency}{new_revenue:,.0f}", delta=f"-{scenario_drop}%")
        with col2:
            st.metric("New Profit / Loss", f"{currency}{new_profit:,.0f}", delta=f"{currency}{new_profit - profit:,.0f}")
        with col3:
            st.metric("New Profit Margin", f"{new_margin:.1f}%", delta=f"{new_margin - profit_margin:.1f}%")

        if new_profit < 0:
            st.markdown('<div class="flag-red">🚨 A revenue drop of this size would push your business into loss. Your cost base is not sustainable at lower revenue.</div>', unsafe_allow_html=True)
        elif new_margin < 10:
            st.markdown('<div class="flag-amber">⚠️ Margin becomes dangerously thin under this scenario. Limited room for unexpected costs.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="flag-green">✅ Business remains profitable under this scenario.</div>', unsafe_allow_html=True)

        st.divider()

        st.button("📄 Download Full Report (PDF) — Coming Soon", disabled=True)

        st.markdown("""
        <div style="text-align:center;color:#aaa;font-size:0.85rem;margin-top:2rem;padding:1rem;
        border-top:1px solid #f0f0f0;">
            PreAudit is a diagnostic tool, not financial advice.<br>
            It does not replace your accountant, CA, or auditor.<br>
            It helps you walk into that conversation better prepared.
        </div>
        """, unsafe_allow_html=True)
    
