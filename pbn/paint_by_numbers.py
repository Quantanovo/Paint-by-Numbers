'''

'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import cv2
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from polylabel import polylabel


class PaintByNumbers:
    def __init__(self, img_path, num_of_colors=12):
        self.img_path = img_path
        self.filename = img_path.split("/")[-1].split(".")[0]
        self.extension = img_path.split("/")[-1].split(".")[1]
        self.img_array = img.imread(img_path)
        self.num_of_colors = num_of_colors
        self.height, self.width, self.colors = self.img_array.shape

    def image_preprocessing(self):
        print(self.height, self.width)
        if self.height < 1200 or self.width < 1200:
            self.img_array = cv2.pyrUp(self.img_array)
            self.height, self.width, self.colors = self.img_array.shape
            print(self.height, self.width)
        median_img = cv2.medianBlur(self.img_array, 15)
        self.processed_img = cv2.bilateralFilter(cv2.bilateralFilter(median_img, 30, 30, 30), 60, 30, 30)
        plt.figure(figsize=(30,20))
        plt.imshow(self.processed_img)
        plt.margins(0,0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.savefig(f"./results/{self.filename}_processed.{self.extension}", format=self.extension, edgecolor="black", bbox_inches = 'tight', pad_inches = 0)
        plt.show()
        return self.processed_img

    def quantise_image(self, img_array):
        img_2d = img_array.reshape(self.height*self.width, self.colors)
        cluster_model = KMeans(n_clusters=self.num_of_colors)
        self.labelled_array = cluster_model.fit_predict(img_2d)
        self.color_of_labels = cluster_model.cluster_centers_.round(0).astype(np.uint8)
        self.quantised_img = self.color_of_labels[self.labelled_array].reshape(self.height, self.width, self.colors)
        plt.figure(figsize=(30,20))
        plt.imshow(self.quantised_img)
        plt.margins(0,0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.savefig(f"./results/{self.filename}_quantised.{self.extension}", format=self.extension, edgecolor="black", bbox_inches = 'tight', pad_inches = 0)
        plt.show()
        return self.quantised_img

    def outline_and_label_image(self):
        labels_2d = np.array(self.labelled_array).reshape(self.height, self.width)
        pos_labels_array = np.zeros((self.height*self.width, 3), dtype=int)
        for index, label in np.ndenumerate(labels_2d):
            pos_labels_array[self.width*index[0]+index[1], 0] = index[0]
            pos_labels_array[self.width*index[0]+index[1], 1] = index[1]
            pos_labels_array[self.width*index[0]+index[1], 2] = label
        db_model = DBSCAN(eps=1.415, min_samples=9, metric='euclidean', algorithm='auto')
        db_labels = db_model.fit_predict(pos_labels_array)
        lbl, counts = np.unique(db_labels, return_counts=True)
        lbl_counts = np.asarray((lbl, counts)).T
        db_img = db_labels.reshape(self.height, self.width)
        self.outlined_img = np.zeros(db_img.shape)
        for index, label in np.ndenumerate(db_img):
            count = 0
            for loc, value in np.ndenumerate(db_img[index[0]-1:index[0]+2, index[1]-1:index[1]+2]):
                if value == label:
                    count += 1
                if count < 9:
                    self.outlined_img[index[0], index[1]] = 0.5
                else:
                    self.outlined_img[index[0], index[1]] = 0.0
        self.outlined_img[0, 0] = 1.0

        border_dict = {}
        for key in lbl_counts:
            if key[0] > -1 and key[1] > 60:
                border_dict[key[0]] = []
        for index, label in np.ndenumerate(db_img):
            count = 0
            for loc, value in np.ndenumerate(db_img[index[0]-1:index[0]+2, index[1]-1:index[1]+2]):
                if value == label:
                    count += 1
            if count < 9:
                if label in border_dict.keys():
                    border_dict[label].append([index[0], index[1]])
        print("Complete!")

        poly_dict = {}
        num = 1
        for key in border_dict:
            polygon = []
            # num2 = 1
            while len(polygon) < len(border_dict[key]):
                for count, index in enumerate(border_dict[key]):
                    if len(polygon) == 0:
                        polygon.append(index)
                    elif len(polygon) == 1:
                        distance = ((polygon[-1][0]-index[0])**2 + (polygon[-1][1]-index[1])**2)**0.5
                        if distance == 1:
                            polygon.append(index)
                    else:
                        distance = ((polygon[-1][0]-index[0])**2 + (polygon[-1][1]-index[1])**2)**0.5
                        if distance < 1.02 and index != polygon[-2]:
                            polygon.append(index)
            polygon.append(polygon[0])
            poly_dict[key] = polygon
            print(f"{num}/{len(border_dict)} completed!")
            num += 1
        print("Done!")
        
        plt.figure(figsize=(30,20))
        plt.imshow(self.outlined_img, cmap='binary')
        for key in poly_dict:
            center = polylabel([poly_dict[key]], precision=0.1, with_distance=True)
            if center[1] < 5.0:
                plt.annotate(text=f"{labels_2d[poly_dict[key][0][0], poly_dict[key][0][1]]+1}",
                            xy = (center[0][1], center[0][0]),
                            xytext=(center[0][1]+35, center[0][0]-35),
                            arrowprops=dict(width=0.3, color='black', headwidth=0.5, headlength=0.5, alpha=0.4),
                            horizontalalignment='center',
                            verticalalignment='center',
                            color="black",
                            alpha=0.6,
                            fontsize=5.0,
                            bbox=dict(boxstyle='circle', facecolor='white', edgecolor='black', alpha=0.6))
            else:
                plt.text(x=center[0][1], y=center[0][0], s=f"{labels_2d[poly_dict[key][0][0], poly_dict[key][0][1]]+1}", horizontalalignment='center', verticalalignment='center', color="black", alpha=0.6, fontsize=5.0)
        plt.margins(0,0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.savefig(f"./results/{self.filename}_pbn.{self.extension}", format=self.extension, edgecolor="black", bbox_inches = 'tight', pad_inches = 0)
        plt.show()
        fig, ax = plt.subplots(1, self.num_of_colors ,figsize=(2*self.num_of_colors,2))
        for i in range(1, self.num_of_colors+1):
            ax[i-1].set_facecolor(self.color_of_labels[i-1]/255)
            ax[i-1].set_title(f'{i}')
            ax[i-1].get_xaxis().set_visible(False)
            ax[i-1].get_yaxis().set_visible(False)
        plt.margins(0,0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.savefig(f"./results/{self.filename}_colors.{self.extension}", format=self.extension, edgecolor="black", bbox_inches = 'tight', pad_inches = 0)
        plt.show()
        return self.outlined_img

