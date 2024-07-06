# python test_inference.py

import inference
import supervision as sv # https://supervision.roboflow.com/
import cv2

# image de test
image_file = "images/6000415-150.jpg"
image = cv2.imread(image_file)

# modele roboflow
model_name = "cheval-mandragore/3"
# chargement du modèle Roboflow
model = inference.get_model(model_name)

# inférence
results = model.infer(image)[0]

# charger les résultats dans l'API Supervision Detections
detections = sv.Detections.from_inference(results)

# créer les annotateurs supervision
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

# annotater l'image avec les résultats de l'inférence
annotated_image = bounding_box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)

# afficher l'image annotée
sv.plot_image(annotated_image)

# exporter les annotations
# https://supervision.roboflow.com/latest/detection/tools/save_detections/#supervision.detection.tools.json_sink.JSONSink
json_sink = sv.JSONSink("./output.json")
json_sink.open()
json_sink.append(detections, custom_data={'file':image_file, 'model':model_name})
json_sink.write_and_close()
