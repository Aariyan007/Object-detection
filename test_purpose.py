import cv2

obj_names = []
class_file = "/Users/lynux/Desktop/My_ODF/data_items.names"
with open(class_file, "rt") as f:
    obj_names = f.read().rstrip("\n").split("\n")

config_path = "/Users/lynux/Desktop/My_ODF/Pretrained vectors mobile_net.pbtxt"
weights_path = "/Users/lynux/Desktop/My_ODF/frozen_inference_graph.pb"

model = cv2.dnn_DetectionModel(weights_path, config_path)
model.setInputSize(320, 320)
model.setInputScale(1.0 / 127.5)
model.setInputMean((127.5, 127.5, 127.5))
model.setInputSwapRB(True)

def detect_objects(frame, threshold, nms_thresh, draw=True, targets=[]):
    class_ids, confidences, boxes = model.detect(frame, confThreshold=threshold, nmsThreshold=nms_thresh)
    if len(targets) == 0:
        targets = obj_names
    detected_objects = []
    if len(class_ids) != 0:
        for class_id, confidence, box in zip(class_ids.flatten(), confidences.flatten(), boxes):
            obj_name = obj_names[class_id - 1]
            if obj_name in targets:
                detected_objects.append([box, obj_name])
                if draw:
                    if obj_name.lower() in ["plastic bottle", "plastic cover", "cup", "paper can"]:
                        color = (0, 0, 255)
                    else:
                        color = (255, 255, 0)
                    cv2.rectangle(frame, box, color=color, thickness=1)
                    cv2.putText(frame, obj_name.upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, color, 1)
                    cv2.putText(frame, str(round(confidence, 2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, color, 1)
    return frame, detected_objects

if __name__ == "__main__":
    video = cv2.VideoCapture(0)
    video.set(3, 640)
    video.set(4, 480)
    
    desired_fps = 10
    delay = int(1000 / desired_fps)
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        result, detected_objects = detect_objects(frame, 0.45, 0.1)
        cv2.imshow("Output", result)
        
        cv2.waitKey(delay)
    
    video.release()
    cv2.destroyAllWindows()
