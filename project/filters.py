import cv2
import numpy as np


def pencil_sketch(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    inverted = 255 - gray

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)

    # Invert the blurred image
    inverted_blurred = 255 - blurred

    # Create the pencil sketch image
    pencil_sketch = cv2.divide(gray, inverted_blurred, scale=256.0)

    # Enhance edges (optional)
    edges = cv2.Canny(gray, 30, 100)
    edges = cv2.dilate(edges, np.ones((1, 1), np.uint8), iterations=1)

    # Blend edges with sketch
    result = cv2.addWeighted(pencil_sketch, 0.8, edges, 0.2, 0)

    return result


def comic_effect(image_path, output_path=None):
    """
    Transform a regular image into a comic-style image.

    Parameters:
    image_path (str): Path to the input image
    output_path (str, optional): Path where the output image will be saved.
                                If None, the function just returns the image.

    Returns:
    numpy.ndarray: The comic-style transformed image
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image from {image_path}")

    # Step 1: Reduce noise and detail with bilateral filter
    # This preserves edges while smoothing flat regions
    smooth = cv2.bilateralFilter(img, d=9, sigmaColor=300, sigmaSpace=300)

    # Step 2: Convert to grayscale for edge detection
    gray = cv2.cvtColor(smooth, cv2.COLOR_BGR2GRAY)

    # Step 3: Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, blockSize=9, C=2
    )

    # Step 4: Convert edges to color (black lines)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Step 5: Color quantization to reduce color palette
    # Convert to float32 for k-means
    Z = smooth.reshape((-1, 3)).astype(np.float32)

    # Define criteria and apply kmeans
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 8  # Number of colors in the comic
    _, labels, centers = cv2.kmeans(
        Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back to uint8 and reshape
    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    quantized = res.reshape(smooth.shape)

    # Step 6: Combine quantized colors with edges
    # Invert edges for black outlines on white
    edges_inv = cv2.bitwise_not(edges_colored)

    # Blend edges with color-quantized image
    comic = cv2.bitwise_and(quantized, edges_inv)

    # Step 7: Optional - Enhance colors
    # Convert to HSV for better color manipulation
    hsv = cv2.cvtColor(comic, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Increase saturation
    s = cv2.add(s, 30)

    # Merge channels back
    hsv_enhanced = cv2.merge([h, s, v])

    # Convert back to BGR
    comic_enhanced = cv2.cvtColor(hsv_enhanced, cv2.COLOR_HSV2BGR)

    # Save if output path is provided
    if output_path:
        cv2.imwrite(output_path, comic_enhanced)

    return comic_enhanced
