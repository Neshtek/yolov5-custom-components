import torch
import cv2
import numpy as np
import sys
import os
import datetime

model = torch.hub.load("ultralytics/yolov5", "custom", path="weights/best.pt")

print("Model loaded")

video_path = 'data.mp4'

camera = cv2.VideoCapture(video_path)
# create named windows for input and output frames
cv2.namedWindow('input', cv2.WINDOW_NORMAL)
cv2.namedWindow('output', cv2.WINDOW_NORMAL)

output_folder = 'Dataset'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

while (camera.isOpened()):
    return_val, frame = camera.read()
    if not return_val:
        print("Video ended or failed")
        sys.exit(0)

    frame_data = cv2.resize(frame, (640, 640))

    result = model(frame_data)
    print(result)

    if hasattr(result, 'xyxyn'):
        labels, cord = result.xyxyn[0][:, -1].to('cpu').numpy(), result.xyxyn[0][:, :-1].to('cpu').numpy()

        x_shape, y_shape = frame.shape[1], frame.shape[0]
        label_len = len(labels)

        output_np = [img for img in result.render()]
        output_np = np.concatenate(output_np, axis=1)

        objects = []
        for i in range(label_len):
            if cord.ndim == 1:
                cord = cord[np.newaxis, :]
            x_center, y_center, width, height, _ = cord[i]
            x1 = int((x_center - width / 2) * x_shape)
            y1 = int((y_center - height / 2) * y_shape)
            x2 = int((x_center + width / 2) * x_shape)
            y2 = int((y_center + height / 2) * y_shape)

            label = labels[i]
            objects.append({'label': label, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})

        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + '.jpg'
        output_path = os.path.join(output_folder, filename)

        for obj in objects:
            cv2.rectangle(output_np, (obj['x1'], obj['y1']), (obj['x2'], obj['y2']), (0, 255, 0), 2)

        cv2.imwrite(output_path, output_np)

        if label_len > 0:
            filepath = os.path.splitext(output_path)[0] + '.txt'
            with open(filepath, 'w') as f:
                for obj in objects:
                    label = obj['label']
                    x_center, y_center, width, height, _ = cord[i]
                    x1 = int((x_center - width / 2) * x_shape)
                    y1 = int((y_center - height / 2) * y_shape)
                    x2 = int((x_center + width / 2) * x_shape)
                    y2 = int((y_center + height / 2) * y_shape)
                    cv2.rectangle(output_np, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    label = labels[i]
                    cv2.imwrite(output_path, output_np)
                    f.write(f"{label} {(x_center * x_shape / 640):.6f} {(y_center * y_shape / 640):.6f} {(width * x_shape / 640):.6f} {(height * y_shape / 640):.6f}\n")
    cv2.imshow('output', output_np)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()