from collections import deque
import numpy as np
import cv2
import time
import math

ORANGE_MIN = np.array([0, 50, 50],np.uint8)
ORANGE_MAX = np.array([8, 255, 255],np.uint8)
RED_MIN = np.array([172, 50, 50],np.uint8)
RED_MAX = np.array([180, 255, 210],np.uint8)
GREEN_MIN = np.array([50, 50, 50],np.uint8)
GREEN_MAX = np.array([70, 255, 255],np.uint8)
PINK_MIN = np.array([160, 50, 50],np.uint8)
PINK_MAX = np.array([170, 255, 255],np.uint8)


class CarTracker:
    perspective_transform = None
    def __init__(self):
        self.car_ROIs = []
        self.car_ROI_hists = []
        self.car_orientations = []
        self.lock_on_timer = None
        self.termination_criteria = None

        self.oldAngles = []
        self.oldHemispheres = []

        self.car_pts = []

    def add_to_ROI_list(self, rect):
        thresh = 30
        in_list = False

        for existing in self.car_ROIs:
            if abs(existing[0] - rect[0]) < thresh and abs(existing[1] - rect[1]) < thresh:
                in_list = True
        if not in_list:
            self.car_ROIs.append(rect)
            self.lock_on_timer = time.time()
            print(len(self.car_ROIs))

    def lock_on(self, image):
        num_cars_found = None
        if self.lock_on_timer is not None:
            elapsed_time = time.time() - self.lock_on_timer
            if elapsed_time > 10: # Count down 5 seconds after last cell identified.
                num_cars_found = len(self.car_ROIs)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 13, 2)

        filtered = cv2.medianBlur(thresh, 3)

        h, w = image.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)
        floodfill = filtered.copy()
        cv2.floodFill(floodfill, mask, (int(h/2),int(w/2)), 255)
        inv_floodfill = cv2.bitwise_not(floodfill)


        _, cnts, _ = cv2.findContours(inv_floodfill, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:#
            perimeter = cv2.arcLength(c, True)
            poly = cv2.approxPolyDP(c, 0.02*perimeter, True)
            if len(poly) == 4:
                x, y, w, h = cv2.boundingRect(poly)
                area = w*h
                aspectRatio = w / float(h)
                if aspectRatio < 0.3 or aspectRatio > 0.7 or area < 2000 or area > 4000:
                    continue
                cv2.drawContours(image, [poly], 0, (255, 0, 0), 3)

                self.add_to_ROI_list([int(x+w/4),int(y+h/4),int(w/2),int(h/2)]) # TEMP


        cv2.namedWindow("id")
        cv2.moveWindow("id", 100,100)
        cv2.imshow("id", image)
        cv2.waitKey(1)

        #cv2.imshow("1", image)
        #if cv2.waitKey(1) & 0xFF == 'q':
        #    quit()

        return num_cars_found


    def track_cars(self, image):
        if self.termination_criteria is None:
            self.camshift_setup(image)
        self.camshift_track(image)

        car_locations = []
        index = 0
        for x, y, w, h in self.car_ROIs:
            center = (x+int(w/2), y+int(h/2))

            angle = self.car_orientations[index]

            # Apply the perspective transform to the point.
            point = np.matrix([center[0], center[1], 1]).T
            hPoint = np.dot(self.perspective_transform, point)
            x = int(hPoint[0])
            y = int(hPoint[1])
            if x < 0 or y < 0:
                worldPosition = (None, None)
            else:
                worldPosition = (x, y)

            dict = {"ID": index, "position": worldPosition, "orientation": angle}
            car_locations.append(dict)
            index += 1

        return car_locations

    def camshift_setup(self, image):
        # Set up ROIs for tracking.
        for x, y, w, h in self.car_ROIs:
            roi = image[y:y+h, x:x+w]
            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
            roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0,180])
            cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

            self.car_ROI_hists.append(roi_hist)
            self.car_orientations.append(0)
            self.oldAngles.append(0)
            self.oldHemispheres.append(1)
            self.car_pts.append(deque(maxlen=64))
        self.termination_criteria = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

    def camshift_track(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # CAMSHIFT track.
        for i in range(len(self.car_ROIs)):
            dst = cv2.calcBackProject([hsv], [0], self.car_ROI_hists[i], [0, 180], 1)
            ret, self.car_ROIs[i] = cv2.CamShift(dst, tuple(self.car_ROIs[i]), self.termination_criteria)

            angle = ret[2]
            oldAngle = self.oldAngles[i]
            oldHemisphere = self.oldHemispheres[i]
            if abs(angle - oldAngle) > 150:
                hemisphere = oldHemisphere * -1
            else:
                hemisphere = oldHemisphere
            self.oldAngles[i] = angle
            self.oldHemispheres[i] = hemisphere

            if hemisphere == -1:
                orientation = int(angle + 180)
            else:
                orientation = int(angle)

            orientation -= 90
            if orientation < 0:
                orientation += 360

            self.car_orientations[i] = orientation

            x, y, w, h = self.car_ROIs[i]
            center = (x+int(w/2), y+int(h/2))

            cv2.line(image, center, (int(center[0] + 20*math.cos(math.radians(orientation))),
                                     int(center[1] + 20*math.sin(math.radians(orientation)))), (255,255,0), 3)

            pts = cv2.boxPoints(ret)
            pts = np.int0(pts)
            cv2.polylines(image, [pts], True, 255, 2)

            self.car_pts[i].appendleft(center)

        for pts in self.car_pts:
            for i in range(1, len(pts)):
                # if either of the tracked points are None, ignore
                # them
                if pts[i - 1] is None or pts[i] is None:
                    continue

                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(64 / float(i + 1)) * 2)
                cv2.line(image, pts[i - 1], pts[i], (200, 200, 0), thickness)

        cv2.namedWindow("id")
        cv2.moveWindow("id", 100,100)
        cv2.imshow("id", image)
        if cv2.waitKey(1) & 0xFF == 'q':
            quit()


def OLD_orientation_finding(image):
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        orange = cv2.inRange(hsv_img, ORANGE_MIN, ORANGE_MAX)
        red = cv2.inRange(hsv_img, RED_MIN, RED_MAX)
        green = cv2.inRange(hsv_img, GREEN_MIN, GREEN_MAX)
        pink = cv2.inRange(hsv_img, PINK_MIN, PINK_MAX)

        kernel = np.ones((5, 5), np.uint8)
        orange_closed = cv2.morphologyEx(orange, cv2.MORPH_CLOSE, kernel)
        red_closed = cv2.morphologyEx(red, cv2.MORPH_CLOSE, kernel)
        green_closed = cv2.morphologyEx(green, cv2.MORPH_CLOSE, kernel)
        pink_closed = cv2.morphologyEx(pink, cv2.MORPH_CLOSE, kernel)

        _, orange_contours, _ = cv2.findContours(orange_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        _, red_contours, _ = cv2.findContours(red_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        _, green_contours, _ = cv2.findContours(green_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        _, pink_contours, _ = cv2.findContours(pink_closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        infoList = [#(orange_closed, orange_contours, (0, 136, 255)),
                    #(red_closed, red_contours, (0, 0, 255)),
                    (green_closed, green_contours, (0, 255, 0)),
                    (pink_closed, pink_contours, (144, 0, 255))]
        for closed, contours, colour in infoList:
            if len(contours) > 0:
                # TODO: We know how big the cars should be - use this knowledge to filter bad boxes.
                c = max(contours, key=cv2.contourArea)

                boundingBox = cv2.boundingRect(c)
                x, y, w, h = boundingBox
                if w*h < 50: # Contour too small to be significant.
                    continue
                #cv2.rectangle(frame, (x, y), (x + w, y + h), colour, 4)
                center = (int(x + w/2), int(y + h/2))
                cv2.circle(image, center, 5, colour, -1)

                orientedRect = cv2.minAreaRect(c)
                box = np.int0(cv2.boxPoints(orientedRect))
                #cv2.drawContours(frame, [box], 0, colour, 2)

                angle = math.radians(orientedRect[2])

                x = orientedRect[0][0]
                y = orientedRect[0][1]
                w = orientedRect[1][0]
                h = orientedRect[1][1]
                a = orientedRect[2]

                if w > h:
                    half1 = ( (x - w/8 + (w/8)*math.sin(-angle), y + (h/4)*math.sin(-angle)), (w/4, h), a )
                    half2 = ( (x + w/8 + (w/8)*math.sin(angle), y + (h/4)*math.sin(angle)), (w/4, h), a)
                else:
                    half1 = ((x - (w/4)*math.sin(-angle), y - h/8 + (h/8)*math.sin(-angle)), (w, h/4), a)
                    half2 = ((x - (w/4)*math.sin(angle), y + h/8 + (h/8)*math.sin(angle)), (w, h/4), a)

                box1 = np.int0(cv2.boxPoints(half1))
                box2 = np.int0(cv2.boxPoints(half2))
                cv2.drawContours(image, [box1], 0, colour, 2)
                cv2.drawContours(image, [box2], 0, colour, 2)

                height, width, _ = image.shape
                mask1 = np.zeros((height, width, 1), np.uint8)
                mask2 = np.zeros((height, width, 1), np.uint8)
                cv2.fillConvexPoly(mask1, box1, 255)
                cv2.fillConvexPoly(mask2, box2, 255)
                first = cv2.bitwise_and(closed, closed, mask=mask1)
                second = cv2.bitwise_and(closed, closed, mask=mask2)

                firstCount = cv2.countNonZero(first)
                secondCount = cv2.countNonZero(second)

                if firstCount < secondCount:
                    car_front = (int(half1[0][0]),int(half1[0][1]))
                    car_back = (int(half2[0][0]),int(half2[0][1]))
                else:
                    car_front = (int(half2[0][0]),int(half2[0][1]))
                    car_back = (int(half1[0][0]),int(half1[0][1]))

                fx = car_front[1]
                fy = car_front[0]
                bx = car_back[1]
                by = car_back[0]

                if fx>bx and fy==by:
                    car_angle = 0
                elif fx>bx and fy>by:
                    car_angle = -a
                elif fx==bx and fy>by:
                    car_angle = 90
                elif fx<bx and fy>by:
                    car_angle = 90 + -a
                elif fx<bx and fy==by:
                    car_angle = 180
                elif fx<bx and fy<by:
                    car_angle = 180 + -a
                elif fx==bx and fy<by:
                    car_angle = 270
                elif fx>bx and fy<by:
                    car_angle = 270 + -a

                cv2.circle(image, car_front, 5, (255, 255, 255), -1)
                linePoint = (int(car_front[0] + 80*math.sin(math.radians(car_angle))), int(car_front[1] + 80*math.cos(math.radians(car_angle))))
                cv2.line(image, car_front, linePoint, colour, 3)

        cv2.imshow("", image)
        cv2.waitKey(1)

