import numpy as np
import time, os, cv2
import threading
import colorsys
from PIL import ImageFont, ImageDraw
from multiprocessing import Event
from multiprocessing import Queue as mpQueue
from PyQt5.QtCore import *
from PIL import Image


class objrThread(threading.Thread):
    dl_detector = None
    finish_signal = Event()

    def __init__(self, filePath, update_signal, finish_signal):
        super(objrThread, self).__init__()
        self.isWorking = False
        self.update_signal = update_signal
        # self.finish_signal = finish_signal

        classes_path = os.path.expanduser('model_data/newclothclass.txt')
        with open(classes_path) as f:
            class_names = f.readlines()
        self.class_names = [c.strip() for c in class_names]

        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))
        np.random.seed(10101)  # Fixed seed for consistent colors across runs.
        np.random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.
        np.random.seed(None)  # Reset seed to default

        self.newImg_event = Event()
        self.subpro_finish_event = Event()
        self.lastepochFlag = False

        if filePath == "":
            self.filePath = "E:/YJF/hotelvideo/video17.MP4"
        else:
            self.filePath = filePath

        self.rlt_queue = mpQueue()

        self.areaClass = ['toilet', 'sink', 'desktop']

        self.errdict = {}
        self.corrList = []
        self.corrDict = {}

        self.testTotalError = []
        self.testTotalCorr = []
        self.testDelError = []
        self.testDelCorr = []

        self.f = open('test.txt')

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter('rltout.avi', fourcc, 30.0, (1920, 1080), True)
        # self.cameraThread = cameraThread(self.imgPath_queue,self.newImg_event, self.cameraThread_finish_event)

    def _run(self):
        while True:
            print('tun in sub_thread')
            time.sleep(1)

    def stop(self):
        self.isWorking = False
        # print('stop')

    def label_match(self, arealabel, clothlabel):
        if (arealabel == 'sink' and clothlabel == 'lightblue') or \
            (arealabel == 'toilet' and clothlabel == 'pink') or \
            (arealabel == 'desktop' and clothlabel == 'orange'):
                return True
        else:
                return False

    def bbox_inter_area(self, box1, box2):
        # Returns the IoU of box1 to box2. box1 is 4, box2 is nx4
        box2 = box2.transpose()

        b1_x1, b1_y1, b1_x2, b1_y2 = box1[0], box1[1], box1[2], box1[3]
        b2_x1, b2_y1, b2_x2, b2_y2 = box2[0], box2[1], box2[2], box2[3]

        # Intersection area
        inter_area = np.maximum(
            np.minimum(b2_x2, np.full(b2_x2.shape, b1_x2)) - np.maximum(b2_x1, np.full(b2_x1.shape, b1_x1)), 0) * \
                     np.maximum(np.minimum(b2_y2, np.full(b2_y2.shape, b1_y2)) - np.maximum(b2_y1, np.full(b2_y1.shape,
                                                                                                           b1_y1)), 0)
        return inter_area

    def run(self):
        self.isWorking = True

        while self.isWorking:
            cam = cv2.VideoCapture(self.filePath)
            cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameIndex = 0
            total_frame = cam.get(cv2.CAP_PROP_FRAME_COUNT)
            print(total_frame)
            WH = np.array((cam.get(cv2.CAP_PROP_FRAME_WIDTH), cam.get(cv2.CAP_PROP_FRAME_HEIGHT)), dtype=float)

            while True:
                ret, frame = cam.read()
                if frameIndex < total_frame:
                    if ret:
                        if frameIndex % 1 == 0:

                            line = self.f.readline().split(';')
                            if  len(line[0]) >0:
                                tmp = []
                                for item in line[0].split(','):
                                    tmp.append(float(item))
                                out_boxes = np.array(tmp).reshape((-1, 4))

                                tmp =[]
                                for item in line[1].split(','):
                                    tmp.append(float(item))
                                out_scores = np.array(tmp)

                                tmp = []
                                for item in line[2].split(','):
                                    tmp.append(int(item))
                                out_classes = np.array(tmp)
                            else:
                                out_boxes=[]
                                out_scores = []
                                out_classes = []


                            image = Image.fromarray(frame)
                            font = ImageFont.truetype(font='font/FiraMono-Medium.otf',
                                                      size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
                            thickness = (image.size[0] + image.size[1]) // 300

                            cloths_box = np.empty(shape=[0, 4])
                            areas_box = np.empty(shape=[0, 4])

                            cloths_label = []
                            areas_label = []

                            for i, c in reversed(list(enumerate(out_classes))):
                                predicted_class = self.class_names[c]
                                box = out_boxes[i]
                                score = out_scores[i]

                                label = '{} {:.2f}'.format(predicted_class, score)
                                draw = ImageDraw.Draw(image)
                                label_size = draw.textsize(label, font)
                                top, left, bottom, right = box
                                top = max(0, np.floor(top + 0.5).astype('int32'))
                                left = max(0, np.floor(left + 0.5).astype('int32'))
                                bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
                                right = min(image.size[0], np.floor(right + 0.5).astype('int32'))

                                if predicted_class in self.areaClass:
                                    areas_box = np.append(areas_box, [[left, top, right, bottom]], axis=0)
                                    areas_label.append(predicted_class)
                                else:
                                    cloths_box = np.append(cloths_box, [[left, top, right, bottom]], axis=0)
                                    cloths_label.append(predicted_class)

                                if top - label_size[1] >= 0:
                                    text_origin = np.array([left, top - label_size[1]])
                                else:
                                    text_origin = np.array([left, top + 1])

                                # My kingdom for a good redistributable image drawing library.
                                for i in range(thickness):
                                    draw.rectangle(
                                        [left + i, top + i, right - i, bottom - i],
                                        outline=self.colors[c])
                                draw.rectangle(
                                    [tuple(text_origin), tuple(text_origin + label_size)],
                                    fill=self.colors[c])
                                draw.text(text_origin, label, fill=(0, 0, 0), font=font)
                                del draw

                            # tmp = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
                            # res = cv2.resize(tmp,None, fx = 0.5, fy=0.5)
                            # cv2.imshow('rlt', res)
                            # if cv2.waitKey(1) & 0xFF == ord('q'):
                            #     break
                            # image.show()

                            if len(areas_label) and len(cloths_label):
                                for i, areas in enumerate(areas_box):
                                    inter_area = self.bbox_inter_area(areas, cloths_box)
                                    for clothIndex in np.nonzero(inter_area)[0]:
                                        if not self.label_match(areas_label[i], cloths_label[clothIndex]):
                                            errkey = '{}-{}'.format(areas_label[i], cloths_label[clothIndex])
                                            if errkey in self.errdict.keys():
                                                self.errdict[errkey][0] += 1
                                                self.errdict[errkey][2] = frameIndex
                                            else:
                                                self.errdict[errkey] = [1, frameIndex, frameIndex, errkey]
                                        else:
                                            if areas_label[i] in self.corrDict.keys():
                                                self.corrDict[areas_label[i]][0] += 1
                                                self.corrDict[areas_label[i]][2] = frameIndex
                                            else:
                                                self.corrDict[areas_label[i]] = [1, frameIndex, frameIndex,
                                                                                 areas_label[i]]

                                            if areas_label[i] not in self.corrList:
                                                self.corrList.append(areas_label[i])

                            # print(self.errdict)
                            notmatchList = []
                            keys = list(self.errdict.keys())
                            for key in keys:
                                if frameIndex - self.errdict[key][2] > 60:
                                    if self.errdict[key][0] > 10:
                                        notmatchList.append(self.errdict[key])
                                        # self.testTotalError[key] = self.errdict[key]
                                        self.testTotalError.append(self.errdict[key])
                                        del (self.errdict[key])
                                    else:
                                        # self.testDelError [key] = self.errdict[key]
                                        self.testDelError.append(self.errdict[key])
                                        del (self.errdict[key])

                            matchList = []
                            corrKeys = list(self.corrDict.keys())
                            for key in corrKeys:
                                if frameIndex - self.corrDict[key][2] > 60:
                                    if self.corrDict[key][0] > 10:
                                        # self.testTotalCorr[key] = self.corrDict[key]
                                        matchList.append(self.corrDict[key])
                                        self.testTotalCorr.append(self.corrDict[key])
                                        del (self.corrDict[key])
                                    else:
                                        self.testDelCorr.append(self.corrDict[key])
                                        del (self.corrDict[key])

                            self.update_signal.emit(np.asarray(image))
                            # print('emit')
                            # print(notmatchList)




if __name__ == '__main__':
    signal = pyqtSignal(np.ndarray)
    signal_finish = pyqtSignal()
    # objrThread = objrThread('C:/Users/yaoji/Documents/WXWork/1688851803330717/Cache/Video/2019-12/video1210.MP4', signal,
    #                         signal_finish)
    objrThread = objrThread('D:/hotel/gopro/video/GH010078.MP4', signal,
                            signal_finish)
    objrThread.start()
    objrThread.join()
