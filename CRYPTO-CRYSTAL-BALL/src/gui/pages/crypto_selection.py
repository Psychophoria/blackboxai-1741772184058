import customtkinter as ctk
from typing import Optional, Callable
import re
from ...utils.constants import SUPPORTED_CRYPTOCURRENCIES
from datetime import datetime, timedelta

class CryptoSelectionPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Configure grid
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI components with enhanced visuals"""
        # Create holographic panel for search
        search_frame = self.create_holographic_panel()
        search_frame.grid(row=0, column=0, padx=20, pady=(20,10), sticky="ew")
        
        # Search Label with glow effect
        search_label = self.create_glowing_label(
            search_frame,
            text="Search Cryptocurrency:",
            font=(self.app.theme_manager.get_font(), 14)
        )
        search_label.pack(side="left", padx=10)
        
        # Search Entry with holographic effect
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.filter_cryptocurrencies)
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            textvariable=self.search_var,
            font=(self.app.theme_manager.get_font(), 12)
        )
        self.search_entry.pack(side="left", padx=10)
        
        # Create holographic panel for dropdown
        dropdown_frame = self.create_holographic_panel()
        dropdown_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Dropdown Label with glow effect
        dropdown_label = self.create_glowing_label(
            dropdown_frame,
            text="Select Cryptocurrency:",
            font=(self.app.theme_manager.get_font(), 14)
        )
        dropdown_label.pack(side="left", padx=10)
        
        # Dropdown List with enhanced visuals
        self.crypto_listbox = ctk.CTkOptionMenu(
            dropdown_frame,
            values=SUPPORTED_CRYPTOCURRENCIES,
            command=self.on_crypto_selected,
            font=(self.app.theme_manager.get_font(), 12)
        )
        self.crypto_listbox.pack(side="left", padx=10)
        
        # Set Button with glow effect
        self.set_button = ctk.CTkButton(
            dropdown_frame,
            text="SET",
            command=self.on_set_clicked,
            width=100,
            font=(self.app.theme_manager.get_font(), 12, "bold")
        )
        self.set_button.pack(side="left", padx=10)
        
        # Create holographic panel for data range
        range_frame = self.create_holographic_panel()
        range_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        # Data Range Label with glow effect
        range_label = self.create_glowing_label(
            range_frame,
            text="Historical Data Range:",
            font=(self.app.theme_manager.get_font(), 14)
        )
        range_label.pack(pady=(0, 10))
        
        # Months Controls
        months_frame = ctk.CTkFrame(range_frame, fg_color="transparent")
        months_frame.pack(fill="x", padx=10, pady=5)
        
        months_label = self.create_glowing_label(
            months_frame,
            text="Months:",
            font=(self.app.theme_manager.get_font(), 12)
        )
        months_label.pack(side="left", padx=10)
        
        self.months_slider = ctk.CTkSlider(
            months_frame,
            from_=1,
            to=12,
            number_of_steps=11,
            command=self.on_months_changed
        )
        self.months_slider.pack(side="left", padx=10, expand=True, fill="x")
        
        self.months_value = self.create_glowing_label(
            months_frame,
            text="1",
            font=(self.app.theme_manager.get_font(), 12)
        )
        self.months_value.pack(side="left", padx=5)
        
        # Years Controls
        years_frame = ctk.CTkFrame(range_frame, fg_color="transparent")
        years_frame.pack(fill="x", padx=10, pady=5)
        
        years_label = self.create_glowing_label(
            years_frame,
            text="Years:",
            font=(self.app.theme_manager.get_font(), 12)
        )
        years_label.pack(side="left", padx=10)
        
        self.years_slider = ctk.CTkSlider(
            years_frame,
            from_=1,
            to=10,
            number_of_steps=9,
            command=self.on_years_changed
        )
        self.years_slider.pack(side="left", padx=10, expand=True, fill="x")
        
        self.years_value = self.create_glowing_label(
            years_frame,
            text="1",
            font=(self.app.theme_manager.get_font(), 12)
        )
        self.years_value.pack(side="left", padx=5)
        
        # Date Range Display
        self.date_range_label = self.create_glowing_label(
            range_frame,
            text="",
            font=(self.app.theme_manager.get_font(), 12, "italic")
        )
        self.date_range_label.pack(pady=(10, 0))
        self.update_date_range_display()
        
        # Next Button with enhanced visuals
        self.next_button = ctk.CTkButton(
            self,
            text="Next →",
            command=self.on_next_clicked,
            state="disabled",
            font=(self.app.theme_manager.get_font(), 14, "bold")
        )
        self.next_button.grid(row=4, column=0, padx=20, pady=20, sticky="e")

    def create_holographic_panel(self) -> ctk.CTkFrame:
        """Create a frame with holographic panel effect"""
        frame = ctk.CTkFrame(self)
        self.app.theme_manager.create_holographic_effect(frame)
        return frame

    def create_glowing_label(self, parent, **kwargs) -> ctk.CTkLabel:
        """Create a label with glow effect"""
        label = ctk.CTkLabel(parent, **kwargs)
        
        def update_glow():
            # Calculate glow color based on time
            t = datetime.now().timestamp()
            intensity = (np.sin(t) + 1) / 2  # Oscillate between 0 and 1
            
            # Get the base color from theme
            base_color = self.app.theme_manager.current_theme["colors"]["text"]
            glow_color = self.app.theme_manager.current_theme["colors"]["holographic"]["glow"]
            
            # Interpolate between base color and glow color
            r1, g1, b1 = int(base_color[1:3], 16), int(base_color[3:5], 16), int(base_color[5:7], 16)
            r2, g2, b2 = int(glow_color[1:3], 16), int(glow_color[3:5], 16), int(glow_color[5:7], 16)
            
            r = int(r1 * (1 - intensity) + r2 * intensity)
            g = int(g1 * (1 - intensity) + g2 * intensity)
            b = int(b1 * (1 - intensity) + b2 * intensity)
            
            color = f'#{r:02x}{g:02x}{b:02x}'
            label.configure(text_color=color)
            
            # Continue animation
            self.after(50, update_glow)
        
        update_glow()
        return label

    def filter_cryptocurrencies(self, *args):
        """Filter the cryptocurrency list based on search input"""
        search_text = self.search_var.get().upper()
        filtered_cryptos = [
            crypto for crypto in SUPPORTED_CRYPTOCURRENCIES
            if search_text in crypto
        ]
        self.crypto_listbox.configure(values=filtered_cryptos)
        if filtered_cryptos:
            self.crypto_listbox.set(filtered_cryptos[0])

    def on_crypto_selected(self, selection: str):
        """Handle cryptocurrency selection"""
        self.selected_crypto = selection
        self.set_button.configure(state="normal")
        self.search_var.set(selection)  # Update search bar with selection

    def on_set_clicked(self):
        """Handle SET button click"""
        if hasattr(self, 'selected_crypto'):
            self.app.update_state({
                "selected_crypto": self.selected_crypto
            })
            self.next_button.configure(state="normal")

    def on_months_changed(self, value: float):
        """Handle months slider change"""
        months = int(value)
        self.months_value.configure(text=str(months))
        self.app.update_state({
            "data_range": {
                "months": months,
                "years": int(self.years_slider.get())
            }
        })
        self.update_date_range_display()

    def on_years_changed(self, value: float):
        """Handle years slider change"""
        years = int(value)
        self.years_value.configure(text=str(years))
        self.app.update_state({
            "data_range": {
                "months": int(self.months_slider.get()),
                "years": years
            }
        })
        self.update_date_range_display()

    def update_date_range_display(self):
        """Update the display of the date range"""
        end_date = datetime.now()
        months = int(self.months_slider.get())
        years = int(self.years_slider.get())
        
        start_date = end_date - timedelta(days=(years * 365 + months * 30))
        
        self.date_range_label.configure(
            text=f"Data Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        )

    def on_next_clicked(self):
        """Handle Next button click"""
        self.app.show_page("model_training")

    def on_show(self):
        """Called when the page is shown"""
        # Reset search
        self.search_var.set("")
        
        # Reset sliders
        self.months_slider.set(1)
        self.years_slider.set(1)
        
        # Update date range display
        self.update_date_range_display()
        
        # Disable next button if no crypto selected
        if not self.app.state["selected_crypto"]:
            self.next_button.configure(state="disabled")
