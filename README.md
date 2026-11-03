# ChatGPT Ethical Hacking

Bachelor thesis project, Technical University of Košice (TUKE), Faculty of Electrical Engineering and Informatics, 2025. Author: Muhammed Tariq Ali Razvi. Supervisor: Anton Baláž.

The thesis asks whether a language model can take over the slow, manual parts of ethical hacking, and answers it by building a small set of tools that do exactly that. One tool runs a whole penetration test from scan to report, and a second set builds phishing simulations for security awareness training. Everything was built and tested inside an isolated virtual lab, with Kali Linux as the attacker and Metasploitable2 as the target. The full thesis is in `thesis/thesis.pdf`.

## Lab use only

These tools are for systems you own or have written permission to test. The phishing tools exist to train people to spot phishing and must never be pointed at real users. Run all of it inside an isolated lab network, and treat anything you generate with it as test material only.

## What is in here

**`src/auto-hack/`** holds the automated penetration test. The script scans a target with Nmap, sends the scan to ChatGPT, takes the Metasploit module that ChatGPT suggests, runs it, and asks ChatGPT to write the report. `chatgpt_pentest.py` is the main version and also checks the vsftpd backdoor port and connects to the shell. `auto_crack.py` is the version that adds post-exploitation looting, and `auto_hack.py` is an earlier version kept to show how the tool developed. The folder also holds an example report and loot file from a lab run against Metasploitable2 at 10.0.2.6. In that run no session opened, so the loot file only contains the Metasploit error messages.

**`src/hack-site-gen/
