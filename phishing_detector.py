"""
==============================================
  Phishing Email Detection Model
  Thiranex Cybersecurity Internship — Task 3
  Author: Srushti | B.Tech CSE (AI/ML), JSPM University Pune
==============================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.pipeline import Pipeline
from scipy.sparse import hstack
import datetime

# ─────────────────────────────────────────────
#  DATASET (built-in, no download needed!)
# ─────────────────────────────────────────────

PHISHING_EMAILS = [
    "Urgent: Your account has been compromised. Click here to verify your password immediately http://malicious-login.com/verify",
    "Congratulations! You've won $1,000,000. Claim your prize now at http://fakeprize.net/claim",
    "Your PayPal account is suspended. Login now to restore access http://paypal-fake.com/login",
    "ALERT: Unusual sign-in activity detected. Confirm your identity http://secure-fake.xyz/confirm",
    "Dear customer, your bank account will be closed. Update info at http://bank-fake.com/update",
    "You have a pending package delivery. Confirm address here http://delivery-phish.com/track",
    "Your Netflix subscription has expired. Renew now http://netflix-fake.net/renew",
    "Action required: Verify your email address to avoid account deletion http://verify-now.xyz",
    "IRS Tax Refund: You are eligible for $3,200 refund. Claim at http://irs-fake.com/refund",
    "Your Apple ID has been locked. Unlock it here http://apple-id-fake.com/unlock",
    "Security breach detected on your account. Reset password immediately http://reset-fake.net",
    "FREE iPhone 15 giveaway! You have been selected. Click http://free-iphone-fake.com/win",
    "Your credit card has been charged $500. Dispute this charge http://dispute-fake.com",
    "Verify your identity or your account will be terminated http://id-verify-fake.xyz/check",
    "You have unclaimed lottery winnings! Collect now http://lottery-phish.net/collect",
    "Dear user, click to confirm your subscription renewal http://sub-renew-fake.com/confirm",
    "Your password expires today! Update now at http://password-fake.com/update",
    "Exclusive offer just for you! Limited time deal http://exclusive-fake.net/offer",
    "Your account shows suspicious activity. Verify immediately http://phish-verify.com",
    "Amazon: Your order has been cancelled. Login to resolve http://amazon-fake.net/order",
    "Win a luxury vacation by clicking here http://vacation-win-fake.com/prize",
    "Your social security number has been compromised http://ssn-protect-fake.com",
    "Urgent payment required to avoid service suspension http://pay-urgent-fake.com",
    "Claim your government stimulus check now http://stimulus-fake.gov-phish.com",
    "Your email storage is full. Click to upgrade for free http://email-upgrade-fake.com",
    "Dear valued customer, unusual login detected verify now http://login-verify-phish.xyz",
    "You have been selected for a special reward click here to claim http://reward-fake.net",
    "Warning your computer has virus click to remove http://virus-remove-fake.com",
    "Confirm your account details to continue using our service http://confirm-phish.com",
    "Your investment account needs immediate attention http://invest-fake.com/urgent",
    "Click to receive your tax return refund today http://tax-refund-phish.com",
    "Your insurance policy is expiring renew immediately http://insurance-fake.net",
    "Validate your email now or lose access http://email-validate-fake.com",
    "Exclusive crypto investment opportunity click now http://crypto-fake.net/invest",
    "Your account was accessed from unknown device verify http://device-verify-phish.com",
    "Final warning your account will be deleted http://final-warning-fake.com",
    "Claim free gift card today limited offer http://giftcard-fake.net/claim",
    "Your loan has been approved click to receive funds http://loan-approved-fake.com",
    "Suspicious transaction on your account click to review http://transaction-phish.com",
    "Update your payment method to avoid interruption http://payment-update-fake.net",
]

SAFE_EMAILS = [
    "Hi team, please find attached the meeting notes from yesterday's standup. Let me know if you have any questions.",
    "Dear Srushti, your interview has been scheduled for Monday at 10am. Please confirm your availability.",
    "Monthly newsletter: Check out our latest blog posts and product updates for this month.",
    "Your order #12345 has been shipped and will arrive by Friday. Track your order on our website.",
    "Reminder: Project deadline is next Friday. Please submit your work before 5pm.",
    "Welcome to our platform! Here are some tips to get started with your new account.",
    "Thank you for your purchase. Your receipt is attached to this email for your records.",
    "Team lunch is scheduled for Thursday at 1pm in the conference room. Please RSVP by Wednesday.",
    "Your appointment with Dr. Smith is confirmed for tomorrow at 2:30pm at the clinic.",
    "Here is your monthly bank statement for the period ending March 31st. Please review it.",
    "Congratulations on completing the course! Your certificate is attached to this email.",
    "The quarterly report is ready for review. Please check the shared folder for the document.",
    "Happy Birthday! Wishing you a wonderful day filled with joy and celebration.",
    "Your flight booking confirmation for May 15th Mumbai to Delhi is attached.",
    "Please find the updated project timeline attached. Let us know if you have feedback.",
    "Your library books are due next week. Please return or renew them before the due date.",
    "Thanks for attending our webinar today. Here is the recording link for future reference.",
    "Reminder to submit your timesheet by end of day Friday for payroll processing.",
    "Your annual performance review is scheduled for next Tuesday with your manager.",
    "The new office policy documents have been updated. Please read and acknowledge them.",
    "Your subscription to our premium plan has been successfully renewed for another year.",
    "We noticed you left items in your cart. Here is your saved cart for your convenience.",
    "Your feedback form has been received. Thank you for helping us improve our services.",
    "Good morning team, here is the agenda for today's all-hands meeting at 10am.",
    "Your gym membership is due for renewal next month. Visit the reception to renew.",
    "Here are the class notes from today's lecture on machine learning fundamentals.",
    "Your internship offer letter is attached. Please sign and return by next Monday.",
    "The hackathon results are out. Congratulations to all participants for their hard work.",
    "Please review the attached proposal and share your comments by Thursday afternoon.",
    "Your annual subscription invoice is attached for your accounting records this quarter.",
    "Team outing is planned for Saturday. Please fill out the availability form by Wednesday.",
    "Your research paper submission has been received and is under review by the committee.",
    "Reminder your car service appointment is tomorrow at 9am at the service center.",
    "The updated employee handbook is now available on the company intranet portal.",
    "Your scholarship application has been received and will be reviewed within two weeks.",
    "Please join the video call at 3pm today using the link shared in the calendar invite.",
    "Your package has been delivered and left at your doorstep as per your instructions.",
    "The new software update is available. Please update your system at your convenience.",
    "Thank you for volunteering at our community event last weekend. We appreciate your help.",
    "Your annual health checkup reminder is attached with the list of recommended tests.",
]

# ─────────────────────────────────────────────
#  FEATURE ENGINEERING
# ─────────────────────────────────────────────

def extract_features(emails):
    features = []
    for email in emails:
        url_count = len(re.findall(r'http[s]?://', email))
        has_urgent = int(bool(re.search(r'\b(urgent|immediately|alert|warning|suspend|verify|confirm|action required)\b', email, re.I)))
        has_money = int(bool(re.search(r'\b(free|win|prize|reward|cash|dollar|refund|lottery|claim)\b', email, re.I)))
        has_threat = int(bool(re.search(r'\b(delete|terminate|expire|blocked|locked|compromised|breach)\b', email, re.I)))
        exclamation_count = email.count('!')
        word_count = len(email.split())
        has_ip_url = int(bool(re.search(r'http[s]?://\d+\.\d+\.\d+\.\d+', email)))
        suspicious_tld = int(bool(re.search(r'http[s]?://\S+\.(xyz|net|info|biz|fake|phish)\b', email, re.I)))

        features.append([
            url_count,
            has_urgent,
            has_money,
            has_threat,
            exclamation_count,
            word_count,
            has_ip_url,
            suspicious_tld,
        ])
    return np.array(features)


# ─────────────────────────────────────────────
#  BUILD DATASET
# ─────────────────────────────────────────────

print("=" * 55)
print("  🔐 Phishing Email Detection Model")
print("  Thiranex Cybersecurity Internship — Task 3")
print("=" * 55)

emails = PHISHING_EMAILS + SAFE_EMAILS
labels = [1] * len(PHISHING_EMAILS) + [0] * len(SAFE_EMAILS)  # 1 = Phishing, 0 = Safe

df = pd.DataFrame({'email': emails, 'label': labels})
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle

print(f"\n[📊] Dataset loaded:")
print(f"     Total emails  : {len(df)}")
print(f"     Phishing      : {sum(labels)}")
print(f"     Safe          : {len(labels) - sum(labels)}")

# ─────────────────────────────────────────────
#  SPLIT DATA
# ─────────────────────────────────────────────

X_text = df['email']
X_manual = extract_features(df['email'].tolist())
y = df['label']

X_text_train, X_text_test, X_manual_train, X_manual_test, y_train, y_test = train_test_split(
    X_text, X_manual, y, test_size=0.2, random_state=42, stratify=y
)

print(f"\n[✂️]  Train/Test Split:")
print(f"     Training samples : {len(y_train)}")
print(f"     Testing samples  : {len(y_test)}")

# ─────────────────────────────────────────────
#  TF-IDF + FEATURE COMBINATION
# ─────────────────────────────────────────────

print("\n[⚙️]  Extracting TF-IDF features...")
tfidf = TfidfVectorizer(max_features=500, stop_words='english', ngram_range=(1, 2))
X_tfidf_train = tfidf.fit_transform(X_text_train)
X_tfidf_test = tfidf.transform(X_text_test)

from scipy.sparse import csr_matrix
X_train_combined = hstack([X_tfidf_train, csr_matrix(X_manual_train)])
X_test_combined = hstack([X_tfidf_test, csr_matrix(X_manual_test)])

# ─────────────────────────────────────────────
#  TRAIN MODEL
# ─────────────────────────────────────────────

print("[🤖] Training Random Forest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_combined, y_train)

# ─────────────────────────────────────────────
#  EVALUATE
# ─────────────────────────────────────────────

y_pred = model.predict(X_test_combined)
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=["Safe", "Phishing"])

print(f"\n{'='*55}")
print(f"  ✅ Model Accuracy: {accuracy * 100:.2f}%")
print(f"{'='*55}")
print("\n[📋] Classification Report:")
print(report)
print("[📊] Confusion Matrix:")
print(cm)

# ─────────────────────────────────────────────
#  SAVE CONFUSION MATRIX PLOT
# ─────────────────────────────────────────────

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Safe', 'Phishing'],
            yticklabels=['Safe', 'Phishing'])
plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n[✅] Confusion matrix saved as: confusion_matrix.png")

# ─────────────────────────────────────────────
#  TEST ON CUSTOM EMAILS
# ─────────────────────────────────────────────

def predict_email(email_text):
    tfidf_feat = tfidf.transform([email_text])
    manual_feat = csr_matrix(extract_features([email_text]))
    combined = hstack([tfidf_feat, manual_feat])
    prediction = model.predict(combined)[0]
    probability = model.predict_proba(combined)[0]
    return {
        "label": "🚨 PHISHING" if prediction == 1 else "✅ SAFE",
        "confidence": f"{max(probability) * 100:.1f}%",
        "raw": prediction
    }

test_samples = [
    "Urgent! Your account has been compromised. Click here to verify immediately http://fake-login.com",
    "Hi, please find attached the meeting notes from our call yesterday. Let me know if you have questions.",
    "Congratulations you won a free iPhone click here to claim your prize http://free-iphone-fake.net",
    "Your order has been shipped and will arrive by Friday. Thank you for shopping with us.",
]

print("\n[🧪] Testing on sample emails:")
print("-" * 55)
results = []
for i, email in enumerate(test_samples):
    result = predict_email(email)
    print(f"\nEmail {i+1}: {email[:60]}...")
    print(f"  → Prediction : {result['label']}")
    print(f"  → Confidence : {result['confidence']}")
    results.append({"email": email, "label": result["label"], "confidence": result["confidence"]})

# ─────────────────────────────────────────────
#  HTML REPORT
# ─────────────────────────────────────────────

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

test_rows_html = "".join([
    f"""<tr>
        <td style="max-width:400px; font-size:13px;">{r['email'][:80]}...</td>
        <td><span class="badge {'badge-bad' if 'PHISHING' in r['label'] else 'badge-good'}">{r['label']}</span></td>
        <td style="font-family:monospace;">{r['confidence']}</td>
    </tr>"""
    for r in results
])

html_report = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Phishing Detection Report</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: system-ui, -apple-system, sans-serif; background: #f5f5f0; color: #1a1a18; padding: 2rem 1rem; }}
    .wrapper {{ max-width: 800px; margin: 0 auto; }}
    header {{ margin-bottom: 1.5rem; }}
    header h1 {{ font-size: 22px; font-weight: 500; }}
    header p {{ font-size: 14px; color: #777; margin-top: 4px; }}
    .card {{ background: #fff; border: 0.5px solid rgba(0,0,0,0.12); border-radius: 12px; padding: 1.25rem; margin-bottom: 12px; }}
    .card-title {{ font-size: 11px; color: #999; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 12px; }}
    .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; }}
    .stat-box {{ background: #f5f5f0; border-radius: 10px; padding: 1rem; text-align: center; }}
    .stat-num {{ font-size: 32px; font-weight: 700; }}
    .stat-lbl {{ font-size: 12px; color: #777; margin-top: 4px; }}
    .badge {{ font-size: 11px; padding: 3px 10px; border-radius: 20px; font-weight: 600; display: inline-block; }}
    .badge-good {{ background: #eaf3de; color: #0f6e56; }}
    .badge-bad {{ background: #fcebeb; color: #a32d2d; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid #eee; color: #999; font-size: 11px; text-transform: uppercase; }}
    td {{ padding: 10px; border-bottom: 0.5px solid #f0f0ec; vertical-align: top; }}
    tr:last-child td {{ border-bottom: none; }}
    .cm-img {{ width: 100%; max-width: 400px; display: block; margin: 0 auto; border-radius: 8px; }}
    footer {{ text-align: center; font-size: 12px; color: #aaa; margin-top: 2rem; }}
  </style>
</head>
<body>
<div class="wrapper">
  <header>
    <h1>📧 Phishing Email Detection Report</h1>
    <p>Generated: {timestamp} &nbsp;|&nbsp; Thiranex Cybersecurity Internship — Task 3</p>
  </header>

  <div class="card">
    <p class="card-title">Model Performance</p>
    <div class="stat-grid">
      <div class="stat-box">
        <div class="stat-num" style="color:#0f6e56">{accuracy*100:.1f}%</div>
        <div class="stat-lbl">Accuracy</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">{len(df)}</div>
        <div class="stat-lbl">Total Emails</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">{len(PHISHING_EMAILS)}</div>
        <div class="stat-lbl">Phishing Samples</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">{len(SAFE_EMAILS)}</div>
        <div class="stat-lbl">Safe Samples</div>
      </div>
    </div>
  </div>

  <div class="card">
    <p class="card-title">Confusion Matrix</p>
    <img src="confusion_matrix.png" alt="Confusion Matrix" class="cm-img"/>
    <p style="text-align:center; font-size:12px; color:#999; margin-top:8px;">Rows = Actual | Columns = Predicted</p>
  </div>

  <div class="card">
    <p class="card-title">Sample Email Predictions</p>
    <table>
      <thead><tr><th>Email Preview</th><th>Prediction</th><th>Confidence</th></tr></thead>
      <tbody>{test_rows_html}</tbody>
    </table>
  </div>

  <div class="card">
    <p class="card-title">About the Model</p>
    <table>
      <tr><td style="color:#777; width:180px;">Algorithm</td><td>Random Forest Classifier</td></tr>
      <tr><td style="color:#777;">Text Features</td><td>TF-IDF (500 features, bigrams)</td></tr>
      <tr><td style="color:#777;">Custom Features</td><td>URL count, urgency words, money words, threats, suspicious TLDs</td></tr>
      <tr><td style="color:#777;">Train/Test Split</td><td>80% / 20%</td></tr>
      <tr><td style="color:#777;">Library</td><td>Scikit-learn 1.6</td></tr>
    </table>
  </div>

  <footer>Phishing Email Detection Model &mdash; Thiranex Cybersecurity Internship &mdash; Srushti</footer>
</div>
</body>
</html>"""

with open("phishing_report.html", "w") as f:
    f.write(html_report)

print("\n[✅] HTML Report saved as: phishing_report.html")
print("\n✅ All done! Open 'phishing_report.html' in your browser.")
print("=" * 55)