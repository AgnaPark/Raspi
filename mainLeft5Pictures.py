from picamera2 import Picamera2, Preview
import time
from collections import Counter
import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
from licence_plate import RoLicensePlate

def calculate_reoccurrence(valid_plates):

    # Check if there are no valid plates
    if not valid_plates:
        return {"percentages": {}, "highest": None}

    # Step 2: Count occurrences of each valid plate
    plate_counter = Counter(valid_plates)

    # Step 3: Calculate the total number of valid plates
    total_plates = len(valid_plates)

    # Step 4: Calculate the percentage for each valid plate
    percentages = {plate: (count / total_plates) * 100 for plate, count in plate_counter.items()}

    # Step 5: Find the plate with the highest occurrence percentage
    # In case of a tie, choose the plate that appears first in the valid_plates list
    highest_plate = max(plate_counter, key=lambda plate: (plate_counter[plate], -valid_plates.index(plate)))

    # Step 6: Prepare the result
    results = {
        'percentages': percentages,
        'highest': highest_plate
    }

    return results

valid_plates = []

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)
picam2.capture_file("Images/CAR0.jpg")
picam2.capture_file("Images/CAR1.jpg")
picam2.capture_file("Images/CAR2.jpg")
picam2.capture_file("Images/CAR3.jpg")
picam2.capture_file("Images/CAR4.jpg")
picam2.capture_file("Images/CAR5.jpg")
picam2.capture_file("Images/CAR6.jpg")
picam2.capture_file("Images/CAR7.jpg")
picam2.capture_file("Images/CAR8.jpg")
picam2.capture_file("Images/CAR9.jpg")
picam2.stop_preview()
picam2.close()
valid_plates = []

for i in range(10):
    picture = "Images/CAR"+str(i)+".jpg"
    print(picture)
    img = cv2.imread(picture,cv2.IMREAD_COLOR)
    #img = cv2.imread('testLeftRight.jpg',cv2.IMREAD_COLOR)
    img = cv2.resize(img, (620,480) )
    
    #!!!!!
    # Split the image (left half)
    height, width, _ = img.shape
    img = img[:, :width // 2]
    #!!!!!
    # Split the image (Right half)
    #height, width, _ = img.shape
    #img = img[:, width // 2:]
    #!!!!!

    height, width, _ = img.shape

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
    edged = cv2.Canny(gray, 30, 200) #Perform Edge detection
    
    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    
    screenCnt = None
    # loop over our contours

    for c in cnts:

        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")

    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
        
        # Masking the part other than the number plate
        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
        new_image = cv2.bitwise_and(img,img,mask=mask)
        
        

        # Now crop
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]
        cv2.imshow('image full',Cropped)
            
        #!!!!!!!
        # Calculate image width and height
        height, width = Cropped.shape

        # Calculate aspect ratio
        aspect_ratio = float(width) / height

        # Classify image based on aspect ratio
        if aspect_ratio > 1.5:  # Adjust this threshold based on your specific shapes
            print("Image is rectangular")
            # Determine the dimensions of the Cropped image
            height, width = Cropped.shape

            # Calculate the starting point for the last 80% of the columns
            start_col = int(width * 0.12)
            # Calculate the end point for the last 80% of the columns
            end_col = int(width * 0.97)

            # Extract the last 80% of the columns
            Cropped = Cropped[:, start_col:end_col]
            cv2.imshow('image 80%',Cropped)
        else:
            print("Image is boxy")
            # Determine the dimensions of the Cropped image
            height, width = Cropped.shape

            # Calculate the starting point for the last 80% of the columns
            start_col = int(width * 0.2)

            # Extract the last 80% of the columns
            Cropped = Cropped[:, start_col:width]
            cv2.imshow('image 80%',Cropped)
            
        #!!!!!!!!
        
        
        #Read the number plate
        personal_config = rf"--psm 11  tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz --oem 3"
        text = pytesseract.image_to_string(Cropped, config=personal_config)
        text = text[:len(text)-1]
        print(f"Detected Number is: {text}")


        plate1 = RoLicensePlate(text)
        if(plate1.is_roLicensePlate()):
            print(f"+Valid\n")
            # Initialize the list with on
            new_plate = plate1.number_plate_toString()
            valid_plates.append(new_plate)
        else:
            print(f"-Invalid\n")

print(valid_plates)
result = calculate_reoccurrence(valid_plates)

# Print the percentages
for plate, percentage in result['percentages'].items():
    print(f"{plate}: {percentage:.2f}%")

# Print the highest occurrence plate
print(f"Highest occurrence: {result['highest']}")
#cv2.imshow('image',img)
#cv2.imshow('Cropped',Cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()


'''
import cv2
import imutils
import numpy as np
import pytesseract
from licence_plate import RoLicensePlate

# Load the image
img = cv2.imread('testLeftRight.jpg', cv2.IMREAD_COLOR)
img = cv2.resize(img, (620, 480))

# Split the image into left and right halves
height, width, _ = img.shape
left_half = img[:, :width // 2]

# Convert left half to grayscale
gray = cv2.cvtColor(left_half, cv2.COLOR_BGR2GRAY)

# Blur to reduce noise
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Perform edge detection
edged = cv2.Canny(gray, 30, 200)

# Find contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

screenCnt = None

# Loop over contours
for c in cnts:
    # Approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)

    # If the contour has four points, assume it's the license plate
    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print("No contour detected")
else:
    detected = 1
    cv2.drawContours(left_half, [screenCnt], -1, (0, 255, 0), 3)

# Mask the region of interest
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
new_image = cv2.bitwise_and(left_half, left_half, mask=mask)

# Find the coordinates of non-zero elements in the mask
(x, y) = np.nonzero(mask)

# Find the bounding box of the contour
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))

# Crop the number plate region
cropped_plate = gray[topx:bottomx + 1, topy:bottomy + 1]

# Read the number plate
text = pytesseract.image_to_string(cropped_plate, config='--psm 11')
print("Detected Number is:", text)

# Validate the number plate
plate1 = RoLicensePlate(text)
print(f"Valid? {plate1.is_roLicensePlate()}\n")

# Display the results
cv2.imshow('Left Half with Contour and License Plate', left_half)
cv2.imshow('Cropped Plate', cropped_plate)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''



