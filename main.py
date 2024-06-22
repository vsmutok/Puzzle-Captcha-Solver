import cv2


class PuzzleCaptchaSolver:
    def __init__(self, gap_image_path, bg_image_path, output_image_path):
        self.gap_image_path = gap_image_path
        self.bg_image_path = bg_image_path
        self.output_image_path = output_image_path

    def remove_whitespace(self, image):
        """

        This method removes whitespace from an image by cropping it to the area containing non-whitespace pixels.

        :param image: A string representing the file path to the image.
        :return: An image array representing the cropped image without whitespace.

        """
        img = cv2.imread(image)
        min_x, min_y, max_x, max_y = 255, 255, 0, 0
        rows, cols, channel = img.shape
        for x in range(1, rows):
            for y in range(1, cols):
                if len(set(img[x, y])) >= 2:
                    min_x, min_y = min(x, min_x), min(y, min_y)
                    max_x, max_y = max(x, max_x), max(y, max_y)
        whitespace_removed_img = img[min_x:max_x, min_y:max_y]
        return whitespace_removed_img

    def apply_edge_detection(self, img):
        """
        Applies edge detection on the given image.

        :param img: The input image.
        :return: The image with edges highlighted.
        """
        grayscale_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(grayscale_img, 100, 200)
        edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        return edges_rgb

    def find_position_of_slide(self, slide_pic, background_pic):
        """
        Find the position of the slide on the background picture.

        :param slide_pic: The slide picture to find.
        :type slide_pic: numpy.ndarray
        :param background_pic: The background picture to search in.
        :type background_pic: numpy.ndarray
        :return: The x-coordinate of the top-left corner of the slide in the background picture.
        :rtype: int
        """
        tpl_height, tpl_width = slide_pic.shape[:2]
        result = cv2.matchTemplate(background_pic, slide_pic, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)
        tl = max_loc
        br = (tl[0] + tpl_width, tl[1] + tpl_height)
        cv2.rectangle(background_pic, tl, br, (0, 0, 255), 2)
        cv2.imwrite(self.output_image_path, background_pic)
        return tl[0]

    def discern(self):
        """
        Performs the discernment process to find the position of the slide in the given images.

        :return: The position of the slide in the images.
        """
        gap_image = self.remove_whitespace(self.gap_image_path)
        edge_detected_gap = self.apply_edge_detection(gap_image)
        bg_image = cv2.imread(self.bg_image_path, 1)
        edge_detected_bg = self.apply_edge_detection(bg_image)
        slide_position = self.find_position_of_slide(edge_detected_gap, edge_detected_bg)
        return slide_position


if __name__ == "__main__":
    solver = PuzzleCaptchaSolver(
        gap_image_path="demo/geetest4/1_slice.png",
        bg_image_path="demo/geetest4/1_bg.png",
        output_image_path="demo/geetest4/1_result.png"
    )
    position = solver.discern()
    print(f"The position of the slide is: {position}")
