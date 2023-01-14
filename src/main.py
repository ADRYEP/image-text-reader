import pytesseract
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar


def extract_text(image_path):
    # Using image_to_string() from pytesseract to extract text from image
    text = pytesseract.image_to_string(image_path)
    return text


def detect_faces(image_path):
    # Load the trained model
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_eye_tree_eyeglasses.xml")

    # Load the image
    img = cv2.imread(image_path)

    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces using the trained model
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5)

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    # Save the image with rectangles around the faces
    cv2.imwrite("./images/detected_face.jpg", img)
    return img


def save_images(image_path):
    # Load the image
    img = cv2.imread(image_path)
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Threshold the image
    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(
        dist_transform, 0.7*dist_transform.max(), 255, 0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0
    markers = cv2.watershed(img, markers)
    img[markers == -1] = [255, 0, 0]
    # Iterate through the markers and save the images
    for marker in np.unique(markers):
        if marker == 0:
            continue
        mask = np.zeros(gray.shape, dtype="uint8")
        mask[markers == marker] = 255
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        c = max(cnts, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        roi = img[y:y+h, x:x+w]
        cv2.imwrite(f"image_{marker}.jpg", roi)
    return img


def read_code(image_path):
    # Cargar la imagen
    image = cv2.imread(image_path)

    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detectar códigos
    codes = pyzbar.decode(gray)

    # Recortar y guardar cada código detectado
    for code in codes:
        print(code.data)
        x, y, w, h = code.rect
        roi = gray[y:y + h, x:x + w]
        cv2.imwrite("image_decoded.jpg", roi)
        return roi


def main():
    while True:  # Menu options
        print("1. Convertir una imagen a texto")
        print("2. Detectar caras")
        print("3. Encuadrar imágenes")
        print("4. Leer QR")
        print("5. Exit")

        choice = input("Ingresa una opción: ")

        if choice == '1':
            image_path = input(  # Function to extract text
                "Introduce una dirección de imagen (debe estar dentro de la carpeta del proyecto): ")
            print(extract_text(image_path))
        elif choice == '2':
            image_path = input(  # Function to detect faces and eyes from image
                "Introduce una dirección de imagen (debe estar dentro de la carpeta del proyecto): ")
            detect_faces(image_path)
        elif choice == '3':
            image_path = input(  # Function to separate image into several parts
                "Introduce una dirección de imagen (debe estar dentro de la carpeta del proyecto): ")
            save_images(image_path)
        elif choice == '4':
            image_path = input(  # Function to separate image into several parts
                "Introduce una dirección de imagen (debe estar dentro de la carpeta del proyecto): ")
            read_code(image_path)
        elif choice == '5':
            break
        else:
            print("Opción inválida")


if __name__ == '__main__':
    main()
