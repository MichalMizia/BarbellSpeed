import cv2 as cv


class Drawer:
    def __init__(self, weight, show_weight=False) -> None:
        # constants for user to edit
        self.weight = weight
        self.show_weight = show_weight
        # real values
        self.prev_velocity = None
        self.max_velocity = None
        self.max_percentage: int = 100
        self.percentage = 100
        self.increment = 3
        self.concentric_velocities = []

    def draw_velocity(
        self,
        image: cv.typing.MatLike,
        velocity: float,
        corner: int = 1,
        radius: int = 128,
        thickness: int = 8,
        offset_percent: float = 0.1,
    ):
        if self.prev_velocity != velocity:
            self.prev_velocity = velocity
            self.concentric_velocities.append(velocity)
            self.percentage = 0
            if self.max_velocity is None or velocity >= self.max_velocity:
                self.max_percentage = 100
                self.max_velocity = velocity
            else:
                self.max_percentage = int(100 * velocity / self.max_velocity)

        if self.percentage < self.max_percentage:
            self.percentage += self.increment

        # Define the radius and thickness of the circle
        offset_x, offset_y = (
            int(image.shape[1] * offset_percent),
            int(image.shape[0] * offset_percent),
        )
        # Define the color of the circle (in BGR format)
        green = (0, 226, 35)  # Green

        # Define the position of the circle based on the chosen corner
        if corner == 1:  # Top-left corner
            position = (radius + thickness + offset_x, radius + thickness + offset_y)
        elif corner == 2:  # Top-right corner
            position = (
                image.shape[1] - radius - thickness - offset_x,
                radius + thickness + offset_y,
            )
        elif corner == 3:  # Bottom-left corner
            position = (
                radius + thickness + offset_x,
                image.shape[0] - radius - thickness - offset_y,
            )
        else:  # Bottom-right corner
            position = (
                image.shape[1] - radius - thickness - offset_x,
                image.shape[0] - radius - thickness - offset_y,
            )

        # Draw the circle
        # circle_overlay = image.copy()
        axes = (radius, radius)
        startAngle = -90
        endAngle = (360 * self.percentage // 100) - 90
        cv.circle(image, position, radius, (0, 0, 0), -1, lineType=16)
        cv.ellipse(image, position, axes, 0, startAngle, endAngle, green, thickness, 16)
        # alpha = 0.85
        # image = cv.addWeighted(circle_overlay, alpha, image, 1 - alpha, 0)

        # Define the font, scale, and thickness of the text
        font, font_scale, font_thickness = cv.FONT_HERSHEY_DUPLEX, 1.2, 3
        text = "{:.2f}".format(velocity) + "m/s"
        font_color = (255, 255, 255)  # White

        textsize = cv.getTextSize(text, font, font_scale, font_thickness)[0]

        # this checks for almost equality of floats
        if self.max_velocity is None or velocity == self.max_velocity:
            # Draw the number inside the circle
            cv.putText(
                image,
                text,
                (position[0] - textsize[0] // 2, position[1] + textsize[1] // 2),
                font,
                font_scale,
                font_color,
                font_thickness,
                16,
            )
        else:
            # also draw the velocity loss
            cv.putText(
                image,
                text,
                (position[0] - textsize[0] // 2, position[1]),
                font,
                font_scale,
                font_color,
                font_thickness,
                16,
            )
            font, font_scale, font_thickness = cv.FONT_HERSHEY_DUPLEX, 0.8, 2
            text = f"-{"{:.1f}".format(100 - (velocity * 100 / self.max_velocity))}%"
            font_color = (150, 150, 255)  # Whiteish red

            sm_textsize = cv.getTextSize(text, font, font_scale, font_thickness)[0]
            cv.putText(
                image,
                text,
                (position[0] - sm_textsize[0] // 2, position[1] + textsize[1] + sm_textsize[1]),
                font,
                font_scale,
                font_color,
                font_thickness,
                16,
            )

        if self.show_weight:
            self.draw_set_data(image, position, radius)

        return image

    def draw_set_data(self, image: cv.typing.MatLike, position, radius):
        text = f"{self.weight}x{len(self.concentric_velocities)}"
        font, font_scale, font_thickness = cv.FONT_HERSHEY_PLAIN, 6.25, 11
        font_color = (255, 255, 255)  
        textsize = cv.getTextSize(text, font, font_scale, font_thickness)[0]
        cv.putText(
            image,
            text,
            (
                position[0] - textsize[0] // 2,
                position[1] - textsize[1] - radius + 5,
            ),
            font,
            font_scale,
            font_color,
            font_thickness,
            16,
        )
