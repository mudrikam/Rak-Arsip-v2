import os
import tkinter as tk

class HeaderImage:
    def __init__(self, root, BASE_DIR):
        self.root = root
        self.BASE_DIR = BASE_DIR

    def add_header_image(self):
        """Method to load and display header image."""
        header_path = os.path.join(self.BASE_DIR, "Img", "header.ppm")  # Path to image

        try:
            if os.path.isfile(header_path):
                img = tk.PhotoImage(file=header_path)  # Load the image using PhotoImage

                # Store the image reference to avoid garbage collection
                self.img = img  # Prevent garbage collection by saving it as a class attribute
                label = tk.Label(self.root, image=img)  # Create a label to display the image
                label.pack()  # Add label to window
            else:
                print("Error: Image file not found!")
                print(f"Checked path: {header_path}")
        except Exception as e:
            print(f"Error loading image: {e}")
