# Now Playing Overlay

A web-based "Now Playing" overlay system for OBS with phone-friendly controls. Display what game/song you're playing on stream and let anyone on your network update it from their phone.

## Features

- Retro pixel-art styled overlay with smooth fade animations
- Mobile-friendly control panel accessible from any device on your network
- Preset setlist browser with one-tap song selection
- Manual input for custom games/songs
- Persistent setlist storage (survives server restarts)
- Add new songs to your setlist on the fly

## Quick Start

**Requirements:** Python 3 (pre-installed on macOS)

1. Install dependencies:
   ```bash
   pip3 install flask flask-cors
   ```

2. Start the server:
   ```bash
   python3 server.py
   ```

3. Add the overlay to OBS:
   - Add a new **Browser Source**
   - URL: `http://localhost:5000/overlay`
   - Width: 1920, Height: 1080
   - Check "Refresh browser when scene becomes active"

4. Open the control panel:
   - On the same computer: `http://localhost:5000/control`
   - From your phone: `http://YOUR_LOCAL_IP:5000/control`
   - Find your local IP: `ipconfig getifaddr en0` (macOS) or `ipconfig` (Windows)

## How to Use

The control panel has three sections:

**Setlist Presets**

- Click a game to see its songs
- Click a song to instantly show it on stream
- Your setlist is stored in `setlist.json`

**Manual / Custom**

- Type any game and song name
- Click "Show on Stream" to display it
- Click "Hide" to remove the overlay
- Click "+ Save to Presets" to add it to your setlist

**Currently on Stream**

- Shows what's currently visible on the overlay

## Files

- `server.py` — Flask server with REST API
- `overlay.html` — OBS browser source (retro styled, 1920x1080)
- `control.html` — Mobile-friendly control panel
- `setlist.json` — Your saved game/song presets

## API Endpoints

If you want to integrate with other tools:

- `GET /state` — Current overlay state
- `POST /update` — Update overlay (JSON: `{game, song, visible}`)
- `GET /setlist` — Get all presets
- `POST /setlist/add-song` — Add song to setlist (JSON: `{game, song}`)

## Customization

**Overlay styling:** Edit `overlay.html` to change colors, fonts, position, or animations.

**Control panel theme:** Edit the `<style>` section in `control.html`.

**Setlist:** Edit `setlist.json` directly or use the "+ Save to Presets" button in the control panel.

## Troubleshooting

**Can't access from phone:**

- Make sure your phone and computer are on the same WiFi network
- Check your firewall isn't blocking port 5000
- Try `http://0.0.0.0:5000/control` if localhost doesn't work

**Overlay not updating in OBS:**

- Right-click the browser source → Interact → check if the page loaded
- Try refreshing the browser source
- Check the server is still running in your terminal

**Server won't start:**

- Make sure Flask is installed: `pip3 install flask flask-cors`
- Check if port 5000 is already in use by another app
