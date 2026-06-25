import requests

def _send_via_gateway(phone, message):
    """
    Helper function to sanitize the phone number and send a message via the local Node.js Gateway.
    """
    cleaned_phone = str(phone).strip().replace("+", "").replace(" ", "")
    if len(cleaned_phone) == 10:
        cleaned_phone = "91" + cleaned_phone

    gateway_url = "http://localhost:3000/send-message"
    try:
        response = requests.post(gateway_url, json={"phone": cleaned_phone, "message": message}, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Failed to route message through Node.js WhatsApp Gateway: {e}")
        return {"error": {"message": f"Local Node Gateway Error: {str(e)}"}}

def send_id_card_template_message(receiver_no, name, reg_no, location, remarks, link):
    """
    Constructs a highly readable custom markdown message and routes it to the local Node.js gateway.
    """
    remarks_text = remarks if remarks and remarks != "N/A" else "None"
    message = (
        f"🚨 *Lost ID Card Alert* 🚨\n\n"
        f"Hello *{name}*,\n"
        f"A student ID card matching your Registration / Roll Number *{reg_no}* has been found on campus.\n\n"
        f"📍 *Found Location*: {location}\n"
        f"📝 *Remarks*: {remarks_text}\n\n"
        f"🔗 *LostLinks Claim Portal*: {link}\n\n"
        f"Please visit the portal above or log in to view the report and claim it. Thank you!"
    )
    print(receiver_no, name, reg_no, location, remarks, link)
    return _send_via_gateway(receiver_no, message)

# if __name__ == "__main__":
#     receiver_no = input("Enter receiver's WhatsApp number : ").strip()
#     response = send_id_card_template_message(
#         receiver_no, 
#         "TEST STUDENT", 
#         "B25CS000", 
#         "Kanhar mess", 
#         "Handed over to security desk", 
#         "https://lostlinks.onrender.com/id/"
#     )
#     print("Response:", response)
