# 📄 NAVA AI – Submittal Review Analytics

**NAVA AI** by **Niti Consulting** is an AI-powered construction schedule intelligence platform.  
This module – **Submittal Review Analytics** – enables rapid review, classification, and export of annotated submittal logs using a streamlined web interface.

---

## 🚀 Features

- Upload submittal logs in `.xlsx` format
- Classify records by:
  - ⏳ Pending / Rejected Items
  - ❌ Missing Activity Links
  - 🔍 Long Open Items
- Export fully annotated logs with one click
- Ready for extension into claims and logic analysis

---

## 📦 Installation

To run locally:

```bash
git clone https://github.com/<your-repo-url>.git
cd nava-ai
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧠 Tech Stack

- **Streamlit** – UI framework
- **Pandas** – Data handling
- **XlsxWriter** – Excel export

---

## 📤 Upload Format

Ensure the uploaded `.xlsx` file includes expected columns like:

- Submittal ID
- Submittal Name
- RFI
- Comments
- Decision
- Responsibility

---

## 🛡️ License

Proprietary software developed by **Niti Consulting**.  
All rights reserved. Contact for commercial licensing or integration inquiries.

---

## 📧 Contact

📨 aditya.deshpande@niticonsulting.ai  
🌐 [www.niticonsulting.ai](https://www.niticonsulting.ai) _(Coming Soon)_

---

> 🧠 **Note:** This module is part of the larger **NAVA AI** platform — including Schedule Logic Analyzer, Delay Mapper, and Claims Builder modules.
