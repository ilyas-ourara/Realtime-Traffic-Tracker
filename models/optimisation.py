from ultralytics import YOLO

model = YOLO("yolov8s.pt")
model.export(format="onnx")
