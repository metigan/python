"""Basic example of using Metigan Python SDK"""

import os
from metigan import MetiganClient

def main():
    # Initialize the client
    api_key = os.getenv("METIGAN_API_KEY")
    if not api_key:
        raise ValueError("METIGAN_API_KEY environment variable is required")

    client = MetiganClient(api_key=api_key)

    # Send an email
    try:
        result = client.email.send_email(
            from_address="Sender <sender@example.com>",
            recipients=["recipient@example.com"],
            subject="Hello from Python!",
            content="<h1>Hello!</h1><p>This email was sent from a Python application.</p>"
        )

        if result.get("success"):
            print("Email sent successfully!")
            print(f"Message: {result.get('message')}")
            print(f"Recipients: {result.get('recipient_count')}")
            print(f"Emails remaining: {result.get('emails_remaining')}")
        else:
            print(f"Failed to send email: {result.get('message')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

