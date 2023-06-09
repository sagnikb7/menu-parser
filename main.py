import cv2
from cv2 import dnn_superres
import os
import re
import pytesseract
import util

MAX_BOUNDING_BOXES = 5
menu_file = "ss2.png"
output_folder = 'temp'
bounding_box_color = (142, 26, 250)

sr = dnn_superres.DnnSuperResImpl_create()
model_path = "FSRCNN_x2.pb"
sr.readModel(model_path)
sr.setModel("fsrcnn", 2)

image_path = os.path.join("test_menu", menu_file)

bounding_boxes = []
current_box = []
current_image = None
drawing = False

# temp directory housekeeping
def housekeeping(output_folder):
    if os.path.exists(output_folder):
        files = os.listdir(output_folder)
        for file in files:
            if file.endswith('.jpg'):
                file_path = os.path.join(output_folder, file)
                os.remove(file_path)
    else:
        os.makedirs(output_folder)


# Mouse callback function
def draw_bounding_box(event, x, y, flags, param):
    global current_image, current_box, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        current_box = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        current_box.append((x, y))
        bounding_boxes.append(tuple(current_box))
        current_box = []

def detectSub(input_string):
    pattern = r"(\S+)\s*/\s*(\S+)"
    match = re.match(pattern, input_string)
    if match:
        # Extract the two parts using group(1) and group(2)
        return match.group(1),match.group(2)
    return False,False




def main():
    image = cv2.imread(image_path)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', draw_bounding_box)

    while True:
        # Display the image and bounding boxes
        display_image = image.copy()
        for box in bounding_boxes:
            cv2.rectangle(display_image, box[0], box[1], bounding_box_color, 2)					 
        # Check if the current box is being drawn
        if drawing and current_box:
            x, y = current_box[0]  # <-- Added this line
            cv2.rectangle(display_image, current_box[0], (x, y), bounding_box_color, 2)

        # Show the image
        cv2.imshow('Image', display_image)

        # Wait for key events
        key = cv2.waitKey(1) & 0xFF
        # Check for key presses
        if key == ord('r'):
            # Remove the last bounding box
            if bounding_boxes:
                bounding_boxes.pop()
        elif key == ord('s') or len(bounding_boxes) >= MAX_BOUNDING_BOXES:
            # Save the segmented images and apply super resolution
            for i, box in enumerate(bounding_boxes):
                x1, y1 = box[0]
                x2, y2 = box[1]
                sub_image_path = os.path.join(output_folder, f'segmented_{i+1}.jpg')
                sub_image = image[y1:y2, x1:x2]
                # Apply super resolution to the sub_image

                # Save the segmented image
                # 
                upscaled_img = sr.upsample(sub_image)
                grey_image = cv2.cvtColor(upscaled_img, cv2.COLOR_BGR2GRAY)
                sharpened_image = cv2.filter2D(grey_image, -1, (1, 1), borderType=cv2.BORDER_REPLICATE)

                cv2.imwrite(sub_image_path, sharpened_image)

            break

    # Close all windows
    cv2.destroyAllWindows()

def parse():
    segmented_files = os.listdir(output_folder)
    segmented_files.sort()

    for file in segmented_files:
        if file.endswith('.jpg'):
            print("Extracting ->")
            file_path = os.path.join(output_folder,file)
            extracted_text = pytesseract.image_to_string(file_path,lang='eng')
            # print(pytesseract.image_to_boxes(file_path))
            sentences = extracted_text.splitlines()
            r = util.cleanup(sentences)
            


housekeeping(output_folder)
main()
parse()