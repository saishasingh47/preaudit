import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PreAudit — Know Your Numbers Before Your CA Does",
    page_icon="📊",
    layout="wide"
)

# --- HEADER ---
st.title("📊 PreAudit")
st.markdown("### Pre-audit diagnostic tool for small businesses and freelancers")
st.markdown("*Know your financial position before your CA does — run your numbers the way an auditor would, before you're ever in that room.*")
st.divider()

# --- MODULE SELECTION ---
st.markdown("#### Select your region to get the right framework")
module = st.radio("", ["🇬🇧 UK — Freelancer / Small Business", "🇮🇳 India — SME / Startup"], horizontal=True)
st.divider()

# --- INPUTS ---
st.header("Step 1 — Enter Your Financial Details")
st.markdown("*These are the numbers an auditor or CA would ask for first. You should know them off the top of your head.*")

col1, col2 = st.columns(2)

with col1:
    if "UK" in module:
        st.markdown("**Revenue & Profitability**")
        revenue = st.number_input("Annual Revenue (£)", min_value=0.0, step=1000.0)
        expenses = st.number_input("Annual Expenses (£)", min_value=0.0, step=1000.0)
        cash = st.number_input("Cash in Bank (£)", min_value=0.0, step=500.0)
    else:
        st.markdown("**Revenue & Profitability**")
        revenue = st.number_input("Annual Revenue (₹)", min_value=0.0, step=10000.0)
        expenses = st.number_input("Annual Expenses (₹)", min_value=0.0, step=10000.0)
        cash = st.number_input("Cash in Bank (₹)", min_value=0.0, step=5000.0)

with col2:
    if "UK" in module:
        st.markdown("**Debt & Obligations**")
        debt = st.number_input("Total Debt / Liabilities (£)", min_value=0.0, step=500.0)
        fixed_costs = st.number_input("Monthly Fixed Costs (£)", min_value=0.0, step=100.0)
        receivables = st.number_input("Money Owed to You / Receivables (£)", min_value=0.0, step=100.0)
    else:
        st.markdown("**Debt & Obligations**")
        debt = st.number_input("Total Debt / Liabilities (₹)", min_value=0.0, step=5000.0)
        fixed_costs = st.number_input("Monthly Fixed Costs (₹)", min_value=0.0, step=1000.0)
        receivables = st.number_input("Money Owed to You / Receivables (₹)", min_value=0.0, step=1000.0)

st.divider()

# --- AUDIT CHECKLIST ---
st.header("Step 2 — Audit Readiness Check")
st.markdown("*Answer honestly. A CA would ask you exactly these questions in the first ten minutes of a review.*")

if "UK" in module:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)")
    q2 = st.checkbox("I have a separate business bank account")
    q3 = st.checkbox("I am registered for VAT — or I know exactly where I stand on the threshold")
    q4 = st.checkbox("I file my self-assessment or company accounts on time, every year")
    q5 = st.checkbox("I have financial records going back at least 2 years")
else:
    q1 = st.checkbox("I keep all receipts and invoices (digital or physical)")
    q2 = st.checkbox("I have a separate business bank account")
    q3 = st.checkbox("I am registered for GST — or I know exactly where I stand on the threshold")
    q4 = st.checkbox("I file GST returns quarterly, consistently and on time")
    q5 = st.checkbox("I maintain records that a CA could review without preparation")

st.divider()

# --- CALCULATE ---
if st.button("Run My Pre-Audit Diagnostic", type="primary", use_container_width=True):

    if revenue == 0:
        st.error("Please enter your annual revenue to run the diagnostic.")

    else:
        # --- CALCULATIONS ---
        currency = "£" if "UK" in module else "₹"
        profit = revenue - expenses
        profit_margin = (profit / revenue) * 100 if revenue > 0 else 0
        expense_ratio = (expenses / revenue) * 100 if revenue > 0 else 0
        debt_to_revenue = (debt / revenue) * 100 if revenue > 0 else 0
        current_ratio = (cash + receivables) / (debt + 1)

        checklist = [q1, q2, q3, q4, q5]
        audit_score = (sum(checklist) / len(checklist)) * 100

        # --- RISK SCORING ---
        risk_points = 0

        if "UK" in module:
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
            red_flags.append("🚨 Your business is operating at a loss — expenses exceed revenue.")
        if expense_ratio > 85:
            red_flags.append("⚠️ Expenses consuming more than 85% of revenue — very little financial buffer.")
        if cash < (fixed_costs * 2):
            red_flags.append("⚠️ Cash reserves below 2 months of fixed costs — liquidity risk.")
        if debt_to_revenue > 60:
            red_flags.append("🚨 Debt is high relative to revenue — significant leverage risk.")
        if current_ratio < 1:
            red_flags.append("🚨 Current ratio below 1 — may struggle to meet short-term obligations.")
        if "UK" in module and revenue > 85000 and not q3:
            red_flags.append("⚠️ Revenue may be above the VAT threshold (£85,000). Verify your registration status immediately.")
        if "India" in module and revenue > 2000000 and not q3:
            red_flags.append("⚠️ Revenue may be above the GST threshold (₹20 Lakhs). Verify your registration status immediately.")

        # --- ESG / GOVERNANCE SCORE ---
        governance_score = audit_score * 0.6 + (20 if q2 else 0) + (20 if q1 else 0)
        governance_score = min(governance_score, 100)

        # --- RESULTS HEADER ---
        st.header("Your Pre-Audit Diagnostic Results")
        st.markdown("*Here is how your business looks through an auditor's lens.*")
        st.divider()

        # --- THREE SCORES ---
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Overall Financial Risk**")
            if overall_risk >= 70:
                st.success(f"# {overall_risk:.0f} / 100\n✅ Low Risk")
            elif overall_risk >= 45:
                st.warning(f"# {overall_risk:.0f} / 100\n⚠️ Moderate Risk")
            else:
                st.error(f"# {overall_risk:.0f} / 100\n🚨 High Risk")

        with col2:
            st.markdown("**Audit Readiness**")
            if audit_score >= 80:
                st.success(f"# {audit_score:.0f}%\n✅ Well Prepared")
            elif audit_score >= 50:
                st.warning(f"# {audit_score:.0f}%\n⚠️ Partially Prepared")
            else:
                st.error(f"# {audit_score:.0f}%\n🚨 Not Audit Ready")

        with col3:
            st.markdown("**Governance Score**")
            if governance_score >= 70:
                st.success(f"# {governance_score:.0f}%\n✅ Strong Controls")
            elif governance_score >= 40:
                st.warning(f"# {governance_score:.0f}%\n⚠️ Needs Attention")
            else:
                st.error(f"# {governance_score:.0f}%\n🚨 Weak Governance")

        st.divider()

        # --- RATIO BREAKDOWN ---
        st.subheader("Financial Ratio Breakdown")
        st.markdown("*These are the ratios a CA or auditor calculates in the first pass of your accounts.*")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Net Profit Margin",
                f"{profit_margin:.1f}%",
                help="Net profit as % of revenue. Benchmark: above 20% healthy (UK), above 15% healthy (India)."
            )
            st.metric(
                "Expense Ratio",
                f"{expense_ratio:.1f}%",
                help="Expenses as % of revenue. Below 80% is healthy. Above 85% is a warning signal."
            )
        with col2:
            st.metric(
                "Debt-to-Revenue Ratio",
                f"{debt_to_revenue:.1f}%",
                help="Total debt relative to annual revenue. Below 30% is low risk. Above 60% is high risk."
            )
            st.metric(
                "Current Ratio",
                f"{current_ratio:.2f}",
                help="Liquidity: (cash + receivables) / debt. Above 2 is healthy. Below 1 is a risk signal."
            )

        st.divider()

        # --- RED FLAGS ---
        st.subheader("Red Flags")
        st.markdown("*These are the issues a CA would flag immediately in a review.*")
        if red_flags:
            for flag in red_flags:
                st.markdown(flag)
        else:
            st.success("✅ No major red flags detected. Your numbers are telling a clean story.")

        st.divider()

        # --- PLAIN ENGLISH SUMMARY ---
        st.subheader("What This Means For You")
        if overall_risk >= 70:
            summary = (
                f"Your business is in a relatively healthy position — risk score {overall_risk:.0f}/100. "
                f"Your profit margins and liquidity look stable. "
                f"Your audit readiness is at {audit_score:.0f}% — "
                f"{'focus on the checklist items you missed before your next CA review.' if audit_score < 100 else 'you are well prepared for a CA review.'}"
            )
        elif overall_risk >= 45:
            weak_area = (
                "cash reserves" if cash < fixed_costs * 2
                else "debt levels" if debt_to_revenue > 60
                else "profit margins"
            )
            summary = (
                f"Your business shows moderate risk — score {overall_risk:.0f}/100. "
                f"The main area of concern is your {weak_area}. "
                f"This is manageable now but needs attention before it becomes critical. "
                f"Your audit readiness sits at {audit_score:.0f}% — address the checklist gaps before any CA review."
            )
        else:
            summary = (
                f"Your business is showing high risk signals — score {overall_risk:.0f}/100. "
                f"Immediate attention is needed across your expense structure, cash position, or debt levels. "
                f"Do not wait for an audit to surface these issues. "
                f"Use this report as a starting point for a conversation with your accountant."
            )
        st.info(f"💡 {summary}")

        st.divider()

        # --- SCENARIO TOOL ---
        st.subheader("Stress Test — What If?")
        st.markdown("*See how your business holds up under pressure. This is what auditors and investors model.*")

        scenario_drop = st.slider("Revenue drops by:", 0, 50, 20, format="%d%%")
        new_revenue = revenue * (1 - scenario_drop / 100)
        new_profit = new_revenue - expenses
        new_margin = (new_profit / new_revenue) * 100 if new_revenue > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Revenue After Drop",
                f"{currency}{new_revenue:,.0f}",
                delta=f"-{scenario_drop}%"
            )
        with col2:
            st.metric(
                "New Profit / Loss",
                f"{currency}{new_profit:,.0f}",
                delta=f"{currency}{new_profit - profit:,.0f}"
            )
        with col3:
            st.metric(
                "New Profit Margin",
                f"{new_margin:.1f}%",
                delta=f"{new_margin - profit_margin:.1f}%"
            )

        if new_profit < 0:
            st.error(f"🚨 A {scenario_drop}% revenue drop would push your business into a loss. Your current cost base is not sustainable at lower revenue.")
        elif new_margin < 10:
            st.warning(f"⚠️ A {scenario_drop}% revenue drop leaves your margin dangerously thin at {new_margin:.1f}%. Limited room for unexpected costs.")
        else:
            st.success(f"✅ Your business remains profitable under a {scenario_drop}% revenue drop — margin holds at {new_margin:.1f}%.")

        st.divider()

        # --- FOOTER ---
        st.markdown(
            "*PreAudit is a diagnostic tool, not financial advice. "
            "It does not replace your accountant, CA, or auditor. "
            "It helps you walk into that conversation better prepared.*"
        )
