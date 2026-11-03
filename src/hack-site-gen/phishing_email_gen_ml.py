import openai
import os

# Load OpenAI API key securely from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

def generate_phishing_email(target_name, company_name, email_type, fake_link=None, language="English"):
    """Generates a phishing email using ChatGPT based on user inputs and desired language."""

    prompt = f"""
You are a cybersecurity expert simulating social engineering attacks for training purposes.
Create a realistic phishing email in **{language}** for the following details:

- Target Name: {target_name}
- Company Name: {company_name}
- Email Type: {email_type}
- Purpose: Capture credentials through a fake login page.
"""

    if fake_link:
        prompt += f"\n- Insert this fake login link somewhere appropriate: {fake_link}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional phishing simulation generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    phishing_email = response.choices[0].message.content.strip()
    return phishing_email

def main():
    print("\n=== AI Phishing Email Generator (Multilingual) ===\n")

    target_name = input("Enter Target Name: ").strip()
    company_name = input("Enter Target Company: ").strip()
    email_type = input("Choose Email Type (security_update / account_lock / password_reset / invoice_scam): ").strip()
    language = input("Choose Language (e.g., English, Slovak, Hindi, Spanish): ").strip()

    fake_link = input("Enter fake login page URL (or leave blank to skip): ").strip()
    if fake_link == "":
        fake_link = None

    print("\n[+] Generating phishing email using AI...\n")
    email_content = generate_phishing_email(target_name, company_name, email_type, fake_link, language)

    filename = f"phishing_email_{target_name.replace(' ', '_')}_{language}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(email_content)

    print(f"\n[+] Phishing email saved as {filename}!")
    print("\n[+] SAMPLE OUTPUT:\n")
    print(email_content)

if __name__ == "__main__":
    main()
