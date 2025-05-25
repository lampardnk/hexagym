# HexaGym

A web application for LaTeX question management and practice.

## Running the Application

### Local Development

To run the application just for yourself:

```
python app.py
```

Then open your browser to http://localhost:5000

### Network Sharing

To share the application with others on your network:

1. Run the server script:

```
python start_server.py
```

2. The script will display your local IP address and the URL to share

3. Share the displayed URL with others on the same network

4. Others can access the application by entering that URL in their browsers

## Requirements

- Python 3.6+
- Flask
- Other dependencies listed in requirements.txt

## Firewall Configuration

If others cannot access your application:

1. Make sure your computer's firewall allows incoming connections on port 5000
2. For Windows:
   - Open Windows Defender Firewall
   - Click "Allow an app or feature through Windows Defender Firewall"
   - Add Python and allow it on private networks
3. For macOS:
   - Open System Preferences > Security & Privacy > Firewall
   - Click "Firewall Options"
   - Add Python and allow incoming connections

## Troubleshooting

- If the URL doesn't work for others, try using your computer's hostname instead of IP
- Make sure you're on the same network (WiFi or LAN)
- Some networks (especially public ones) may block device-to-device communication 