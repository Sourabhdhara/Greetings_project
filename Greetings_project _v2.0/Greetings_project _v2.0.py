import tkinter as tk
from tkinter import ttk
from datetime import datetime
import math
import random

# A class to represent a single star for the night animation
class Star:
    def __init__(self):
        self.x = random.randint(50, 750)
        self.y = random.randint(50, 200)
        self.size = random.uniform(1, 3)
        self.brightness = random.uniform(0.5, 1.0)
        self.phase_offset = random.uniform(0, 2 * math.pi)

    def update(self, animation_frame):
        # Update brightness for a twinkling effect
        self.brightness = 0.5 + 0.5 * math.sin(animation_frame * 0.1 + self.phase_offset)
        self.size = 1 + 2 * self.brightness

    def draw(self, canvas, theme):
        # Get color based on brightness
        alpha = int(255 * self.brightness)
        # Using a fixed light color for stars for better contrast
        color = "#E6E6FA" 
        canvas.create_oval(self.x - self.size, self.y - self.size,
                           self.x + self.size, self.y + self.size,
                           fill=color, outline="", tags="background")

class AnimatedTimeGreeting:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated Time Greeting")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")

        # Animation variables
        self.animation_frame = 0
        self.shooting_star = None
        self.stars = [Star() for _ in range(50)]
        self.clouds = self.init_clouds()
        
        # Create canvas for animations
        self.canvas = tk.Canvas(root, width=800, height=600, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Start the animation loop
        self.update_display()

    def init_clouds(self):
        """Initialize cloud positions for morning/afternoon animations"""
        return [{'x': random.randint(-200, 800), 'y': random.randint(50, 250), 'speed': random.uniform(0.5, 1.5), 'size': random.uniform(0.8, 1.2)} for _ in range(5)]

    def get_time_data(self):
        """Get current time and determine greeting"""
        current_time = datetime.now()
        formatted = current_time.strftime("%A\n%d %B, %Y\n%I:%M %p")
        h = int(current_time.strftime("%H"))

        if 6 <= h < 12:
            greeting = "Good Morning"
            period = "morning"
        elif 12 <= h < 17:
            greeting = "Good Afternoon"
            period = "afternoon"
        elif 17 <= h < 21:
            greeting = "Good Evening"
            period = "evening"
        else:
            greeting = "Good Night"
            period = "night"

        return greeting, formatted, period

    def get_theme_colors(self, period):
        """Get theme colors based on time period with refined palettes"""
        themes = {
            "morning": {
                "bg_start": "#87CEEB", "bg_end": "#B0E0E6",  # Sky blue to powder blue
                "text_color": "#2F4F4F", "accent": "#FF6347"  # Dark slate gray to tomato red
            },
            "afternoon": {
                "bg_start": "#F0E68C", "bg_end": "#F5DEB3",  # Khaki to wheat
                "text_color": "#8B4513", "accent": "#FF8C00"  # Saddle brown to dark orange
            },
            "evening": {
                "bg_start": "#4B0082", "bg_end": "#8A2BE2",  # Indigo to blue violet
                "text_color": "#F0E68C", "accent": "#FF1493"  # Khaki to deep pink
            },
            "night": {
                "bg_start": "#0F0F23", "bg_end": "#191970",  # Very dark blue to midnight blue
                "text_color": "#E6E6FA", "accent": "#6495ED"  # Lavender to cornflower blue
            }
        }
        return themes[period]

    def draw_background_animation(self, period, theme):
        """Draw animated background based on time period"""
        self.canvas.delete("background")

        # Smooth gradient background
        for i in range(0, 600, 5):
            color_ratio = i / 600
            start_rgb = self.root.winfo_rgb(theme["bg_start"])
            end_rgb = self.root.winfo_rgb(theme["bg_end"])
            
            r = int(start_rgb[0] / 256 + (end_rgb[0] / 256 - start_rgb[0] / 256) * color_ratio)
            g = int(start_rgb[1] / 256 + (end_rgb[1] / 256 - start_rgb[1] / 256) * color_ratio)
            b = int(start_rgb[2] / 256 + (end_rgb[2] / 256 - start_rgb[2] / 256) * color_ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_rectangle(0, i, 800, i + 5, fill=color, outline="", tags="background")
        
        # Draw period-specific animations
        if period == "morning":
            self.draw_morning_animation(theme)
        elif period == "afternoon":
            self.draw_afternoon_animation(theme)
        elif period == "evening":
            self.draw_evening_animation(theme)
        else:
            self.draw_night_animation(theme)

    def draw_morning_animation(self, theme):
        """Draw morning animation with sun rays and moving clouds"""
        # Animated sun with pulsing rays
        sun_x, sun_y = 150, 100
        sun_size = 40 + 10 * math.sin(self.animation_frame * 0.1)
        self.canvas.create_oval(sun_x - sun_size, sun_y - sun_size, sun_x + sun_size, sun_y + sun_size,
                                fill="#FFD700", outline="#FFA500", width=3, tags="background")
        
        for i in range(8):
            angle = (i * 45 + self.animation_frame * 2) * math.pi / 180
            start_x = sun_x + (sun_size + 10) * math.cos(angle)
            start_y = sun_y + (sun_size + 10) * math.sin(angle)
            end_x = sun_x + (sun_size + 30) * math.cos(angle)
            end_y = sun_y + (sun_size + 30) * math.sin(angle)
            self.canvas.create_line(start_x, start_y, end_x, end_y,
                                     fill="#FFD700", width=3, tags="background")
        
        # Moving clouds
        self.draw_clouds(theme)

    def draw_afternoon_animation(self, theme):
        """Draw afternoon animation with bright sun and moving clouds"""
        # Shimmering sun
        sun_x, sun_y = 650, 80
        for i in range(3):
            size = 35 - i * 5 + 5 * math.sin(self.animation_frame * 0.1 + i)
            self.canvas.create_oval(sun_x - size, sun_y - size, sun_x + size, sun_y + size,
                                     fill="#FFD700", outline="", tags="background")
        
        # Moving clouds
        self.draw_clouds(theme)

    def draw_evening_animation(self, theme):
        """Draw evening animation with sunset colors and floating particles"""
        # Setting sun
        sun_x = 400 + 150 * math.cos(self.animation_frame * 0.01)
        sun_y = 400 + 50 * math.sin(self.animation_frame * 0.01)
        self.canvas.create_oval(sun_x - 30, sun_y - 30, sun_x + 30, sun_y + 30,
                                fill="#FF4500", outline="#FF1493", width=2, tags="background")
        
        # Floating particles
        for i in range(10):
            x = (50 + i * 70 + self.animation_frame) % 800
            y = 200 + 50 * math.sin((x + i * 100) * 0.01)
            size = 3 + 2 * math.sin(self.animation_frame * 0.1 + i)
            self.canvas.create_oval(x - size, y - size, x + size, y + size,
                                     fill="#FF69B4", outline="", tags="background")

    def draw_night_animation(self, theme):
        """Draw night animation with stars and moon"""
        # Twinkling stars
        for star in self.stars:
            star.update(self.animation_frame)
            star.draw(self.canvas, theme)

        # Moon with a subtle glow
        moon_x, moon_y = 650, 100
        moon_glow = 5 * math.sin(self.animation_frame * 0.05)
        self.canvas.create_oval(moon_x - 25 - moon_glow, moon_y - 25 - moon_glow,
                                moon_x + 25 + moon_glow, moon_y + 25 + moon_glow,
                                fill="#E6E6FA", outline="#D3D3D3", width=2, tags="background")

        # Random shooting star
        if self.shooting_star:
            self.draw_shooting_star()
        if random.random() < 0.01 and not self.shooting_star:  # 1% chance per frame
            self.shooting_star = {'x': random.randint(100, 700), 'y': random.randint(50, 150), 'length': 0}

    def draw_shooting_star(self):
        """Draws a shooting star animation"""
        star = self.shooting_star
        if star['length'] < 100:
            x1 = star['x']
            y1 = star['y']
            x2 = star['x'] + star['length']
            y2 = star['y'] + star['length']
            self.canvas.create_line(x1, y1, x2, y2, fill="white", width=2, tags="background")
            star['x'] += 5
            star['y'] += 5
            star['length'] += 5
        else:
            self.shooting_star = None

    def draw_clouds(self, theme):
        """Helper function to draw and move clouds"""
        cloud_color = self.get_translucent_color(255, 255, 255, 0.7)  # White translucent
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']
            if cloud['x'] > 850:
                cloud['x'] = -200
                cloud['y'] = random.randint(50, 250)
                cloud['speed'] = random.uniform(0.5, 1.5)
            
            # Draw cloud shapes
            self.canvas.create_oval(cloud['x'], cloud['y'], cloud['x'] + 80 * cloud['size'], cloud['y'] + 40 * cloud['size'], fill="white", outline="", tags="background")
            self.canvas.create_oval(cloud['x'] + 30 * cloud['size'], cloud['y'] - 20 * cloud['size'], cloud['x'] + 100 * cloud['size'], cloud['y'] + 20 * cloud['size'], fill="white", outline="", tags="background")
            self.canvas.create_oval(cloud['x'] + 60 * cloud['size'], cloud['y'], cloud['x'] + 140 * cloud['size'], cloud['y'] + 40 * cloud['size'], fill="white", outline="", tags="background")


    def get_translucent_color(self, r, g, b, a):
        """Simulates a translucent color for the canvas, not natively supported"""
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        return hex_color
    
    def draw_text_elements(self, greeting, formatted_time, theme):
        """Draw animated text elements with improved styling"""
        self.canvas.delete("text")
        
        # Pulsing greeting text
        pulse = 1 + 0.1 * math.sin(self.animation_frame * 0.15)
        greeting_font_size = int(48 * pulse)
        
        # Greeting with subtle drop shadow
        self.canvas.create_text(402, 252, text=greeting,
                                font=("Helvetica", greeting_font_size, "bold"),
                                fill="#000000", tags="text", anchor="center")
        self.canvas.create_text(400, 250, text=greeting,
                                font=("Helvetica", greeting_font_size, "bold"),
                                fill=theme["accent"], tags="text", anchor="center")
        
        # Time display with gentle animation
        time_offset = 5 * math.sin(self.animation_frame * 0.1)
        lines = formatted_time.split('\n')
        
        for i, line in enumerate(lines):
            y_pos = 350 + i * 40 + time_offset
            
            # Time with subtle drop shadow
            self.canvas.create_text(401, y_pos + 1, text=line,
                                     font=("Helvetica", 24, "normal"),
                                     fill="#000000", tags="text", anchor="center")
            self.canvas.create_text(400, y_pos, text=line,
                                     font=("Helvetica", 24, "normal"),
                                     fill=theme["text_color"], tags="text", anchor="center")

    def update_display(self):
        """Main update loop"""
        greeting, formatted_time, period = self.get_time_data()
        theme = self.get_theme_colors(period)

        # Draw animations
        self.draw_background_animation(period, theme)
        self.draw_text_elements(greeting, formatted_time, theme)

        # Update animation frame
        self.animation_frame += 1

        # Schedule next update
        self.root.after(50, self.update_display)

def main():
    root = tk.Tk()
    root.resizable(False, False)

    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (800 // 2)
    y = (root.winfo_screenheight() // 2) - (600 // 2)
    root.geometry(f"800x600+{x}+{y}")

    app = AnimatedTimeGreeting(root)
    root.mainloop()

if __name__ == "__main__":
    main()
