from ultralytics import YOLO
import pprint
import os
import cv2
import csv
import numpy as np
from pathlib import Path
import torch  # Ensure PyTorch is imported for device management

# Check if CUDA is available and set the device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load YOLOv8 model
model = YOLO('/work/cshah/updatedYOLOv8/ultralytics/runs/detect/train176/weights/best.pt')

# Move model to the selected device
model.model.to(device)

# Directory for test frames
testset = '/work/cshah/updatedYOLOv8/ultralytics/extracted_FRAMESn/'

# List of class names
#####class_names = [...]  # Your list of class names

class_names= ['ACANTHURUS-170160100','ACANTHURUSCOERULEUS-170160102','ALECTISCILIARIS-170110101','ANISOTREMUSVIRGINICUS-170190105','ANOMURA-999100401','ARCHOSARGUSPROBATOCEPHALUS-170213601',
'BALISTESCAPRISCUS-189030502','BALISTESVETULA-189030504','BODIANUSPULCHELLUS-170280201','BODIANUSRUFUS-170280202','CALAMUS-170210600','CALAMUSBAJONADO-170210602','CALAMUSLEUCOSTEUS-170210604',
'CALAMUSNODOSUS-170210608','CALAMUSPRORIDENS-170210605','CALLIONYMIDAE-170420000','CANTHIDERMISSUFFLAMEN-189030402','CANTHIGASTERROSTRATA-189080101','CARANGIDAE-170110000',
'CARANXBARTHOLOMAEI-170110801','CARANXCRYSOS-170110803','CARANXRUBER-170110807','CARCHARHINUS-108020200','CARCHARHINUSFALCIFORMIS-108020202','CARCHARHINUSPEREZI-108020211',
'CARCHARHINUSPLUMBEUS-108020208','CAULOLATILUSCHRYSOPS-170070104','CAULOLATILUSCYANOPS-170070101','CAULOLATILUSMICROPS-170070103','CENTROPRISTISOCYURUS-170024804',
'CENTROPRISTISPHILADELPHICA-170024805','CEPHALOPHOLISCRUENTATA-170020401','CEPHALOPHOLISFULVA-170020403','CHAETODON-170260300','CHAETODONCAPISTRATUS-170260302',
'CHAETODONOCELLATUS-170260307','CHAETODONSEDENTARIUS-170260309','CHROMIS-170270300','CHROMISENCHRYSURUS-170270302','CHROMISINSOLATUS-170270304',
'DECAPTERUS-170111200','DERMATOLEPISINERMIS-170020301','DIODONTIDAE-189090000','DIPLECTRUM-170020900','DIPLECTRUMFORMOSUM-170020903','EPINEPHELUS-170021200',
'EPINEPHELUSADSCENSIONIS-170021203','EPINEPHELUSMORIO-170021211','EQUETUSLANCEOLATUS-170201104','GOBIIDAE-170550000','GONIOPLECTRUSHISPANUS-170021403',
'GYMNOTHORAXMORINGA-143060202','GYMNOTHORAXSAXICOLA-143060205','HAEMULONALBUM-170191002','HAEMULONAUROLINEATUM-170191003','HAEMULONFLAVOLINEATUM-170191005',
'HAEMULONMACROSTOMUM-170191017','HAEMULONMELANURUM-170191007','HAEMULONPLUMIERI-170191008','HALICHOERES-170281200','HALICHOERESBATHYPHILUS-170281201',
'HALICHOERESBIVITTATUS-170281202','HALICHOERESGARNOTI-170281205','HOLACANTHUS-170290100','HOLACANTHUSBERMUDENSIS-170290102','HOLOCENTRUS-161110200',
'HOLOCENTRUSADSCENSIONIS-161110201','HYPOPLECTRUS-170021500','HYPOPLECTRUSGEMMA-170021503','HYPOPLECTRUSUNICOLOR-170021501','HYPORTHODUSFLAVOLIMBATUS-170021206',
'HYPORTHODUSNIGRITUS-170021202','IOGLOSSUS -170550800','IOGLOSSUS-170550800','KYPHOSUS-170240300','LACHNOLAIMUSMAXIMUS-170281801','LACTOPHRYSTRIGONUS-189070205',
'LIOPROPOMAEUKRINES-170025602','LUTJANUS-170151100','LUTJANUSANALIS-170151101','LUTJANUSAPODUS-170151102','LUTJANUSBUCCANELLA-170151106','LUTJANUSCAMPECHANUS-170151107',
'LUTJANUSGRISEUS-170151109','LUTJANUSSYNAGRIS-170151113','LUTJANUSVIVANUS-170151114','MALACANTHUSPLUMIERI-170070301','MULLOIDICHTHYSMARTINICUS-170220101',
'MURAENARETIFERA-143060402','MYCTEROPERCA-170022100','MYCTEROPERCABONACI-170022101','MYCTEROPERCAINTERSTITIALIS-170022103','MYCTEROPERCAMICROLEPIS-170022104',
'MYCTEROPERCAPHENAX-170022105','OCYURUSCHRYSURUS-170151501','OPHICHTHUSPUNCTICEPS-143150402','OPHICHTHUSPUNCTICEPS-143150402','OPISTOGNATHUS-170310200',
'OPISTOGNATHUSAURIFRONS-170310203','PAGRUSPAGRUS-170212302','PARANTHIASFURCIFER-170022701','PAREQUESUMBROSUS-170201105','POMACANTHUS-170290200',
'POMACANTHUSARCUATUS-170290201','POMACANTHUSPARU-170290203','POMACENTRIDAE-170270000','POMACENTRUS-170270500','POMACENTRUSPARTITUS-170270502',
'PRIACANTHUSARENATUS-170050101','PRISTIGENYSALTA-170050401','PRISTIPOMOIDES-170151800','PROGNATHODESACULEATUS-170260305',
'PROGNATHODESAYA-170260301','PRONOTOGRAMMUSMARTINICENSIS-170025101','PSEUDUPENEUSMACULATUS-170220701','PTEROIS-168011900','RACHYCENTRONCANADUM-170100101',
'RHOMBOPLITESAURORUBENS-170152001','RYPTICUSMACULATUS-170030106','SCARIDAE-170300000','SCARUSVETULA-170301107','SCOMBEROMORUS-170440800',
'SERIOLA-170113100','SERIOLADUMERILI-170113101','SERIOLAFASCIATA-170113103','SERIOLARIVOLIANA-170113105','SERIOLAZONATA-170113106','SERRANUS-170024200',
'SERRANUSANNULARIS-170024201','SERRANUSATROBRANCHUS-170024202','SERRANUSPHOEBE-170024208','SPARIDAE-170210000','SPARISOMAAUROFRENATUM-170301201',
'SPARISOMAVIRIDE-170301206','SPHYRAENABARRACUDA-165030101','SPHYRNALEWINI-108040102','STENOTOMUSCAPRINUS-170213403','SYACIUM-183011000','SYNODONTIDAE-129040000',
'THALASSOMABIFASCIATUM-170282801','UNKNOWNFISH','UPENEUSPARVUS-170220605','UROPHYCISREGIA-148010105','XANTHICHTHYSRINGENS-189030101']

# Define file paths
csv_file_path = 'detection_output.csv'

# Define video path and frame extraction settings
video_path = r'../../datasets/2021TestVideo/762101178_cam3.avi'
cap = cv2.VideoCapture(video_path)
frame_rate = 5  # Extract frames every 5 seconds

if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

frame_count = 0
frame_id_dict = {}
tracker = {}
csv_data = []  # Initialize csv_data as an empty list

def iou(box1, box2):
    """Compute the Intersection over Union (IoU) of two bounding boxes."""
    x1, y1, x2, y2 = box1
    x1p, y1p, x2p, y2p = box2
    
    # Compute intersection
    ix1 = max(x1, x1p)
    iy1 = max(y1, y1p)
    ix2 = min(x2, x2p)
    iy2 = min(y2, y2p)
    
    iw = max(ix2 - ix1 + 1, 0)
    ih = max(iy2 - iy1 + 1, 0)
    inter_area = iw * ih
    
    # Compute union
    box1_area = (x2 - x1 + 1) * (y2 - y1 + 1)
    box2_area = (x2p - x1p + 1) * (y2p - y1p + 1)
    union_area = box1_area + box2_area - inter_area
    
    return inter_area / union_area

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Extract frames at the specified rate
    if frame_count % int(cap.get(cv2.CAP_PROP_FPS) / frame_rate) == 0:
        frame_filenamen = f'762101178_cam3_{frame_count // int(cap.get(cv2.CAP_PROP_FPS) / frame_rate) + 1}.png'
        img_id = frame_count // int(cap.get(cv2.CAP_PROP_FPS) / frame_rate) + 1
        image_names = frame_filenamen

        image_name = image_names
        unique_frame_id = frame_id_dict.get(image_name, len(frame_id_dict))
        frame_id_dict[image_name] = unique_frame_id
        image_path = os.path.join(testset, f'{image_name}')

        # Run detection
        detections = model(image_path)

        detections_to_save = []

        # Process detections
        for i, result in enumerate(detections):
            for j, bbox in enumerate(result.boxes):
                if bbox.conf >= 0.5 and len(bbox.xyxy) != 0:
                    bbox_xyxyn = result.boxes.xyxy
                    bboxo = bbox_xyxyn[j].cpu().numpy()
                    bbox_conf = result.boxes.conf
                    bbox_cls = result.boxes.cls
                    class_names_detected = [class_names[idx] for idx in bbox_cls.int()]
                    bboxconf = bbox_conf[j].cpu().numpy()
                    confidence = bboxconf
                    class_name = class_names_detected[j]

                    # Track detection
                    max_iou = 0
                    best_track_id = None
                    for track_id, (previous_bbox, _) in tracker.items():
                        iou_score = iou(bboxo, previous_bbox)
                        if iou_score > max_iou:
                            max_iou = iou_score
                            best_track_id = track_id
                    
                    if max_iou > 0.3:  # IoU threshold for tracking
                        tracker[best_track_id] = (bboxo, confidence)
                        track_id = best_track_id
                    else:
                        track_id = len(tracker) + 1
                        tracker[track_id] = (bboxo, confidence)

                    detections_to_save.append([track_id, image_name, unique_frame_id, *bboxo, confidence, -1, class_name, confidence])

        csv_data.extend(detections_to_save)

    frame_count += 1

# Save detections to CSV
csv_header = ['# 1: Detection or Track-id', '2: Video or Image Identifier', '3: Unique Frame Identifier',
              '4-7: Img-bbox(TL_x', 'TL_y', 'BR_x', 'BR_y)', '8: Detection or Length Confidence',
              '9: Target Length (0 or -1 if invalid)', '10-11+: Repeated Species', 'Confidence Pairs or Attributes']

with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(csv_header)
    csv_writer.writerows(csv_data)

print(f'Detections saved to {csv_file_path}')

cap.release()