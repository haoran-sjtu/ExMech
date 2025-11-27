import numpy as np
import cv2
import matplotlib.pyplot as plt

def display_with_subplot(image, title, subplot_pos):
    plt.subplot(subplot_pos)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    return

def target_estimation(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    binary_image[:, 0:85] = 0
    binary_image[:, 759:849] = 0
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image, connectivity=8)
    colored_labels = np.zeros_like(image)
    colors = [[142, 207, 201], [255, 190, 122], [250, 127, 111]]
    kernel = np.ones((5, 5), np.uint8)
    colored_labels = cv2.dilate(colored_labels, kernel, iterations=1)
    colored_labels = cv2.erode(colored_labels, kernel, iterations=1)
    filtered_labels = np.zeros_like(colored_labels)
    i = 0
    targets = []
    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        contours, _ = cv2.findContours((labels == label).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        epsilon = 0.045 * cv2.arcLength(contours[0], True)
        approx = cv2.approxPolyDP(contours[0], epsilon, True)
        if len(approx) == 4 and 1100 < area < 3200:
            filtered_labels[labels == label] = colors[i]
            rect = cv2.minAreaRect(contours[0])
            center, size, angle = rect
            center = tuple(map(int, center))
            size = tuple(map(int, size))
            length = max(size)  # Longest side
            # Standardize angle, arrow along the long axis, arrow_angle: angle between arrow and positive x-axis, clockwise positive, range [-90, 90]
            if length == size[0]:
                endpoint = (int(center[0] + length * np.cos(np.radians(angle))),
                            int(center[1] + length * np.sin(np.radians(angle))))
                arrow_angle = -angle
            else:
                endpoint = (int(center[0] + length * np.sin(np.radians(angle))),
                            int(center[1] - length * np.cos(np.radians(angle))))
                arrow_angle = 90 - angle
            centroid = tuple(map(int, centroids[label]))
            cv2.drawContours(filtered_labels, [cv2.boxPoints(rect).astype(int)], 0, (255, 255, 255), 2)
            cv2.arrowedLine(filtered_labels, centroid, endpoint, (255, 255, 255), 2)
            cv2.circle(filtered_labels, centroid, 5, (255, 255, 255), -1)
            cv2.putText(filtered_labels, str(i), (centroid[0]+30, centroid[1]+30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
            print(f"The filtered area {i}: Connected Component {label} - Area: {stats[label, cv2.CC_STAT_AREA]}, Position: {stats[label, cv2.CC_STAT_LEFT]}, {stats[label, cv2.CC_STAT_TOP]}, Size: {stats[label, cv2.CC_STAT_WIDTH]}, {stats[label, cv2.CC_STAT_HEIGHT]}")
            print(f"The center of the area {i}: {centroid}, Direction Angle: {arrow_angle}")
            i += 1
            target = {
                "centroid": centroid,
                "endpoint": endpoint,
                "target_image": filtered_labels,
                "rect": rect,
                "binary_image": binary_image,
                "colored_image": colored_labels,
                "arrow_angle": arrow_angle
            }
            targets.append(target)
    return targets


