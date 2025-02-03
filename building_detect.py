import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
from pathlib import Path
from config_ import Config

class ObjectDetectionProcessor:
    """
    A class to handle object detection, cropping, and saving of images.
    """

    def __init__(self, module_url, target_classes, input_dir, output_dir, threshold=0.3, expand_factor=0.1, min_dim=200):
        self.module_url = module_url
        self.target_classes = target_classes
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.threshold = threshold
        self.expand_factor = expand_factor
        self.min_dim = min_dim
        self.detector = self.load_detector()

        # Create the output directory if it does not exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_detector(self):
        """
        Load the object detection model from TensorFlow Hub.
        """
        return hub.load(self.module_url).signatures['default']

    def crop_and_save(self, original_image, box, save_path):
        """
        Crop the image based on the bounding box and save it to the specified path.
        """
        img_height, img_width, _ = original_image.shape
        ymin, xmin, ymax, xmax = box

        # Calculate expansion in both height and width
        box_width = xmax - xmin
        box_height = ymax - ymin
        expand_w = box_width * self.expand_factor
        expand_h = box_height * self.expand_factor

        # Expand the bounding box
        xmin_expanded = max(0, xmin - expand_w)
        ymin_expanded = max(0, ymin - expand_h)
        xmax_expanded = min(1, xmax + expand_w)
        ymax_expanded = min(1, ymax + expand_h)

        # Convert normalized coordinates to pixel coordinates
        xmin_pixel = int(xmin_expanded * img_width)
        ymin_pixel = int(ymin_expanded * img_height)
        xmax_pixel = int(xmax_expanded * img_width)
        ymax_pixel = int(ymax_expanded * img_height)

        # Crop the image
        cropped_image = original_image[ymin_pixel:ymax_pixel, xmin_pixel:xmax_pixel]
        cropped_height, cropped_width, _ = cropped_image.shape

        if cropped_width < self.min_dim or cropped_height < self.min_dim:
            return

        # Save the cropped image
        cropped_image = (cropped_image * 255).astype(np.uint8)
        cropped_image_pil = Image.fromarray(cropped_image)
        cropped_image_pil.save(save_path, format="JPEG", quality=90)

    def calculate_iou(self, box1, box2):
        """
        Calculate the Intersection over Union (IoU) between two bounding boxes.
        """
        y1_1, x1_1, y2_1, x2_1 = box1
        y1_2, x1_2, y2_2, x2_2 = box2

        intersection_y1 = max(y1_1, y1_2)
        intersection_x1 = max(x1_1, x1_2)
        intersection_y2 = min(y2_1, y2_2)
        intersection_x2 = min(x2_1, x2_2)

        intersection_area = max(0, intersection_x2 - intersection_x1) * max(0, intersection_y2 - intersection_y1)
        box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
        box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)

        union_area = box1_area + box2_area - intersection_area
        return intersection_area / union_area if union_area > 0 else 0

    def process_images(self):
        """
        Process all images in the input directory for object detection.
        """
        image_files = [f for f in self.input_dir.iterdir() if f.suffix.lower() in {".jpg", ".jpeg", ".png"}]

        for image_file in image_files:
            print(f"Processing image: {image_file}")
            image = tf.io.read_file(str(image_file))
            image = tf.image.decode_image(image, channels=3)
            image = tf.image.resize(image, (3600, 3600))
            image = tf.expand_dims(image, axis=0)  # Add batch dimension
            image = tf.cast(image, tf.float32) / 255.0  # Normalize

            output_dict = self.detector(image)
            boxes = output_dict['detection_boxes'].numpy()
            scores = output_dict['detection_scores'].numpy()
            classes = output_dict['detection_class_entities'].numpy()

            detected_indices = np.where(scores >= self.threshold)[0]
            original_image = tf.squeeze(image).numpy()

            final_detections = []
            iou_threshold = 0.5
            original_image_name = image_file.stem

            for i, detection_index in enumerate(detected_indices):
                class_name = classes[detection_index].decode('utf-8').capitalize()
                if class_name in self.target_classes:
                    current_box = boxes[detection_index]
                    current_score = scores[detection_index]

                    is_duplicate = False
                    for existing_detection in final_detections:
                        if self.calculate_iou(current_box, existing_detection['box']) > iou_threshold:
                            if current_score > existing_detection['score']:
                                final_detections.remove(existing_detection)
                                final_detections.append({
                                    'class': class_name,
                                    'box': current_box,
                                    'score': current_score
                                })
                            is_duplicate = True
                            break

                    if not is_duplicate:
                        final_detections.append({
                            'class': class_name,
                            'box': current_box,
                            'score': current_score
                        })

            for detection_index, detection in enumerate(final_detections):
                save_path = self.output_dir / f"{original_image_name}-{detection_index + 1}.jpg"
                self.crop_and_save(original_image, detection['box'], save_path)

        print("Processing complete for all images.")

if __name__ == "__main__":
    configuration = Config.get_config_detection()
    processor = ObjectDetectionProcessor(
        module_url=configuration["module_url"],
        target_classes=configuration["target_classes"],
        input_dir=configuration["input_dir"],
        output_dir=configuration["output_dir"],
        threshold=configuration["threshold"],
        expand_factor=configuration["expand_factor"],
        min_dim=configuration["min_dim"]
    )
    processor.process_images()