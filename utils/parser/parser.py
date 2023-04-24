import json
import os

def sort_order(prediction):
    return prediction['score']

def filter_class_by_threshold(clase, threshold):
    def filter_by_threshold(clase):
        return clase['score'] >= threshold
    return list(filter(filter_by_threshold, clase))

def contains_class(prediction, clase):
    def filter_by_class(prediction):
        return clase in prediction['class']
    return list(filter(filter_by_class, prediction))

def parse_predictions(predictions):
    classes = []

    # dirname = os.path.dirname(os.path.abspath(__file__))

    # with open(os.path.join(dirname, 'label_map.json'), 'r') as f:
    #     labels = json.load(f)

    labels = json.loads(os.environ.get("LABEL_MAP"))

    # generales = generalizer(predictions)

    for i in range(len(predictions)):
        clase = {}
        clase['class'] = labels[str(i)]
        clase['score'] = float("{:.3f}".format(float(predictions[i])))
        classes.append(clase)
    
    classes = sorted(classes, reverse=True, key=sort_order)
    classes_level2 = classes
    classes = filter_class_by_threshold(classes, float(os.environ.get('THRESHOLD')))

    class_name = ""
    if len(classes) == 0:
        class_name = "NULL"
    elif len(classes) > 2:
        class_name = "NOT_SURE"
    else:
        class_name = classes[0]['class']

    return {
        'preditcion': class_name,
        'full_prediction': classes_level2
    }