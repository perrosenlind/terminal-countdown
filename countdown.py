#!/usr/bin/env python3
# filepath: /Users/per.rosenlind/Documents/GitHub/Personal/terminal-countdown/countdown.py

import argparse
import re
import sys
import time
from rich.console import Console
from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from rich import box
import os
import pyfiglet

def parse_time(time_str):
    """Convert time string like '10m', '2h' to seconds."""
    match = re.match(r'(\d+)([hms])', time_str)
    if not match:
        raise ValueError(f"Invalid time format: {time_str}. Use formats like '10m', '2h', '30s'")
    
    value, unit = match.groups()
    value = int(value)
    
    if unit == 's':
        return value
    elif unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 3600
    else:
        raise ValueError(f"Unknown time unit: {unit}")

def format_time(seconds):
    """Format seconds into hours, minutes, seconds string."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def get_optimal_figlet_font(console_width, time_str):
    """Determine the best figlet font based on terminal width."""
    # List of fonts in descending size preference
    fonts = [
        "banner3", "banner", "big", "slant", "standard", "small"
    ]
    
    for font in fonts:
        try:
            fig = pyfiglet.Figlet(font=font)
            width = max(len(line) for line in fig.renderText(time_str).split('\n'))
            if width <= console_width * 0.9:  # Leave some margin
                return font
        except Exception:
            continue
    
    # Fallback to the smallest font
    return "small"

def get_completion_font(console_width):
    """Get an appropriate font for the completion message that definitely fits."""
    # Try progressively smaller fonts until we find one that fits
    test_text = "COMPLETED!"
    fonts = ["big", "standard", "small", "mini"]
    
    for font in fonts:
        try:
            fig = pyfiglet.Figlet(font=font)
            rendered = fig.renderText(test_text)
            lines = rendered.split('\n')
            if lines:
                max_width = max(len(line) for line in lines if line.strip())
                # Use a very conservative width estimate (70% of terminal)
                if max_width < console_width * 0.7:
                    return font
        except Exception:
            continue
    
    return "small"  # Safe fallback

# Replace the get_final_countdown_concert_art function
def get_final_countdown_concert_art(seconds_left):
    """Get rock concert ASCII art for the final countdown."""
    # Multiple frames showing headbanging musicians and crowd
    concert_art = [
        """
  \\o/ \\m/ \\o/    THE FINAL    \\o/ \\m/ \\o/
   |   |   |     COUNTDOWN      |   |   |
  / \\  |  / \\                  / \\  |  / \\
*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*
  \\o/ \\o/ \\o/ \\o/ \\o/ \\o/ \\o/ \\o/ \\o/ \\o/
   |   |   |   |   |   |   |   |   |   |
""",
        """
  \\o/ \\m/ \\o/    THE FINAL    \\o/ \\m/ \\o/
   |   |   |     COUNTDOWN      |   |   |
  / >  |  / >                  / >  |  / >
*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*
  \\o/ \\o/ \\m/ \\o/ \\o/ \\m/ \\o/ \\o/ \\m/ \\o/
   |   |   |   |   |   |   |   |   |   |
"""
    ]
    
    # For the very last seconds, make it more intense
    if seconds_left <= 3:
        concert_art = [
        """
  \\m/ \\m/ \\m/    THE FINAL    \\m/ \\m/ \\m/
   |   |   |     COUNTDOWN      |   |   |
  / \\  |  / \\     * * * *      / \\  |  / \\
*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*
  \\o/ \\m/ \\o/ \\m/ \\o/ \\m/ \\o/ \\m/ \\o/ \\m/
 /|\\  |  /|\\  |  /|\\  |  /|\\  |  /|\\  |
""",
        """
  \\m/ \\m/ \\m/    THE FINAL    \\m/ \\m/ \\m/
 _|_  |  _|_    COUNTDOWN     _|_  |  _|_
  / \\  |  / \\     * * * *      / \\  |  / \\
*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*·*
  \\m/ \\o/ \\m/ \\o/ \\m/ \\o/ \\m/ \\o/ \\m/ \\o/
   |  /|\\  |  /|\\  |  /|\\  |  /|\\  |  /|\\
"""
    ]
    
    return concert_art[seconds_left % len(concert_art)]

# Modify the existing function
def get_final_countdown_effect(seconds_left):
    """Get special visual effects for the final countdown."""
    # Colors alternate between these values - more dramatic for last seconds
    if seconds_left <= 3:
        colors = ["bright_red", "bright_white", "bright_yellow"]
    else:
        colors = ["bright_blue", "bright_yellow", "bright_red"]
    return colors[seconds_left % len(colors)]

# Add this function to create thematic text for the final countdown
def get_countdown_thematic_text(seconds_left):
    """Get thematic text for the final countdown without using copyrighted lyrics."""
    countdown_phrases = [
        "COUNTDOWN INITIATED",
        "GET READY FOR LIFTOFF",
        "FINAL MOMENTS APPROACHING",
        "PREPARE FOR THE FINALE",
        "THE MOMENT IS COMING"
    ]
    
    if seconds_left <= 5:
        # More dramatic for the final seconds
        return countdown_phrases[seconds_left % len(countdown_phrases)]
    else:
        return "THE FINAL COUNTDOWN"

def countdown(duration_seconds):
    """Run the countdown timer using Rich for formatting."""
    console = Console()
    end_time = time.time() + duration_seconds
    
    # Calculate the maximum width needed for the display
    starting_time = format_time(duration_seconds)
    font = get_optimal_figlet_font(console.width, starting_time)
    fig = pyfiglet.Figlet(font=font)
    
    # Create sample displays for both the longest possible time and the current time
    # This helps us determine the maximum width needed
    max_time = "00:00:00" if ":" in starting_time and len(starting_time) > 5 else "00:00"
    max_width_art = fig.renderText(max_time)
    max_width = max(len(line) for line in max_width_art.split('\n'))
    
    try:
        while True:
            remaining = max(0, int(end_time - time.time()))
            if remaining <= 0:
                break
                
            # Clear screen
            console.clear()
            
            time_str = format_time(remaining)
            
            # Generate large ASCII art for the time using the SAME font every time
            ascii_art = fig.renderText(time_str)
            
            # Special handling for final 10 seconds
            if remaining <= 10:
                # Create colorful text from the ASCII art with special effects
                color = get_final_countdown_effect(remaining)
                styled_text = Text(ascii_art, style=f"bold {color}")
                
                # Add rock concert above the timer - preserve formatting exactly
                concert_art = get_final_countdown_concert_art(remaining)
                concert_text = Text.from_ansi(concert_art)
                
                # Add thematic text instead of lyrics
                theme_text = get_countdown_thematic_text(remaining)
                theme_styled = Text(f"\n      {theme_text}\n", style="bold bright_white")
                
                # Make headbangers and crowd go wild with colors
                if remaining <= 5:
                    # More intense colors for final 5 seconds
                    crowd_color = "bright_" + ["red", "yellow", "green", "blue", "magenta"][remaining % 5]
                    concert_text.stylize(crowd_color)
                    theme_styled.stylize(crowd_color)
                
                # Combine everything
                styled_text = Text("\n") + concert_text + theme_styled + styled_text
                
                # Add title reference
                title = "THE FINAL COUNTDOWN"
                border_style = color
            else:
                # Regular styling
                styled_text = Text(ascii_art, style="bold cyan")
                title = "COUNTDOWN"
                border_style = "bright_blue"
            
            # Create panel with the countdown with FIXED width
            panel = Panel(
                Align.center(styled_text),
                box=box.ROUNDED,
                border_style=border_style,
                padding=(1, 2),
                title=title,
                title_align="center",
                width=max_width + 10  # Add padding to ensure text fits
            )
            
            # Center the panel in the terminal
            console.print(Align.center(panel, vertical="middle"))
            
            # Speed up updates during final countdown for more dramatic effect
            sleep_time = 0.1 if remaining > 10 else 0.05
            time.sleep(sleep_time)
            
        # Countdown finished
        console.clear()
        
        # Get fireworks animation frames
        fireworks_frames = get_fireworks_art()

        # Animate fireworks first (3 cycles)
        for cycle in range(3):
            for frame in fireworks_frames:
                console.clear()
                
                # Display fireworks frame
                fireworks_text = Text(frame, style="bright_yellow")
                console.print(Align.center(fireworks_text, vertical="middle"))
                
                # Change colors for each frame
                colors = ["bright_red", "bright_green", "bright_blue", "bright_magenta", "bright_yellow"]
                fireworks_text.stylize(colors[cycle % len(colors)])
                
                time.sleep(0.2)

        # Now show the completed message with fireworks
        try:
            # Use a conservative width - 60% of terminal width
            available_width = int(console.width * 0.6)
            
            # Try standard font first
            fig = pyfiglet.Figlet(font="standard")
            completed_ascii = fig.renderText("COMPLETED!")
            
            # Check if it fits
            lines = completed_ascii.split('\n')
            max_line_width = max(len(line) for line in lines if line.strip())
            
            # If it doesn't fit, fall back to small font
            if max_line_width > available_width:
                fig = pyfiglet.Figlet(font="small")
                completed_ascii = fig.renderText("COMPLETED!")
            
            # Create panel without explicit width so it fits content
            completed_text = Text(completed_ascii, style="bold green")
            
            # Add fireworks above and below the completion message
            fireworks_frame = fireworks_frames[0]  # Use first frame
            fireworks_text = Text(fireworks_frame + "\n", style="bright_yellow")
            
            # Combine everything
            final_display = fireworks_text + completed_text + Text("\n") + fireworks_text
            
            completed_panel = Panel(
                Align.center(final_display),
                box=box.DOUBLE,
                border_style="green",
                padding=(2, 4),
                title="Time's Up",
                title_align="center"
            )
            
            # Center in the terminal
            console.print(Align.center(completed_panel, vertical="middle"))
            
            # Continue with fireworks animation after showing completion
            for i in range(5):  # Show 5 more color changes
                time.sleep(0.3)
                color = ["bright_red", "bright_green", "bright_blue", "bright_yellow", "bright_magenta"][i % 5]
                fireworks_text.stylize(color)
                console.print(Align.center(completed_panel, vertical="middle"))

        # Fallback if anything goes wrong with figlet
        except Exception:
            # Simple text fallback that will definitely work
            completed_text = Text("COMPLETED!", style="bold green", justify="center")
            completed_text.stylize("bold green")
            
            # Make it as large as Rich allows
            completed_panel = Panel(
                Align.center(completed_text, vertical="middle"),
                box=box.DOUBLE,
                border_style="green",
                padding=(3, 6),
                title="Time's Up",
                title_align="center"
            )
            
            # Center in the terminal
            console.print(Align.center(completed_panel, vertical="middle"))
        
        # Sound the terminal bell
        console.bell()
        
    except KeyboardInterrupt:
        console.clear()
        console.print("Countdown interrupted.", style="yellow")
        sys.exit(0)

# Add this new function to generate fireworks
def get_fireworks_art():
    """Generate ASCII art fireworks for the completion screen."""
    fireworks = [
        """
      *    *       *    *      *
    *   *     *  *    *   *      *
   *      * *     .    *       *
  *  *      *     *       *   *
   *    *    *  *    *   *    *
      *   *    *   *    *   *
    *        *      *       *
       *  *     *      *     *
    """,
        """
     \\o/     \\o/      \\o/    \\o/
      |       |        |      |
     / \\     / \\      / \\    / \\
    *   *   *   *    *   *  *   *
   *     * *     *  *     **     *
  *       *       **       *       *
 *         *     *  *     *         *
*           *   *    *   *           *
    """,
        """
     .'.   .'.    .'.    .'.   .'.
    :   : :   :  :   :  :   : :   :
     '.'   '.'    '.'    '.'   '.'
    * * * * * * * * * * * * * * * *
   *   *   *   *   *   *   *   *   *
  *     *     *     *     *     *   *
 *       *       *       *       *   *
*         *         *         *       *
    """
    ]
    return fireworks

def main():
    parser = argparse.ArgumentParser(description='Terminal countdown timer with Rich formatting.')
    parser.add_argument('time', help='Time to countdown in format like "10m", "2h", "30s"')
    args = parser.parse_args()
    
    try:
        duration = parse_time(args.time)
        countdown(duration)
    except ValueError as e:
        console = Console()
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()