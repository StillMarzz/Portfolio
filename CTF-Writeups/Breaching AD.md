# **CTF Write-Up: NTLM Authentication & LDAP Attacks**

**Author:** StillMarzz(Sl1M)  
**Platform:** TryHackMe
**Category:** Exploiting Active Directory  
**Date:** 2/23/2025

---

## **1. Introduction**

This CTF walkthrough demonstrates various authentication-based attacks in an Active Directory environment, highlighting weaknesses in **NTLM authentication, password spraying, LDAP pass-back attacks, and credential extraction from PXE boot images and databases**.

The simulated environment consists of:
- **Domain Controller** (`THMDC - 10.200.80.101`)
- **Web Server** (`THM IIS - 10.200.80.201`)
- **PXE Boot Server** (`THM MDT - 10.200.80.202`)
- **Attacking System** (Kali/Linux machine)

### **Objectives**
✅ Enumerate NTLM authentication mechanisms  
✅ Exploit weak credentials via password spraying  
✅ Capture NTLM authentication hashes via LDAP attacks  
✅ Extract stored credentials from PXE boot images  
✅ Analyze sensitive credentials in the McAfee database  

---

## **2. Reconnaissance & Initial Access**

The first step was verifying if the **targeted domain name resolution** was correctly set. We configured our DNS settings to use the domain controller (`10.200.80.101`).

**Screenshot:**  ![DNS Setup](screenshots//Screenshot_20250223_130420.png)  

Once configured, an **nslookup query** was performed to validate DNS resolution.

**Screenshot:**  ![nslookup query](screenshots//Screenshot_20250223_130506.png)  

We then checked for previously compromised credentials using the public breach-checking site:

**Q1: What popular website can be used to verify if your email address or password has ever been exposed in a publicly disclosed data breach?**
📝 **Answer:** `haveibeenpwned`

---

## **3. Password Spraying Attack**

To identify weak credentials, we attempted a **password spraying attack** against NTLM authentication.

**Q2: What is the name of the challenge-response authentication mechanism that uses NTLM?**
📝 **Answer:** `netntlm`

Using an **NTLM password spraying script**, we tested a default password (`Changeme123`) against a list of known usernames.

**Screenshot:**  ![Password Spraying Script](screenshots//Screenshot_20250223_130738.png)  

The attack was **successful**, revealing **four valid credential pairs**:
- **Third Valid Username:** `gordon.stevens`
- **Total Valid Credentials Found:** `4`

**Screenshot:**  ![Successful Logins](screenshots//Screenshot_20250223_130815.png)  

Testing one of the compromised accounts on the **NTLM-secured web application** displayed the following response:

**Q5: What is the message displayed by the web application when authenticating with a valid credential pair?**
📝 **Answer:** `Hello World`

**Screenshot:**  ![Successful Authentication](screenshots//Screenshot_20250223_130711.png)  

---

## **4. LDAP Pass-Back Attack**

Next, we targeted **LDAP authentication vulnerabilities** by setting up a **rogue LDAP server** to capture plaintext credentials.

**Q6: What type of attack can be performed against LDAP Authentication systems not commonly found against Windows Authentication systems?**
📝 **Answer:** `ldap pass-back attack`

We allowed **`login` and `plain` authentication mechanisms** to force unencrypted logins.

**Screenshot:**  ![LDAP Capture Setup](screenshots//Screenshot_20250223_131411.png)  

Captured credentials:
- **Username:** `svcLDAP`
- **Password:** `tryhackmeldappass1@`

**Screenshot:**  ![Captured Credentials](screenshots//Screenshot_20250223_132003.png)  

---

## **5. NTLM Authentication Poisoning**

To capture **NTLM authentication hashes**, we deployed **Responder**.

**Q9: What is the name of the tool we can use to poison and capture authentication requests on the network?**
📝 **Answer:** `responder`

**Screenshot:**  ![Responder Setup](screenshots//Screenshot_20250223_132043.png)  

Captured credentials:
- **Username:** `svcFileCopy`
- **Cracked Password:** `FPassword1!`

**Screenshot:**  ![Cracked Hash](screenshots//Screenshot_20250223_132158.png)  

---

## **6. PXE Boot Image Credential Extraction**

Using **TFTP**, we retrieved PXE Boot configuration files to extract credentials.

**Q12: What Microsoft tool is used to create and host PXE Boot images in organisations?**
📝 **Answer:** `Microsoft Deployment Toolkit`

**Q13: What network protocol is used for recovery of files from the MDT server?**
📝 **Answer:** `TFTP`

Extracted credentials:
- **Username:** `svcMDT`
- **Password:** `PXEBootSecure1@`

**Screenshot:**  ![Extracted PXE Credentials](screenshots//Screenshot_20250223_134019.png)  

---

## **7. McAfee Database Credential Extraction**

Extracting stored credentials from the McAfee **`ma.db`** database.

**Q18: What table in this database stores the credentials of the orchestrator?**
📝 **Answer:** `AGENT_REPOSITORIES`

Decrypted credentials using a python script ![Mcafee-sitelist-pwd-decryption](https://github.com/funoverip/mcafee-sitelist-pwd-decryption):
- **Username:** `svcAV`
- **Password:** `MyStrongPassword!`

**Screenshot:**  ![Decrypted Credentials](screenshots//Screenshot_20250223_134552.png)  

---

## **8. Conclusion & Lessons Learned**

### **Key Findings:**
- Weak passwords enabled **password spraying attacks**.
- **LDAP authentication** was vulnerable to **pass-back attacks**, exposing plaintext credentials.
- **NTLM authentication poisoning** allowed **credential interception and cracking**.
- **PXE boot images stored domain admin-level credentials**.
- **McAfee database contained stored credentials**, which were easily decrypted.

### **Mitigation Strategies:**
✅ Enforce strong passwords & eliminate default credentials  
✅ Disable NTLM authentication where possible  
✅ Enforce LDAP signing & channel binding  
✅ Restrict access to PXE boot files and encrypt stored credentials  
✅ Secure McAfee configurations by hashing and salting stored passwords  

🚀 **Stay secure, and keep hacking!**

