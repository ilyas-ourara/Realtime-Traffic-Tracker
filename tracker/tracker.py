import numpy as np 
import matplotlib.pyplot as plt 
import ultralytics 
from ultralytics import YOLO
import cv2
import time
import os
import moviepy as mp
import cvzone 

# Résoudre les problèmes liés à l'initialisation multiple de la bibliothèque OpenMP
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


#lien vers la video https://mega.nz/file/FgMCGbjS#FBSzyOi000-n27IU6aOTpxtSNTy-nVNHQIHtAa8enGs

class Tracker:
    def __init__(self,model_path,input_path,output_path):
        self.model=YOLO(model_path)
        self.input=input_path
        self.bytetrack_yaml_path = "/home/ilyas-ourara/Bureau/venv/lib/python3.12/site-packages/ultralytics/cfg/trackers/bytetrack.yaml"   
        self.output=output_path
      #  self.ligne_sortie_v1=[0,600,630,600]   #ligne de sortie pour la video 1
        self.ligne_sortie_v2=[72,303,439,303]   #ligne de sortie pour la video 2

        self.count_tracker={"car": {"in": 0, "out": 0}, "motorcycle": {"in": 0, "out": 0}, "truck": {"in": 0, "out": 0},"bus": {"in": 0, "out": 0}}  #dictionnaire pour stocker le compteur des objects
        self.crossed_ids=set()      #pour stocker les IDs des objects qui ont traverse la ligne de sortie
        self.offset=7   #marge d'erreur pour la detection de la ligne de sortie
        self.previous_positions={}  #dictionnaire pour stocker les positions précédentes des objets

       


#_____________________fonction pour dessiner un rectangle
    def dessiner_rectangle(self, frame, *args, color=(0, 255, 0), thickness=2):
        """
        Draw a rectangle on `frame`.

        Accepts either:
          dessiner_rectangle(frame, (x1,y1,x2,y2), color=(...), thickness=N)
        or
          dessiner_rectangle(frame, x1, y1, x2, y2, color=(...), thickness=N)
        """
        # If first positional arg is a tuple/list, unpack it
        if len(args) == 1 and (isinstance(args[0], (tuple, list))):
            x1, y1, x2, y2 = map(int, args[0])
        elif len(args) == 4:
            x1, y1, x2, y2 = map(int, args)
        else:
            raise TypeError("dessiner_rectangle expects either a box tuple or four coordinates")

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
    
    def draw_vehicle_icon(self, frame, vehicle_type, x, y, color):
        """
        Dessine une icône compacte pour chaque type de véhicule
        """
        if vehicle_type == "car":
            # Icône voiture - PLUS PETITE
            cv2.rectangle(frame, (x, y), (x+18, y+8), color, -1)
            cv2.circle(frame, (x+3, y+8), 2, (50, 50, 50), -1)  # Roue gauche
            cv2.circle(frame, (x+15, y+8), 2, (50, 50, 50), -1)  # Roue droite
            
        elif vehicle_type == "truck":
            # Icône camion - PLUS PETITE
            cv2.rectangle(frame, (x, y), (x+20, y+10), color, -1)
            cv2.rectangle(frame, (x+15, y-3), (x+20, y+3), color, -1)  # Cabine
            cv2.circle(frame, (x+3, y+10), 2, (50, 50, 50), -1)
            cv2.circle(frame, (x+17, y+10), 2, (50, 50, 50), -1)
            
        elif vehicle_type == "motorcycle":
            # Icône moto - PLUS PETITE
            cv2.rectangle(frame, (x+6, y), (x+12, y+7), color, -1)
            cv2.circle(frame, (x+2, y+7), 2, (50, 50, 50), -1)
            cv2.circle(frame, (x+16, y+7), 2, (50, 50, 50), -1)
            
        elif vehicle_type == "bus":
            # Icône bus - PLUS PETITE
            cv2.rectangle(frame, (x, y), (x+22, y+10), color, -1)
            cv2.rectangle(frame, (x+3, y+2), (x+6, y+5), (255, 255, 255), -1)  # Fenêtre
            cv2.rectangle(frame, (x+10, y+2), (x+13, y+5), (255, 255, 255), -1)  # Fenêtre
            cv2.circle(frame, (x+5, y+10), 2, (50, 50, 50), -1)
            cv2.circle(frame, (x+17, y+10), 2, (50, 50, 50), -1)

    def draw_professional_counter_with_icons(self, frame):
        """
        Design professionnel compact avec icônes géométriques - Position haut droite
        """
        # Fond du panneau - COMMENÇANT À X=350
        cv2.rectangle(frame, (350, 5), (630, 145), (30, 30, 30), -1)
        cv2.rectangle(frame, (350, 5), (630, 145), (100, 100, 100), 2)
        
        # Titre - DÉCALÉ À X=350
        cv2.putText(frame, "COUNTER", (355, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.line(frame, (355, 30), (615, 30), (100, 100, 100), 1)
        
        vehicles_config = [
            ("CAR", "car", 45, (100, 150, 255)),
            ("TRUCK", "truck", 63, (50, 255, 50)),
            ("MOTO", "motorcycle", 81, (255, 100, 100)),
            ("BUS", "bus", 99, (255, 255, 100))
        ]
        
        for label, key, y_pos, color in vehicles_config:
            # Dessiner l'icône - DÉCALÉE À X=355
            self.draw_vehicle_icon(frame, key, 355, y_pos-8, color)
            
            # Texte du véhicule - DÉCALÉ À X=380
            cv2.putText(frame, label, (380, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            
            # Compteurs - DÉCALÉS
            in_count = self.count_tracker[key]["in"]
            out_count = self.count_tracker[key]["out"]
            
            cv2.putText(frame, f"IN:{in_count:02d}", (445, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
            cv2.putText(frame, f"OUT:{out_count:02d}", (505, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 100, 255), 1)
        
        # Total - DÉCALÉ
        total_in = sum(self.count_tracker[v]["in"] for v in ["car", "truck", "motorcycle", "bus"])
        total_out = sum(self.count_tracker[v]["out"] for v in ["car", "truck", "motorcycle", "bus"])
        
        cv2.line(frame, (355, 110), (615, 110), (100, 100, 100), 1)
        cv2.putText(frame, f"TOTAL: IN {total_in} | OUT {total_out}", (355, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#___________________fonction pour calculer le centre d'un rectangle
    def centre_rectangle(self,x1,y1,x2,y2):
        
        cx=int((x1+x2)/2)
        cy=int((y1+y2)/2)
        return cx,cy
    
          
#____________________# Fonction pour calculer le temps passé par chaque client à la caisse

    def temps_passe_caisse(self,results,zone_caisse,ligne_sortie,frame):
        pass


    #fonction principale pour lancer le tracker

    def run_detection(self) :

        

        cap = cv2.VideoCapture(self.input)           #pour ouvrir la video 1
        
        #verifier si la video est ouvert correctement     
        if not cap.isOpened():        
            raise RuntimeError(f"Impossible d'ouvrir  les videos")    #si une video parmis les deux videos n'a pas pu etre ouverte on affiche un mesage d'erreur 
                                                                       #et on arrete le programme



        width_1  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height_1 = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps_1    = cap.get(cv2.CAP_PROP_FPS) or 25.0

        print(f""" ****les dimensions de la video_1 est : width :{width_1},\nheight: {height_1}, fps: {fps_1}.\n
                """)
        
      
        
       

        frames = []  # Liste pour stocker les frames annotées de la video
        while True:
            ret,frame=cap.read()  #lire une frame de la video
            if not ret:
                break
            start_time =time.time()
            frame=cv2.resize(frame,(640,640))
            results = self.model.track(source=frame, persist=True, tracker=self.bytetrack_yaml_path)
            


           
            cv2.line(frame,(self.ligne_sortie_v2[0],self.ligne_sortie_v2[1]),(self.ligne_sortie_v2[2],self.ligne_sortie_v2[3]),(0,255,0),2)
            cv2.circle(frame, (72,303), 5, (255, 0, 255), -1)  # rayon=5, -1 = rempli
            cv2.circle(frame, (439,303), 5, (255, 0, 255), -1)  # rayon=5, -1 = rempli

            for res in results:   # results_1  c'est une liste qui contient toutes les information
                                                            # de  detetion de l'image . on peut faire seulement res=results[0]

                boxes = res.boxes.xyxy.cpu().numpy()
               
                classes = res.boxes.cls.cpu().numpy().astype(int)
                classe_names = res.names
                print("*"*50,"classes",classe_names,"*"*50)

                masks = res.masks.data.cpu().numpy() if res.masks is not None else None
               
                ids = res.boxes.id.cpu().numpy().astype(int)
                
                confidence = res.boxes.conf.cpu().numpy()
               
                print("*"*50,"ids_1",ids,"*"*50)

                for i in range(len(classes)) :

                    class_name=classe_names[int(classes[i])]
                    if class_name in ["car","bus","truck","motorcycle"] :
                    
                        if boxes is not None and confidence[i] > 0.5:
                           
                                x1,y1,x2,y2=map(int,boxes[i])
                                cx,cy=self.centre_rectangle(x1,y1,x2,y2)


                                # pour compter les objet qui entre
                                if self.ligne_sortie_v2[1] <(cy+self.offset) and self.ligne_sortie_v2[1] >(cy-self.offset) and ids[i] not in self.crossed_ids:
                                    if ids[i] in  self.previous_positions:
                                        cv2.circle(frame, (cx, cy), 3, (255, 0, 255), -1)  # rayon=5, -1 = rempli

                                        prev_x,prev_y = self.previous_positions[ids[i]]
                                        if prev_y < cy :
                                            self.count_tracker[f"{class_name}"]["in"] += 1
                                        else:
                                            self.count_tracker[f"{class_name}"]["out"] += 1


                                        self.crossed_ids.add(ids[i])
                                # Mettre à jour la position précédente
                                self.previous_positions[ids[i]] = (cx, cy)
                                
                                if class_name == "car":
                                    col = (255,255,200)
                                elif class_name == "bus":
                                    col = (0, 255, 0)
                                elif class_name == "truck":
                                    col = (0, 0, 255)
                                elif class_name == "motorcycle":
                                    col = (255, 255, 0)

                                somme=self.count_tracker[class_name]["in"]+self.count_tracker[class_name]["out"]
                                cv2.putText(frame,f'{class_name}_id:{ids[i]}', (x1+5,y1-5),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,200),1)
                                self.dessiner_rectangle(frame,x1,y1,x2,y2,color=col,thickness=2)
                              

            self.draw_professional_counter_with_icons(frame)
            cv2.imshow("Tracking", frame)
            #if writer:
             #   writer.write(frame)
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Ajouter la frame annotée à la liste des frames
            frames.append(frame)


            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        #if writer:
         #   writer.release()
        cv2.destroyAllWindows()
        # Enregistrement avec moviepy
        video_clip = mp.ImageSequenceClip(frames, fps=30)
        video_clip.write_videofile(self.output, codec='libx264')

                            


                               
                               
          
