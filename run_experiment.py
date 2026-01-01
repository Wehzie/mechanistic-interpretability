#!/usr/bin/env python3
"""
Main entry point for running the steganography experiment.

Usage:
    python run_experiment.py              # Run all phases
    python run_experiment.py --phase 1   # Run specific phase
    python run_experiment.py --no-resume # Start fresh
"""

from src.experiment import main

if __name__ == "__main__":
    main()

