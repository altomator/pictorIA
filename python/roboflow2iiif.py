# convert Roboflow annotations to IIIF annotations (API Presentation 2.0)
# The annotations can then be uploaded in a IIIF viewer
# Usage:
# python3 roboflow2iiif.py ARK_id page_number ratio json_file

import json
import argparse

parser = argparse.ArgumentParser(description='Convert Roboflow annotations to IIIF annotations (API Presentation 2.0)')
parser.add_argument('ark',  type=str,
                    help='ARK identifier')
parser.add_argument('page',  type=int,
                    help='page number')
parser.add_argument('ratio',  type=float, default=1.0,
                    help='image dimensions ratio')
parser.add_argument('data',  type=str,
                    help='input JSON data')

args = parser.parse_args()

ark=args.ark
page=args.page
data=args.data
ratio=args.ratio
out=ark+"_"+str(page)+"_iiif.json"

print("---------------------------------------")
print("...processing: ", args.data)
print("...output in: ", out)

def create_annotation(id, body, target, label=None):
    annotation = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": id,
        "@type": "oa:Annotation",
        "motivation": "oa:describing",
        "resource": body,
        "on": f"https://gallica.bnf.fr/iiif/ark:/12148/{ark}/canvas/f{page}#xywh={target}",
    }
    print (f"https://gallica.bnf.fr/iiif/ark:/12148/{ark}/canvas/f{page}#xywh={target}")

    return annotation

def write_annotations_to_file(annotations, filename):
    with open(filename, 'w') as f:
        f.write("{")
        f.write(f"\"https://gallica.bnf.fr/iiif/ark:/12148/{ark}/manifest.json\"")
        f.write(": {\n")
        f.write(f"\"https://gallica.bnf.fr/iiif/ark:/12148/{ark}/canvas/f{page}\"")
        f.write(": ")
        json.dump(annotations, f, indent=4)
        f.write("}}")

def create_annotations_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)

    annotations = []
    for i, prediction in enumerate(data):
        id = f"{ark}-{page}-{i}"
        x = prediction["x_min"]
        y = prediction["y_min"]
        width = prediction["x_max"] - x
        height = prediction["y_max"] - y
        class_name = prediction["class_name"]
        conf = "{:.2f}".format(prediction["confidence"])
        label = f"{class_name} ({conf})"

        target = f"{int(x*ratio)},{int(y*ratio)},{int(width*ratio)},{int(height*ratio)}"

        body = [{
        "@type": "dctypes:Text",
        "format": "text/html",
        "chars": f"<p>{label}</p>"}]

        annotation = create_annotation(id, body, target, label)
        annotations.append(annotation)

    return annotations

# Example usage:
annotations = create_annotations_from_file(data)
write_annotations_to_file(annotations, out)
