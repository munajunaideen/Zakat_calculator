import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
from fpdf import FPDF
from datetime import datetime
import os

# ------------------------------------------------
# App configuration
# ------------------------------------------------
st.set_page_config(
    page_title="Zakat Calculator | حاسبة الزكاة",
    layout="centered"
)

# ------------------------------------------------
# Language selection
# ------------------------------------------------
language = st.sidebar.radio("🌐 Select Language / اختر اللغة", ["English", "العربية"])

# ------------------------------------------------
# Apply RTL style when Arabic selected
# ------------------------------------------------
if language == "العربية":
    st.markdown("""
        <style>
        body { direction: rtl; text-align: right; font-family: "Tajawal", "Amiri", "Arial", sans-serif; }
        .st-emotion-cache-1v0mbdj, .st-emotion-cache-1kyxreq, label, p, h1, h2, h3, h4, h5, h6 { direction: rtl; text-align: right; }
        input, .stNumberInput { text-align: right !important; }
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# ------------------------------------------------
# Texts for each language
# ------------------------------------------------
if language == "English":
    title = "Zakat Calculator"
    desc = "Calculate your annual Zakat accurately according to Islamic principles."
    assets_header = "Enter Your Assets"
    liabilities_header = "Enter Your Liabilities"
    labels = {
        "cash": "Cash on hand / bank (QAR)",
        "gold": "Value of gold (QAR)",
        "silver": "Value of silver (QAR)",
        "inv": "Investments / Shares (QAR)",
        "biz": "Business assets / inventory (QAR)",
        "rec": "Receivables / Money owed (QAR)",
        "debt": "Short-term debts / obligations (QAR)",
        "gold_price": "Current gold price per gram (QAR)"
    }
    nisab_label = "Nisab Threshold"
    results_label = "Results"
    chart_label = "Wealth Composition"
    report_label = "Download Zakat Report (PDF)"
    eligible = "✅ You are eligible to pay Zakat."
    not_eligible = "❎ Your wealth is below the Nisab threshold. No Zakat is due."
    footer = "Developed with ❤️ for Islamic Financial Awareness | © 2025"
    dua = "May Allah accept your Zakat and bless your wealth 🤲"
else:
    title = "حاسبة الزكاة"
    desc = "احسب زكاتك السنوية بدقة وفقاً للمبادئ الإسلامية."
    assets_header = "أدخل أصولك"
    liabilities_header = "أدخل التزاماتك"
    labels = {
        "cash": "النقد في اليد أو البنك (ريال قطري)",
        "gold": "قيمة الذهب (ريال قطري)",
        "silver": "قيمة الفضة (ريال قطري)",
        "inv": "الاستثمارات / الأسهم (ريال قطري)",
        "biz": "الأصول التجارية / المخزون (ريال قطري)",
        "rec": "الديون المستحقة لك (ريال قطري)",
        "debt": "الديون القصيرة الأجل (ريال قطري)",
        "gold_price": "سعر غرام الذهب الحالي (ريال قطري)"
    }
    nisab_label = "نصاب الزكاة"
    results_label = "النتائج"
    chart_label = "توزيع الثروة"
    report_label = "تحميل تقرير الزكاة (PDF)"
    eligible = "✅ أنت مؤهل لدفع الزكاة."
    not_eligible = "❎ ثروتك أقل من النصاب. لا زكاة عليك."
    footer = "تم التطوير بحب لتعزيز الوعي المالي الإسلامي | © 2025"
    dua = "نسأل الله أن يتقبل زكاتك ويبارك في مالك 🤲"

# ------------------------------------------------
# Page title & description
# ------------------------------------------------
st.title(title)
st.write(desc)

# ------------------------------------------------
# Input sections
# ------------------------------------------------
st.header(assets_header)
col1, col2 = st.columns(2)
with col1:
    cash = st.number_input(labels["cash"], min_value=0.0, step=100.0)
    gold = st.number_input(labels["gold"], min_value=0.0, step=100.0)
    silver = st.number_input(labels["silver"], min_value=0.0, step=100.0)
with col2:
    investments = st.number_input(labels["inv"], min_value=0.0, step=100.0)
    business_assets = st.number_input(labels["biz"], min_value=0.0, step=100.0)
    receivables = st.number_input(labels["rec"], min_value=0.0, step=100.0)

st.header(liabilities_header)
liabilities = st.number_input(labels["debt"], min_value=0.0, step=100.0)

# ------------------------------------------------
# Nisab section
# ------------------------------------------------
st.header(nisab_label)
gold_price = st.number_input(labels["gold_price"], value=250.0, step=1.0)
nisab_value = 85 * gold_price
st.info(f"{nisab_label}: **QAR {nisab_value:,.2f}**")

# ------------------------------------------------
# Zakat calculation (accurate)
# ------------------------------------------------
total_assets = cash + gold + silver + investments + business_assets + receivables
if math.isnan(total_assets): total_assets = 0.0
zakatable_wealth = total_assets - liabilities
if zakatable_wealth < 0: zakatable_wealth = 0.0

if zakatable_wealth >= nisab_value:
    zakat_due = zakatable_wealth * 0.025
else:
    zakat_due = 0.0

# ------------------------------------------------
# Display results
# ------------------------------------------------
st.header(results_label)
st.write(f"💰 **Total Assets:** QAR {total_assets:,.2f}")
st.write(f"💸 **Liabilities:** QAR {liabilities:,.2f}")
st.write(f"📊 **Zakatable Wealth:** QAR {zakatable_wealth:,.2f}")

if zakat_due > 0:
    st.success(f"{eligible}\n\n**Zakat Due: QAR {zakat_due:,.2f}**")
else:
    st.info(not_eligible)

# ------------------------------------------------
# Visualization
# ------------------------------------------------
st.header(chart_label)
data = {
    "Category": ["Cash", "Gold", "Silver", "Investments", "Business Assets", "Receivables"],
    "Value": [cash, gold, silver, investments, business_assets, receivables]
}
df = pd.DataFrame(data)
if df["Value"].sum() > 0:
    fig, ax = plt.subplots()
    ax.pie(df["Value"], labels=df["Category"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
else:
    st.write("No assets entered yet to display composition chart.")

# ------------------------------------------------
# PDF export (Unicode-safe with fpdf2)
# ------------------------------------------------
if st.button(report_label):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()

    # Load a Unicode font
    if not os.path.exists("Amiri-Regular.ttf"):
        st.warning("⚠️ Please place 'Amiri-Regular.ttf' (Arabic font) in the same folder for Arabic support.")
    else:
        pdf.add_font("Amiri", "", "Amiri-Regular.ttf", uni=True)
        pdf.set_font("Amiri", size=12)

    pdf.multi_cell(180, 10, txt="Zakat Calculation Report")
    pdf.multi_cell(180, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    pdf.multi_cell(180, 10, txt=f"Total Assets: QAR {total_assets:,.2f}")
    pdf.multi_cell(180, 10, txt=f"Liabilities: QAR {liabilities:,.2f}")
    pdf.multi_cell(180, 10, txt=f"Net Zakatable Wealth: QAR {zakatable_wealth:,.2f}")
    pdf.multi_cell(180, 10, txt=f"Nisab: QAR {nisab_value:,.2f}")
    pdf.multi_cell(180, 10, txt=f"Zakat Due: QAR {zakat_due:,.2f}")
    pdf.multi_cell(180, 10, txt=dua)

    file_name = "Zakat_Report.pdf"
    pdf.output(file_name)

    with open(file_name, "rb") as f:
        st.download_button("📥 Download PDF", data=f, file_name=file_name, mime="application/pdf")
    

# ------------------------------------------------
# Footer
# ------------------------------------------------
st.markdown("---")
st.caption(footer)
