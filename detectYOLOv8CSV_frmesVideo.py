from ultralytics import YOLO
import pprint
import os
import cv2
import csv
import torch
from pathlib import Path
# Importing the glob library
import glob 

#### Load a pretrained YOLOv8n model
##model = YOLO('yolov8n.pt')

#model = YOLO('/work/cshah/YOLOv8/runs/detect/train265/weights/best.pt')

#model = YOLO('/work/cshah/YOLOv8_weights_saved/YOLOv8l/weights/best.pt')

#model = YOLO('/work/cshah/YOLOv8_weights_saved/YOLOvn/weights/best.pt')

model = YOLO('/work/cshah/YOLOv8_weights_saved/Yolov8m_enh_128batch/weights/best.pt')


### Run inference on an image
#results = model('bus.jpg')

###results = model('../../datasets/images/test/', save=True)
#results = model('../../datasets/images/test/YSC4_Camera4_08-07-19_19-01-400004.png',save=True)

#results = model('../../datasets/2021TestVideo/762101449_cam3.avi',save=True)

#testset = r'/work/cshah/updatedYOLOv8/ultralytics/extracted_FRAMES/'
#testset = r'/work/cshah/updatedYOLOv8/ultralytics/extracted_FRAMESn/'

testset = '/work/cshah/updatedYOLOv8/ultralytics/extracted_FRAMESn/'

##results = model('/work/cshah/updatedYOLOv8/ultralytics/extracted_FRAMES/762101028_cam3_69.png',save=True)

#results = model(testset, save=True)

### List files in the directory
list_test_files = os.listdir(testset)

###files_sort = list_test_files.sort()

##files_sort = sorted(list_test_files)

#### Sort the files based on their modification time
#files_sort = sorted(list_test_files, key=lambda x: os.path.getctime(os.path.join(testset, x)))

#files_sort = sorted(list(Path(testset).iterdir()),
#                     key=lambda path: int(path.stem))

# Extract the list of filenames
###files_sort = glob.glob(testset + '*', recursive=False)

#files_sort = sorted(Path(testset).iterdir(), key=lambda x: x.name)

#files_sort = sorted(list(Path(testset).iterdir()),
#                     key=lambda path: int(path.stem))

#directory = os.path.dirname(testset[0])

# Get all files in the directory and sort them
#files_sort = sorted(os.listdir(directory))

files_sort = sorted(os.listdir(testset))

# Get all files in the directory using Pathlib
###files_sort = [file for file in Path(testset).iterdir() if file.is_file()]

###files_sort = files_sort.sort()

#files = os.listdir(testset)

#files_sort = files.sort()
###files_sort = list_test_files.sort()

##print('test files',list_test_files)
print('sorted test files',files_sort)


#print('first image in sorted files',files_sort[0])
#print('last image in sorted files',files_sort[7501])

# Sort the files based on their creation time (or modification time)
##sortedfiles = list_test_files.sort(key=lambda x: os.path.getmtime(os.path.join(testset, x)))

#sortedfiles = sorted(list_test_files)

#print('last test files',list_test_files[7501])
#print('last test files',sortedfiles)

totalimags = len(list_test_files)
print('total images in test sest',totalimags)

#print('name of testset in 1',testset[40])

#video_path = '../../datasets/2021TestVideo/762101449_cam3.avi'

#results = model('../../datasets/images/test//YSC4_Camera4_08-07-19_19-01-400004.png',save=True)


#print('pprint results to detect position')
#pprint.pprint(results)

class_names= ['ACANTHURUSCOERULEUS', 'ACANTHURUS', 'ALECTISCILIARIS', 'ANISOTREMUSVIRGINICUS','ANOMURA','ANTHIINAE','ARCHOSARGUSPROBATOCEPHALUS','BALISTESCAPRISCUS',
       'BALISTESVETULA','BODIANUSPULCHELLUS','BODIANUSRUFUS','CALAMUSBAJONADO','CALAMUSLEUCOSTEUS','CALAMUSNODOSUS','CALAMUSPRORIDENS','CALAMUS','CANTHIDERMISSUFFLAMEN',
       'CANTHIGASTERROSTRATUS','CARANXBARTHOLOMAEI','CARANXCRYSOS','CARANXRUBER','CARCHARHINUSFALCIFORMIS','CARCHARHINUSPEREZI','CARCHARHINUSPLUMBEUS','CAULOLATILUSCHRYSOPS',
       'CAULOLATILUS CYANOPS','CAULOLATILUSCYANOPS','CENTROPRISTISOCYURA','CEPHALOPHOLISCRUENTATA','CEPHALOPHOLISFULVA','CHAETODONACULEATUS','CHAETODONCAPISTRATUS',
       'CHAETODONOCELLATUS','CHAETODONSEDENTARIUS','CHAETODON','CHROMISENCHRYSURUS','CHROMISINSOLATUS','CHROMIS','DERMATOLEPISINERMIS','DIODONTIDAE','DIPLECTRUMFORMOSUM',
       'DIPLECTRUM','EPINEPHELUSADSCENSIONIS','EPINEPHELUSFLAVOLIMBATUS','EPINEPHELUSMORIO','EPINEPHELUSNIGRITUS','EPINEPHELUS','EQUETUSLANCEOLATUS','EQUETUSUMBROSUS',
       'GONIOPLECTRUSHISPANUS','GYMNOTHORAXMORINGA','GYMNOTHORAXSAXICOLA','HAEMULONAUROLINEATUM','HAEMULONFLAVOLINEATUM','HAEMULONMACROSTOMUM','HAEMULONMELANURUM',
       'HAEMULONPLUMIERI','HALICHOERESBATHYPHILUS','HALICHOERESBIVITTATUS','HALICHOERESGARNOTI','HALICHOERES','HOLACANTHUSBERMUDENSIS','HOLACANTHUS','HOLANTHIUSMARTINICENSIS',
       'HOLOCENTRUS','HYPOPLECTRUSGEMMA','HYPOPLECTRUS','HYPOPLECTRUSUNICOLOR','IOGLOSSUS','KYPHOSUS','LACHNOLAIMUSMAXIMUS','LACTOPHRYSTRIGONUS','LIOPROPOMAEUKRINES',
       'LUTJANUSANALIS','LUTJANUSAPODUS','LUTJANUSBUCCANELA','LUTJANUSCAMPECHANUS','LUTJANUSGRISEUS','LUTJANUSSYNAGRIS','LUTJANUS','LUTJANUSVIVANUS','MALACANTHUSPLUMIERI',
       'MULLOIDICHTHYSMARTINICUS','MURAENARETIFERA','MYCTEROPERCABONACI','MYCTEROPERCAINTERSTIALIS','MYCTEROPERCAINTERSTITIALIS','MYCTEROPERCAMICROLEPIS','MYCTEROPERCAPHENAX',
       'MYCTEROPERCA','OCYURUSCHRYSURUS','OPHICHTHUSPUNCTICEPS','OPISTOGNATHUSAURIFRONS','PAGRUSPAGRUS','PARANTHIASFURCIFER','POMACANTHUSARCUATUS','POMACANTHUSPARU',
       'POMACANTHUS','POMACENTRIDAE','POMACENTRUSPARTITUS','POMACENTRUS','PRIACANTHUSARENATUS','PRISTIGENYSALTA','PRISTIPOMOIDESAQUILONARIS','PSEUDUPENEUSMACULATUS','PTEROIS',
       'RACHYCENTRONCANADUM','RHOMBOPLITESAURORUBENS','RYPTICUSMACULATUS','SCARIDAE','SCARUSVETULA','SERIOLADUMERILI','SERIOLAFASCIATA','SERIOLARIVOLIANA','SERIOLA',
       'SERIOLAZONATA','SERRANUSANNULARIS','SERRANUSPHOEBE','SERRANUS','SPARIDAE','SPARISOMAAUROFRENATUM','SPARISOMAVIRIDE','SPHYRAENABARRACUDA','SPHYRNALEWINI',
       #'STENOTOMUSCAPRINUS','SYACIUM','SYNODONTIDAE','THALASSOMABIFASCIATUM']
       'STENOTOMUSCAPRINUS','SYACIUM','SYNODONTIDAE','THALASSOMABIFASCIATUM','UPENEUSPARVUS','XANTHICHTHYSRINGENS']


#print('results on test image',results)

### Extract bounding boxes and class names
### Extract bounding boxes and class names

#print('shape of results',results.shape)

#for r in results:
#    boxes = r.boxes
#    for box in boxes:
#        b = box.xyxy[0]   # get box coordinates
#        confc = box.conf
#        c = box.cls
#    print('box',b)
#    print('conf pred',confc)
#    print('class',c)

#for result in results:
    ###detection results
#    bbox_xyxy = result.boxes.xyxy
#    bbox_xywh = result.boxes.xywh
    ###bbox_xyxyn = result.boxes.xyxyn
    ###bbox_xywhn = result.boxes.xywhn
#    bbox_conf = result.boxes.conf
#    bbox_cls = result.boxes.cls
#    class_names = class_names
#    class_indices = bbox_cls.int()
#    class_names_detected = [class_names[idx] for idx in class_indices]

#    print('box xyxy',bbox_xyxy) ##Pascal VOC format
    ###print('box xywh',bbox_xywh)
#    print('conf pred',bbox_conf)
#    print('class no',bbox_cls)
#    print('class_names_detected',class_names_detected)


# Output CSV file path
csv_file_path = 'detections_2_16.csv'

# Header for the CSV file
csv_header = ['# 1: Detection or Track-id', '2: Video or Image Identifier', '3: Unique Frame Identifier',
              '4-7: Img-bbox(TL_x', 'TL_y', 'BR_x', 'BR_y)', '8: Detection or Length Confidence',
              '9: Target Length (0 or -1 if invalid)', '10-11+: Repeated Species', 'Confidence Pairs or Attributes']

# Save detections to CSV
csv_data = [csv_header]

directory = r'/work/cshah/updatedYOLOv8/ultralytics/extracted_FRAMESn/'

print('directory of extracted frames',directory)

# Dictionary to map image names to unique frame identifiers
frame_id_dict = {}
##img_id = 0
for img_id in range(totalimags):
    ### Extract the image name from the dataset
    #image_name = os.path.splitext(os.path.basename(testset.ids[img_id][1]))[0]
    # List files in the directory

    print('total images',totalimags)

    files = list_test_files

    print('image id',img_id)

    #print('files total',files)
    #image_names = os.path.basename(files[img_id])[16]
    image_names = os.path.basename(files[0])
    print('image name 0',image_names)

    print('files name 0',files[0])

    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]

   ### Extract the filename of the first image in the list
    if files:
        first_image_name = os.path.basename(files[0])
        print("First image name:", first_image_name)

    #image_names = os.path.basename(files[2])
    #print('image name 2',image_names)


    image_name = os.path.basename(files[img_id])

    #image_name = [os.path.splitext(file)[0] for file in files if os.path.isfile(os.path.join(testset, file))]
    print('image name',image_name)

    # Get or create unique frame identifier
    unique_frame_id = frame_id_dict.get(image_name, len(frame_id_dict))
    frame_id_dict[image_name] = unique_frame_id

    ### Form the correct path to the image
    #image_path = os.path.join(args.dataset_root, 'VOC2007', 'JPEGImages', f'{image_name}.png')

    image_path = os.path.join(testset, f'{image_name}')    

    print('image path name',image_path)

    image = cv2.imread(image_path)

    #print('image read im path',image)

    # Preprocess the image
    #xx = x.unsqueeze(0)

    ## Perform inference
    #with torch.no_grad():
    #    detections = net(xx)

    detections = model(image_path) 

    #print('detections fo image',detections)
    print('size of detections',len(detections))

    # Process and save the detection results
    detections_to_save = []  # Define detections_to_save here

    #for i in range(totalimags):
    #    j = 0
    #    while detections[0, i, j, 0] >= 0.5:
    #        score = detections[0, i, j, 0].item()  # Get the float value of the tensor
    #        label_name = VOC_CLASSES[i - 1]
    #        pt = (detections[0, i, j, 1:5] * torch.Tensor([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])).cpu().numpy()
    #        bbox = [pt[0], pt[1], pt[2], pt[3]]
    #        confidence = score
    #        class_name = label_name
    #        detections_to_save.append([j + 1, image_name, unique_frame_id, *bbox, confidence, -1, class_name, confidence])
    #        j += 1

    print('length of detections',len(detections))
     
    for i in range(len(detections)):    
        j = 0
        for result in detections:
            print('conf score in bbox',result.boxes.conf)
            ###while result.boxes.conf >= 0.5:
            #while len(result.boxes.xyxy) != 0:
            if len(result.boxes.xyxy) != 0:

                  bbox_xyxy = result.boxes.xyxy
                  bbox_conf = result.boxes.conf
                  bbox_cls = result.boxes.cls
                  class_names = class_names
                  class_indices = bbox_cls.int()
                  class_names_detected = [class_names[idx] for idx in class_indices]
                  #print('box xyxy',bbox_xyxy)
            
                  ######pt = bbox_xyxy
                  bbox = bbox_xyxy
                  #bboxnum = bbox.numpy()
 
                  class_name = class_names_detected
                  confidence = bbox_conf
                  detections_to_save.append([j + 1, image_name, unique_frame_id, *bbox, confidence, -1, class_name, confidence])
                  j = j + 1

                  print('box xyxy',bbox_xyxy)
        ####print('box xywh',bbox_xywh)
                  print('conf pred',bbox_conf)
                  print('class no',bbox_cls)
                  print('class_names_detected',class_names_detected)

    csv_data.extend(detections_to_save)

# Write CSV data to file
with open(csv_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(csv_data)

print(f'Detections saved to {csv_file_path}')


# Extract bounding boxes, class indices, and confidence scores
#bounding_boxes = [result['bbox'] for result in results]
#class_indices = [result['class_idx'] for result in results]
#confidence_scores = [result['confidence'] for result in results]

#bounding_boxes = results[:, :4]
#class_indices = results[:, 4].astype(int)
#confidence_scores = results[:, 5]

#print('bounding_boxes pred on test results',bounding_boxes)

#bounding_boxes = [result['boxes'] for result in results]
#print('bounding boxes yolov8',bounding_boxes)

#confidence_scores = [result['confidence'] for result in results]
#print('confidence scores yolov8',confidence_scores)

#results = model('../../datasets/2021TestVideo/762101178_cam3.avi',save=True)


#result_folder = '/work/cshah/updatedYOLOv8/ultralytics/detectedresults'

##path = model.export(format="onnx")  # export the model to ONNX format
##print('path')