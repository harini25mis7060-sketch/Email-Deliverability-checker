# Email-Deliverability-checker:-

Email-Deliverability-checker is a lightweight web application built with Python and Streamlit that evaluates 
a list of email addresses and reports whether each address is **Likely to be delivered**, **Likely to bounce** or **Unknown**.

# Live Demo:-
For a live demo of how the app works it is available at : **https://email-deliverability-checker.streamlit.app/**


# How It Works:-
The app evaluates email addresses across three verification stages without sending any actual emails:

1. **Syntax Check**: Validates RFC compliance (structure, `@` symbol, domain format).
2. **DNS & Mail Exchange Verification**: Queries domain name servers to verify domain registration and active Mail Exchanger (MX) records.
3. **SMTP Handshake Probe**: Initiates an SMTP connection to the destination mail server and issues `HELO`, `MAIL FROM`, and `RCPT TO`
    commands to check mailbox status,
5. then terminates the connection before any message is sent.

# Local Setup
1.)Clone the repository: Download the project files to your computer by running :
  **git clone https://github.com/harini25mis7060-sketch/Email-Deliverability-checker.git**
  
2.)Navigate into the project folder by running cd Email-Deliverability-checker.

3.)Install all required Python packages by running pip install -r requirements.txt.

4.)Launch the application in your browser by running python -m streamlit run app.py.


# Status Definitions:-
1.) **Likely to be delivered**: The destination mail server explicitly accepted the recipient address (`250 OK`).
2.) **Likely to bounce**: Syntax is invalid, the domain does not exist, no mail exchange servers exist, or the mail server returned
  an explicit rejection (`550 / 554 Mailbox not found`).
3.) **Unknown**: Verification could not be conclusively determined.


# Deployed App Limitations:-
Cloud hosting platforms block outbound traffic .The cloud provider's firewall acts like a locked door.
Whenever the program tries to open a connection specifically on Port 25, the cloud host immediately drops the request.

# What the Deployed Version Can Check:
-  Malformed or invalid email syntax (Likely to bounce)
-  Non-existent domains or missing MX records (Likely to bounce)
-  Disposable/burner email domains (Likely to bounce)

# What the Deployed Version Cannot Check:
- Live Mailbox Existence Probe (Port 25): Because cloud providers block direct outbound SMTP(simple mail transfer protocol) traffic on port 25.
-  the handshake to verify individual mailbox existence will time out. For valid domains, the status will correctly report as **Unknown**.
- Anti-Harvester Mail Servers: Major providers deliberately do not verify individual recipients
-  At the SMTP stage to protect users from address scraping.

 **Note**: To observe live SMTP responses for addresses that accept recipient probes,run the application locally 
  on a network where port 25 is not restricted by the internet service provider.




