import customtkinter as ctk
from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime
from ...utils.constants import GRAPH_TYPES, OVERLAY_TYPES

class PredictionGraphsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI components with enhanced visuals"""
        # Controls Panel (Left Side) with holographic effect
        controls_frame = self.create_holographic_panel()
        controls_frame.grid(row=0, rowspan=2, column=0, padx=10, pady=10, sticky="nsew")
        
        # Graph Controls
        controls_label = self.create_glowing_label(
            controls_frame,
            text="Graph Controls",
            font=(self.app.theme_manager.get_font(), 16, "bold")
        )
        controls_label.pack(pady=10)
        
        # Graph Type Selection
        type_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        type_frame.pack(fill="x", padx=10, pady=5)
        
        type_label = self.create_glowing_label(
            type_frame,
            text="Graph Type:",
            font=(self.app.theme_manager.get_font(), 12)
        )
        type_label.pack(side="left", padx=5)
        
        self.graph_type = ctk.CTkOptionMenu(
            type_frame,
            values=GRAPH_TYPES,
            command=self.update_graph,
            font=(self.app.theme_manager.get_font(), 12)
        )
        self.graph_type.pack(side="left", padx=5)
        
        # Model Visibility Controls
        models_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        models_frame.pack(fill="x", padx=10, pady=10)
        
        models_label = self.create_glowing_label(
            models_frame,
            text="Show/Hide Models:",
            font=(self.app.theme_manager.get_font(), 12)
        )
        models_label.pack(anchor="w", padx=5, pady=5)
        
        self.model_switches = {}
        self.model_colors = {}
        
        for model in self.app.state["enabled_models"]:
            if self.app.state["enabled_models"][model]:
                model_frame = ctk.CTkFrame(models_frame, fg_color="transparent")
                model_frame.pack(fill="x", padx=5, pady=2)
                
                switch = ctk.CTkSwitch(
                    model_frame,
                    text=model,
                    command=self.update_graph,
                    font=(self.app.theme_manager.get_font(), 12)
                )
                switch.pack(side="left", padx=5)
                switch.select()
                self.model_switches[model] = switch
                
                # Color picker button
                color_button = ctk.CTkButton(
                    model_frame,
                    text="Color",
                    width=60,
                    command=lambda m=model: self.pick_color(m),
                    font=(self.app.theme_manager.get_font(), 12)
                )
                color_button.pack(side="left", padx=5)
                
                # Initialize with theme color
                self.model_colors[model] = self.app.theme_manager.get_graph_color(model)
        
        # Overlay Controls
        overlays_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        overlays_frame.pack(fill="x", padx=10, pady=10)
        
        overlays_label = self.create_glowing_label(
            overlays_frame,
            text="Overlays:",
            font=(self.app.theme_manager.get_font(), 12)
        )
        overlays_label.pack(anchor="w", padx=5, pady=5)
        
        self.overlay_switches = {}
        for overlay_id, overlay_name in OVERLAY_TYPES.items():
            overlay_frame = ctk.CTkFrame(overlays_frame, fg_color="transparent")
            overlay_frame.pack(fill="x", padx=5, pady=2)
            
            switch = ctk.CTkSwitch(
                overlay_frame,
                text=overlay_name,
                command=self.update_graph,
                font=(self.app.theme_manager.get_font(), 12)
            )
            switch.pack(side="left", padx=5)
            self.overlay_switches[overlay_id] = switch
            
            # Color picker for overlay
            color_button = ctk.CTkButton(
                overlay_frame,
                text="Color",
                width=60,
                command=lambda o=overlay_id: self.pick_overlay_color(o),
                font=(self.app.theme_manager.get_font(), 12)
            )
            color_button.pack(side="left", padx=5)
        
        # Graph Display (Right Side) with holographic effect
        graph_frame = self.create_holographic_panel()
        graph_frame.grid(row=0, rowspan=2, column=1, padx=10, pady=10, sticky="nsew")
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Data Display (Bottom) with holographic effect
        data_frame = self.create_holographic_panel()
        data_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        data_label = self.create_glowing_label(
            data_frame,
            text="Prediction Data",
            font=(self.app.theme_manager.get_font(), 16, "bold")
        )
        data_label.pack(pady=10)
        
        # Create tabs for different data views
        self.data_notebook = ctk.CTkTabview(data_frame)
        self.data_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Static Predictions Tab
        static_tab = self.data_notebook.add("Static Predictions")
        self.setup_data_tab(static_tab, "static")
        
        # Live Predictions Tab
        live_tab = self.data_notebook.add("Live Predictions")
        self.setup_data_tab(live_tab, "live")
        
        # Live Actual Data Tab
        actual_tab = self.data_notebook.add("Live Actual Data")
        self.setup_data_tab(actual_tab, "actual")
        
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
        
    def setup_data_tab(self, tab: ctk.CTkFrame, data_type: str):
        """Setup a data display tab with enhanced visuals"""
        # Create a scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True)
        
        if data_type in ["static", "live"]:
            for model in self.app.state["enabled_models"]:
                if self.app.state["enabled_models"][model]:
                    model_frame = self.create_holographic_panel()
                    model_frame.pack(fill="x", padx=5, pady=5)
                    
                    model_label = self.create_glowing_label(
                        model_frame,
                        text=f"{model} Predictions:",
                        font=(self.app.theme_manager.get_font(), 12, "bold")
                    )
                    model_label.pack(anchor="w", padx=5, pady=5)
                    
                    # Placeholder for prediction data
                    data_label = self.create_glowing_label(
                        model_frame,
                        text="Loading prediction data...",
                        font=(self.app.theme_manager.get_font(), 10)
                    )
                    data_label.pack(anchor="w", padx=5, pady=5)
        else:  # actual data tab
            actual_frame = self.create_holographic_panel()
            actual_frame.pack(fill="x", padx=5, pady=5)
            
            actual_label = self.create_glowing_label(
                actual_frame,
                text="Live Market Data:",
                font=(self.app.theme_manager.get_font(), 12, "bold")
            )
            actual_label.pack(anchor="w", padx=5, pady=5)
            
            # Placeholder for actual data
            data_label = self.create_glowing_label(
                actual_frame,
                text="Loading market data...",
                font=(self.app.theme_manager.get_font(), 10)
            )
            data_label.pack(anchor="w", padx=5, pady=5)
    
    def update_graph(self, *args):
        """Update the graph display with enhanced visuals"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        # Set dark theme for plot
        self.figure.patch.set_facecolor(self.app.theme_manager.current_theme["colors"]["background"])
        ax.set_facecolor(self.app.theme_manager.current_theme["colors"]["background"])
        
        # Plot enabled models
        if hasattr(self.app.state, "master_prediction") and hasattr(self.app.state, "individual_predictions"):
            for model_name, switch in self.model_switches.items():
                if switch.get():
                    if model_name == "MASTER":
                        data = self.app.state["master_prediction"]
                    else:
                        data = self.app.state["individual_predictions"][model_name]
                    
                    if self.graph_type.get() == "line":
                        ax.plot(data.index, data["Close"],
                               label=model_name,
                               color=self.model_colors[model_name])
                    elif self.graph_type.get() == "candle":
                        self.plot_candlesticks(ax, data, model_name)
                    elif self.graph_type.get() == "bar":
                        ax.bar(data.index, data["Close"],
                              label=model_name,
                              color=self.model_colors[model_name],
                              alpha=0.5)
        
        # Add overlays
        for overlay_id, switch in self.overlay_switches.items():
            if switch.get():
                self.add_overlay(ax, overlay_id)
        
        # Customize plot appearance
        ax.set_title(f"{self.app.state['selected_crypto']} Price Prediction",
                    color=self.app.theme_manager.current_theme["colors"]["text"])
        ax.set_xlabel("Time", color=self.app.theme_manager.current_theme["colors"]["text"])
        ax.set_ylabel("Price", color=self.app.theme_manager.current_theme["colors"]["text"])
        
        # Style grid
        ax.grid(True, color=self.app.theme_manager.current_theme["colors"]["secondary"], alpha=0.2)
        
        # Style ticks
        ax.tick_params(colors=self.app.theme_manager.current_theme["colors"]["text"])
        
        # Style legend
        ax.legend(facecolor=self.app.theme_manager.current_theme["colors"]["background"],
                 edgecolor=self.app.theme_manager.current_theme["colors"]["accent"],
                 labelcolor=self.app.theme_manager.current_theme["colors"]["text"])
        
        self.canvas.draw()
    
    def plot_candlesticks(self, ax, data, model_name):
        """Plot candlestick chart"""
        width = 0.6
        up_color = self.app.theme_manager.get_indicator_color("buy")
        down_color = self.app.theme_manager.get_indicator_color("sell")
        
        for i in range(1, len(data)):
            open_price = data["Close"].iloc[i-1]
            close_price = data["Close"].iloc[i]
            high_price = max(open_price, close_price)
            low_price = min(open_price, close_price)
            
            color = up_color if close_price >= open_price else down_color
            
            # Plot candlestick body
            ax.bar(data.index[i], close_price - open_price,
                  bottom=open_price, width=width,
                  color=color, alpha=0.8)
            
            # Plot wicks
            ax.plot([data.index[i], data.index[i]],
                   [low_price, high_price],
                   color=color, linewidth=1)
    
    def add_overlay(self, ax, overlay_id):
        """Add overlay to the graph"""
        if overlay_id == "buy_sell":
            # Add buy/sell signals
            for model_name, switch in self.model_switches.items():
                if switch.get():
                    if model_name == "MASTER":
                        data = self.app.state["master_prediction"]
                    else:
                        data = self.app.state["individual_predictions"][model_name]
                    
                    # Calculate signals (example logic)
                    sma = data["Close"].rolling(window=20).mean()
                    buy_signals = data[data["Close"] > sma].index
                    sell_signals = data[data["Close"] < sma].index
                    
                    ax.scatter(buy_signals, data.loc[buy_signals, "Close"],
                             marker="^", color=self.app.theme_manager.get_indicator_color("buy"),
                             label=f"{model_name} Buy", alpha=0.7)
                    ax.scatter(sell_signals, data.loc[sell_signals, "Close"],
                             marker="v", color=self.app.theme_manager.get_indicator_color("sell"),
                             label=f"{model_name} Sell", alpha=0.7)
        
        elif overlay_id == "high_low":
            # Add high/low points
            for model_name, switch in self.model_switches.items():
                if switch.get():
                    if model_name == "MASTER":
                        data = self.app.state["master_prediction"]
                    else:
                        data = self.app.state["individual_predictions"][model_name]
                    
                    # Calculate local maxima/minima
                    window = 20
                    highs = data["Close"].rolling(window=window, center=True).max()
                    lows = data["Close"].rolling(window=window, center=True).min()
                    
                    ax.plot(data.index, highs, '--',
                           color=self.app.theme_manager.get_indicator_color("buy"),
                           alpha=0.5, label=f"{model_name} High")
                    ax.plot(data.index, lows, '--',
                           color=self.app.theme_manager.get_indicator_color("sell"),
                           alpha=0.5, label=f"{model_name} Low")
        
        elif overlay_id == "volatility":
            # Add volatility bands
            for model_name, switch in self.model_switches.items():
                if switch.get():
                    if model_name == "MASTER":
                        data = self.app.state["master_prediction"]
                    else:
                        data = self.app.state["individual_predictions"][model_name]
                    
                    # Calculate Bollinger Bands
                    window = 20
                    std = data["Close"].rolling(window=window).std()
                    sma = data["Close"].rolling(window=window).mean()
                    upper = sma + (std * 2)
                    lower = sma - (std * 2)
                    
                    ax.fill_between(data.index, upper, lower,
                                  color=self.model_colors[model_name],
                                  alpha=0.1, label=f"{model_name} Volatility")
        
        elif overlay_id == "volume":
            # Add volume indicators
            ax2 = ax.twinx()  # Create second y-axis
            
            for model_name, switch in self.model_switches.items():
                if switch.get():
                    if model_name == "MASTER":
                        data = self.app.state["master_prediction"]
                    else:
                        data = self.app.state["individual_predictions"][model_name]
                    
                    # Calculate volume profile
                    volume = data["Close"].diff().abs()  # Simulated volume based on price changes
                    ax2.bar(data.index, volume,
                           color=self.model_colors[model_name],
                           alpha=0.3, label=f"{model_name} Volume")
            
            ax2.set_ylabel("Volume", color=self.app.theme_manager.current_theme["colors"]["text"])
            ax2.tick_params(colors=self.app.theme_manager.current_theme["colors"]["text"])
    
    def pick_color(self, model: str):
        """Open color picker for model graph"""
        # Create color picker dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Pick Color for {model}")
        dialog.geometry("300x400")
        
        color_frame = self.create_holographic_panel()
        color_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add color options
        colors = [
            "#FF0000", "#00FF00", "#0000FF",
            "#FFFF00", "#FF00FF", "#00FFFF",
            "#FF8000", "#80FF00", "#0080FF",
            "#8000FF", "#FF0080", "#00FF80"
        ]
        
        for color in colors:
            button = ctk.CTkButton(
                color_frame,
                text="",
                width=40,
                height=40,
                fg_color=color,
                command=lambda c=color: self.set_color(model, c, dialog)
            )
            button.pack(pady=5)
    
    def set_color(self, model: str, color: str, dialog: ctk.CTkToplevel):
        """Set the color for a model and close the picker"""
        self.model_colors[model] = color
        self.update_graph()
        dialog.destroy()
    
    def pick_overlay_color(self, overlay_id: str):
        """Open color picker for overlay"""
        # Similar to pick_color but for overlays
        pass
    
    def update_data_display(self):
        """Update the data display with latest predictions and market data"""
        if hasattr(self.app.state, "master_prediction") and hasattr(self.app.state, "individual_predictions"):
            # Update static predictions
            for model_name, predictions in self.app.state["individual_predictions"].items():
                if model_name in self.model_switches:
                    latest_pred = predictions["Close"].iloc[-1]
                    change = (latest_pred - predictions["Close"].iloc[0]) / predictions["Close"].iloc[0] * 100
                    
                    text = f"Latest: {latest_pred:.2f}\nChange: {change:+.2f}%"
                    self.model_switches[model_name].configure(text=f"{model_name}\n{text}")
            
            # Update live predictions if enabled
            if self.app.state["live_predictions"]:
                # Similar updates for live predictions
                pass
    
    def on_show(self):
        """Called when the page is shown"""
        self.update_graph()
        self.update_data_display()
