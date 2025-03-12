import customtkinter as ctk
from typing import Dict, Any
import json
import os
import colorsys

class ThemeManager:
    def __init__(self, app):
        self.app = app
        self.default_theme = {
            "colors": {
                "primary": "#1f538d",
                "secondary": "#14213d",
                "accent": "#00ff9d",
                "background": "#000000",
                "text": "#ffffff",
                "holographic": {
                    "base": "#102030",
                    "highlight": "#204060",
                    "glow": "#00ff9d"
                },
                "graph_colors": {
                    "LSTM": "#ff0000",
                    "CatBoost": "#00ff00",
                    "LightGBM": "#0000ff",
                    "Prophet": "#ffff00",
                    "RandomForest": "#ff00ff",
                    "XGBoost": "#00ffff",
                    "MASTER": "#ffffff",
                    "Live": "#ffa500"
                },
                "indicators": {
                    "buy": "#00ff00",
                    "sell": "#ff0000",
                    "neutral": "#ffffff"
                }
            },
            "fonts": {
                "main": "Helvetica",
                "secondary": "Arial",
                "monospace": "Courier New"
            },
            "appearance": {
                "mode": "dark",
                "transparency": 0.95,
                "animation_speed": 1.0,
                "holographic_effect": True,
                "glow_effect": True
            },
            "animations": {
                "title": {
                    "enabled": True,
                    "speed": 1.0,
                    "color_shift": True,
                    "3d_effect": True
                },
                "buttons": {
                    "enabled": True,
                    "hover_effect": True,
                    "glow_effect": True
                },
                "graphs": {
                    "enabled": True,
                    "transition_speed": 1.0,
                    "hover_highlight": True
                }
            },
            "layout": {
                "padding": 20,
                "border_radius": 10,
                "shadow": True
            }
        }
        
        self.current_theme = self.load_theme()
        self.apply_theme()

    def load_theme(self) -> Dict[str, Any]:
        """Load theme from file or return default"""
        theme_path = os.path.join("configs", "theme.json")
        try:
            if os.path.exists(theme_path):
                with open(theme_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading theme: {e}")
        return self.default_theme.copy()

    def save_theme(self):
        """Save current theme to file"""
        theme_path = os.path.join("configs", "theme.json")
        os.makedirs(os.path.dirname(theme_path), exist_ok=True)
        try:
            with open(theme_path, 'w') as f:
                json.dump(self.current_theme, f, indent=4)
        except Exception as e:
            print(f"Error saving theme: {e}")

    def apply_theme(self):
        """Apply the current theme to the application"""
        # Set appearance mode
        ctk.set_appearance_mode(self.current_theme["appearance"]["mode"])
        
        # Set default color theme
        ctk.set_default_color_theme("dark-blue")
        
        # Configure window transparency
        self.app.attributes("-alpha", self.current_theme["appearance"]["transparency"])
        
        # Configure widget colors and styles
        self.configure_widgets()

    def configure_widgets(self):
        """Configure colors and styles for all widgets"""
        style = {
            "CTkButton": {
                "fg_color": self.current_theme["colors"]["primary"],
                "hover_color": self.current_theme["colors"]["secondary"],
                "text_color": self.current_theme["colors"]["text"],
                "corner_radius": self.current_theme["layout"]["border_radius"]
            },
            "CTkFrame": {
                "fg_color": self.current_theme["colors"]["background"],
                "border_color": self.current_theme["colors"]["accent"],
                "corner_radius": self.current_theme["layout"]["border_radius"]
            },
            "CTkLabel": {
                "text_color": self.current_theme["colors"]["text"],
                "corner_radius": self.current_theme["layout"]["border_radius"]
            },
            "CTkEntry": {
                "fg_color": self.current_theme["colors"]["secondary"],
                "text_color": self.current_theme["colors"]["text"],
                "border_color": self.current_theme["colors"]["accent"],
                "corner_radius": self.current_theme["layout"]["border_radius"]
            },
            "CTkOptionMenu": {
                "fg_color": self.current_theme["colors"]["primary"],
                "button_color": self.current_theme["colors"]["secondary"],
                "button_hover_color": self.current_theme["colors"]["accent"],
                "text_color": self.current_theme["colors"]["text"],
                "corner_radius": self.current_theme["layout"]["border_radius"]
            },
            "CTkSwitch": {
                "progress_color": self.current_theme["colors"]["accent"],
                "button_color": self.current_theme["colors"]["primary"],
                "button_hover_color": self.current_theme["colors"]["secondary"],
                "text_color": self.current_theme["colors"]["text"]
            },
            "CTkSlider": {
                "progress_color": self.current_theme["colors"]["accent"],
                "button_color": self.current_theme["colors"]["primary"],
                "button_hover_color": self.current_theme["colors"]["secondary"]
            },
            "CTkProgressBar": {
                "progress_color": self.current_theme["colors"]["accent"],
                "border_color": self.current_theme["colors"]["primary"]
            },
            "CTkTabview": {
                "fg_color": self.current_theme["colors"]["background"],
                "segmented_button_fg_color": self.current_theme["colors"]["primary"],
                "segmented_button_selected_color": self.current_theme["colors"]["accent"],
                "segmented_button_unselected_color": self.current_theme["colors"]["secondary"],
                "text_color": self.current_theme["colors"]["text"]
            }
        }
        
        for widget_type, config in style.items():
            try:
                widget_class = getattr(ctk, widget_type)
                widget_class._set_appearance_mode(self.current_theme["appearance"]["mode"])
                for prop, value in config.items():
                    setattr(widget_class, f"_default_{prop}", value)
            except Exception as e:
                print(f"Error configuring {widget_type}: {e}")

    def create_holographic_effect(self, widget):
        """Create holographic effect for a widget"""
        if not self.current_theme["appearance"]["holographic_effect"]:
            return
            
        canvas = widget.canvas if hasattr(widget, "canvas") else None
        if canvas:
            def update_effect():
                width = canvas.winfo_width()
                height = canvas.winfo_height()
                
                if width > 1 and height > 1:
                    canvas.delete("holographic")
                    
                    # Create gradient effect
                    for i in range(height):
                        # Calculate color based on position and time
                        hue = (i/height + (datetime.now().timestamp() % 5) / 5) % 1
                        rgb = colorsys.hsv_to_rgb(hue, 0.2, 0.1)  # Low saturation for subtle effect
                        color = f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'
                        
                        canvas.create_line(
                            0, i, width, i,
                            fill=color,
                            tags="holographic"
                        )
                    
                    # Add highlight effect
                    highlight_pos = (datetime.now().timestamp() % 2) / 2  # Move highlight up and down
                    highlight_y = int(height * highlight_pos)
                    
                    canvas.create_line(
                        0, highlight_y, width, highlight_y,
                        fill=self.current_theme["colors"]["holographic"]["highlight"],
                        width=2,
                        tags="holographic"
                    )
                    
                    if self.current_theme["appearance"]["glow_effect"]:
                        # Add glow effect
                        glow_color = self.current_theme["colors"]["holographic"]["glow"]
                        canvas.create_line(
                            0, highlight_y-1, width, highlight_y-1,
                            fill=glow_color,
                            width=1,
                            tags="holographic"
                        )
                        canvas.create_line(
                            0, highlight_y+1, width, highlight_y+1,
                            fill=glow_color,
                            width=1,
                            tags="holographic"
                        )
                
                widget.after(50, update_effect)
            
            update_effect()

    def get_graph_color(self, model_name: str) -> str:
        """Get the color for a specific model's graph"""
        return self.current_theme["colors"]["graph_colors"].get(
            model_name,
            self.default_theme["colors"]["graph_colors"].get(model_name, "#ffffff")
        )

    def get_indicator_color(self, indicator_type: str) -> str:
        """Get the color for a specific indicator type"""
        return self.current_theme["colors"]["indicators"].get(
            indicator_type,
            self.default_theme["colors"]["indicators"].get(indicator_type, "#ffffff")
        )

    def get_font(self, font_type: str = "main") -> str:
        """Get the specified font"""
        return self.current_theme["fonts"].get(
            font_type,
            self.default_theme["fonts"].get(font_type, "Helvetica")
        )

    def update_theme(self, updates: Dict[str, Any]):
        """Update theme with new values"""
        def deep_update(d, u):
            for k, v in u.items():
                if isinstance(v, dict) and k in d:
                    deep_update(d[k], v)
                else:
                    d[k] = v
        
        deep_update(self.current_theme, updates)
        self.save_theme()
        self.apply_theme()
