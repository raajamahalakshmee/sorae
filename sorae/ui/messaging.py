def welcome_message():
    return (
        "✨ Welcome to Sorae ✨\n"
        "Your empathy-driven, passwordless authentication experience starts here.\n"
    )

def empathetic_login_greeting(email):
    return (f"Hello {email}!\n"
            "Log in the secure way – your comfort, safety, and trust matter to us.")

def error_message(context):
    messages = {
        "token": "That token doesn't look right. Double-check your inbox or try again. We'll guide you at every step!",
        "biometrics": "Hmmm, your typing pattern seems a bit off – maybe tired hands? Let's try again or use account recovery."
    }
    return messages.get(context, "Oops! Something didn’t work. We’re here to help.")

def empathy_recovery_intro(email):
    return (f"We know it's tough being locked out, {email}.\n"
            "Let's make it easy to get you back in. Please enter your backup code below.")

def empathy_recovery_success():
    return "You’re safely back in. Thanks for verifying! If you need extra support, we’re always here."
