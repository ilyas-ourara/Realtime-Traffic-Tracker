from tracker import Tracker
import os

model_path= "models/yolov8s.onnx"   #le chemin vers le modele
video_path="input/2.mp4"  #le chemin vers la video 
output_path="output/out.mp4"



# Vérifier si le répertoire pour l'enregistrement n'existe pas, et le créer
if not os.path.exists(os.path.dirname(output_path)):
    os.makedirs(os.path.dirname(output_path))

# Vérifier si le fichier modèle et la vidéo existent
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Le modèle spécifié n'existe pas : {model_path}")
if not os.path.exists(video_path):
    raise FileNotFoundError(f"La vidéo spécifiée n'existe pas : {video_path}")


def run_tracking() :
    ot=Tracker(model_path,video_path,output_path)
    print("Début du suivi des objets...")
    ot.run_detection()
    print("Suivi des objets terminé. La vidéo annotée est enregistrée à :", output_path)


if __name__=="__main__" :
    run_tracking()
    
    




