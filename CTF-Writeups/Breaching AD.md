
## **CTF Write-Up: NTLM Authentication & LDAP Attacks**

**Author:** [Your Name]  
**Platform:** [Hack The Box / TryHackMe]  
**Category:** Threat Intelligence / SOC Analysis  
**Date:** [Date Completed]  

---

## **1. Introduction**

This CTF focused on **NTLM authentication, password spraying, LDAP authentication weaknesses, and rogue server attacks**. The objective was to enumerate users, exploit authentication weaknesses, and capture credentials across different protocols.

The environment consisted of:
- **Domain Controller** (`THMDC - 10.200.80.101`)
- **Web Server** (`THM IIS - 10.200.80.201`)
- **Attacking System** (Kali/Linux machine)

During this engagement, we:
✅ Verified credential exposures in public breaches.  
✅ Performed **password spraying** to identify valid credentials.  
✅ Exploited **LDAP downgrade attacks** for clear-text authentication.  
✅ Captured and cracked NTLM authentication challenges.  
✅ Extracted credentials from **PXE boot images**.  
✅ Analyzed **McAfee database** to retrieve service account passwords.  

---

## **2. Challenge Questions & Answers**

### **Q1: What popular website can be used to verify if your email address or password has ever been exposed in a publicly disclosed data breach?**

📝 **Answer:** `Have I Been Pwned (https://haveibeenpwned.com/)`

🔍 **How I Found It:**  
- This is a well-known public resource for checking compromised credentials.  
- Often used for OSINT and security awareness.  

---

### **Q2: What is the name of the challenge-response authentication mechanism that uses NTLM?**

📝 **Answer:** `NTLMv2 Challenge-Response`

🔍 **How I Found It:**  
- NTLM authentication operates on a **challenge-response mechanism** where a server sends a challenge, and the client responds with a hashed password.  

---

### **Q3: What is the username of the third valid credential pair found by the password spraying script?**

📝 **Answer:** `gordon.stevens`

🔍 **How I Found It:**  
- Ran a **password spraying attack** using `ntlm_passwordspray.py`.
- The script tested **a username list against a default password** (`Changeme123`).
- The third valid credential pair found was **gordon.stevens**.

**Screenshot:**  ![password spraying results](/mnt/data/Screenshot_20250223_130738.png)  

---

### **Q4: How many valid credential pairs were found by the password spraying script?**

📝 **Answer:** `4`

🔍 **How I Found It:**  
- The output of the **password spraying attack** showed a total of **4 valid credential pairs**.
- Captured credentials were extracted from the script execution logs.

**Screenshot:**  ![password spraying success count](/mnt/data/Screenshot_20250223_130815.png)  

---

### **Q5: What is the message displayed by the web application when authenticating with a valid credential pair?**

📝 **Answer:** `Hello World`

🔍 **How I Found It:**  
- Attempted login using **valid credentials** extracted from password spraying.
- Observed the web application’s response message **upon successful authentication**.

**Screenshot:**  ![authentication success](/mnt/data/Screenshot_20250223_130711.png)  

---

### **Q6: What type of attack can be performed against LDAP authentication systems not commonly found against Windows Authentication systems?**

📝 **Answer:** `LDAP Pass-Back Attack`

🔍 **How I Found It:**  
- Set up a **rogue LDAP server** to capture authentication attempts.  
- Used **netcat** to listen on LDAP port `389` and captured incoming authentication data.  

**Screenshot:**  ![LDAP pass-back attack setup](/mnt/data/Screenshot_20250223_131443.png)  

---

### **Q7: What two authentication mechanisms do we allow on our rogue LDAP server to downgrade the authentication and make it clear text?**

📝 **Answer:** `PLAIN & LOGIN`

🔍 **How I Found It:**  
- Configured **slapd** LDAP server to allow `PLAIN` and `LOGIN` authentication mechanisms.
- Modified **olcSaslSecProps.ldif** to weaken security restrictions.  

**Screenshot:**  ![LDAP authentication downgrade](/mnt/data/Screenshot_20250223_131702.png)  

---

### **Q8: What is the password associated with the svcLDAP account?**

📝 **Answer:** `dappass1@`

🔍 **How I Found It:**  
- Captured authentication traffic using **tcpdump**.
- Extracted **LDAP credentials from network capture**.

**Screenshot:**  ![svcLDAP credentials captured](/mnt/data/Screenshot_20250223_132003.png)  

---

### **Q9: What is the name of the tool we can use to poison and capture authentication requests on the network?**

📝 **Answer:** `Responder`

🔍 **How I Found It:**  
- Used `Responder` to intercept NTLM authentication hashes on the network.  

**Screenshot:**  ![Responder capturing NTLM requests](/mnt/data/Screenshot_20250223_132043.png)  

---

### **Q10: What is the username associated with the challenge that was captured?**

📝 **Answer:** `ZA\svcFileCopy`

🔍 **How I Found It:**  
- Extracted **captured NTLM challenge responses** from Responder logs.  

**Screenshot:**  ![Captured NTLM challenge](/mnt/data/Screenshot_20250223_132115.png)  

---

### **Q11: What is the value of the cracked password associated with the challenge that was captured?**

📝 **Answer:** `Password1!`

🔍 **How I Found It:**  
- Used `hashcat` with NTLM hash mode to **crack the captured challenge response**.  
- Successfully retrieved the plaintext password.  

**Screenshot:**  ![Cracked NTLM hash](/mnt/data/Screenshot_20250223_132158.png)  

---

## **3. Conclusion & Lessons Learned**

- **Summary of findings**: Successfully exploited **NTLM, LDAP, and PXE authentication weaknesses** to extract credentials.  
- **Impact on organization**: These vulnerabilities could allow an **attacker to laterally move** within a network.  
- **Future recommendations**: Implement **multi-factor authentication (MFA), disable NTLM authentication**, and **restrict anonymous LDAP binds**.  

---

## **4. References & Tools Used**
📌 **OSINT Tools**: `Have I Been Pwned`, `ldapsearch`  
📌 **Password Cracking**: `hashcat`, `john the ripper`  
📌 **Network Exploitation**: `Responder`, `CrackMapExec`  
📌 **Microsoft Deployment**: `MDT`, `TFTP`  
📌 **Relevant Articles**: `[Insert any supporting articles]`  

