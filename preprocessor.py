import sys

if hasattr(sys, 'base_prefix'):
    print("A virtual environment is active.")
else:
    print("No virtual environment is active.")
