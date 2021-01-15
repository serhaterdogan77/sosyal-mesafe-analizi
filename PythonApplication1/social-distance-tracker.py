import cv2
import imutils
import numpy as np
import argparse


def detect(frame):
    bounding_box_cordinates, weights = HOGCV.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.03)

    person = 1
    en = 0
    people_list = []
    for x, y, w, h in bounding_box_cordinates:
        en += x + w
        person += 1
        people_list.append([x, y, w, h, 0])

    en = (en / person) / 4

    i = 0
    while i != len(people_list):
        selected_person = people_list[i]
        for other_person in people_list:
            if other_person != selected_person and (selected_person[4] == 0 or other_person[4] == 0):
                selected_person_x_axis = (selected_person[0] - en, selected_person[0] + selected_person[2] + en)
                other_person_x_axis = (other_person[0], other_person[2])
                selected_person_y_axis = (selected_person[1] - en, selected_person[1] + selected_person[3] + en)
                other_person_y_axis = (other_person[1], other_person[3])
                if (selected_person_x_axis[0] <= other_person_x_axis[0] <= selected_person_x_axis[1] or
                    selected_person_x_axis[0] <= other_person_x_axis[1] <= selected_person_x_axis[1]) and (
                        selected_person_y_axis[0] <= other_person_y_axis[0] <= selected_person_y_axis[1] or
                        selected_person_y_axis[0] <= other_person_y_axis[1] <= selected_person_y_axis[1]):
                    selected_person[4] = 1
                    other_person[4] = 1
        i += 1
    person = 1

    for x, y, w, h, status in people_list:
        #### mesafe range'i start
        t1 = int(x - en)
        t2 = int(y - en)
        t3 = int(x + w + en)
        t4 = int(y + h + en)
        cv2.rectangle(frame, (t1, t2), (t3, t4), (250, 250, 250), 2)
        #### mesafe range'i end
        if status == 1:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 250), 2)
            cv2.putText(frame, f'person {person} Sosyal Mesafeye Uymuyor', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 1)
        else:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f'person {person}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        person += 1

    sosyal_mesafeye_uymayan_sayisi = 0
    for i in people_list:
        if i[4] == 1: sosyal_mesafeye_uymayan_sayisi += 1

    cv2.putText(frame, 'Status : Detecting ', (40, 40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(frame, f'Total Persons : {person - 1}', (40, 70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.putText(frame, f'Sosyal Mesafeye Uymayan Kisi Sayisi : {sosyal_mesafeye_uymayan_sayisi}', (0, 430),
                cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 0), 2)
    cv2.imshow('output', frame)

    return frame


def detectByPathVideo(path):
    video = cv2.VideoCapture(path)
    check, frame = video.read()
    if check == False:
        print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
        return

    print('Detecting people...')
    while video.isOpened():
        check, frame = video.read()

        if check:
            frame = imutils.resize(frame, width=min(800, frame.shape[1]))
            frame = detect(frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        else:
            break
    video.release()
    cv2.destroyAllWindows()


path = "test.mp4"
HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

detectByPathVideo(path)




























