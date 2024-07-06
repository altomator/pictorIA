# python test_inference.py

import inference
import supervision as sv # https://supervision.roboflow.com/
import cv2

# image de test
image_file = "images/6000415-150.jpg"
image = cv2.imread(image_file)

# chargement du modèle Roboflow
model = inference.get_model("cheval-mandragore/3")

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
