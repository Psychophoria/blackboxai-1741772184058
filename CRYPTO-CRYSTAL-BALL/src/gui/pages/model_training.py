import customtkinter as ctk
from typing import Dict, Any
import threading
from datetime import datetime, timedelta
import time
import numpy as np
from ...utils.constants import MODEL_INFO, FORECAST_LENGTH_LIMITS

class ModelTrainingPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Configure grid
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.model_switches: Dict[str, ctk.CTkSwitch] = {}
        self._stop_acquisition = False
        self._stop_prediction = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI components with enhanced visuals"""
        # Models Frame with holographic effect
        models_frame = self.create_holographic_panel()
        models_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Models Label with glow effect
        models_label = self.create_glowing_label(
            models_frame,
            text="Prediction Models",
            font=(self.app.theme_manager.get_font(), 16, "bold")
        )
        models_label.pack(pady=10)
        
        # Model Switches with enhanced visuals
        for model_name, description in MODEL_INFO.items():
            switch_frame = ctk.CTkFrame(models_frame, fg_color="transparent")
            switch_frame.pack(fill="x", padx=20, pady=5)
            
            switch = ctk.CTkSwitch(
                switch_frame,
                text=model_name,
                command=lambda m=model_name: self.on_model_toggle(m),
                font=(self.app.theme_manager.get_font(), 12)
            )
            switch.pack(side="left", padx=10)
            self.model_switches[model_name] = switch
            
            info_label = self.create_glowing_label(
                switch_frame,
                text=description,
                font=(self.app.theme_manager.get_font(), 12),
                anchor="w"
            )
            info_label.pack(side="left", padx=10, fill="x", expand=True)
            
            # Enable all switches by default
            switch.select()
        
        # Forecast Length Frame with holographic effect
        forecast_frame = self.create_holographic_panel()
        forecast_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Forecast Length Label
        forecast_label = self.create_glowing_label(
            forecast_frame,
            text="Forecast Length",
            font=(self.app.theme_manager.get_font(), 14, "bold")
        )
        forecast_label.pack(pady=10)
        
        # Hours Controls
        hours_frame = ctk.CTkFrame(forecast_frame, fg_color="transparent")
        hours_frame.pack(fill="x", padx=10, pady=5)
        
        hours_label = self.create_glowing_label(
            hours_frame,
            text="Hours:",
            font=(self.app.theme_manager.get_font(), 12)
        )
        hours_label.pack(side="left", padx=10)
        
        self.hours_slider = ctk.CTkSlider(
            hours_frame,
            from_=FORECAST_LENGTH_LIMITS["hours"]["min"],
            to=FORECAST_LENGTH_LIMITS["hours"]["max"],
            number_of_steps=FORECAST_LENGTH_LIMITS["hours"]["max"] - FORECAST_LENGTH_LIMITS["hours"]["min"],
            command=self.on_hours_changed
        )
        self.hours_slider.pack(side="left", padx=10, expand=True, fill="x")
        
        self.hours_value = self.create_glowing_label(
            hours_frame,
            text="1",
            font=(self.app.theme_manager.get_font(), 12)
        )
        self.hours_value.pack(side="left", padx=5)
        
        # Days Controls
        days_frame = ctk.CTkFrame(forecast_frame, fg_color="transparent")
        days_frame.pack(fill="x", padx=10, pady=5)
        
        days_label = self.create_glowing_label(
            days_frame,
            text="Days:",
            font=(self.app.theme_manager.get_font(), 12)
        )
        days_label.pack(side="left", padx=10)
        
        self.days_slider = ctk.CTkSlider(
            days_frame,
            from_=FORECAST_LENGTH_LIMITS["days"]["min"],
            to=FORECAST_LENGTH_LIMITS["days"]["max"],
            number_of_steps=FORECAST_LENGTH_LIMITS["days"]["max"] - FORECAST_LENGTH_LIMITS["days"]["min"],
            command=self.on_days_changed
        )
        self.days_slider.pack(side="left", padx=10, expand=True, fill="x")
        
        self.days_value = self.create_glowing_label(
            days_frame,
            text="0",
            font=(self.app.theme_manager.get_font(), 12)
        )
        self.days_value.pack(side="left", padx=5)
        
        # Live Prediction Frame
        live_frame = self.create_holographic_panel()
        live_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.live_switch = ctk.CTkSwitch(
            live_frame,
            text="Enable Live Predictions",
            command=self.on_live_toggle,
            font=(self.app.theme_manager.get_font(), 12)
        )
        self.live_switch.pack(side="left", padx=10)
        self.live_switch.select()  # Enable by default
        
        # Buttons Frame
        buttons_frame = self.create_holographic_panel()
        buttons_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        
        # Back Button
        self.back_button = ctk.CTkButton(
            buttons_frame,
            text="← Back",
            command=self.on_back_clicked,
            font=(self.app.theme_manager.get_font(), 12)
        )
        self.back_button.pack(side="left", padx=10)
        
        # Acquire Data Button
        self.acquire_button = ctk.CTkButton(
            buttons_frame,
            text="ACQUIRE DATA",
            command=self.on_acquire_clicked,
            font=(self.app.theme_manager.get_font(), 12, "bold")
        )
        self.acquire_button.pack(side="left", padx=10)
        
        # Start Prediction Button
        self.predict_button = ctk.CTkButton(
            buttons_frame,
            text="START PREDICTION",
            command=self.on_predict_clicked,
            state="disabled",
            font=(self.app.theme_manager.get_font(), 12, "bold")
        )
        self.predict_button.pack(side="left", padx=10)
        
        # Progress Frame with holographic effect
        progress_frame = self.create_holographic_panel()
        progress_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)
        
        self.progress_label = self.create_glowing_label(
            progress_frame,
            text="",
            font=(self.app.theme_manager.get_font(), 12)
        )
        self.progress_label.pack(pady=5)
        
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
        
    def on_model_toggle(self, model_name: str):
        """Handle model toggle"""
        enabled_models = {
            name: switch.get() for name, switch in self.model_switches.items()
        }
        self.app.update_state({"enabled_models": enabled_models})
        
    def on_hours_changed(self, value: float):
        """Handle hours slider change"""
        hours = int(value)
        self.hours_value.configure(text=str(hours))
        self.app.update_state({
            "forecast_length": {
                "hours": hours,
                "days": int(self.days_slider.get())
            }
        })
        
    def on_days_changed(self, value: float):
        """Handle days slider change"""
        days = int(value)
        self.days_value.configure(text=str(days))
        self.app.update_state({
            "forecast_length": {
                "hours": int(self.hours_slider.get()),
                "days": days
            }
        })
        
    def on_live_toggle(self):
        """Handle live predictions toggle"""
        self.app.update_state({
            "live_predictions": self.live_switch.get()
        })
        
    def on_back_clicked(self):
        """Handle Back button click"""
        self.app.show_page("crypto_selection")
        
    def on_acquire_clicked(self):
        """Handle Acquire Data button click"""
        self.acquire_button.configure(state="disabled")
        self.back_button.configure(state="disabled")
        
        def acquire_data():
            start_time = time.time()
            try:
                # Get data using DataAcquisition
                data = self.app.data_acquisition.get_historical_data(
                    self.app.state["selected_crypto"],
                    start_date=(datetime.now() - timedelta(
                        days=self.app.state["data_range"]["years"] * 365 +
                             self.app.state["data_range"]["months"] * 30
                    )).strftime("%Y-%m-%d"),
                    end_date=datetime.now().strftime("%Y-%m-%d")
                )
                
                # Store data in app state
                self.app.update_state({"historical_data": data})
                
                self.progress_bar.set(1)
                self.progress_label.configure(text="Data acquisition complete!")
                self.predict_button.configure(state="normal")
                self.back_button.configure(state="normal")
                
            except Exception as e:
                self.progress_label.configure(text=f"Error: {str(e)}")
                self.acquire_button.configure(state="normal")
                self.back_button.configure(state="normal")
        
        self._stop_acquisition = False
        threading.Thread(target=acquire_data, daemon=True).start()
        
    def on_predict_clicked(self):
        """Handle Start Prediction button click"""
        self.predict_button.configure(state="disabled")
        self.back_button.configure(state="disabled")
        
        def run_prediction():
            start_time = time.time()
            try:
                # Train models and generate predictions
                self.app.master_predictor.train_models(
                    self.app.state["historical_data"],
                    self.app.state["enabled_models"]
                )
                
                master_prediction, individual_predictions = self.app.master_predictor.predict(
                    self.app.state["historical_data"],
                    self.app.state["forecast_length"],
                    self.app.state["enabled_models"]
                )
                
                # Store predictions in app state
                self.app.update_state({
                    "master_prediction": master_prediction,
                    "individual_predictions": individual_predictions
                })
                
                self.progress_bar.set(1)
                self.progress_label.configure(text="Predictions complete!")
                
                # Show completion popup
                self.show_completion_popup()
                
            except Exception as e:
                self.progress_label.configure(text=f"Error: {str(e)}")
                self.predict_button.configure(state="normal")
                self.back_button.configure(state="normal")
        
        self._stop_prediction = False
        threading.Thread(target=run_prediction, daemon=True).start()
        
    def show_completion_popup(self):
        """Show prediction completion popup with enhanced visuals"""
        popup = ctk.CTkToplevel(self)
        popup.title("Predictions Complete")
        popup.geometry("400x200")
        
        # Create holographic panel for popup
        popup_frame = self.create_holographic_panel()
        popup_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        label = self.create_glowing_label(
            popup_frame,
            text="Price predictions have been generated & are complete!",
            font=(self.app.theme_manager.get_font(), 14),
            wraplength=300
        )
        label.pack(pady=20)
        
        button = ctk.CTkButton(
            popup_frame,
            text="VIEW PREDICTION GRAPHS & DATA",
            command=lambda: [popup.destroy(), self.app.show_page("prediction_graphs")],
            font=(self.app.theme_manager.get_font(), 12, "bold")
        )
        button.pack(pady=20)
        
    def on_show(self):
        """Called when the page is shown"""
        # Reset progress
        self.progress_bar.set(0)
        self.progress_label.configure(text="")
        
        # Reset buttons
        self.acquire_button.configure(state="normal")
        self.predict_button.configure(state="disabled")
        self.back_button.configure(state="normal")
        
        # Stop any running processes
        self._stop_acquisition = True
        self._stop_prediction = True
