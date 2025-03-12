import os
import sys
from src.gui.app import CryptoCrystalBallApp

def setup_environment():
    """Setup required directories and environment"""
    # Create necessary directories
    directories = ['models', 'plots', 'logs', 'data']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

    # Add src directory to Python path
    src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
    if src_dir not in sys.path:
        sys.path.append(src_dir)

def main():
    """Main entry point of the application"""
    # Setup environment
    setup_environment()
    
    # Create and run the application
    app = CryptoCrystalBallApp()
    app.run()

if __name__ == "__main__":
    main()
