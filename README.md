# Metigan Python SDK

Official Metigan SDK for Python. Send emails, manage forms, contacts, and audiences with ease.

## 📦 Installation

```bash
pip install metigan
# or
pip3 install metigan
```

## 🚀 Quick Start

```python
from metigan import MetiganClient

# Initialize the client
client = MetiganClient(api_key="your-api-key")

# Send email
result = client.email.send_email(
    from_address="Sender <sender@example.com>",
    recipients=["customer@email.com"],
    subject="Welcome!",
    content="<h1>Hello!</h1><p>Thank you for signing up.</p>"
)

if result["success"]:
    print("Email sent successfully!")
    print(f"Emails remaining: {result.get('emailsRemaining', 'N/A')}")
```

## 📧 Email Module

### Basic Send

```python
result = client.email.send_email(
    from_address="sender@example.com",
    recipients=["recipient@example.com"],
    subject="Email Subject",
    content="<h1>HTML Content</h1>"
)
```

### With Attachments

```python
with open("document.pdf", "rb") as f:
    file_data = f.read()

result = client.email.send_email(
    from_address="company@email.com",
    recipients=["customer@email.com"],
    subject="Important Document",
    content="Please find the document attached.",
    attachments=[
        {
            "content": file_data,
            "filename": "document.pdf",
            "content_type": "application/pdf"
        }
    ]
)
```

### With CC and BCC

```python
result = client.email.send_email(
    from_address="company@email.com",
    recipients=["main@email.com"],
    subject="Meeting",
    content="Email content",
    cc=["copy@email.com"],
    bcc=["hidden-copy@email.com"],
    reply_to="reply-here@email.com"
)
```

### With Template

```python
result = client.email.send_email_with_template(
    template_id="template-123",
    variables={
        "name": "John Doe",
        "company": "Acme Inc"
    },
    from_address="sender@example.com",
    recipients=["recipient@example.com"]
)
```

## 👥 Contacts Module

### Create Contact

```python
contact = client.contacts.create(
    email="new@email.com",
    first_name="Jane",
    last_name="Doe",
    audience_id="audience-123",
    tags=["customer", "newsletter"]
)
```

### List Contacts

```python
result = client.contacts.list(
    audience_id="audience-123",
    status="subscribed",
    page=1,
    limit=50
)

for contact in result["contacts"]:
    print(f"{contact['email']}: {contact['first_name']}")
```

### Update Contact

```python
updated = client.contacts.update(
    contact_id="contact-456",
    first_name="Jane Marie",
    tags=["customer", "vip"]
)
```

## 📊 Audiences Module

### Create Audience

```python
audience = client.audiences.create(
    name="Main Newsletter",
    description="Main subscriber list"
)
```

### List Audiences

```python
result = client.audiences.list(page=1, limit=10)

for audience in result["audiences"]:
    print(f"{audience['name']}: {audience['count']} contacts")
```

### Get Statistics

```python
stats = client.audiences.get_stats("audience-123")
print(f"Total: {stats['total']}")
print(f"Subscribed: {stats['subscribed']}")
```

## ⚙️ Configuration

```python
from metigan import MetiganClient

client = MetiganClient(
    api_key="your-api-key",
    timeout=30,          # Optional, defaults to 30 seconds
    retry_count=3,       # Optional, defaults to 3
    retry_delay=2,       # Optional, defaults to 2 seconds
    debug=False          # Optional, defaults to False
)
```

## 🔒 Error Handling

```python
from metigan import MetiganClient, ApiError, ValidationError

try:
    result = client.email.send_email(options)
except ValidationError as e:
    print(f"Validation Error: {e.message}")
    if e.field:
        print(f"Field: {e.field}")
except ApiError as e:
    print(f"API Error: {e.status_code} - {e.message}")
except Exception as e:
    print(f"Unknown error: {e}")
```

## 📝 Examples

See the [examples](examples/) directory for more complete examples.

## 📄 License

MIT © Metigan

## 🔗 Links

- [Documentation](https://docs.metigan.com)
- [Dashboard](https://app.metigan.com)
- [API Reference](https://docs.metigan.com/api)
