import readimage
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
def crop_bird(image_path,birds,mean_size,folder='DATASET/outliers/'):
    # Reshape the flat list of vertices into pairs of (x, y)
    segmentation=birds.segmentation
    foldername=folder+birds.aiclass
    id=birds.id

    polygon_vertices = np.array(segmentation).reshape(-1, 2)

    # Load the image using PIL
    print(image_path)
    image = Image.open('DATASET/' + image_path)
    image_np = np.array(image)

    # Create an empty mask with the same size as the image
    mask = np.zeros((image_np.shape[0], image_np.shape[1]), dtype=np.uint8)

    # Create a Path object for the polygon
    polygon_path = Path(polygon_vertices)

    # Generate a grid of points (x, y coordinates for each pixel)
    x, y = np.meshgrid(np.arange(image_np.shape[1]), np.arange(image_np.shape[0]))
    points = np.vstack((x.flatten(), y.flatten())).T

    # Check which points (pixels) are inside the polygon
    mask_points = polygon_path.contains_points(points)
    mask_points = mask_points.reshape(image_np.shape[0], image_np.shape[1])

    # Apply the mask to the image
    masked_image = np.zeros_like(image_np)
    masked_image[mask_points] = image_np[mask_points]

    # Find the bounding box to crop the relevant region
    coords = np.column_stack(np.where(mask_points))
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)

    cropped_image = masked_image[y_min:y_max+1, x_min:x_max+1]

    # Plot the original image and cropped image
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Display the original image
    ax[0].imshow(image_np)
    ax[0].set_title("Original Image")

    # Overlay the polygon on the original image
    patch = PathPatch(polygon_path, edgecolor='red', facecolor='none', lw=2)
    ax[0].add_patch(patch)

    # Add average size text for the original image
    ax[0].text(0.5, -0.1, f'Average Size: {mean_size} pixels', 
               ha='center', va='top', transform=ax[0].transAxes)

    # Display the cropped polygon area
    ax[1].imshow(cropped_image)
    ax[1].set_title("Cropped Polygon Area")
    ax[1].text(0.5, -0.1, f'outlier Size: {birds.area_size} pixels', 
               ha='center', va='top', transform=ax[1].transAxes)
    # Create the output folder if it doesn't exist
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    # Save the figure with the red overlay
    plt.savefig(os.path.join(foldername, f'{id}.jpg'), dpi=300)
    plt.close(fig)  # Close the figure to free up memory



    #return cropped_image
if __name__=='__main__':
    pass
