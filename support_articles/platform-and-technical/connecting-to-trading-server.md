# Connecting to the Trading Server

**Last Updated:** November 4, 2025

---

If your MT5 platform is showing a "No Connection" or "Invalid Account" error, this guide will help you troubleshoot and connect to the MarketEdgePros server.

## Step 1: Check Your Credentials

The most common reason for connection issues is incorrect login information. Please carefully check the credentials email you received from us.

- **Login:** Your unique account number.
- **Password:** The password is case-sensitive. Be careful with characters like `O`/`0` or `I`/`l`.
- **Server:** You must select the exact server name specified in the email (e.g., `MarketEdgePros-Demo`).


## Step 2: Manually Rescan for Servers

Sometimes, the server list in MT5 may not update automatically. You can force a rescan:

1. At the bottom-right of the MT5 terminal, click on the connection status icon.
2. Click **"Rescan Servers"**.
3. Wait a few moments for the list to refresh. The connection status should change from a red "No Connection" icon to a green icon showing your connection speed.


## Step 3: Log In Again

If rescanning doesn't work, try logging in again manually:

1. Go to **File > Login to Trade Account**.
2. Re-enter your Login, Password, and select the correct Server.
3. Click **"OK"**.


## Step 4: Check Your Internet and Firewall

- **Internet Connection:** Ensure you have a stable internet connection.
- **Firewall/Antivirus:** Sometimes, a firewall or antivirus software can block MT5 from connecting to the internet. Try temporarily disabling it to see if that resolves the issue. If it does, you will need to add an exception for `terminal64.exe` (the MT5 application) in your firewall settings.


## Step 5: Check the Server Address

In rare cases, you may need to add the server address manually.

1. Go to **Tools > Options > Server**.
2. In the "Server" field, you can manually type the server address provided in your welcome email.

---

### Still Not Working?

If you have tried all the steps above and still cannot connect, please contact our technical support team. We are available 24/7 to help you.

- [Contact Support](/contact)
- [Troubleshooting Connection Issues](/support/troubleshooting-connection-issues)
