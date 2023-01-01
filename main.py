import pywt
import cv2
import numpy as np
import customtkinter
from PIL import Image, ImageEnhance

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("dark-blue")

imgsize = (475, 600)

# coffcient to apply fusion filter 
def fuseCoeff(cooef1, cooef2, method):
    if (method == 'mean'):
        cooef = (cooef1 + cooef2) / 2
    elif (method == 'min'):
        cooef = np.minimum(cooef1, cooef2)
    elif (method == 'max'):
        cooef = np.maximum(cooef1, cooef2)
    else:
        cooef = []
    return cooef


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Image Filter.py")
        self.geometry(f"{1500}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)
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

        self.sidebar_button_7 = customtkinter.CTkButton(self.sidebar_frame, text="Noise Reduction",
                                                        command=self.sidebar_button7_event)
        self.sidebar_button_7.grid(row=7, column=0, padx=20, pady=10)

        self.sidebar_button_8 = customtkinter.CTkButton(self.sidebar_frame, text="Colour to grayscale",
                                                        command=self.sidebar_button8_event)
        self.sidebar_button_8.grid(row=8, column=0, padx=20, pady=10)

        # self.sidebar_button_9 = customtkinter.CTkButton(self.sidebar_frame, text="Grayscale to colour",
        #                                                 command=self.sidebar_button9_event)
        # self.sidebar_button_9.grid(row=9, column=0, padx=20, pady=10)

        self.sidebar_button_9 = customtkinter.CTkButton(self.sidebar_frame, text="Fusion",
                                                        command=self.sidebar_button9_event)
        self.sidebar_button_9.grid(row=9, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(
            row=11, column=0, padx=20, pady=(10, 0))

        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                                       values=[
                                                                           "Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=12, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=13, column=0, padx=20, pady=(10, 0))

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                               values=[
                                                                   "80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=14, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry1 = customtkinter.CTkEntry(
            self, placeholder_text="Path for the first image")
        self.entry1.grid(row=3, column=1, columnspan=2, padx=(
            20, 0), pady=(20, 20), sticky="nsew")

        self.entry2 = customtkinter.CTkEntry(
            self, placeholder_text="Path for the second image")
        self.entry2.grid(row=4, column=1, columnspan=2, padx=(
            20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="Import the first image", command=self.main_button1_event,
                                                     fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=6, padx=(
            20, 20), pady=(20, 20), sticky="nsew")

        self.main_button_2 = customtkinter.CTkButton(master=self, text="Import the second image", command=self.main_button2_event,
                                                     fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"))
        self.main_button_2.grid(row=4, column=6, padx=(
            20, 20), pady=(20, 20), sticky="nsew")

        # Create image frame
        self.image_frame = customtkinter.CTkFrame(
            self, width=1, corner_radius=0)
        self.image_frame.grid(row=0, column=1, rowspan=3,
                              columnspan=1, sticky="nsew")
        self.image_frame.grid_rowconfigure(0, weight=2)

        # Creating filtered image frame
        self.filtered_image_frame = customtkinter.CTkFrame(
            self, width=5, corner_radius=0)
        self.filtered_image_frame.grid(
            row=0, column=2, rowspan=3, columnspan=1, sticky="nsew")
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
        factor = 5  # Sharpen the image
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
        factor = 0.01  # Blurs the image
        afterimage = enhancer.enhance(factor)
        global filteredimage
        filteredimage = 'filtered.jpeg'
        afterimage = afterimage.resize(imgsize)
        afterimage.save(filteredimage)
        self.display()

    def sidebar_button7_event(self):
        print("Noise button")
        img = cv2.imread(filename)
        # Applying mean filter to remove noise 
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        dst = cv2.resize(dst, ((475, 600)))
        global filteredimage
        filteredimage = 'filtered.jpeg'
        cv2.imwrite(filteredimage, dst)
        self.display()

    def sidebar_button8_event(self):
        print("COLOR to GrayScale button")
        # Reading image in Gray Scale
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, ((475, 600)))
        global filteredimage
        filteredimage = 'filtered.jpeg'
        cv2.imwrite(filteredimage, img)
        self.display()

    def sidebar_button9_event(self):
        # Discrete Wavelength transform
        
        # Params
        FUSION_METHOD = 'mean'  # Can be 'min' || 'max || anything you choose according theory

        # Read the two image
        I1 = cv2.imread(filename, cv2.IMREAD_COLOR)
        I2 = cv2.imread(filteredimage, cv2.IMREAD_COLOR)

        # We need to have both images the same size
        I1 = cv2.resize(I1, (475, 600))
        I2 = cv2.resize(I2, (475, 600))

        # Fusion algo

        # First: Do wavelet transform on each image
        wavelet = 'db1'

        cooef1 = pywt.wavedec2(I1[:, :], wavelet)
        cooef2 = pywt.wavedec2(I2[:, :], wavelet)

        # Second: for each level in both image do the fusion according to the desire option
        fusedCooef = []
        for i in range(len(cooef1)-1):

            # The first values in each decomposition is the apprximation values of the top level
            if (i == 0):

                fusedCooef.append(fuseCoeff(cooef1[0], cooef2[0], FUSION_METHOD))

            else:

            # For the rest of the levels we have tupels with 3 coeeficents
                c1 = fuseCoeff(cooef1[i][0], cooef2[i][0], FUSION_METHOD)
                c2 = fuseCoeff(cooef1[i][1], cooef2[i][1], FUSION_METHOD)
                c3 = fuseCoeff(cooef1[i][2], cooef2[i][2], FUSION_METHOD)

                fusedCooef.append((c1, c2, c3))

        # Third: After we fused the cooefficent we need to transfor back to get the image
        fusedImage = pywt.waverec2(fusedCooef, wavelet)

        # Forth: normmalize values to be in uint8
        fusedImage = np.multiply(np.divide(
            fusedImage - np.min(fusedImage), (np.max(fusedImage) - np.min(fusedImage))), 255)
        fusedImage = fusedImage.astype(np.uint8)

        # Fith: Show imag
        # fusedImage = cv2.resize(fusedImage, imgsize)
        
        # Saving Image
        Image.fromarray(fusedImage).save('res.png')

        # Clearing the images from screen

        self.afterlabel = customtkinter.CTkLabel(self.filtered_image_frame, text="", anchor="w",
                                                 width=700,
                                                 height=700)
        self.afterlabel.grid(row=2, column=0)

        self.beforelabel = customtkinter.CTkLabel(self.image_frame, text="", anchor="w", width=700,
                                                  height=700)
        self.beforelabel.grid(row=1, column=0)

        # Showing image on screen

        beforeimage = customtkinter.CTkImage(light_image=Image.open('res.png'),
                                             size=imgsize)
        self.beforelabel = customtkinter.CTkLabel(self.image_frame, image=beforeimage, text="", anchor="w", width=700,
                                                  height=700)
        self.beforelabel.grid(row=1, column=0)

    def main_button1_event(self):
        global filename
        filename = self.entry1.get()
        print(f"main_button1 click\n {filename}")
        global beforeimage
        # Reading image
        beforeimage = customtkinter.CTkImage(light_image=Image.open(filename),
                                             size=imgsize)
        # Showing Image on screen
        self.beforelabel = customtkinter.CTkLabel(self.image_frame, image=beforeimage, text="", anchor="w", width=700,
                                                  height=700)
        self.beforelabel.grid(row=1, column=0)

    def main_button2_event(self):
        print(f"main_button2 click\n {filename}")
        global filteredimage
        # getting filename from the entry
        filteredimage = self.entry2.get()
        self.display()


if __name__ == "__main__":
    app = App()
    app.mainloop()
