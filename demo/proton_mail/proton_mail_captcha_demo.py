import cv2

from main import PuzzleCaptchaSolver

# Load the original image
original_image = cv2.imread("proton_mail_captcha.png")

# Define the area to crop (top-left corner 115x115 pixels)
# These numbers may differ depending on the size of the input photo.
x, y = 0, 0
width, height = 115, 115

# Crop the slice we need, usually it is located at the top left
cropped_image = original_image[y : y + height, x : x + width]
cv2.imwrite("slice.png", cropped_image)  # Save the slice

# Remove the top 115 pixels from the original image.
# This is done because the slice is located at the top, so the solution definitely won't be there
cropped_from_top = original_image[height:, :]
cv2.imwrite("bg.png", cropped_from_top)  # Save the background

if __name__ == "__main__":
    # Use PuzzleCaptchaSolver to solve ProtonMail Captcha
    proton_mail_captcha_solver = PuzzleCaptchaSolver(
        gap_image_path="slice.png",
        bg_image_path="bg.png",
        output_image_path="result.png",
    )
    position = proton_mail_captcha_solver.discern()
    print(f"The position of the slide is: {position}")
