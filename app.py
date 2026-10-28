import re
import joblib
import streamlit as st
from pathlib import Path


# Page configuration
st.set_page_config(
    page_title="Email Shield | Spam Detection",
    page_icon="🛡️",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
    /* Main page */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
        color: var(--text-color);
    }

    .subtitle {
        text-align: center;
        font-size: 16px;
        margin-bottom: 30px;
        color: var(--text-color);
        opacity: 0.8;
    }

    /* Information cards */
    .info-card {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        padding: 22px;
        border-radius: 14px;
        border: 1px solid var(--text-color);
        margin-bottom: 18px;
    }

    .info-card h3,
    .info-card p {
        color: var(--text-color) !important;
    }

    /* Labels and normal text */
    label,
    .stMarkdown p,
    .stMarkdown h1,
    .stMarkdown h2,
    .stMarkdown h3 {
        color: var(--text-color);
    }

    /* Input fields */
    .stTextInput input,
    .stTextArea textarea {
        color: var(--text-color) !important;
        background-color: var(--secondary-background-color) !important;
        border: 1px solid var(--text-color);
    }

    /* Placeholder text */
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: var(--text-color) !important;
        opacity: 0.65;
    }

    /* Button */
    div.stButton > button {
        width: 100%;
        border-radius: 9px;
        padding: 12px;
        font-weight: 600;
    }

    /* Footer */
    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# Load model
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "model" / "spam_model.pkl"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

try:
    model = load_model()
except Exception:
    st.error("Model not found. Please run: python train_model.py")
    st.stop()


# Phishing warning checker
def check_phishing(message):
    text = message.lower()
    score = 0
    reasons = []

    urgent_words = [
        "urgent", "immediately", "act now",
        "account will be blocked", "account suspended",
        "verify your account", "unusual activity"
    ]

    for word in urgent_words:
        if word in text:
            score += 1
            reasons.append(f"Urgent or alarming language: '{word}'")
            break

    sensitive_words = [
        "password", "bank details", "credit card",
        "otp", "one-time password", "pin number",
        "social security number"
    ]

    for word in sensitive_words:
        if word in text:
            score += 1
            reasons.append(f"Sensitive information mentioned: '{word}'")
            break

    urls = re.findall(r"https?://\S+|www\.\S+", text)

    for url in urls:
        if (
            "bit.ly" in url
            or "tinyurl.com" in url
            or "is.gd" in url
            or "t.co/" in url
            or "@" in url
        ):
            score += 1
            reasons.append("A potentially suspicious link was found.")
            break

    phishing_phrases = [
        "click here to claim",
        "confirm your identity",
        "verify your identity",
        "click the link",
        "your account has been compromised",
        "update your account details",
        "claim your prize"
    ]

    for phrase in phishing_phrases:
        if phrase in text:
            score += 1
            reasons.append(f"Potential phishing phrase: '{phrase}'")
            break

    return score, reasons


# Header
st.markdown(
    '<div class="main-title">🛡️ Email Shield</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Intelligent Email Spam and Phishing Detection System</div>',
    unsafe_allow_html=True
)

st.info(
    "Analyze an email to identify spam and potential phishing warning signs."
)

# Main layout
left, right = st.columns([1.6, 1])

with left:
    st.markdown("### 📩 Analyze an Email")

    subject = st.text_input(
        "Email Subject",
        placeholder="Enter the email subject"
    )

    body = st.text_area(
        "Email Message",
        height=220,
        placeholder="Paste the email message here..."
    )

    analyze = st.button("🔍 Analyze Email")

with right:
    st.markdown("""
    <div class="info-card">
        <h3>🔎 What We Check</h3>
        <p>📨 Spam and unwanted messages</p>
        <p>⚠️ Suspicious wording and urgent requests</p>
        <p>🔗 Potentially suspicious links</p>
        <p>🔐 Requests for sensitive information</p>
    </div>

    <div class="info-card">
        <h3>⚙️ Technology Used</h3>
        <p>Python</p>
        <p>Scikit-learn and TF-IDF</p>
        <p>Naive Bayes classifier</p>
        <p>Streamlit interface</p>
    </div>
    """, unsafe_allow_html=True)


# Analyze email
if analyze:
    message = (subject.strip() + " " + body.strip()).strip()

    if not message:
        st.warning("Please enter an email subject or message.")

    else:
        prediction = model.predict([message])[0]
        phishing_score, reasons = check_phishing(message)

        st.markdown("---")
        st.markdown("## 📊 Analysis Result")

        if phishing_score >= 2:
            st.error("⚠️ Phishing / Suspicious Email")
            st.write(
                "Multiple warning signs were detected. "
                "Avoid clicking links or sharing sensitive information."
            )

        elif prediction == "phishing":
            st.error("⚠️ Phishing / Suspicious Email")
            st.write(
                "The machine-learning model classified this message "
                "as phishing. Review it carefully."
            )

        elif prediction == "spam":
            st.warning("📨 Spam Email")
            st.write(
                "The machine-learning model classified this message as spam."
            )

        elif phishing_score == 1:
            st.warning("⚠️ Suspicious Email — Review Carefully")
            st.write(
                "One warning sign was detected. This does not prove "
                "the email is malicious."
            )

        else:
            st.success("✅ Likely Legitimate Email")
            st.write(
                "The model classified this message as legitimate, "
                "and no major warning signs were detected."
            )

        if reasons:
            st.markdown("### 🚩 Detected Warning Signs")
            for reason in reasons:
                st.write(f"- {reason}")

        st.caption(
            "Security note: This application provides an automated estimate. "
            "A legitimate result does not guarantee that an email is safe."
        )


# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align:center;color:#64748b;">'
    'Email Shield | Machine Learning Project'
    '</p>',
    unsafe_allow_html=True
)