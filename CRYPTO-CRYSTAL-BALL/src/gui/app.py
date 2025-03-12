import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
import yaml
import os
from datetime import datetime
import threading
import colorsys
from ..utils.constants import SUPPORTED_CRYPTOCURRENCIES
from ..utils.theme import ThemeManager
from .pages.crypto_selection import CryptoSelectionPage
from .pages.model_training import ModelTrainingPage
from .pages.prediction_graphs import PredictionGraphsPage
from .pages.settings import SettingsPage
from ..data.data_acquisition import DataAcquisition
from ..models.master_predictor import MasterPredictor

class CryptoCrystalBallApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("CRYSTAL-CRYPTO-BALL")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        # Initialize components
        self.theme_manager = ThemeManager(self)
        self.data_acquisition = DataAcquisition()
        self.master_predictor = MasterPredictor()
        
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create header with holographic effect
        self.create_header()
        
        # Create main container with holographic panel effect
        self.main_container = self.create_holographic_panel()
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Initialize pages
        self.pages = {}
        self.current_page = None
        self.initialize_pages()
        
        # Show initial page
        self.show_page("crypto_selection")
        
        # Initialize state
        self.state = {
            "selected_crypto": None,
            "data_range": {"months": 1, "years": 1},
            "forecast_length": {"hours": 1, "days": 0},
            "enabled_models": {
                "LSTM": True,
                "CatBoost": True,
                "LightGBM": True,
                "Prophet": True,
                "RandomForest": True,
                "XGBoost": True,
                "MASTER": True
            },
            "live_predictions": True
        }

    def create_holographic_panel(self) -> ctk.CTkFrame:
        """Create a frame with holographic panel effect"""
        frame = ctk.CTkFrame(self)
        
        # Add gradient overlay
        gradient_canvas = tk.Canvas(frame, highlightthickness=0)
        gradient_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        def update_gradient():
            width = gradient_canvas.winfo_width()
            height = gradient_canvas.winfo_height()
            
            if width > 1 and height > 1:  # Only draw if dimensions are valid
                gradient_canvas.delete("gradient")
                
                # Create smooth gradient effect
                for i in range(height):
                    # Calculate color based on position
                    r = int(20 + (i/height) * 10)  # Dark blue base
                    g = int(30 + (i/height) * 15)
                    b = int(50 + (i/height) * 20)
                    color = f'#{r:02x}{g:02x}{b:02x}'
                    
                    gradient_canvas.create_line(
                        0, i, width, i,
                        fill=color,
                        tags="gradient"
                    )
                
                # Add subtle animation
                self.after(50, update_gradient)
        
        frame.bind("<Configure>", lambda e: update_gradient())
        return frame

    def create_header(self):
        """Create the animated header with holographic title effect"""
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        # Create canvas for title animation
        self.title_canvas = tk.Canvas(
            header_frame,
            height=100,
            bg=self.theme_manager.current_theme["colors"]["background"],
            highlightthickness=0
        )
        self.title_canvas.pack(fill="x", pady=(10, 5))
        
        # Create subtitle
        self.subtitle_label = ctk.CTkLabel(
            header_frame,
            text="CREATED BY PSYCHOPHORIA",
            font=("Helvetica", 12, "italic")
        )
        self.subtitle_label.pack(pady=(0, 10))
        
        # Initialize title animation
        self.title_angle = 0
        self.animate_title()

    def animate_title(self):
        """Animate the title with 3D color-shifting effect"""
        self.title_canvas.delete("all")
        width = self.title_canvas.winfo_width()
        height = self.title_canvas.winfo_height()
        
        # Title text
        text = "CRYSTAL-CRYPTO-BALL"
        font_size = min(width//20, 36)  # Responsive font size
        
        # Calculate 3D effect positions
        layers = 5
        for i in range(layers):
            # Calculate color based on layer and time
            hue = (datetime.now().timestamp() % 10) / 10 + (i / layers)
            if hue > 1:
                hue -= 1
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            color = f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'
            
            # Calculate offset based on animation angle
            offset_x = int(10 * np.cos(self.title_angle + i/layers))
            offset_y = int(10 * np.sin(self.title_angle + i/layers))
            
            # Draw text layer
            self.title_canvas.create_text(
                width/2 + offset_x,
                height/2 + offset_y,
                text=text,
                font=("Helvetica", font_size, "bold"),
                fill=color
            )
        
        # Update animation angle
        self.title_angle += 0.1
        if self.title_angle > 2 * np.pi:
            self.title_angle = 0
        
        # Update subtitle color to match the top layer
        hue = (datetime.now().timestamp() % 10) / 10
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        color = f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'
        self.subtitle_label.configure(text_color=color)
        
        # Continue animation
        self.after(50, self.animate_title)

    def initialize_pages(self):
        """Initialize all application pages"""
        self.pages = {
            "crypto_selection": CryptoSelectionPage(self.main_container, self),
            "model_training": ModelTrainingPage(self.main_container, self),
            "prediction_graphs": PredictionGraphsPage(self.main_container, self),
            "settings": SettingsPage(self.main_container, self)
        }
        
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name: str):
        """Show the specified page and hide others"""
        if page_name in self.pages:
            if self.current_page:
                self.current_page.grid_remove()
            self.pages[page_name].grid()
            self.current_page = self.pages[page_name]
            
            # Update page if needed
            if hasattr(self.current_page, "on_show"):
                self.current_page.on_show()

    def update_state(self, updates: Dict[str, Any]):
        """Update the application state"""
        self.state.update(updates)
        
        # Notify pages of state change
        for page in self.pages.values():
            if hasattr(page, "on_state_change"):
                page.on_state_change(self.state)

    def run(self):
        """Start the application"""
        self.mainloop()

if __name__ == "__main__":
    app = CryptoCrystalBallApp()
    app.run()
