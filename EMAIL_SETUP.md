# Setting Up Email for Todo App

This guide will help you set up email functionality for your Todo app, which is needed for sending reminder emails.

## Gmail Setup

If you're using Gmail, you'll need to create an "App Password" since Gmail no longer allows less secure apps to use simple username/password authentication.

### Create a Gmail App Password

1. Go to your [Google Account](https://myaccount.google.com/).
2. Select **Security**.
3. Under "Signing in to Google," select **2-Step Verification** (you must have this enabled first).
4. At the bottom of the page, select **App passwords**.
5. Select **Mail** as the app and **Other (Custom name)** as the device.
6. Enter "Todo App" or any name you prefer.
7. Click **Generate**.
8. Google will display the 16-character app password. **Copy this password**.

### Update Your .env File

1. Create a `.env` file in your project root (copy from `.env.example`).
2. Update the email settings:

```
MAIL_USERNAME=your_gmail_address@gmail.com
MAIL_PASSWORD=your_16_character_app_password
MAIL_DEFAULT_SENDER=your_gmail_address@gmail.com
```

## Other Email Providers

If you're using another email provider:

1. Find the SMTP server and port details from your email provider.
2. Update the `.env` file with appropriate settings:

```
MAIL_SERVER=smtp.your_provider.com
MAIL_PORT=587  # or the port your provider uses
MAIL_USERNAME=your_email@provider.com
MAIL_PASSWORD=your_password
MAIL_USE_TLS=True  # or False, depending on provider
MAIL_USE_SSL=False  # or True, depending on provider
MAIL_DEFAULT_SENDER=your_email@provider.com
```

## Testing Email Functionality

After setting up your `.env` file and installing all requirements:

1. Run your application: `python app.py`
2. Log in to your account
3. Visit the `/test-email` route (e.g., http://localhost:5002/test-email)
4. Check your email inbox for the test email

## Troubleshooting

### Common Issues

1. **No email received**: 
   - Check spam/junk folder
   - Verify SMTP settings are correct
   - Ensure app password is entered correctly (for Gmail)

2. **Authentication errors**:
   - For Gmail, make sure you're using an App Password, not your regular password
   - Check that your username is complete (include @domain.com)

3. **Connection errors**:
   - Check if your network allows outgoing connections on the specified port
   - Verify MAIL_USE_TLS and MAIL_USE_SSL settings are correct

4. **Debug Errors**:
   - Check the console output for detailed error messages
   - Try sending a test email from the `/test-email` route

### Gmail-Specific Issues

- If using Gmail, you must use an App Password if you have 2-Step Verification enabled
- Gmail may block authentication attempts from less secure apps by default

## Important Notes

- Don't commit your `.env` file to version control
- In production, use environment variables set on your server instead of a `.env` file
- For high-volume email sending, consider using a dedicated email service like SendGrid or Mailgun 