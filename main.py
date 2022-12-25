import tkinter
import tkinter.messagebox
import customtkinter
from PIL import ImageTk, Image, ImageEnhance

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

imgsize = (475, 600)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1500}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Image Filters",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="brighten",
                                                        command=self.sidebar_button1_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Darken",
                                                        command=self.sidebar_button2_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Increase Contrast",
                                                        command=self.sidebar_button3_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Decrease Contrast",
                                                        command=self.sidebar_button4_event)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Sharpen",
                                                        command=self.sidebar_button5_event)
        self.sidebar_button_5.grid(row=5, column=0, padx=20, pady=10)

        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, text="Blur",
                                                        command=self.sidebar_button6_event)
        self.sidebar_button_6.grid(row=6, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=8, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=11, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=12, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Path")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="Import", command=self.main_button_event,
                                                     fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=6, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Create image frame
        self.image_frame = customtkinter.CTkFrame(self, width=1, corner_radius=0)
        self.image_frame.grid(row=0, column=1, rowspan=3, columnspan=1, sticky="nsew")
        self.image_frame.grid_rowconfigure(0, weight=2)

        # Creating filtered image frame
        self.filtered_image_frame = customtkinter.CTkFrame(self, width=5, corner_radius=0)
        self.filtered_image_frame.grid(row=0, column=2, rowspan=3, columnspan=1, sticky="nsew")
        self.filtered_image_frame.grid_rowconfigure(0, weight=2)

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def display(self):
        self.beforelabel = customtkinter.CTkLabel(self.image_frame, image=beforeimage, text="", anchor="w", width=700,
                                                  height=700)
        self.beforelabel.grid(row=2, column=0)
        afterimage = customtkinter.CTkImage(light_image=Image.open(filteredimage),
                                            size=imgsize)
        self.afterlabel = customtkinter.CTkLabel(self.filtered_image_frame, text="", image=afterimage, anchor="w",
                                                 width=700,
                                                 height=700)
        self.afterlabel.grid(row=2, column=0)
    def sidebar_button1_event(self):
        print("brighten button")
        image = Image.open(
            filename
        )
        enhancer = ImageEnhance.Brightness(image)
        factor = 1.5  # brightens the image
        global filteredimage
        afterimage = enhancer.enhance(factor)
        filteredimage = 'filtered.jpeg'
        afterimage = afterimage.resize(imgsize)
        afterimage.save(filteredimage)
        self.display()

    def sidebar_button2_event(self):
        print("Darken button")
        image = Image.open(
            filename
        )
        enhancer = ImageEnhance.Brightness(image)
        factor = 0.5  # Darkens the image
        afterimage = enhancer.enhance(factor)
        global filteredimage
        filteredimage = 'filtered.jpeg'
        afterimage = afterimage.resize(imgsize)
        afterimage.save(filteredimage)
        self.display()

    def sidebar_button3_event(self):
        print("increase Contrast button")
        image = Image.open(
            filename
        )
        enhancer = ImageEnhance.Contrast(image)
        factor = 1.5  # Increase the Contrast of the image
        afterimage = enhancer.enhance(factor)
        global filteredimage
        filteredimage = 'filtered.jpeg'
        afterimage = afterimage.resize(imgsize)
        afterimage.save(filteredimage)
        self.display()

    def sidebar_button4_event(self):
        print("Decrease Contrast button")
        image = Image.open(
            filename
        )
        enhancer = ImageEnhance.Contrast(image)
        factor = 0.5  # Decrease the Contrast of the image
        afterimage = enhancer.enhance(factor)
        global filteredimage
        filteredimage = 'filtered.jpeg'
        afterimage = afterimage.resize(imgsize)
        afterimage.save(filteredimage)
        self.display()

    def sidebar_button5_event(self):
        print("Sharpen button")
        image = Image.open(
            filename
        )
        enhancer = ImageEnhance.Sharpness(image)
        factor = 1.5  # Sharpen the image
        afterimage = enhancer.enhance(factor)
        global filteredimage
        filteredimage = 'filtered.jpeg'
        afterimage = afterimage.resize(imgsize)
        afterimage.save(filteredimage)
        self.display()

    def sidebar_button6_event(self):
        print("Blur button")
        image = Image.open(
            filename
        )
        enhancer = ImageEnhance.Sharpness(image)
        factor = 0.07  # Blurs the image
        afterimage = enhancer.enhance(factor)
        global filteredimage
        filteredimage = 'filtered.jpeg'
        afterimage = afterimage.resize(imgsize)
        afterimage.save(filteredimage)
        self.display()

    def main_button_event(self):
        global filename
        filename = self.entry.get()
        print(f"main_button click\n {filename}")
        global beforeimage
        beforeimage = customtkinter.CTkImage(light_image=Image.open(filename),
                                             size=imgsize)
        self.beforelabel = customtkinter.CTkLabel(self.image_frame, image=beforeimage, text="", anchor="w", width=700,
                                                  height=700)
        self.beforelabel.grid(row=1, column=0)
        self.textlabelbefore = customtkinter.CTkLabel(self.image_frame, text="Before", anchor="w")
        self.textlabelbefore.grid(row=0, column=0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
