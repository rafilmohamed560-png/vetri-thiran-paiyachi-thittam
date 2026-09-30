from __future__ import annotations

import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv

from utils.document_utils import format_html_preview
from utils.exporters import format_docx, format_pdf, format_txt

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .hero {
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #111827, #1f2937);
        color: white;
        margin-bottom: 1rem;
    }
    .hero h1 { margin: 0; }
    .hero p { margin: .35rem 0 0; color: #d1d5db; }
    .preview {
        background: #111827;
        color: #f3f4f6;
        border-radius: 12px;
        padding: 1.25rem;
        max-height: 600px;
        overflow-y: auto;
        border: 1px solid #374151;
    }
    .preview p, .preview h3 { color: #f3f4f6; }
    .notice {
        padding: .8rem 1rem;
        border-radius: 10px;
        background: #fff7ed;
        border: 1px solid #fed7aa;
        color: #7c2d12;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>⚖️ LegalEase AI</h1>
      <p>AI-assisted legal document drafting, editing and export.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="notice"><strong>Legal notice:</strong> LegalEase creates drafts and '
    'legal information for assistance. It is not a law firm or a substitute for advice '
    'from a qualified lawyer.</div>',
    unsafe_allow_html=True,
)
st.write("")

if "document" not in st.session_state:
    st.session_state.document = ""
if "generated_type" not in st.session_state:
    st.session_state.generated_type = "Legal Document"
if "terms" not in st.session_state:
    st.session_state.terms = ""

left, right = st.columns([1, 1.35], gap="large")

with left:
    st.subheader("Document details")
    document_type = st.selectbox(
        "Document type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement",
            "Residential Lease Agreement",
            "Employment Offer Letter",
            "Service Agreement",
            "Freelance Work Contract",
            "Partnership Agreement",
            "General Agreement",
        ],
    )
    custom_type = st.text_input("Or enter a custom document type")
    if custom_type.strip():
        document_type = custom_type.strip()

    parties = st.text_area(
        "Parties involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=110,
    )
    terms = st.text_area(
        "Terms & conditions",
        value=st.session_state.terms,
        placeholder="Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice",
        height=150,
        help="Separate each term with a semicolon.",
    )
    effective_date = st.date_input("Effective date", value=date.today())
    extra = st.text_area(
        "Additional instructions (optional)",
        placeholder="Use a formal structure. Include signature blocks.",
        height=100,
    )

    generate = st.button("✨ Generate Document", type="primary", use_container_width=True)

    if generate:
        if not parties.strip() or not terms.strip():
            st.error("Please provide the parties and at least one term.")
        else:
            payload = {
                "document_type": document_type,
                "parties": parties,
                "terms": terms,
                "effective_date": effective_date.isoformat(),
                "extra_instructions": extra,
            }
            try:
                with st.spinner("Generating your legal draft..."):
                    response = requests.post(
                        f"{BACKEND_URL}/generate",
                        json=payload,
                        timeout=120,
                    )
                if response.ok:
                    data = response.json()
                    st.session_state.document = data["content"]
                    st.session_state.generated_type = document_type
                    st.session_state.terms = terms
                    st.success(
                        "Document generated "
                        + ("in demo mode." if data.get("demo_mode") else "with Gemini.")
                    )
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text
                    st.error(f"Backend error: {detail}")
            except requests.RequestException as exc:
                st.error(
                    "Could not connect to the FastAPI backend. Start it with "
                    "`uvicorn backend.main:app --reload`."
                )
                st.caption(str(exc))

with right:
    st.subheader("Editable preview")
    if st.session_state.document:
        edited = st.text_area(
            "Edit the generated document before exporting",
            value=st.session_state.document,
            height=520,
            label_visibility="collapsed",
        )
        st.session_state.document = edited

        st.markdown("#### Styled preview")
        st.markdown(
            f'<div class="preview">{format_html_preview(st.session_state.document)}</div>',
            unsafe_allow_html=True,
        )

        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button(
                "⬇️ TXT",
                data=format_txt(st.session_state.document),
                file_name="legalease_document.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with c2:
            st.download_button(
                "⬇️ DOCX",
                data=format_docx(
                    st.session_state.document,
                    st.session_state.generated_type,
                    st.session_state.terms,
                ),
                file_name="legalease_document.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        with c3:
            st.download_button(
                "⬇️ PDF",
                data=format_pdf(
                    st.session_state.document,
                    st.session_state.generated_type,
                    st.session_state.terms,
                ),
                file_name="legalease_document.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    else:
        st.info("Your generated document will appear here. You can edit it before downloading.")
