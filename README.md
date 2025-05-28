# IP Location Finder

A modern Python application that visualizes geographical locations of multiple IP addresses on an interactive map with clustering support.

![image](https://github.com/user-attachments/assets/4d830dcc-e875-48b5-88e8-9ca91232b7ae)

## Features

- 🌍 Interactive map with marker clustering
- 📋 Clipboard support for quick IP input
- 🔍 Detailed location information for each IP
- 🎨 Dark/Light theme support
- 🖱️ Interactive markers with detailed popups
- 📊 Multiple IP address processing
- 🔄 Automatic marker clustering for better visualization
- 🎯 Zoom-dependent marker grouping

## Requirements

- Python 3.8 or higher
- Internet connection for IP geolocation and map tiles

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AlexEnotov/map_ip_finder.git
cd ip-location-finder
```

2. Install the required dependencies:
```bash
pip install customtkinter
pip install tkintermapview
pip install requests
pip install pillow
```

## Usage

1. Run the application:
```bash
python map_ip.py
```

2. Enter IP addresses in one of two ways:
   - Type IP addresses directly into the text box (one per line)
   - Copy IP addresses to clipboard and click "Paste IPs" button

3. Click "Find Locations" to display the locations on the map

4. Interact with the map:
   - Use mouse wheel to zoom in/out
   - Click and drag to pan
   - Click on markers to view detailed information
   - Markers automatically cluster when zoomed out
   - Zoom in to see individual markers

5. Additional controls:
   - Use the Dark/Light mode switch to change theme
   - Click "Clear All" to reset the application

## Example Input

```
8.8.8.8
1.1.1.1
208.67.222.222
```

## Features in Detail

### Marker Clustering
- Markers close to each other automatically group when zoomed out
- Groups show the number of contained markers
- Zoom in to see individual markers
- Helps manage visual clutter with many IP addresses

### Location Details
Click on any marker to see detailed information:
- IP Address
- Country, City, Region
- ZIP Code
- ISP and Organization
- Exact Coordinates
- Timezone
- AS Number

### Theme Support
- Switch between Dark and Light themes
- Persistent across sessions
- Affects entire application UI

## Dependencies

The application requires the following Python packages:
- `customtkinter`: Modern UI widgets and theming
- `tkintermapview`: Interactive map display
- `requests`: API communication for IP geolocation
- `pillow`: Image processing support
- `threading`: Asynchronous operations

## API Usage

This application uses the [ip-api.com](http://ip-api.com) service for IP geolocation. The free tier includes:
- Up to 45 requests per minute
- No API key required
- Non-commercial use only

## Error Handling

The application includes robust error handling for:
- Invalid IP addresses
- Network connectivity issues
- API rate limiting
- Empty clipboard
- Invalid input formats

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Map tiles provided by OpenStreetMap
- IP geolocation data provided by ip-api.com
- Built with Python and CustomTkinter

## Support

If you encounter any problems or have suggestions, please open an issue on GitHub.
