import os
import shutil

import numpy as np
import xml.etree.ElementTree as ET

import cv2
from PIL import Image
import base64
from io import BytesIO

OVERLAPPING_CRITERIA = {
    "left": 30,
    "right": 30
}


class OverlappingDetector:
    @classmethod
    def text_positions(cls, image, std_level=0, cut_pixels=0, return_gap=False):
        im_arr = np.array(image)[cut_pixels:-cut_pixels - 1, :, 0]  # cut pixels from top and bottom text

        avg = np.mean(im_arr)
        s_d = np.std(im_arr)
        im_bin = np.int8(np.where(avg + s_d * std_level > im_arr, 0, 1))  # binarization

        sum_bins_width = np.array([np.sum(item) for item in im_bin.T])
        invert = False
        if max(sum_bins_width) >= .95 * im_bin.shape[0]:
            sum_bins_width = -1 * (sum_bins_width - max(sum_bins_width))
            invert = True

        sum_bins_width_idx = sum_bins_width.nonzero()[0]
        gaps = np.array(
            [sum_bins_width_idx[i] - sum_bins_width_idx[i - 1] for i in range(1, len(sum_bins_width_idx))]) - 1
        right_decor_gap = gaps.nonzero()[0][0]
        right_gap = gaps[gaps.nonzero()[0][0]]
        left_decor_gap = gaps.nonzero()[0][-1]
        left_gap = gaps[gaps.nonzero()[0][-1]]

        sum_bins_height = np.array([np.sum(item) for item in im_bin[:, right_decor_gap:-right_decor_gap - 1]])
        if invert:
            sum_bins_height = -1 * (sum_bins_height - max(sum_bins_height))

        sum_bins_height_idx = sum_bins_height.nonzero()[0]
        if return_gap:
            return left_gap, right_gap

        return (sum_bins_height_idx[1] + cut_pixels, right_decor_gap + right_gap), \
               (sum_bins_height_idx[-1] + cut_pixels, im_bin.shape[1] - left_gap - right_decor_gap)

    @classmethod
    def distances_to_left_and_rigth(cls, image, std_level=0, cut_pixels=0):
        (con_1, con_2) = cls.text_positions(image, std_level=std_level, cut_pixels=cut_pixels)
        total_length = np.array(image)[cut_pixels:-cut_pixels, :, 0].shape[1]
        left_distance = con_1[0]
        right_distance = total_length  # - con_2[0]
        return left_distance, right_distance


class Screenshoot:

    def __init__(self, driver):
        self._driver = driver
        self._screenshot = None
        self._page_source = None
        if os.path.exists('screens'):
            shutil.rmtree('screens')
        os.mkdir('screens')

    def process_elements(self, elements):

        processed_elements = []

        for el in elements:
            if {'x', 'y', 'width', 'height'}.difference(set(el.keys())):
                continue
            x = int(el['x'])
            y = int(el['y'])
            width = int(el['width'])
            height = int(el['height'])

            element = self.get_element_from_image(x, y, width, height)
            if element is not None:
                processed_elements.append(element)
        return processed_elements

    def get_element_from_image(self, x, y, w, h):

        screen_size = self._driver.get_window_size()
        screen_width, screen_height = screen_size['width'], screen_size['height']

        width, height = tuple(self.screenshot.shape[1::-1])
        x_mult = width / screen_width
        y_mult = height / screen_height

        x, w = map(lambda i: int(i * x_mult), (x, w))
        y, h = map(lambda i: int(i * y_mult), (y, h))

        if (y + h) > height:
            return None

        element = self.screenshot[y:y + h, x:x + w]
        return element

    def _process_image(self, base64_image):

        img = Image.open(BytesIO(base64.b64decode(base64_image)))

        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    @property
    def screenshot(self):
        if self._screenshot is None:
            self._screenshot = self._process_image(self._driver.get_screenshot_as_base64())
        return self._screenshot

    @property
    def page_source(self):
        if self._page_source is None:
            self._page_source = self._driver.page_source

        return self._page_source

    def save_image(self, image, file_name):
        cv2.imwrite(file_name, image)

    def find_elements(self, selector):
        root = ET.fromstring(self.page_source)
        elements = list(map(lambda x: x.attrib, root.findall(selector)))

        return self.process_elements(elements)

    def check_overlapping(self, el):
        if not isinstance(el, list):
            el = [el]

        overlapped_text = []
        for idx, e in enumerate(el):
            self.save_image(e, f'screens/{idx}.jpg')
            el = Image.open(f'screens/{idx}.jpg').convert('LA')
            right_position, left_position = OverlappingDetector.text_positions(el, return_gap=True)

            if left_position > OVERLAPPING_CRITERIA['left'] and right_position > OVERLAPPING_CRITERIA['right']:
                continue

            overlapped_text.append((idx, 'Text is overlapped'))

        return overlapped_text
