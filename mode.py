import utils
import file
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords # Import the stop word list
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
stops = set(stopwords.words("english"))

org_train_filename = './dataset/train_en.json'
train_data = file.load_file(org_train_filename)

org_test_filename = './dataset/test_en.json'
test_data = file.load_file(org_test_filename)


def train_data_process(train_data):
    """
    将传入的list转化为词袋模型
    :param train_data: list
    :return:
    """
    for i in range(len(train_data)):
        train_data[i]['content'] = utils.gettext(train_data[i]['content'])
        utils.text_process(train_data[i]['content'])
        train_data[i]['content'] = utils.getwords(train_data[i]['content'])
        train_data[i]['content'] = [w for w in train_data[i]['content'] if not w in stops]
        train_data[i]['content'] = ' '.join(train_data[i]['content'])
    return train_data
def test_data_process(test_data):
    """

    :param test_data:
    :return:
    """
    for i in range(len(test_data)):
        test_data[i]['content'] = utils.gettext(test_data[i]['content'])
        utils.text_process(test_data[i]['content'])
        test_data[i]['content'] = utils.getwords(test_data[i]['content'])
        test_data[i]['content'] = [w for w in test_data[i]['content'] if not w in stops]
        test_data[i]['content'] = ' '.join(test_data[i]['content'])
    return test_data





def divide_feature(train_data):
    """
    传入经过token——process的数据，将其转化为仅包含content和label的数据
    :param train_data: list
    :return: list
    """
    train_feature = []
    train_label = []
    for i in range(len(train_data)):
        train_feature.append(train_data[i]['content'])
        train_label.append(train_data[i]['label'])
    return train_feature,train_label


##1.数据预处理
train_data = train_data_process(train_data)
clean_train_data, clean_train_label = divide_feature(train_data)





def tokens(x):
    return x.split(' ')

def my_tokenizer(X):
    newlist = []
    for alist in X:
        newlist.append(alist[0].split(' '))
    return newlist
##2.模型训练

vectorizer = CountVectorizer(analyzer = "word",
                             tokenizer = None,
                             preprocessor = None,
                             stop_words = None,
                             max_features = 5000)
#transformer = TfidfVectorizer(tokenizer=tokens ,use_idf=True, smooth_idf=True, sublinear_tf=False,max_features=5000)

train_data_features = vectorizer.fit_transform(clean_train_data)
#transformer.fit(list(train_data_features_before))
#train_data_features = transformer.transform(list(train_data_features_before))

train_data_features = train_data_features.toarray()
test_data = test_data_process(test_data)

clean_test_data = []
for i in range(len(test_data)):
    clean_test_data.append(test_data[i]['content'])

test_data_features = vectorizer.transform(clean_test_data)
#test_data_features = transformer.transform(test_data_features)
test_data_features = test_data_features.toarray()

#train_x,train_y,test_x,test_y = train_test_split(train_data_features,clean_train_label,test_size=0.3,random_state=0)
train_x = train_data_features[:1800]
train_y = clean_train_label[:1800]
test_x = train_data_features[1801:]
test_y = clean_train_label[1801:]
accuracy = []
microf1 = []
macrof1 = []
trees_num = []

print("Training the random forest...")
for i in range(10):
    j=i*8+2
    trees_num.append(j)
# Initialize a Random Forest classifier with 100 trees
    forest = RandomForestClassifier(n_estimators = j)
    forest = forest.fit( train_x, train_y)
    # Use the random forest to make sentiment label predictions
    result = forest.predict(test_x)
    accuracy.append(accuracy_score(result,test_y))
    #microf1.append(f1_score(test_y,result,average='micro'))
    #macrof1.append(f1_score(test_y,result,average='macro'))
    print(accuracy)
    #print(macrof1)
    #print(microf1)

plt.plot(trees_num,accuracy,label='accuracy',color='r')
plt.xlabel('trees_num')
plt.legend()
plt.plot()
plt.show()





# Copy the results to a pandas dataframe with an "id" column and
# a "sentiment" column
#np.savetxt(fname="result.csv", X=result, fmt="%d",delimiter="\n")
#print('result have been saved')
# Use pandas to write the comma-separated output file


