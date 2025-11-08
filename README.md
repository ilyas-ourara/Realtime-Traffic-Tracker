
# Traffic Vision YOLOv11 🚗📊

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-Ultralytics-orange.svg)](https://github.com/ultralytics/ultralytics)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)


## Demo 🚗


![Demo](https://github.com/ilyas-ourara/realtime-traffic-tracker/raw/main/demo.gif)


## 📋 Description

Système de détection et suivi de véhicules en temps réel utilisant YOLOv11 (Ultralytics) et ByteTrack. Le projet fournit un pipeline complet pour l'analyse du trafic avec comptage IN/OUT, affichage professionnel des bounding boxes et panneau de statistiques interactif.

### ✨ Fonctionnalités

- **Détection multi-classe** : Voitures, camions, motos, bus
- **Suivi en temps réel** : Algorithme ByteTrack pour la continuité des objets
- **Comptage bidirectionnel** : Analyse des flux IN/OUT avec détection de ligne
- **Interface professionnelle** : Bounding boxes avec badges colorés et panneau de statistiques
- **Export vidéo** : Enregistrement des résultats avec annotations

### 🔮 Roadmap

- [ ] **Estimation de vitesse** : Calcul de vitesse basé sur la distance/temps
- [ ] **OCR plaques** : Reconnaissance automatique des plaques d'immatriculation
- [ ] **Détection feux rouges** : Surveillance des violations de signalisation
- [ ] **Analytics avancées** : Export CSV/JSON des données de trafic

## 🚀 Installation

### Prérequis

```bash
Python 3.8+
CUDA (optionnel, pour GPU)
```

### Installation des dépendances

```bash
# Cloner le repository
git clone https://github.com/votre-username/traffic-vision-yolov11.git
cd traffic-vision-yolov11

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Requirements.txt

```
ultralytics>=8.0.0
opencv-python>=4.5.0
cvzone>=1.6.0
moviepy>=1.0.3
numpy>=1.21.0
matplotlib>=3.3.0
```

## 📁 Structure du projet

```
traffic-vision-yolov11/
├── main.py                 # Script principal
├── tracker/
│   ├── __init__.py
│   └── tracker.py         # Classe Tracker principale
├── speed/
│   ├── __init__.py
│   └── speed.py          # Module estimation vitesse (à venir)
├── models/
│   ├── yolov8n.pt        # Modèle YOLOv8 nano
│   └── yolov8s.pt        # Modèle YOLOv8 small
├── input/                # Vidéos d'entrée
├── output/               # Vidéos traitées
├── requirements.txt      # Dépendances Python
└── README.md            # Documentation
```

## 🎯 Utilisation

### Utilisation de base

```bash
python main.py
```

### Configuration

Modifiez les paramètres dans `main.py` :

```python
# Chemins des fichiers
model_path = "models/yolov8n.pt"
input_path = "input/your_video.mp4"
output_path = "output/result.mp4"

# Créer le tracker
tracker = Tracker(model_path, input_path, output_path)
tracker.run_detection()
```

### Personnalisation des zones de détection

Dans `tracker/tracker.py`, ajustez les coordonnées de la ligne de comptage :

```python
# Coordonnées pour image 1920x1080
self.ligne_sortie_v2 = [72, 303, 439, 303]  # [x1, y1, x2, y2]
```

## 📊 Fonctionnalités détaillées

### Détection et Classification

- **Classes supportées** : car, truck, motorcycle, bus
- **Seuil de confiance** : 0.5 (configurable)
- **Modèles** : YOLOv8n/s/m/l/x (Ultralytics)

### Suivi Multi-Objets

- **Algorithme** : ByteTrack
- **Persistance** : IDs uniques maintenues entre frames
- **Robustesse** : Gestion des occultations temporaires

### Comptage Intelligent

- **Direction** : Détection du sens de passage (IN/OUT)
- **Anti-doublons** : Chaque véhicule compté une seule fois
- **Zone configurable** : Ligne de détection personnalisable

### Interface Utilisateur

- **Panneau statistiques** : Compteurs temps réel par catégorie
- **Bounding boxes** : Badges colorés avec ID et classe
- **Indicateurs visuels** : Ligne de détection et points de passage





## 📝 Roadmap 

### Phase 1 - Base (✅ Terminé)
- [x] Détection YOLOv11
- [x] Tracking ByteTrack
- [x] Comptage bidirectionnel
- [x] Interface basique

### Phase 2 - Analytics (🔄 En cours)
- [ ] Estimation de vitesse
- [ ] Zones de détection multiples
- [ ] Export données CSV/JSON
- [ ] Dashboard temps réel

### Phase 3 - IA Avancée (📋 Planifié)
- [ ] OCR plaques d'immatriculation
- [ ] Détection violations feux rouges
- [ ] Classification comportements
- [ ] Alertes automatiques

### Phase 4 - Production (🎯 Futur)
- [ ] API REST
- [ ] Interface web
- [ ] Base de données
- [ ] Notifications temps réel



⭐ **N'hésitez pas à star le projet si il vous a aidé !** ⭐
