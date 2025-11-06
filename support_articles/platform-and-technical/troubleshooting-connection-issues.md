# Troubleshooting Connection Issues

**Last Updated:** November 4, 2025

---

If you are experiencing frequent disconnections or lag on your MT5 platform, this guide provides steps to diagnose and resolve the issue.

## Step 1: Check Your Internet Connection

The most common cause of connection problems is an unstable internet connection.

- **Run a Speed Test:** Use a website like Speedtest.net to check your internet speed and ping.
A high ping (over 100ms) can cause lag.
- **Use a Wired Connection:** A wired Ethernet connection is generally more stable than Wi-Fi.
- **Restart Your Router:** A simple router restart can often fix connection problems.


## Step 2: Check the Server Ping

MT5 allows you to see your connection speed to our different data centers. 

1. Go to **File > Open an Account**.
2. When the server list appears, you will see a ping time in milliseconds (ms) next to each server name.
3. Choose the server with the **lowest ping** for the best connection.


## Step 3: Check Your Firewall and Antivirus

Security software can sometimes interfere with MT5's connection.

- **Add an Exception:** Add `terminal64.exe` (the MT5 application) to your firewall's and antivirus's list of allowed applications.
- **Temporarily Disable:** Try temporarily disabling your firewall or antivirus to see if it resolves the issue. If it does, you know it's the cause.


## Step 4: Reduce Platform Load

If you have many charts open or are running complex EAs, it can slow down your platform.

- **Close Unused Charts:** Close any chart windows you are not actively using.
- **Reduce Max Bars:** Go to **Tools > Options > Charts** and reduce the "Max bars in chart" number. A value of 5000 is usually sufficient.
- **Disable News:** In the "Server" tab, uncheck "Enable news".


## Step 5: Contact Support

If you have tried all of the above and are still experiencing issues, please contact our support team. Provide us with the following information:

- Your account number
- Your location
- A screenshot of your server ping times
- Your MT5 journal logs (from the "Journal" tab in the Terminal)

This will help us diagnose the problem more quickly.

---

### Need More Help?

- [Contact Support](/contact)
- [Connecting to Trading Server](/support/connecting-to-trading-server)
