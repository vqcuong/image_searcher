import os
import time
import torch
import numpy as np
from PIL import Image
from torchvision import models
from torchvision import transforms
from sklearn.metrics.pairwise import cosine_similarity


class DirectedImagePool():
    FEATURE_FILE = ".feature.npy"
    IMG_FEATURES = None
    IMG_FILES = None

    def __init__(self, image_folder: str, feature_file: str = None) -> None:
        self.transform = transforms.Compose([      #[1]
            transforms.Resize(256),                    #[2]
            transforms.CenterCrop(224),                #[3]
            transforms.ToTensor(),                     #[4]
            transforms.Normalize(                      #[5]
            mean=[0.485, 0.456, 0.406],                #[6]
            std=[0.229, 0.224, 0.225]                  #[7]
        )])
        model = models.resnet50(pretrained=True)
        self.model_extract = torch.nn.Sequential(*(list(model.children())[:-1]))
        self.model_extract.eval()
        self.initialize_pool(image_folder, feature_file)

    def initialize_pool(self, image_folder: str, feature_file: str):
        self.IMAGE_FOLDER = image_folder
        if feature_file is None:
            self.FEATURE_FILE = os.path.join(self.IMAGE_FOLDER, ".feature.npy")
        else:
            self.FEATURE_FILE = feature_file

        if os.path.exists(self.IMAGE_FOLDER):
            if os.path.exists(self.FEATURE_FILE):
                try:
                    features = np.load(self.FEATURE_FILE)
                    self.IMG_FEATURES = features[:,:-1].astype(np.float64)
                    self.IMG_FILES = features[:,-1]
                    print(f"Loaded existed feature file: {self.FEATURE_FILE}")
                except:
                    raise Exception(f"Unable load {self.FEATURE_FILE}")
            else:
                print(f"Not found {self.FEATURE_FILE}. Initilizing pool")
                img_files = os.listdir(self.IMAGE_FOLDER)
                for img_file in img_files:
                    self.add_image(os.path.join(self.IMAGE_FOLDER, img_file))
                    print(f"Added image: {img_file}")
                print("Initialized pool")
                self.cache()
                print("Cached feature")
        else:
            print(f"Folder {self.IMAGE_FOLDER} doesn't existed. Mask as unavailable pool")

    def add_image(self, img_file: str):
        img = Image.open(img_file)
        img_feature = self.extract(img)
        self.IMG_FEATURES = img_feature if self.IMG_FEATURES is None \
            else np.concatenate([self.IMG_FEATURES, img_feature], axis=0)
        self.IMG_FILES = np.array([img_file], dtype=str) if self.IMG_FILES is None \
            else np.concatenate([self.IMG_FILES, np.array([img_file], dtype=str)], axis=0)

    def remove_image(self, img_file: str):
        found_index = np.where(self.IMG_FILES == img_file)
        self.IMG_FEATURES = np.delete(self.IMG_FEATURES, found_index)
        self.IMG_FILES = np.delete(self.IMG_FILES, found_index)

    def search_image(self, img_file: str, threshold: float = 0.95):
        img = Image.open(img_file)
        img_feature = self.extract(img).reshape((2048,))
        scores = cosine_similarity([img_feature], self.IMG_FEATURES)[0]
        found_indexs = np.where(scores >= threshold)[0].tolist()
        result = {}
        for i in found_indexs:
            result[self._get_image(i)] = scores[i]
        return result

    def _get_image(self, index):
        return self.IMG_FILES[index]

    def extract(self, img):
        img_t = self.transform(img)
        batch_t = torch.unsqueeze(img_t, 0)
        out = self.model_extract(batch_t)
        result = out.detach().cpu().numpy()
        result = np.reshape(result, (1, 2048))
        return result

    def cache(self):
        dumpy = np.concatenate([self.IMG_FEATURES, self.IMG_FILES.reshape((-1, 1))], axis=1)
        np.save(self.FEATURE_FILE, dumpy)

if __name__ == '__main__':
    start_time = time.time()
    pool = DirectedImagePool(image_folder="D:\\abc")

    load_time = time.time()
    print(f"Load {load_time - start_time}")
    res = pool.search_image("../img.jpg")
    print(res)
    print(f"Tooks {time.time() - load_time}")
