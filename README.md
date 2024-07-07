# Tutoriels PictorIA

Cet espace propose des tutoriels réalisés dans le cadre des activités du consortium Huma-Num [PictorIA](https://pictoria.hypotheses.org/).

## Détection d'objets avec Roboflow

_Atelier BnF Datalab — 26 juin 2024._

Projet Roboflow :  https://mandragore.bnf.fr/

### Tutoriel

[Slides](https://docs.google.com/presentation/d/1-a0tdgQRa2K5ESwN5IhTn8VnGtDaxeseK37TgvtaiHY/edit#)

### Code 

#### [Inférence locale d'un modèle Roboflow](https://github.com/altomator/pictorIA/blob/main/python/test_inference.py)
` python test_inference.py images/6000415-150.jpg "cheval-mandragore/3" `

![inférence Roboflow sur image de test](./demo/inference.png)


#### [Conversion des annotations Roboflow vers le format IIIF]()

` python roboflow2iiif.py btv1b6000415h 150 2.438 images/6000415-150.json `
