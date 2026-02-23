#!/usr/bin/env python3
"""
Raspberry Pi Math Quiz - Educational GPIO Project

A simple math addition quiz that provides visual feedback using LEDs:
- GREEN LED (Pin 33): Lights up when answer is CORRECT
- RED LED (Pin 35): Lights up when answer is WRONG

Hardware Requirements:
- Raspberry Pi (any model with GPIO)
- 2x LEDs (green and red)
- 2x 220Ω resistors (current limiting)
- Breadboard and jumper wires

Wiring:
- Pin 2 (5V) → VCC for LEDs (through resistors)
- Pin 6 (GND) → Ground
- Pin 33 (GPIO 13) → Green LED (cathode to GND)
- Pin 35 (GPIO 19) → Red LED (cathode to GND)

Author: Rajmani Shukla
License: MIT
"""

from __future__ import annotations

import sys
import time
from contextlib import contextmanager
from typing import Generator

try:
    from RPi import GPIO
except ImportError:
    # Mock GPIO for development/testing on non-RPi systems
    print("Warning: RPi.GPIO not found. Running in simulation mode.")
    
    class MockGPIO:
        """Mock GPIO class for testing on non-Raspberry Pi systems."""
        BOARD = "BOARD"
        OUT = "OUT"
        HIGH = 1
        LOW = 0
        
        @staticmethod
        def setwarnings(flag: bool) -> None:
            pass
        
        @staticmethod
        def setmode(mode: str) -> None:
            print(f"[SIM] GPIO mode set to {mode}")
        
        @staticmethod
        def setup(pin: int, mode: str) -> None:
            print(f"[SIM] Pin {pin} configured as {mode}")
        
        @staticmethod
        def output(pin: int, state: int) -> None:
            state_str = "HIGH" if state else "LOW"
            print(f"[SIM] Pin {pin} → {state_str}")
        
        @staticmethod
        def cleanup() -> None:
            print("[SIM] GPIO cleanup complete")
    
    GPIO = MockGPIO()


# Pin Configuration (BOARD numbering)
PIN_GREEN_LED = 33  # GPIO 13 - Correct answer indicator
PIN_RED_LED = 35    # GPIO 19 - Wrong answer indicator

# Timing
LED_ON_DURATION = 5  # seconds (reduced from 20 for better UX)


@contextmanager
def gpio_context() -> Generator[None, None, None]:
    """
    Context manager for GPIO setup and cleanup.
    
    Ensures GPIO resources are properly released even if an exception occurs.
    
    Yields:
        None
    
    Example:
        >>> with gpio_context():
        ...     # GPIO operations here
        ...     pass
    """
    try:
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN_GREEN_LED, GPIO.OUT)
        GPIO.setup(PIN_RED_LED, GPIO.OUT)
        # Initialize both LEDs to OFF (HIGH = off for active-low configuration)
        GPIO.output(PIN_GREEN_LED, GPIO.HIGH)
        GPIO.output(PIN_RED_LED, GPIO.HIGH)
        yield
    finally:
        GPIO.cleanup()


def flash_led(pin: int, duration: float = LED_ON_DURATION) -> None:
    """
    Flash an LED on for a specified duration, then turn it off.
    
    Args:
        pin: GPIO pin number (BOARD numbering)
        duration: How long to keep LED on in seconds
    
    Note:
        Uses active-low configuration (LOW = ON, HIGH = OFF)
    """
    GPIO.output(pin, GPIO.LOW)   # Turn ON
    time.sleep(duration)
    GPIO.output(pin, GPIO.HIGH)  # Turn OFF


def get_integer_input(prompt: str) -> int:
    """
    Safely get an integer input from the user.
    
    Args:
        prompt: Message to display to the user
        
    Returns:
        Integer value entered by user
        
    Raises:
        KeyboardInterrupt: If user presses Ctrl+C
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Please enter a valid integer.")
        except EOFError:
            print("\n⚠️  Input stream closed.")
            sys.exit(1)


def run_quiz() -> None:
    """
    Run the math addition quiz.
    
    Asks user for two numbers and their sum, then provides
    visual feedback via LEDs based on correctness.
    """
    print("\n" + "=" * 50)
    print("🧮 RASPBERRY PI MATH QUIZ")
    print("=" * 50)
    print("Answer correctly to see the GREEN light!")
    print("Wrong answers get the RED light.\n")
    
    with gpio_context():
        try:
            while True:
                # Get numbers from user
                num1 = get_integer_input("Enter first number: ")
                num2 = get_integer_input("Enter second number: ")
                user_answer = get_integer_input(f"What is {num1} + {num2}? ")
                
                # Calculate correct answer
                correct_answer = num1 + num2
                
                # Provide feedback
                if user_answer == correct_answer:
                    print(f"✅ Correct! {num1} + {num2} = {correct_answer}")
                    print("🟢 Green LED ON")
                    flash_led(PIN_GREEN_LED)
                else:
                    print(f"❌ Wrong! {num1} + {num2} = {correct_answer} (you said {user_answer})")
                    print("🔴 Red LED ON")
                    flash_led(PIN_RED_LED)
                
                # Ask to continue
                print()
                again = input("Try another? (y/n): ").strip().lower()
                if again != 'y':
                    break
                print()
                
        except KeyboardInterrupt:
            print("\n\n👋 Quiz ended. Goodbye!")


def main() -> int:
    """
    Main entry point.
    
    Returns:
        Exit code (0 for success)
    """
    run_quiz()
    return 0


if __name__ == "__main__":
    sys.exit(main())
