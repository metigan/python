"""Simple example - based on your code, corrected"""

from metigan import MetiganClient

# Initialize the client
client = MetiganClient(api_key="sp_63ace7496fb7692b6cace8f77d3d1bf8bc0db95cd944d498cbfc7679a1d5987b")

# Send email
result = client.email.send_email(
    from_address="Sender <sender@metigan.com>",
    recipients=["jaimeinoque20@email.com", "franciscojaimeinoque@gmail.com", "savanapoint.tech@gmail.com"],
    subject="Welcome!",
    content="<h1>Hello!</h1><p>Thank you for signing up.</p>"
)

# IMPORTANT: API returns fields in camelCase (emailsRemaining), not snake_case (emails_remaining)
if result.get("success"):
    print("Email sent successfully!")
    print(f"Message: {result.get('message')}")
    print(f"Recipients: {result.get('recipientCount', 0)}")
    # CORRECTED: Use emailsRemaining (camelCase), not emails_remaining (snake_case)
    print(f"Emails remaining: {result.get('emailsRemaining', 'N/A')}")
else:
    print(f"Failed to send email: {result.get('message', 'Unknown error')}")
