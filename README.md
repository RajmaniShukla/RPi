# 🍓 Raspberry Pi Math Quiz

An educational IoT project that uses Raspberry Pi GPIO pins to provide visual feedback for a simple math quiz. Green LED lights up for correct answers, red LED for wrong answers.

## 🎯 Purpose

This project demonstrates:
- **GPIO Control**: Basic input/output operations on Raspberry Pi
- **LED Control**: Switching LEDs on/off programmatically
- **Interactive Programs**: Getting user input and providing feedback
- **Educational IoT**: Making learning fun with physical computing

Perfect for beginners learning Raspberry Pi programming!

## 🔧 Hardware Requirements

| Component | Quantity | Notes |
|-----------|----------|-------|
| Raspberry Pi | 1 | Any model with GPIO pins |
| Green LED | 1 | 5mm, ~20mA |
| Red LED | 1 | 5mm, ~20mA |
| 220Ω Resistor | 2 | Current limiting |
| Breadboard | 1 | Half-size or larger |
| Jumper Wires | 5+ | Male-to-female |

## 📌 Wiring Diagram

```
Raspberry Pi (BOARD Pin Numbering)
┌─────────────────────────────────────┐
│  [1] 3.3V    [2] 5V ─────┐          │
│  [3] GPIO2   [4] 5V      │          │
│  [5] GPIO3   [6] GND ────┼──┐       │
│  ...         ...         │  │       │
│  [33] GPIO13 ────────┐   │  │       │  ← GREEN LED
│  ...         ...     │   │  │       │
│  [35] GPIO19 ────┐   │   │  │       │  ← RED LED
│  ...             │   │   │  │       │
└──────────────────│───│───│──│───────┘
                   │   │   │  │
                   ▼   ▼   │  │
              ┌────┐ ┌────┐│  │
              │ R  │ │ R  ││  │  R = 220Ω Resistor
              │220Ω│ │220Ω││  │
              └──┬─┘ └──┬─┘│  │
                 │      │  │  │
              ┌──▼──┐┌──▼──┐│  │
              │ RED ││GREEN││  │  LEDs (longer leg = anode = +)
              │ LED ││ LED ││  │
              └──┬──┘└──┬──┘│  │
                 │      │  │  │
                 └──────┴──┴──┘
                     GND (Common Ground)
```

### Pin Connections

| Pi Pin (BOARD) | GPIO | Connection |
|----------------|------|------------|
| Pin 2 | 5V | Power (if using separate power for LEDs) |
| Pin 6 | GND | Common ground |
| Pin 33 | GPIO13 | Green LED (through 220Ω resistor) |
| Pin 35 | GPIO19 | Red LED (through 220Ω resistor) |

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/RajmaniShukla/RPi.git
cd RPi
```

### 2. Ensure GPIO access

On Raspberry Pi OS, GPIO access is typically available. If you encounter permission issues:

```bash
sudo usermod -a -G gpio $USER
# Log out and back in
```

### 3. Run the quiz

```bash
python3 raspberry_pi_math_quiz.py
```

## 💻 Usage

```
$ python3 raspberry_pi_math_quiz.py

==================================================
🧮 RASPBERRY PI MATH QUIZ
==================================================
Answer correctly to see the GREEN light!
Wrong answers get the RED light.

Enter first number: 5
Enter second number: 3
What is 5 + 3? 8
✅ Correct! 5 + 3 = 8
🟢 Green LED ON

Try another? (y/n): y

Enter first number: 10
Enter second number: 7
What is 10 + 7? 15
❌ Wrong! 10 + 7 = 17 (you said 15)
🔴 Red LED ON

Try another? (y/n): n
```

## 📁 Project Structure

```
RPi/
├── README.md                   # This file
├── raspberry_pi_math_quiz.py   # Main program (improved version)
├── Respberry_pi.py             # Original legacy code
├── Respberry_pi.txt            # Original pin reference
├── res.py                      # Backup of original code
└── .gitignore                  # Git ignore file
```

## 🔍 How It Works

1. **GPIO Setup**: Configures pins 33 (green) and 35 (red) as outputs
2. **User Input**: Asks for two numbers and the user's answer
3. **Validation**: Compares user's answer to the correct sum
4. **Feedback**: 
   - ✅ Correct → Green LED flashes for 5 seconds
   - ❌ Wrong → Red LED flashes for 5 seconds
5. **Loop**: Asks if user wants to continue

### Active-Low Configuration

The LEDs use **active-low** logic:
- `GPIO.HIGH` = LED **OFF** (no current flow)
- `GPIO.LOW` = LED **ON** (current flows to ground)

This is a common configuration that protects the GPIO pins.

## 🧪 Testing Without Hardware

The improved script includes a **simulation mode** that works on any computer:

```bash
# On a non-Pi system, you'll see simulated output:
$ python3 raspberry_pi_math_quiz.py
Warning: RPi.GPIO not found. Running in simulation mode.
[SIM] GPIO mode set to BOARD
[SIM] Pin 33 configured as OUT
[SIM] Pin 35 configured as OUT
...
```

## 🛠️ Customization

### Change LED Duration

Edit `LED_ON_DURATION` in `raspberry_pi_math_quiz.py`:

```python
LED_ON_DURATION = 5  # Change to desired seconds
```

### Different GPIO Pins

Modify the pin constants:

```python
PIN_GREEN_LED = 33  # Change to your green LED pin
PIN_RED_LED = 35    # Change to your red LED pin
```

### Add More Operations

Extend the quiz to include subtraction, multiplication, etc.:

```python
import random

operations = [
    ('+', lambda a, b: a + b),
    ('-', lambda a, b: a - b),
    ('×', lambda a, b: a * b),
]

op_symbol, op_func = random.choice(operations)
correct_answer = op_func(num1, num2)
```

## ⚠️ Safety Notes

1. **Resistors Required**: Always use current-limiting resistors (220Ω) with LEDs
2. **Double-Check Wiring**: Incorrect wiring can damage your Pi
3. **5V vs 3.3V**: GPIO pins output 3.3V; don't connect 5V directly to GPIO inputs
4. **Current Limits**: Each GPIO pin can source ~16mA; total GPIO current ~50mA

## 📜 Original Files

The original files (`Respberry_pi.py`, `res.py`, `Respberry_pi.txt`) are preserved for reference. The main issue in the original code was:

```python
# Bug: input() returns strings, so this concatenates instead of adding
a = input("Enter First Number:")
b = input("Enter Sec number:")
d = a + b  # "5" + "3" = "53", not 8!
```

The improved version fixes this with proper integer conversion:

```python
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
correct_answer = num1 + num2  # 5 + 3 = 8 ✓
```

## 🤝 Contributing

Feel free to submit issues and PRs! Ideas for improvement:
- [ ] Add multiplication/division modes
- [ ] Score tracking
- [ ] Difficulty levels
- [ ] Sound feedback (buzzer)
- [ ] LCD display integration

## 📄 License

MIT License - Feel free to use for educational purposes!

## 👤 Author

**Rajmani Shukla**
- GitHub: [@RajmaniShukla](https://github.com/RajmaniShukla)

---

*Made with ❤️ for learning Raspberry Pi and Python*
