# Call inference for a image with a Roboflow model.

# Usage:
# python test_inference.py

import inference
import supervision as sv # https://supervision.roboflow.com/
import cv2
import argparse
import os.path
import sys

parser = argparse.ArgumentParser(description='Infer an image relatively to a Roboflow model')
parser.add_argument('image',  type=str,
                    help='image file')
parser.add_argument('model',  type=str,
                    help='Roboflow model name')

args = parser.parse_args()

# image de test #image_file = "images/6000415-150.jpg"
image_file=args.image
if os.path.isfile(image_file):
    # file exists
    print("...processing: ",image_file)
    image = cv2.imread(image_file)
else:
    sys.exit(f"# Error! file not exists: {image_file}  #\n...ending")

# modèle Roboflow #model_name = "cheval-mandragore/3"
model_name = args.model
# chargement du modèle Roboflow
model = inference.get_model(model_name)
print("...with model: ",model_name)

# inférence
results = model.infer(image)[0]

# charger les résultats dans l'API Supervision Detections
detections = sv.Detections.from_inference(results)

# créer les annotateurs supervision
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

# annoter l'image avec les résultats de l'inférence
annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)

# afficher l'image annotée
sv.plot_image(annotated_image)

# exporter les annotations au format JSON
# https://supervision.roboflow.com/latest/detection/tools/save_detections/#supervision.detection.tools.json_sink.JSONSink
output_file = os.path.splitext(image_file)[0]+'.json'
print("...writing JSON data in: ",output_file)
json_sink = sv.JSONSink(output_file)
json_sink.open()
json_sink.append(detections, custom_data={'file':image_file, 'model':model_name})
json_sink.write_and_close()
