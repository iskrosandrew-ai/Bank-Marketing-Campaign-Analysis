import streamlit as st
import streamlit.components.v1 as components
import os

def render_footer():
    """Renders a professional footer with Andrew Iskros's credentials and embedded Digital CV."""
    st.write("---")
    
    # Footer Styling
    st.markdown("""
    <style>
        .author-footer {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 1.8rem 2rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            color: #F8FAFC;
        }
        .author-name {
            font-size: 1.35rem;
            font-weight: 700;
            color: #38BDF8;
            margin-bottom: 0.2rem;
        }
        .author-role {
            font-size: 0.95rem;
            color: #94A3B8;
            margin-bottom: 0.8rem;
        }
        .cred-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 0.5rem;
        }
        .cred-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.2);
            padding: 5px 12px;
            border-radius: 9999px;
            color: #CBD5E1;
            font-size: 0.82rem;
        }
        .author-links {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 1rem;
        }
        .author-link-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #0F172A;
            border: 1px solid #334155;
            padding: 7px 14px;
            border-radius: 9999px;
            color: #E2E8F0;
            font-size: 0.85rem;
            text-decoration: none;
            transition: all 0.2s ease;
        }
        .author-link-pill:hover {
            border-color: #38BDF8;
            color: #38BDF8;
            transform: translateY(-2px);
        }
    </style>
    
    <div class="author-footer">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:18px;">
            <div style="flex:1; min-width:280px;">
                <div class="author-name">👨‍💼 Andrew Iskros</div>
                <div class="author-role">Business Analyst · Technical Account Manager · Digital Marketing & AI Specialist</div>
                <div style="font-size:0.85rem; color:#64748B; margin-bottom:0.6rem;">📍 Trento, Italy · Business × Technology × AI</div>
            </div>
            <div style="flex:1; min-width:280px;">
                <div style="font-size:0.78rem; color:#64748B; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">Academic Credentials</div>
                <div class="cred-row">
                    <span class="cred-pill">🎓 MSc International Management — Univ. of Trento (103/110)</span>
                    <span class="cred-pill">🎓 BSc Business Information Systems — AAST (GPA 3.96/4.0)</span>
                    <span class="cred-pill">🎓 Diploma in Data Science & ML — EPSILON Global</span>
                    <span class="cred-pill">🌍 Erasmus+ — Univ. de Valladolid, Spain</span>
                </div>
                <div style="font-size:0.78rem; color:#64748B; text-transform:uppercase; letter-spacing:1px; margin-top:10px; margin-bottom:6px;">International Experience</div>
                <div class="cred-row">
                    <span class="cred-pill">🏎️ Ferrari — Marketing & Branding</span>
                    <span class="cred-pill">🚗 BMW — Int'l Business Management</span>
                    <span class="cred-pill">🏦 Intesa Sanpaolo — Credit & Loans</span>
                    <span class="cred-pill">🏭 Duravit — Supply Chain</span>
                </div>
            </div>
        </div>
        <div class="author-links">
            <a class="author-link-pill" href="mailto:iskrosandrew@gmail.com" target="_blank">✉️ iskrosandrew@gmail.com</a>
            <a class="author-link-pill" href="tel:+393896631688">📞 +39 389 663 1688</a>
            <a class="author-link-pill" href="https://www.linkedin.com/in/andrew-iskros-355352b0/" target="_blank">💼 LinkedIn</a>
            <a class="author-link-pill" href="https://github.com/iskrosandrew-ai" target="_blank">💻 GitHub</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Embedded Interactive Digital CV
    cv_path = "Andrew Iskros - Digital CV (1).html"
    if os.path.exists(cv_path):
        with open(cv_path, "r", encoding="utf-8") as f:
            cv_html = f.read()
            
        with st.expander("📄 View Full Interactive Digital CV — Andrew Iskros", expanded=False):
            st.download_button(
                label="📥 Download Digital CV (Standalone HTML)",
                data=cv_html,
                file_name="Andrew_Iskros_Digital_CV.html",
                mime="text/html",
                use_container_width=True
            )
            components.html(cv_html, height=750, scrolling=True)
            
    st.markdown(
        "<div style='text-align:center; color:#475569; font-size:0.78rem; padding:12px 0;'>"
        "© 2026 Andrew Iskros · Bank Marketing Intelligence Hub · AI Diploma Project · EPSILON Global"
        "</div>",
        unsafe_allow_html=True
    )
