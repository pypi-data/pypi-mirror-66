import numpy as np
import torch

from ..libs.mtcnn.box_utils import nms, calibrate_box, get_image_boxes, convert_to_square
from ..libs.mtcnn.first_stage import run_first_stage
from ..libs.mtcnn.get_nets import PNet, RNet, ONet


class MtcnnDetector:
    def __init__(self, model_dir="models", ctx_id=-1):
        self.device = torch.device("cuda:" + str(ctx_id)) if ctx_id > -1 else torch.device("cpu")
        self.pnet, self.rnet, self.onet = None, None, None
        self.load_models(model_dir)

    def load_models(self, model_dir):
        self.pnet = PNet(model_dir)
        if torch.cuda.is_available():
            self.pnet.to(self.device)

        self.rnet = RNet(model_dir)
        if torch.cuda.is_available():
            self.rnet.to(self.device)

        self.onet = ONet(model_dir)
        if torch.cuda.is_available():
            self.onet.to(self.device)
        self.onet.eval()

    def detect(self, image, min_face_size=20.0, thresholds=[0.6, 0.7, 0.8], nms_thresholds=[0.7, 0.7, 0.7]):
        # BUILD AN IMAGE PYRAMID
        width, height = image.shape[:2][::-1]
        min_length = min(height, width)

        min_detection_size = 12
        factor = 0.707  # sqrt(0.5)

        # scales for scaling the image
        scales = []

        # scales the image so that
        # minimum size that we can detect equals to
        # minimum face size that we want to detect
        m = min_detection_size / min_face_size
        min_length *= m

        factor_count = 0
        while min_length > min_detection_size:
            scales.append(m * factor ** factor_count)
            min_length *= factor
            factor_count += 1

        # STAGE 1
        # it will be returned
        bounding_boxes = []

        # run P-Net on different scales
        for s in scales:
            boxes = run_first_stage(image, self.pnet, scale=s, threshold=thresholds[0], device=self.device)
            bounding_boxes.append(boxes)

        # collect boxes (and offsets, and scores) from different scales
        bounding_boxes = [i for i in bounding_boxes if i is not None]
        bounding_boxes = np.vstack(bounding_boxes)

        keep = nms(bounding_boxes[:, 0:5], nms_thresholds[0])
        bounding_boxes = bounding_boxes[keep]

        # use offsets predicted by pnet to transform bounding boxes
        bounding_boxes = calibrate_box(bounding_boxes[:, 0:5], bounding_boxes[:, 5:])
        # shape [n_boxes, 5]

        bounding_boxes = convert_to_square(bounding_boxes)
        bounding_boxes[:, 0:4] = np.round(bounding_boxes[:, 0:4])

        # STAGE 2
        img_boxes = get_image_boxes(bounding_boxes, image, size=24)

        img_boxes = torch.FloatTensor(img_boxes)
        if torch.cuda.is_available():
            img_boxes = img_boxes.to(self.device)

        output = self.rnet(img_boxes)
        offsets = output[0].cpu().data.numpy()  # shape [n_boxes, 4]
        probs = output[1].cpu().data.numpy()  # shape [n_boxes, 2]

        keep = np.where(probs[:, 1] > thresholds[1])[0]
        bounding_boxes = bounding_boxes[keep]
        bounding_boxes[:, 4] = probs[keep, 1].reshape((-1,))
        offsets = offsets[keep]

        keep = nms(bounding_boxes, nms_thresholds[1])
        bounding_boxes = bounding_boxes[keep]
        bounding_boxes = calibrate_box(bounding_boxes, offsets[keep])
        bounding_boxes = convert_to_square(bounding_boxes)
        bounding_boxes[:, 0:4] = np.round(bounding_boxes[:, 0:4])

        # STAGE 3
        img_boxes = get_image_boxes(bounding_boxes, image, size=48)
        if len(img_boxes) == 0:
            return [], []

        img_boxes = torch.FloatTensor(img_boxes)
        if torch.cuda.is_available():
            img_boxes = img_boxes.to(self.device)

        output = self.onet(img_boxes)
        landmarks = output[0].cpu().data.numpy()  # shape [n_boxes, 10]
        offsets = output[1].cpu().data.numpy()  # shape [n_boxes, 4]
        probs = output[2].cpu().data.numpy()  # shape [n_boxes, 2]

        keep = np.where(probs[:, 1] > thresholds[2])[0]
        bounding_boxes = bounding_boxes[keep]
        bounding_boxes[:, 4] = probs[keep, 1].reshape((-1,))
        offsets = offsets[keep]
        landmarks = landmarks[keep]

        # compute landmark points
        width = bounding_boxes[:, 2] - bounding_boxes[:, 0] + 1.0
        height = bounding_boxes[:, 3] - bounding_boxes[:, 1] + 1.0
        xmin, ymin = bounding_boxes[:, 0], bounding_boxes[:, 1]
        landmarks[:, 0:5] = np.expand_dims(xmin, 1) + np.expand_dims(width, 1) * landmarks[:, 0:5]
        landmarks[:, 5:10] = np.expand_dims(ymin, 1) + np.expand_dims(height, 1) * landmarks[:, 5:10]

        bounding_boxes = calibrate_box(bounding_boxes, offsets)
        keep = nms(bounding_boxes, nms_thresholds[2], mode='min')
        bounding_boxes = bounding_boxes[keep]
        landmarks = landmarks[keep]

        return bounding_boxes, landmarks
