from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.list import OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.list import ThreeLineAvatarIconListItem, IconLeftWidget, IconRightWidget, IRightBodyTouch
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
from database import Database
from ocr_engine import OCREngine
from routing import RouteOptimizer
from kivy.properties import NumericProperty
import os
from datetime import datetime
try:
    from kivy_garden.mapview import MapView, MapMarker
except ImportError:
    print("MapView not available - install with: pip install kivy_garden.mapview")

class RightButtons(IRightBodyTouch, MDBoxLayout):
    pkg_id = NumericProperty()
    adaptive_width = True

class HomeScreen(MDScreen):
    pass

class ScanScreen(MDScreen):
    pass

class MapScreen(MDScreen):
    pass

class DeliveryScreen(MDScreen):
    pass

class WindowManager(MDScreenManager):
    pass

class ZustellApp(MDApp):
    dialog = None
    scan_mode = "package" # "package" or "master"
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"
        self.db = Database()
        self.ocr = OCREngine()
        self.route_optimizer = RouteOptimizer()
        return Builder.load_file("ui/main.kv")
    
    def on_start(self):
        """Called when the app starts"""
        self.refresh_packages()

    def refresh_packages(self):
        """Refresh the package list on home screen"""
        try:
            package_list = self.root.get_screen('home').ids.package_list
            package_list.clear_widgets()
            
            packages = self.db.get_packages()
            
            if not packages:
                item = OneLineListItem(text="Keine Pakete vorhanden")
                package_list.add_widget(item)
            else:
                for i, pkg in enumerate(packages):
                    # p.id(0), address(1), status(2), type(3), notes(4), lat(5), lon(6), order(7), area_id(8), ts(9), area_name(10)
                    pkg_id, address, status, pkg_type, notes, lat, lon, order, area_id, timestamp, area_name = pkg
                    status_icon = "check-circle" if status == "delivered" else "package-variant"
                    
                    # Display index and area if available
                    title_text = f"{i+1}. {address[:40]}..." if len(address) > 40 else f"{i+1}. {address}"
                    area_display = f" | Bereich: {area_name}" if area_name else " | Kein Bereich"
                    
                    item = ThreeLineAvatarIconListItem(
                        text=title_text,
                        secondary_text=f"Status: {status} | Typ: {pkg_type}{area_display}",
                        tertiary_text=f"Notizen: {notes if notes else 'Keine'}",
                        on_release=lambda x, p=pkg: self.show_edit_dialog(p)
                    )
                    
                    # Left icon for status
                    left_icon = IconLeftWidget(icon=status_icon)
                    item.add_widget(left_icon)
                    
                    # Right container for multiple buttons
                    right_container = RightButtons(pkg_id=pkg_id)
                    item.add_widget(right_container)
                    
                    package_list.add_widget(item)
        except Exception as e:
            print(f"Error refreshing packages: {e}")

    def show_edit_dialog(self, package):
        """Show dialog to edit package address and notes"""
        pkg_id, address, status, pkg_type, notes, lat, lon, order, area_id, timestamp, area_name = package
        
        content = MDBoxLayout(orientation="vertical", spacing="12dp", size_hint_y=None, height="160dp")
        area_info = MDLabel(text=f"Bereich: {area_name if area_name else 'Unbekannt'}", theme_text_color="Hint")
        self.edit_address = MDTextField(text=address, hint_text="Adresse", mode="rectangle")
        self.edit_notes = MDTextField(text=notes if notes else "", hint_text="Notizen", mode="rectangle")
        content.add_widget(area_info)
        content.add_widget(self.edit_address)
        content.add_widget(self.edit_notes)

        self.dialog = MDDialog(
            title="Paket bearbeiten",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="Abbrechen", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="Speichern", on_release=lambda x: self.save_package_edit(pkg_id))
            ],
        )
        self.dialog.open()

    def save_package_edit(self, pkg_id):
        """Save edited package to database"""
        new_address = self.edit_address.text
        new_notes = self.edit_notes.text
        self.db.update_package(pkg_id, new_address, new_notes)
        self.dialog.dismiss()
        self.refresh_packages()

    def confirm_delete_dialog(self, pkg_id):
        """Confirm deletion of a package"""
        self.dialog = MDDialog(
            title="Paket löschen?",
            text="Möchten Sie dieses Paket wirklich permanent löschen?",
            buttons=[
                MDFlatButton(text="Abbrechen", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="Löschen", text_color=self.theme_cls.error_color, 
                             on_release=lambda x: self.delete_package(pkg_id))
            ],
        )
        self.dialog.open()

    def delete_package(self, pkg_id):
        """Delete package from database"""
        self.db.delete_package(pkg_id)
        self.dialog.dismiss()
        self.refresh_packages()

    def capture_address(self):
        """Capture image from camera and extract address"""
        try:
            camera = self.root.get_screen('scan').ids.camera
            address_input = self.root.get_screen('scan').ids.address_input
            
            # Ensure directory exists
            if not os.path.exists("captures"):
                os.makedirs("captures")
            
            filename = f"captures/scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            camera.export_to_png(filename)
            
            image_path = filename # Assuming ocr.capture_image() would do this
            if image_path:
                text = self.ocr.extract_text(image_path) # Assuming ocr.perform_ocr is extract_text
                if text:
                    if self.scan_mode == "master":
                        self.process_master_list(text)
                    else:
                        address = self.ocr.extract_address(text) # Assuming ocr.parse_address is extract_address
                        if address:
                            # Add package and refresh
                            self.db.add_package(address, notes="Gescannt") # Added notes for consistency
                            self.refresh_packages()
                            print(f"Added package from scan: {address}")
                            self.root.get_screen('scan').ids.address_input.text = address # Update text field
                        else:
                            print(f"No address found in text: {text}")
                            self.root.get_screen('scan').ids.address_input.text = "Keine Adresse erkannt"
                else:
                    print("No text detected in image")
                    self.root.get_screen('scan').ids.address_input.text = "Keine Adresse erkannt"
        except Exception as e:
            print(f"Error capturing image: {e}")
    
    def process_master_list(self, text):
        """Process multiple addresses from a master list scan"""
        lines = [line.strip() for line in text.split('\n') if len(line.strip()) > 5]
        print(f"Processing master list with {len(lines)} lines...")
        # Simple heuristic: treat each non-empty line as an address for demo
        # For a real app, we'd need better parsing or a specific area ID
        area_id = self.db.add_delivery_area("Scanned Area")
        for i, addr in enumerate(lines):
            self.db.add_master_route_entry(area_id, addr, i + 1)
        print(f"Added {len(lines)} master route entries to 'Scanned Area'")
    
    def add_scanned_package(self):
        """Add the scanned package to database"""
        try:
            address_input = self.root.get_screen('scan').ids.address_input
            address = address_input.text
            
            if address and address != "Keine Adresse erkannt":
                self.db.add_package(address, notes="Gescannt")
                address_input.text = ""
                print(f"Package added: {address}")
                self.refresh_packages()
        except Exception as e:
            print(f"Error adding package: {e}")
    
    def show_route(self):
        """Switch to map screen and show route"""
        self.root.current = "map"
        self.optimize_route()
    
    def on_speed_dial_action(self, button):
        """Handle speed dial actions"""
        icon = button.icon
        if icon == "camera":
            self.root.current = "scan"
        elif icon == "map":
            self.root.current = "map"
        elif icon == "routes":
            self.optimize_route()
        elif icon == "trash-can":
            self.confirm_clear_dialog()

    def confirm_clear_dialog(self):
        """Confirm clearing all packages"""
        self.dialog = MDDialog(
            title="Alle Pakete löschen?",
            text="Möchten Sie wirklich die gesamte aktuelle Tour löschen?",
            buttons=[
                MDFlatButton(text="Abbrechen", on_release=lambda x: self.dialog.dismiss()),
                MDFlatButton(text="Löschen", text_color=self.theme_cls.error_color, 
                             on_release=lambda x: self.clear_all_packages())
            ],
        )
        self.dialog.open()

    def clear_all_packages(self):
        """Clear all packages from database"""
        self.db.clear_all_data()
        if self.dialog:
            self.dialog.dismiss()
        self.refresh_packages()
        print("All packages cleared")

    def start_delivery_session(self):
        """Start the focused delivery mode"""
        self.current_stop_index = 0
        self.root.current = "delivery"
        self.update_delivery_screen()

    def stop_delivery_session(self):
        """Exit delivery mode"""
        self.root.current = "home"
        self.refresh_packages()

    def update_delivery_screen(self):
        """Update the focused delivery screen with current and next stops"""
        try:
            packages = self.db.get_packages(status="pending")
            screen = self.root.get_screen('delivery')
            
            if not packages:
                screen.ids.current_address.text = "Alle Pakete zugestellt!"
                screen.ids.current_notes.text = "-"
                screen.ids.next_stop_1.text = "Keine weiteren Stopps"
                screen.ids.next_stop_2.text = "-"
                return

            # Current Stop
            curr = packages[0]
            screen.ids.current_address.text = curr[1] # address
            screen.ids.current_notes.text = f"Notizen: {curr[4] if curr[4] else 'Keine'}"
            
            # Next Stops
            if len(packages) > 1:
                screen.ids.next_stop_1.text = f"Nächster: {packages[1][1]}"
            else:
                screen.ids.next_stop_1.text = "Ende der Tour"
                
            if len(packages) > 2:
                screen.ids.next_stop_2.text = f"Danach: {packages[2][1]}"
            else:
                screen.ids.next_stop_2.text = "-"
        except Exception as e:
            print(f"Error updating delivery screen: {e}")

    def mark_delivered_and_next(self):
        """Mark current package as delivered and move to next"""
        try:
            packages = self.db.get_packages(status="pending")
            if packages:
                pkg_id = packages[0][0]
                self.db.update_package_status(pkg_id, "delivered")
                # Advance UI
                self.update_delivery_screen()
                print(f"Package {pkg_id} marked as delivered")
            else:
                self.stop_delivery_session()
        except Exception as e:
            print(f"Error marking delivered: {e}")

    def optimize_route(self):
        """Optimize delivery route and display on map"""
        try:
            packages = self.db.get_packages_with_coordinates()
            
            if not packages or len(packages) < 2:
                print("Not enough packages with coordinates for route optimization")
                return
            
            # Extract coordinates
            coords = [(pkg[5], pkg[6]) for pkg in packages if pkg[5] and pkg[6]]  # lat, lon
            
            if len(coords) < 2:
                print("Not enough geocoded addresses")
                return
            
            # Optimize route
            optimized_indices = self.route_optimizer.optimize_route(coords)
            
            # Update delivery_order in database for ALL packages in the optimized route
            for i, idx in enumerate(optimized_indices):
                pkg_id = packages[idx][0]
                self.db.update_delivery_order(pkg_id, i + 1)
            
            # Update map
            mapview = self.root.get_screen('map').ids.mapview
            mapview.clear_widgets()
            
            # Add markers for optimized route
            for i, idx in enumerate(optimized_indices):
                lat, lon = coords[idx]
                marker = MapMarker(lat=lat, lon=lon)
                mapview.add_widget(marker)
            
            # Center map on first location
            if optimized_indices:
                first_lat, first_lon = coords[optimized_indices[0]]
                mapview.center_on(first_lat, first_lon)
            
            print(f"Route optimized with {len(optimized_indices)} stops and persisted to database")
            self.refresh_packages() # Refresh list to show new order
        except Exception as e:
            print(f"Error optimizing route: {e}")

    def move_package_up(self, pkg_id):
        """Move a package up in the delivery order"""
        packages = self.db.get_packages()
        for i, pkg in enumerate(packages):
            if pkg[0] == pkg_id and i > 0:
                prev_pkg = packages[i-1]
                # Swap orders (delivery_order is at index 7)
                self.db.update_delivery_order(pkg[0], prev_pkg[7])
                self.db.update_delivery_order(prev_pkg[0], pkg[7])
                self.refresh_packages()
                break

    def move_package_down(self, pkg_id):
        """Move a package down in the delivery order"""
        packages = self.db.get_packages()
        for i, pkg in enumerate(packages):
            if pkg[0] == pkg_id and i < len(packages) - 1:
                next_pkg = packages[i+1]
                # Swap orders (delivery_order is at index 7)
                self.db.update_delivery_order(pkg[0], next_pkg[7])
                self.db.update_delivery_order(next_pkg[0], pkg[7])
                self.refresh_packages()
                break

    def start_navigation(self):
        """Start turn-by-turn navigation"""
        print("Navigation feature - opening external maps for current stop")
        packages = self.db.get_packages(status="pending")
        if packages:
            # Open first pending package in external maps
            first_pkg = packages[0]
            lat, lon = first_pkg[5], first_pkg[6]
            if lat and lon:
                import webbrowser
                url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
                webbrowser.open(url)
            else:
                print("No coordinates for first pending package")
        else:
            print("No pending packages found")

    def on_stop(self):
        self.db.close()

if __name__ == "__main__":
    ZustellApp().run()
