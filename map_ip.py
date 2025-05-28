import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import tkintermapview
import requests
import threading
from PIL import Image, ImageTk
import math

class MarkerPopup(ctk.CTkToplevel):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.title("Location Details")
        self.geometry("400x500")
        self.configure(fg_color="#1f1f1f", corner_radius=10)
        
        # Make the popup modal
        self.transient(parent)
        self.grab_set()
        
        # Create text widget with modern styling
        self.text = ctk.CTkTextbox(self, width=380, height=480, fg_color="#2a2a2a", text_color="white", corner_radius=10)
        self.text.pack(padx=15, pady=15, fill="both", expand=True)
        
        # Insert data with modern font and spacing
        details = f"""📍 Location Details:
        
IP: {data.get('ip', 'Unknown')}
Country: {data.get('country', 'Unknown')}
City: {data.get('city', 'Unknown')}
Region: {data.get('regionName', 'Unknown')}
ZIP Code: {data.get('zip', 'Unknown')}
        
🌐 Network Details:
        
ISP: {data.get('isp', 'Unknown')}
Organization: {data.get('org', 'Unknown')}
        
📌 Coordinates:
        
Latitude: {data.get('lat', 'Unknown')}
Longitude: {data.get('lon', 'Unknown')}
        
⚡ Additional Info:
        
Timezone: {data.get('timezone', 'Unknown')}
AS: {data.get('as', 'Unknown')}
"""
        self.text.insert("1.0", details)
        self.text.configure(state="disabled")
        
        # Center the popup
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

class MarkerCluster:
    def __init__(self, map_widget, parent):
        self.map_widget = map_widget
        self.parent = parent
        self.markers = []
        self.clusters = []
        self.cluster_radius = 30
        self.current_zoom = 3
        self.marker_data = {}  # Store data for each marker
        
    def add_marker(self, lat, lon, text, data):
        marker = self.map_widget.set_marker(lat, lon, text=text, command=self.create_marker_callback(data))
        self.markers.append({
            'marker': marker,
            'lat': lat,
            'lon': lon,
            'text': text,
            'visible': True,
            'data': data
        })
        return marker
    
    def create_marker_callback(self, data):
        def callback(marker):
            MarkerPopup(self.parent, data)
        return callback
        
    def clear_clusters(self):
        for cluster in self.clusters:
            if 'marker' in cluster:
                cluster['marker'].delete()
        self.clusters = []
        
    def show_marker(self, marker_info, show):
        if marker_info['visible'] != show:
            if show:
                marker_info['marker'] = self.map_widget.set_marker(
                    marker_info['lat'],
                    marker_info['lon'],
                    text=marker_info['text'],
                    command=self.create_marker_callback(marker_info['data'])
                )
            else:
                marker_info['marker'].delete()
            marker_info['visible'] = show

    def update_clusters(self, zoom_level=None):
        if zoom_level is not None:
            self.current_zoom = zoom_level
            
        self.clear_clusters()
        
        for marker_info in self.markers:
            self.show_marker(marker_info, True)
            
        if self.current_zoom < 6:
            clusters = []
            processed = set()
            
            for i, marker1 in enumerate(self.markers):
                if i in processed:
                    continue
                    
                cluster = {
                    'markers': [marker1],
                    'center_lat': marker1['lat'],
                    'center_lon': marker1['lon']
                }
                processed.add(i)
                
                for j, marker2 in enumerate(self.markers):
                    if j in processed:
                        continue
                        
                    lat_diff = abs(marker1['lat'] - marker2['lat'])
                    lon_diff = abs(marker1['lon'] - marker2['lon'])
                    distance = math.sqrt(lat_diff**2 + lon_diff**2)
                    
                    threshold = 5.0 / (2 ** self.current_zoom)
                    
                    if distance <= threshold:
                        cluster['markers'].append(marker2)
                        processed.add(j)
                        lats = [m['lat'] for m in cluster['markers']]
                        lons = [m['lon'] for m in cluster['markers']]
                        cluster['center_lat'] = sum(lats) / len(lats)
                        cluster['center_lon'] = sum(lons) / len(lons)
                
                clusters.append(cluster)
            
            for cluster in clusters:
                if len(cluster['markers']) > 1:
                    for marker_info in cluster['markers']:
                        self.show_marker(marker_info, False)
                    
                    marker_text = f"🔵 {len(cluster['markers'])}"
                    cluster_marker = self.map_widget.set_marker(
                        cluster['center_lat'],
                        cluster['center_lon'],
                        text=marker_text,
                        font=("Arial", 12, "bold")
                    )
                    cluster['marker'] = cluster_marker
                    self.clusters.append(cluster)

    def clear_all(self):
        for marker_info in self.markers:
            if marker_info['visible']:
                marker_info['marker'].delete()
        self.clear_clusters()
        self.markers = []
        self.current_zoom = 3

class ModernIPFinder(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("IP Location Finder")
        self.geometry("1200x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20,10))
        self.header_frame.grid_columnconfigure(1, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="IP Location Finder",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=1, padx=20, pady=10)

        # Theme switcher
        self.theme_switch = ctk.CTkSwitch(
            self.header_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.grid(row=0, column=2, padx=20, pady=10)
        self.theme_switch.select()

        # Search frame
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        self.search_frame.grid_columnconfigure(1, weight=1)

        # IP Entry Label
        self.ip_label = ctk.CTkLabel(
            self.search_frame,
            text="Enter IP addresses:",
            font=ctk.CTkFont(size=12)
        )
        self.ip_label.grid(row=0, column=0, padx=10, pady=10)

        # IP Entry
        self.ip_entry = ctk.CTkTextbox(
            self.search_frame,
            height=60,
            width=400,
            font=ctk.CTkFont(size=12)
        )
        self.ip_entry.grid(row=0, column=1, padx=10, pady=10)
        self.ip_entry.insert("1.0", "Enter multiple IP addresses (one per line)")

        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.search_frame, fg_color="transparent")
        self.buttons_frame.grid(row=0, column=2, padx=10, pady=10)

        # Paste button
        self.paste_button = ctk.CTkButton(
            self.buttons_frame,
            text="Paste IPs",
            command=self.paste_ips,
            fg_color="gray30",
            hover_color="gray40"
        )
        self.paste_button.grid(row=0, column=0, padx=5, pady=5)

        # Search button
        self.search_button = ctk.CTkButton(
            self.buttons_frame,
            text="Find Locations",
            command=self.get_locations
        )
        self.search_button.grid(row=1, column=0, padx=5, pady=5)

        # Clear button
        self.clear_button = ctk.CTkButton(
            self.buttons_frame,
            text="Clear All",
            command=self.clear_all,
            fg_color="gray30",
            hover_color="gray40"
        )
        self.clear_button.grid(row=2, column=0, padx=5, pady=5)

        # Results frame
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.results_frame.grid_columnconfigure(1, weight=1)
        self.results_frame.grid_rowconfigure(0, weight=1)

        # Location details frame
        self.details_frame = ctk.CTkFrame(self.results_frame)
        self.details_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Location details text
        self.location_text = ctk.CTkTextbox(
            self.details_frame,
            width=300,
            height=400,
            font=ctk.CTkFont(size=12)
        )
        self.location_text.pack(padx=10, pady=10, fill="both", expand=True)
        self.location_text.insert("1.0", "Location details will appear here...")
        self.location_text.configure(state="disabled")

        # Map frame
        self.map_frame = ctk.CTkFrame(self.results_frame)
        self.map_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.map_frame.grid_columnconfigure(0, weight=1)
        self.map_frame.grid_rowconfigure(0, weight=1)

        # Create map widget
        self.map_widget = tkintermapview.TkinterMapView(self.map_frame, width=800, height=600, corner_radius=0)
        self.map_widget.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.map_widget.set_zoom(3)

        # Initialize marker cluster manager
        self.marker_cluster = MarkerCluster(self.map_widget, self)

        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=3, column=0, pady=5)

        # Bind click event to clear placeholder text
        self.ip_entry.bind("<FocusIn>", self.clear_placeholder)
        
        # Bind mouse wheel event for zoom
        self.map_widget.bind("<MouseWheel>", self.on_mouse_wheel)

    def paste_ips(self):
        try:
            clipboard_text = self.clipboard_get()
            if clipboard_text:
                self.ip_entry.delete("1.0", tk.END)
                self.ip_entry.insert("1.0", clipboard_text)
        except tk.TclError:
            messagebox.showwarning("Clipboard Error", "No text found in clipboard.")

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.marker_cluster.current_zoom = min(self.marker_cluster.current_zoom + 1, 19)
        else:
            self.marker_cluster.current_zoom = max(self.marker_cluster.current_zoom - 1, 2)
        
        self.after(100, self.marker_cluster.update_clusters)

    def clear_placeholder(self, event):
        if self.ip_entry.get("1.0", tk.END).strip() == "Enter multiple IP addresses (one per line)":
            self.ip_entry.delete("1.0", tk.END)

    def toggle_theme(self):
        if self.theme_switch.get() == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def show_loading(self, show=True):
        if show:
            self.status_label.configure(text="Loading...")
            self.search_button.configure(state="disabled")
        else:
            self.status_label.configure(text="")
            self.search_button.configure(state="normal")

    def clear_all(self):
        self.marker_cluster.clear_all()
        self.ip_entry.delete("1.0", tk.END)
        self.location_text.configure(state="normal")
        self.location_text.delete("1.0", tk.END)
        self.location_text.insert("1.0", "Location details will appear here...")
        self.location_text.configure(state="disabled")
        self.map_widget.set_zoom(3)
        self.map_widget.set_position(0, 0)

    def update_location_details(self, data_list):
        self.location_text.configure(state="normal")
        self.location_text.delete("1.0", tk.END)
        
        for i, data in enumerate(data_list, 1):
            details = f"""📍 Location {i}:
            
IP: {data.get('query', 'Unknown')}
Country: {data.get('country', 'Unknown')}
City: {data.get('city', 'Unknown')}
Region: {data.get('regionName', 'Unknown')}
ZIP Code: {data.get('zip', 'Unknown')}
            
🌐 Network Details:
ISP: {data.get('isp', 'Unknown')}
Organization: {data.get('org', 'Unknown')}
            
📌 Coordinates:
Latitude: {data.get('lat', 'Unknown')}
Longitude: {data.get('lon', 'Unknown')}
            
⚡ Additional Info:
Timezone: {data.get('timezone', 'Unknown')}
AS: {data.get('as', 'Unknown')}
{'=' * 40}
"""
            self.location_text.insert(tk.END, details + "\n")
        
        self.location_text.configure(state="disabled")

    def fit_markers_in_view(self, bounds):
        if not bounds:
            return
        
        min_lat = min(lat for lat, _ in bounds)
        max_lat = max(lat for lat, _ in bounds)
        min_lon = min(lon for _, lon in bounds)
        max_lon = max(lon for _, lon in bounds)
        
        lat_padding = (max_lat - min_lat) * 0.1
        lon_padding = (max_lon - min_lon) * 0.1
        min_lat -= lat_padding
        max_lat += lat_padding
        min_lon -= lon_padding
        max_lon += lon_padding
        
        center_lat = (min_lat + max_lat) / 2
        center_lon = (min_lon + max_lon) / 2
        
        self.map_widget.set_position(center_lat, center_lon)
        
        lat_range = max_lat - min_lat
        lon_range = max_lon - min_lon
        zoom_lat = int(-1.4 * (lat_range - 180))
        zoom_lon = int(-1.4 * (lon_range - 360))
        zoom = max(min(zoom_lat, zoom_lon, 19), 2)
        
        self.map_widget.set_zoom(zoom)
        self.marker_cluster.current_zoom = zoom

    def get_locations(self):
        ip_text = self.ip_entry.get("1.0", tk.END).strip()
        if ip_text == "" or ip_text == "Enter multiple IP addresses (one per line)":
            messagebox.showwarning("Input Error", "Please enter at least one IP address.")
            return

        ip_list = [ip.strip() for ip in ip_text.split('\n') if ip.strip()]
        
        if not ip_list:
            messagebox.showwarning("Input Error", "Please enter at least one valid IP address.")
            return

        self.show_loading(True)
        thread = threading.Thread(target=self._fetch_locations, args=(ip_list,))
        thread.daemon = True
        thread.start()

    def _fetch_locations(self, ip_list):
        try:
            self.after(0, self.clear_all)
            
            results = []
            bounds = []

            for ip in ip_list:
                try:
                    url = f"http://ip-api.com/json/{ip}"
                    response = requests.get(url, timeout=5)
                    data = response.json()
                    
                    if data['status'] == 'success':
                        data['ip'] = ip  # Add IP to data for marker popup
                        results.append(data)
                        lat = data.get('lat')
                        lon = data.get('lon')
                        location_name = f"{data.get('city', '')}, {data.get('country', '')}"
                        
                        if lat is not None and lon is not None:
                            bounds.append((lat, lon))
                            self.after(0, lambda lat=lat, lon=lon, name=location_name, data=data: 
                                     self.marker_cluster.add_marker(lat, lon, name, data))
                    else:
                        self.after(0, lambda: messagebox.showwarning(
                            "Warning", f"Could not locate IP: {ip}\nError: {data.get('message', 'Unknown error')}"))
                        
                except Exception as e:
                    self.after(0, lambda: messagebox.showwarning(
                        "Warning", f"Error processing IP {ip}: {str(e)}"))

            if results:
                self.after(0, lambda: self.update_location_details(results))
                
                if bounds:
                    self.after(0, lambda: self.fit_markers_in_view(bounds))
                    self.after(100, self.marker_cluster.update_clusters)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
        
        finally:
            self.after(0, lambda: self.show_loading(False))

if __name__ == "__main__":
    app = ModernIPFinder()
    app.mainloop()
