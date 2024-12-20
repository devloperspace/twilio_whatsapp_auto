import streamlit as st
from twilio.rest import Client
import os

# Load Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "ACe84945d35d2ca3b2e614012916850742")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "57f3c7eda94f317f19c29fe7a11ff7d0")
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"  # Twilio's official WhatsApp sandbox number

# Initial list of contacts
contacts = {
    '1': 'whatsapp:+919545883002',
    '2': 'whatsapp:+917498157771',
    '3': 'whatsapp:+918208805916'
}

# Function to send WhatsApp message
def send_whatsapp_message(client, to_number, message):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=to_number
        )
        st.success(f"Message sent to {to_number}")
    except Exception as e:
        st.error(f"Error sending message to {to_number}: {e}")

# Function to send message to all contacts
def send_to_all(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for num in contacts.values():
        send_whatsapp_message(client, num, message)

# Streamlit app
def main():
    st.title("WhatsApp Automation App")

    # Sidebar options
    menu = ["Send Message to All", "Send Message to Specific Contact", "Add New Contact", "View Contacts"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Send Message to All":
        st.subheader("Send Message to All Contacts")
        message = st.text_area("Enter your message")

        if st.button("Send to All"):
            if message.strip():
                send_to_all(message)
            else:
                st.error("Message cannot be empty.")

    elif choice == "Send Message to Specific Contact":
        st.subheader("Send Message to a Specific Contact")
        contact_list = {key: value for key, value in contacts.items()}
        contact = st.selectbox("Select a contact", list(contact_list.keys()))
        message = st.text_area("Enter your message")

        if st.button("Send Message"):
            if message.strip():
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                send_whatsapp_message(client, contacts[contact], message)
            else:
                st.error("Message cannot be empty.")

    elif choice == "Add New Contact":
        st.subheader("Add New Contact")
        name = st.text_input("Enter a name for the contact")
        number = st.text_input("Enter the contact number (in international format, e.g., whatsapp:+919XXXXXXXXX)")

        if st.button("Add Contact"):
            if name.strip() and number.strip():
                new_key = str(len(contacts) + 1)
                contacts[new_key] = number
                st.success(f"Contact {name} added successfully!")
            else:
                st.error("Both name and number are required.")

    elif choice == "View Contacts":
        st.subheader("View Contacts")
        if contacts:
            for key, value in contacts.items():
                st.write(f"{key}: {value}")
        else:
            st.info("No contacts available.")

if __name__ == '__main__':
    main()
