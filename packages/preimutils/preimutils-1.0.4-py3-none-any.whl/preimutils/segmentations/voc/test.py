from count import export_path_count_for_each_label
from augment import SegmentationAug
import cv2
import numpy as np
from dataset_info import Dataset,LabelMap
import utils 

ut
if __name__ == "__main__":
    PATH = '/home/amir/segmentation/hazmat/hazmat-dataset/VOC2012'
    PATH_N = '/home/amir/segmentation/hazmat/hazmat-dataset/amir'
    dataset = Dataset(PATH)
    label_handler = LabelMap(PATH + '/labelmap.txt')
    dataset.seprate_dataset(shuffle=True)   # a = export_path_count_for_each_label(label_handler.color_label(),dataset.images_dir,dataset.mask_dir)
    utils.custom_to_voc(dataset.masks_dir,dataset.images_dir,PATH_N)
    # seg_aug = SegmentationAug(PATH + '/labelmap.txt',dataset.mask_dir,dataset.images_dir)
    # seg_aug.auto_augmentation(1000)
    # seg_aug.encode_mask_dataset(label_handler.color_list())

    # img = cv2.imread('/home/amir/segmentation/hazmat/hazmat-dataset/VOC2012/SegmentationClass/pre_encoded/image_1058.png',0)
