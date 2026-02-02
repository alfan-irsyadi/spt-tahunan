import streamlit as st
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Arsip PDF GPP", layout="wide")

PDF_DIR = Path("pdf_data")

st.title("📄 SPT TAHUNAN Kemenag Batu Bara 2025")
st.caption('created by Muhammad Alfan Irsyadi Hutagalung')
st.caption("Filter berdasarkan NIP atau Nama (berdasarkan nama file)")

# ===== Ambil semua PDF =====
files = list(PDF_DIR.glob("*.pdf"))

data = []
for f in files:
    try:
        nip, nama = f.stem.split(" - ", 1)
        data.append({
            "NIP": nip,
            "NAMA": nama,
            "FILE": f
        })
    except ValueError:
        pass  # skip file aneh

df = pd.DataFrame(data)

# ===== FILTER =====
col1, col2 = st.columns(2)

with col1:
    filter_nip = st.text_input("Cari NIP")

with col2:
    filter_nama = st.text_input("Cari Nama")

if filter_nip:
    df = df[df["NIP"].str.contains(filter_nip, case=False)]

if filter_nama:
    df = df[df["NAMA"].str.contains(filter_nama, case=False)]

st.write(f"📊 Ditemukan {len(df)} file")

# ===== TAMPILKAN =====
for _, row in df.iterrows():
    with st.container(border=True):
        st.markdown(f"**{row['NAMA']}**")
        st.caption(row["NIP"])

        with open(row["FILE"], "rb") as f:
            st.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name=row["FILE"].name,
                mime="application/pdf"
            )
