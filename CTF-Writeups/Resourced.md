
# Resourced.local Domain Compromise

## 1. Overview

This assessment simulated an internal threat actor compromising a Windows Active Directory environment through credential abuse and privilege escalation via misconfigured Active Directory permissions. The attacker escalated privileges from a domain user to full control over the Domain Controller.

---

## 2. Initial Enumeration

### 🔍 Nmap Scan

Performed a port scan to identify exposed services on the target.

![Nmap](.github/screenshots/screenshot1.png)

Notable Identified services:
- SMB
- RPC
- LDAP
- WinRM

---

## 3. SMB Enumeration

Tested anonymous SMB login — no shares were available.

![Anonymous SMB](.github/screenshots/screenshot2.png)

Used `rpcclient` to enumerate user RIDs and descriptions.

![rpcclient enum](.github/screenshots/screenshot3.png)

Discovered user account `V.Ventz` with a description that hinted at a password.

![Interesting Description](.github/screenshots/screenshot4.png)

---

## 4. Gaining Initial Access

Checked this password with crackmapexec and found some readable shares:

![Shares](.github/screenshots/screenshot5.png)

Enumerated available shares and identified sensitive files on the "Password Audit" share.

![Files](.github/screenshots/screenshot6.png)

---

## 5. Dumping Credentials

Downloaded `ntds.dit` and `SYSTEM` files from the share and extracted all domain user hashes.

![ntds](.github/screenshots/screenshot7.png)
![secretsdump](.github/screenshots/screenshot8.png)

Extracted accounts included `Administrator`, `L.Livingstone`, and others.  
Tested pass-the-hash and found a valid one:

![crackmapexec success](.github/screenshots/screenshot9.png)

---

## 6. Remote Access via Evil-WinRM

Logged into the target using the `L.Livingstone` NTLM hash via WinRM.

![evil-winrm](.github/screenshots/screenshot10.png)

⚠️ Evil-WinRM was very slow and unresponsive, so I opted for offline enumeration.

---

## 7. Offline AD Enumeration via BloodHound

Used `bloodhound-python` with the NTLM hash to collect AD data externally.

![BloodHound collect](.github/screenshots/screenshot11.png)

Loaded data into BloodHound and identified a misconfiguration:

![BloodHound UI](.github/screenshots/screenshot12.png)
![GenericAll to DC](.github/screenshots/screenshot13.png)

`L.Livingstone` had `GenericAll` on the Domain Controller object.

---

## 8. Privilege Escalation via RBCD

### 8.1 Create a Machine Account

Used current access to create a new computer account in the domain.

![addcomputer](.github/screenshots/screenshot14.png)

### 8.2 Delegate to the DC

Used `rbcd.py` to set delegation rights on the DC.

![rbcd attack](.github/screenshots/screenshot15.png)

---

## 9. Domain Admin via Ticket Forging

### 9.1 Get Administrator TGT

Used Impacket’s `getST` to forge a TGT for the Administrator user.

### 9.2 Use the Ticket

Used the forged TGT with `psexec.py` to gain SYSTEM shell access to the DC.

🎉 Full compromise of the `resourced.local` domain achieved.

---

## 10. Lessons Learned

- User descriptions can leak sensitive credentials.
- Readable shares exposing `ntds.dit` and `SYSTEM` provide full credential dumps.
- `GenericAll` on a DC object enables full domain compromise via RBCD.
- Offline BloodHound recon is powerful when shells are unstable.
