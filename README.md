# Meraki MT
Meraki MT Sensor Homeassistant Integration

# Getting Started
1. Create an API key for the integration by going to Organization -> API & Webhooks -> Generate API Key. Copy your API key and don't lose it, you'll need it in step 4.
2. Find your Organization ID by looking at the very bottom of the dashboard. Underneath the copyright and login information, you should see `Data for <account_name> (organization ID: <organization_id>) is hosted in <location>`
  a. Alternatively, you can visit `https://api.meraki.com/api/v1/organizations` in your browser, or send a GET request with your API key as a bearer token to retreive your organization ID.
3. (Optional) If you wish to filter by a specific network, you'll need to obtain your network ID, you can visit `https://api.meraki.com/api/v1/organizations/{organizationId}/networks` in your browser, or send a GET request with your API key as a bearer token to retreive your network ID. 
