#! /usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue, Event
import  cv2
from PIL import Image

class CameraProc(Process):
    def __init__(self, filePath, imageQueue,  start_signal, pause_signal,  stop_signal, newInput_signal, inputEnd_Signal, detDone_signal, newRltSignal):
        Process.__init__(self)
        self.filePath = filePath
        self.imageQueue = imageQueue
        self.start_signal = start_signal
        self.notPause_signal = pause_signal
        self.stop_signal = stop_signal
        self.newInput_signal = newInput_signal
        self.inputEnd_Signal = inputEnd_Signal
        # self.proc_endSignal = proc_finishSignal
        self.detDone_signal = detDone_signal
        self.newRltSignal = newRltSignal
        self.isWorking = True

    def run(self):
        while self.isWorking:

            self.start_signal.wait()

            cam = cv2.VideoCapture(self.filePath.value)
            cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameIndex = 0
            total_frame = cam.get(cv2.CAP_PROP_FRAME_COUNT)

            # addcount =0

            while True:
                self.notPause_signal.wait()
                self.detDone_signal.wait()
                ret, frame = cam.read()
                if frameIndex < total_frame:
                    if ret :
                        if frameIndex % 10 == 0:
                            # frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB )
                            # image = Image.fromarray(frame)
                            self.imageQueue.put((frame, frameIndex))

                            # addcount +=1
                            # print('readimage {}'.format(addcount))

                            if not self.newInput_signal.is_set():
                                self.newInput_signal.set()

                            if  self.detDone_signal.is_set():
                                self.detDone_signal.clear()

                            if  self.stop_signal.is_set():
                                cam.release()
                                break

                        frameIndex +=1
                else:
                    cam.release()
                    self.inputEnd_Signal.set()
                    self.newRltSignal.set()
                    self.start_signal.clear()
                    # print('camera end')
                    # print('imagesize{}'.format(self.imageQueue.qsize()))
                    break
