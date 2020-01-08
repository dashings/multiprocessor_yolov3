from multiprocessing import Process, Queue, Event
import yolo_inference as DLModel
import cv2
from PIL import Image
import time


class DetectorProc(Process):
    dl_detector = None

    def __init__(self, inputQueue, resultQueue, newInputSignal, newRltSignal, detDoneSignal,  model_path, classes_path, anchors_path):
        Process.__init__(self)
        self.inputQueue = inputQueue
        self.resultQueue = resultQueue
        self.newInputSignal = newInputSignal
        self.newRltSignal = newRltSignal
        self.detDoneSignal = detDoneSignal
        self.model_path = model_path
        self.classes_path = classes_path
        self.anchors_path = anchors_path


    @staticmethod
    def get_detector_instance(model_path, classes_path, anchors_path):
        if DetectorProc.dl_detector is None:
            DetectorProc.dl_detector = DLModel.YOLO(model_path, classes_path, anchors_path)
        return DetectorProc.dl_detector


    def run(self):

        dl_detector = DetectorProc.get_detector_instance(self.model_path, self.classes_path, self.anchors_path)

        detcoutn = 0
        while True:
            self.newInputSignal.wait()
            while not self.inputQueue.empty():
                print('det queue size {}'.format(self.inputQueue.qsize()))
                
                frame, frameIndex = self.inputQueue.get()
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB )
                image = Image.fromarray(frame)
                out_boxes, out_scores, out_classes, image = dl_detector.detect_image(image)
                self.resultQueue.put((out_boxes, out_scores, out_classes, image, frameIndex))
                # detcoutn +=1
                # print('det proc count {}'.format(detcoutn))
                if not self.newRltSignal.is_set():
                    self.newRltSignal.set()

                if not self.detDoneSignal.is_set():
                    self.detDoneSignal.set()



if __name__ == '__main__':
    # detect_img(YOLO())
    newImg_event = Event()
    subpro_finish_event = Event()
    rlt_queue = Queue()
    detproc = DetectorProc('C:/Users/yaoji/Documents/WXWork/1688851803330717/Cache/Video/2019-12/video(6).MP4', rlt_queue, newImg_event, subpro_finish_event)
    detproc.start()
    detproc.join()