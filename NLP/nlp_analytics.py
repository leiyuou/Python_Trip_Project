#%%
import jieba
import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

os.chdir('/Users/shanyue/Github/CMU-Python/project_deliver/')

ctrip = pd.read_csv("dataset/ctrip_cleaned_data.csv")

#%%
ctrip_spot = []
ctrip_MEL = ctrip[ctrip["city"]=="墨尔本"].place.tolist()
ctrip_SD = ctrip[ctrip["city"]=="悉尼"].place.tolist()
ctrip_BU= ctrip[ctrip["city"]=="布里斯班"].place.tolist()
ctrip_AD= ctrip[ctrip["city"]=="阿德莱德"].place.tolist()
ctrip_KA=ctrip[ctrip["city"]=="堪培拉"].place.tolist()

ctrip_spot.append(ctrip_SD)
ctrip_spot.append(ctrip_MEL)
ctrip_spot.append(ctrip_BU)
ctrip_spot.append(ctrip_AD)
ctrip_spot.append(ctrip_KA)

print(ctrip_spot)

#%%
def cleanse_text(value):
    import re
    if value:
        text = "".join(re.findall(r"[\u4e00-\u9fff]+", value))
        return text if len(text) > 0 else None
    else:
        return None

#%%
def get_word_cloud(spot):
    ctrip_temp = ctrip.loc[ctrip.place == spot]

    ctrip_temp["clean"] = ctrip_temp.comments.apply(lambda t: cleanse_text(t))
    ctrip_comments_clean = ctrip_temp.clean.apply(lambda t: list(jieba.cut(t)))

    stopwords = set([line.strip() for line in open("NLP/cn_stop_words.txt", 'r', encoding='utf-8').readlines()])
    words_cleanse_remove_stopwords = [list(filter(lambda w: w not in stopwords, words)) for words in ctrip_comments_clean]
    word_freq = Counter([w for words in words_cleanse_remove_stopwords for w in words])
    word_freq_df = pd.DataFrame(word_freq.items())
    word_freq_df.columns = ['word', 'count']

    word_freq_df.sort_values('count', ascending=0).head(10)

    top_K = 100
    word_freq_dict = dict(list(
        word_freq_df.sort_values('count', ascending=0).head(top_K).apply(lambda row: (row['word'], row['count']),
                                                                         axis=1)))
    # generate word cloud
    plt.rcParams['figure.figsize'] = (16, 8)
    wc = WordCloud(font_path="NLP/danchunmhxqx.ttf",background_color="white",max_words=2000)
    print(word_freq_dict)
    wc.generate_from_frequencies(word_freq_dict)

    # show word cloud
    plt.imshow(wc)
    plt.axis("off")
    plt.figure(figsize=(16, 8), dpi=1000)
    plt.show()

#%%
def get_five_top_tourism_attraction(city):
    city_df = ctrip[ctrip["city"]==city]
    city_df = city_df.groupby("place")
    city_df = city_df.aggregate(np.mean)
    city_df = city_df.sort_values(by="rating", ascending=False)
    return list(city_df.index)

if __name__ == '__main__':
    five_place_list = get_five_top_tourism_attraction("悉尼")
    for place in five_place_list:
        get_word_cloud(place)