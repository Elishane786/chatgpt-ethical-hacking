import openai
import os

# Load OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

def generate_html_login_page(description):
    """Generates a professional fake login page HTML code based on description."""

    prompt = f"""
You are a cybersecurity expert simulating phishing login pages for security awareness training.
Create a professional-looking HTML login page based on this description:

{description}

Requirements:
- Only output pure HTML code. Do not include any explanations, markdown formatting, or extra description.
- Use a centered layout with clean styling.
- Use an external CSS file named 'static/style.css' for styling.
- The form must POST to '/login'.
- Allow basic JavaScript validation using 'static/script.js' if necessary.
- Ensure the page looks like a realistic login page for the provided description.
- Keep it educational and simulation-safe.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional web page generator for social engineering simulations."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    html_code = response.choices[0].message.content.strip()
    return html_code

def main():
    print("\n=== AI Fake Login Page Generator ===\n")

    description = input("Describe how the login page should look: \n\n").strip()

    print("\n[+] Generating HTML login page using AI...\n")
    html_content = generate_html_login_page(description)

    os.makedirs("templates", exist_ok=True)
    os.makedirs("static", exist_ok=True)

    html_filename = "templates/login.html"
    css_filename = "static/style.css"

    with open(html_filename, "w") as f:
        f.write(html_content)

    # Create a basic style.css if not already present
    if not os.path.exists(css_filename):
        with open(css_filename, "w") as f:
            f.write("""
body {
    background-color: #f0f2f5;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}

.login-container {
    background: white;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}

input[type="text"], input[type="password"] {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button {
    width: 100%;
    padding: 10px;
    background-color: #1877f2;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #165ec9;
}
""")

    print(f"\n[+] Login page saved as {html_filename}!")
    print("\n[!] Now run 'python3 server.py' to start hosting the page.")

if __name__ == "__main__":
    main()
