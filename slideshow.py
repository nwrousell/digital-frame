import tkinter as tk
from PIL import Image, ImageTk


class Slideshow:
    def __init__(self, im_paths=[], pad_color="black"):
        """Initialize the full-screen viewer."""
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)  # Set the window to fullscreen

        # Exit full-screen on pressing Escape
        self.root.bind("<Escape>", lambda _: self.root.destroy())

        # Placeholder for the image label
        self.label = tk.Label(self.root)
        self.label.pack()

        self.im_paths = im_paths
        self.current_image_index = 0
        self.pad_color = pad_color

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

    def display_image(self, image_path):
        """Display an image in the existing full-screen viewer."""
        image = Image.open(image_path)

        # Calculate the new size while maintaining aspect ratio
        image_ratio = image.width / image.height
        screen_ratio = self.screen_width / self.screen_height

        if image_ratio > screen_ratio:
            # Image is wider than screen
            new_width = self.screen_width
            new_height = int(self.screen_width / image_ratio)
        else:
            # Image is taller than screen
            new_height = self.screen_height
            new_width = int(self.screen_height * image_ratio)

        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create a new image with a solid color background and paste the resized image
        background = Image.new(
            "RGB", (self.screen_width, self.screen_height), color=self.pad_color
        )
        x_offset = (self.screen_width - new_width) // 2
        y_offset = (self.screen_height - new_height) // 2
        background.paste(resized_image, (x_offset, y_offset))

        # Convert to a format Tkinter can use
        photo = ImageTk.PhotoImage(background)

        # Update the label with the new image
        self.label.config(image=photo)
        self.label.image = photo  # Keep a reference to prevent garbage collection

    def start(self):
        """Start the Tkinter main loop."""
        self.root.config(cursor="none")
        self.root.mainloop()

    def start_slideshow(self, interval):
        """Start a slideshow, changing the image every `interval` milliseconds."""
        self.display_image(self.im_paths[self.current_image_index])
        self.current_image_index = (self.current_image_index + 1) % len(self.im_paths)
        self.root.after(interval, self.start_slideshow, interval)
