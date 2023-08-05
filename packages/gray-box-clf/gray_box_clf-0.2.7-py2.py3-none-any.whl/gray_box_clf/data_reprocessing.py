import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


class SpectraPrapering:

    def __init__(self, X):
        self.X = X

    def spectra_normalization(self, plot=False):
        df = pd.DataFrame(self.X.T)
        df = df.apply(lambda v: v / ((v ** 2).sum()) ** 0.5)
        df = df.apply(lambda v: v / v.max())
        self.X_norm = df.T.values

        if plot:
            fig, (ax1, ax2) = plt.subplots(2)
            ax1.plot(self.X.T)
            ax1.set_title("Original")
            ax2.plot(self.X_norm.T)
            ax2.set_title("Normalized")
            plt.show()
        return self.X_norm


def sticking_imges(imgs_list, sorting="horizontal", show_out_ph=True, resize_tuple="none", save=False, out_name_end_type="out.tif", out_type="tiff",
                   dpi=600):
    """

    :param imgs_list: list contain the location of the images (list of strings)
    :param sorting: defoalt "horizontal" and can change to "vertical" (string)
    :param show_out_ph:  do you want to see the final image? True or False (boolean)
    :param resize_tuple: new size (tuple)
    :param save: do you want to save the final image? True or False (boolean)
    :param out_name_end_type: the name or location of the final image in order to save (string)
    :param out_type: type of tinal image, defoal is "tiff" (string)
    :param dpi: 300, 600, 1200 (integer)
    :return: sticking images
    """
    numpyes = []
    intinal_sizes = np.zeros((len(imgs_list), 2))
    for im in imgs_list:
        if resize_tuple == "none":
            img = Image.open(im)
        else:
            img = Image.open(im).resize(resize_tuple, Image.ANTIALIAS)

        numpyes.append(np.array(img))

    if sorting == "horizontal":
        im_out = Image.fromarray(np.hstack(tuple(numpyes)))



    elif sorting == "vertical":
        im_out = Image.fromarray(np.vstack(tuple(numpyes)))

    if show_out_ph:
        im_out.show()

    if save:
        if out_type == "tiff":
            im_out.save(out_name_end_type,
                        compression='tiff_lzw',
                        dpi=(dpi, dpi),
                        optimize=True,
                        )
        else:
            im_out.save(out_name_end_type,
                        dpi=(dpi, dpi))


def image_resizing_ratio(init_location, final_location, percent, dpi=300):
    """
    Resize image input image and percent | Keep aspect ratio
    :param init_location:
    :param final_location:
    :param percent:
    :return:
    """
    img = Image.open(init_location)
    w, h = img.size
    img_resized = img.resize((int(float(percent*w)/float(100)),int(float(percent*h)/float(100))))
    img_resized.show()
    img_resized.save(final_location, dpi=(dpi, dpi))


def references_comparing_for_papers_edit(text_file_location):
    """
    This function checking if there are duplicate references in papers.
    Copy the refernces from the paper "with the numbers" and paste it in Notepad text file
    then write in a new first row the word "title".
    :param text_file_location:  Notepad text file location
    :return: report (pandas df)
    """
    df = pd.read_fwf(text_file_location).drop("Unnamed: 1", axis=1)
    X = df["title"].values.astype(str)
    df_ = pd.DataFrame(X, columns=["ref"])
    string_list = list(df_["ref"].apply(lambda _: _[_.find("\t") + 1:]))
    vectroized = CountVectorizer().fit_transform(string_list)
    vectors = vectroized.toarray()
    csim = cosine_similarity(vectors)
    similarity = np.around(csim[(csim > .70) & (csim < .95)] * 100, 0).astype(int)
    similarity = similarity[: int(0.5 * len(similarity))]
    v = np.argwhere((csim > .70) & (csim < .95))
    v = v[: int(0.5 * len(v))]
    df_out = pd.DataFrame()
    df_out["references_1_num"] = (v[:, 0] + 1)
    df_out["references_2_num"] = (v[:, 1] + 1)
    df_out["reference_text_1"] = df_out["references_1_num"].apply(lambda _: string_list[_ - 1])
    df_out["reference_text_2"] = df_out["references_2_num"].apply(lambda _: string_list[_ - 1])
    df_out["similarity %"] = similarity

    return df_out