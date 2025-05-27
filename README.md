# Terminal Countdown

A feature-rich terminal countdown timer with large digits, animations, and special effects. Perfect for presentations, timing breaks, or any situation where you need a visually impressive countdown.

## Demo

![Terminal Countdown Demo](countdown.gif)

*The final 12 seconds of the countdown showing the rock concert animations, color cycling, and completion fireworks.*

## Features

- **Large, visible digits** that automatically scale to your terminal size
- **Multiple time formats**: Hours, minutes, and seconds (e.g., `2h`, `10m`, `30s`)
- **Fixed-position display** that doesn't "wander" as digits change
- **Special "Final Countdown" sequence** during the last 10 seconds featuring:
  - Animated rock concert with headbanging musicians and crowd
  - Color-cycling effects
  - Dramatic thematic text
- **Celebratory fireworks** animation when the countdown completes

## Installation

1. Ensure you have Python 3.6+ installed
2. Install the required packages:

```bash
pip install rich pyfiglet
```

3. Download the script and make it executable:

```bash
chmod +x countdown.py
```

## Usage

Run the countdown with a time specification:

```bash
./countdown.py 10m   # 10 minutes
./countdown.py 2h    # 2 hours
./countdown.py 30s   # 30 seconds
```

The script accepts the following time formats:
- `Xh` - Hours (e.g., `2h` for 2 hours)
- `Xm` - Minutes (e.g., `10m` for 10 minutes)
- `Xs` - Seconds (e.g., `30s` for 30 seconds)

## The Final Countdown

When the timer reaches the final 10 seconds, it transforms into an exciting "Final Countdown" sequence inspired by the famous song by Europe:

- The countdown digits begin cycling through vibrant colors
- A rock concert scene appears with animated musicians and crowd
- Thematic countdown phrases are displayed
- The border and title change to match the dramatic moment

## Completion Celebration

When the countdown reaches zero:
1. A colorful fireworks animation plays
2. "COMPLETED!" is displayed in large text
3. More fireworks surround the completion message
4. A terminal bell sounds to alert you that time is up

## Keyboard Controls

- **Ctrl+C**: Interrupt and exit the countdown at any time

## Requirements

- Python 3.6+
- Rich library (for terminal formatting)
- Pyfiglet library (for ASCII art text)
- A terminal with color support
- Recommended: A large terminal window for the best visual experience