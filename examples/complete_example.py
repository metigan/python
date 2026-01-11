"""Complete example showing how to use the Metigan Python SDK"""

from metigan import MetiganClient

# Initialize the client with your API key
client = MetiganClient(
    api_key="your-api-key-here",
    # Optional parameters:
    # timeout=30,      # Request timeout in seconds (default: 30)
    # retry_count=3,   # Number of retries for failed requests (default: 3)
    # retry_delay=2,   # Delay between retries in seconds (default: 2)
    # debug=False      # Enable debug mode (default: False)
)

def example_send_email():
    """Example: Send a simple email"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Send Email")
    print("=" * 60)
    
    try:
        result = client.email.send_email(
            from_address="Sender <sender@example.com>",
            recipients=["recipient@example.com"],
            subject="Welcome to Metigan!",
            content="<h1>Hello!</h1><p>Thank you for signing up.</p>"
        )
        
        # IMPORTANT: API returns fields in camelCase, not snake_case
        if result.get("success"):
            print("✅ Email sent successfully!")
            print(f"   Message: {result.get('message')}")
            print(f"   Recipients: {result.get('recipientCount', 0)}")
            print(f"   Emails remaining: {result.get('emailsRemaining', 'N/A')}")
            
            # Access successful emails
            successful_emails = result.get('successfulEmails', [])
            for email in successful_emails:
                print(f"   ✅ Sent to: {email.get('recipient')}")
                print(f"      Tracking ID: {email.get('trackingId')}")
        else:
            print(f"❌ Failed: {result.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_send_email_with_cc_bcc():
    """Example: Send email with CC and BCC"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Send Email with CC and BCC")
    print("=" * 60)
    
    try:
        result = client.email.send_email(
            from_address="Company <company@example.com>",
            recipients=["main@example.com"],
            subject="Meeting Reminder",
            content="<p>Don't forget about our meeting tomorrow.</p>",
            cc=["copy1@example.com", "copy2@example.com"],
            bcc=["hidden@example.com"],
            reply_to="reply@example.com"
        )
        
        if result.get("success"):
            print("✅ Email sent successfully!")
            print(f"   Emails remaining: {result.get('emailsRemaining', 'N/A')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_send_email_with_attachments():
    """Example: Send email with attachments"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Send Email with Attachments")
    print("=" * 60)
    
    try:
        # Read file content (example with binary data)
        # In a real scenario, you would read from a file:
        # with open("document.pdf", "rb") as f:
        #     file_data = f.read()
        
        # For this example, we'll use dummy data
        file_data = b"PDF file content here..."
        
        result = client.email.send_email(
            from_address="Company <company@example.com>",
            recipients=["customer@example.com"],
            subject="Important Document",
            content="<p>Please find the document attached.</p>",
            attachments=[
                {
                    "content": file_data,
                    "filename": "document.pdf",
                    "content_type": "application/pdf"
                }
            ]
        )
        
        if result.get("success"):
            print("✅ Email with attachment sent successfully!")
            print(f"   Attachments: {result.get('attachmentsCount', 0)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_send_email_with_template():
    """Example: Send email using a template"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Send Email with Template")
    print("=" * 60)
    
    try:
        result = client.email.send_email_with_template(
            template_id="template-123",
            variables={
                "name": "John Doe",
                "company": "Acme Inc"
            },
            from_address="Sender <sender@example.com>",
            recipients=["recipient@example.com"],
            reply_to="reply@example.com"
        )
        
        if result.get("success"):
            print("✅ Email with template sent successfully!")
            print(f"   Is template: {result.get('isTemplate', False)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_contacts():
    """Example: Manage contacts"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Contacts Management")
    print("=" * 60)
    
    try:
        # Create a contact
        contact = client.contacts.create(
            email="newcontact@example.com",
            audience_id="audience-123",
            first_name="Jane",
            last_name="Doe",
            phone="+1234567890",
            tags=["customer", "newsletter"],
            status="subscribed"
        )
        print(f"✅ Contact created: {contact.get('email')}")
        
        # List contacts
        contacts_result = client.contacts.list(
            audience_id="audience-123",
            status="subscribed",
            page=1,
            limit=10
        )
        print(f"✅ Found {len(contacts_result.get('contacts', []))} contacts")
        
        # Get contact by ID
        contact_id = contact.get('id')
        if contact_id:
            contact_details = client.contacts.get(contact_id)
            print(f"✅ Contact retrieved: {contact_details.get('email')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_audiences():
    """Example: Manage audiences"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Audiences Management")
    print("=" * 60)
    
    try:
        # Create an audience
        audience = client.audiences.create(
            name="Newsletter Subscribers",
            description="Main newsletter list"
        )
        print(f"✅ Audience created: {audience.get('name')}")
        
        # List audiences
        audiences_result = client.audiences.list(page=1, limit=10)
        audiences = audiences_result.get('audiences', [])
        print(f"✅ Found {len(audiences)} audiences")
        
        # Get audience stats
        audience_id = audience.get('id')
        if audience_id:
            stats = client.audiences.get_stats(audience_id)
            print(f"✅ Audience stats retrieved")
            
    except Exception as e:
        print(f"❌ Error: {e}")


def example_templates():
    """Example: Manage templates"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Templates Management")
    print("=" * 60)
    
    try:
        # List templates
        templates = client.templates.list(page=1, limit=10)
        print(f"✅ Found {len(templates)} templates")
        
        # Get template by ID
        if templates:
            template_id = templates[0].get('id')
            if template_id:
                template = client.templates.get(template_id)
                print(f"✅ Template retrieved: {template.get('name', 'N/A')}")
                
    except Exception as e:
        print(f"❌ Error: {e}")


def example_forms():
    """Example: Manage forms"""
    print("\n" + "=" * 60)
    print("EXAMPLE: Forms Management")
    print("=" * 60)
    
    try:
        # List forms
        forms_result = client.forms.list(page=1, limit=10)
        forms = forms_result.get('forms', [])
        print(f"✅ Found {len(forms)} forms")
        
        # Get form by ID or slug
        if forms:
            form_id = forms[0].get('id')
            if form_id:
                form = client.forms.get(form_id)
                print(f"✅ Form retrieved: {form.get('name', 'N/A')}")
        
        # Submit form data
        submission = client.forms.submit(
            form_id="form-123",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "message": "Hello from Python!"
            }
        )
        print(f"✅ Form submitted: {submission.get('message', 'Success')}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("METIGAN PYTHON SDK - COMPLETE EXAMPLES")
    print("=" * 60)
    
    # IMPORTANT: Replace "your-api-key-here" with your actual API key
    if client.http_client.api_key == "your-api-key-here":
        print("\n⚠️  WARNING: Please set your API key in the code!")
        print("   client = MetiganClient(api_key='your-actual-api-key')")
        print("\n   Uncomment the examples below to test them:")
        print("\n")
    else:
        # Uncomment the examples you want to test:
        
        # Email examples
        example_send_email()
        # example_send_email_with_cc_bcc()
        # example_send_email_with_attachments()
        # example_send_email_with_template()
        
        # Other examples
        # example_contacts()
        # example_audiences()
        # example_templates()
        # example_forms()
        
    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETE")
    print("=" * 60 + "\n")
