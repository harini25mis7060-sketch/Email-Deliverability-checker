import re
import smtplib
import time
import dns.resolver
import streamlit as st

st.title("Email Deliverability Checker")

text = st.text_area("Paste email addresses (one per line):", height=150)

def check_email(email):
    # 1. Syntax check
    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return "Likely to bounce", "Invalid format"

    domain = email.split("@")[1].strip()

    # 2. MX record lookup & priority sorting
    try:
        answers = dns.resolver.resolve(domain, "MX")
        sorted_records = sorted(answers, key=lambda r: r.preference)
        mx_host = str(sorted_records[0].exchange).rstrip(".")
    except Exception:
        return "Likely to bounce", "Domain or mail server does not exist"

    # 3. SMTP probe
    server = None
    try:
        server = smtplib.SMTP(timeout=6)
        server.connect(mx_host, 25)
        server.helo("verify-app.local")
        server.mail("check@verify-app.local")
        code, _ = server.rcpt(email)
        server.quit()

        if code == 250:
            return "Likely to be delivered", f"Accepted by {mx_host} (250 OK)"
        elif code in (550, 551, 552, 553, 554, 501):
            return "Likely to bounce", f"Mailbox rejected ({code})"
        elif code in (421, 450, 451, 452):
            return "Unknown", f"Rate-limited/greylisted ({code})"
        return "Unknown", f"Server response: {code}"

    except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
        return "Unknown", "Server disconnected (anti-scraping protection)"
    except Exception:
        return "Unknown", "Connection timed out (Port 25 throttled or blocked)"
    finally:
        if server:
            try:
                server.close()
            except Exception:
                pass


if st.button("Check Deliverability"):
    emails = [e.strip() for e in text.splitlines() if e.strip()]
    results = []

    progress_bar = st.progress(0)
    for idx, email in enumerate(emails):
        status, reason = check_email(email)
        results.append({"Email": email, "Status": status, "Details": reason})
        
        # 1-second delay between checks to avoid immediate rate-limiting
        if idx < len(emails) - 1:
            time.sleep(1.0)
            
        progress_bar.progress((idx + 1) / len(emails))

    st.table(results)