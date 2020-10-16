import os
import pickle
import torch
import numpy as np
from sklearn.metrics import classification_report
from model.GCN import GCN

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def load_dataset(task):
    X_train_tid, X_train, y_train, word_embeddings, adj = pickle.load(open("dataset/"+task+"/train.pkl", 'rb'))
    X_dev_tid, X_dev, y_dev = pickle.load(open("dataset/"+task+"/dev.pkl", 'rb'))
    X_test_tid, X_test, y_test = pickle.load(open("dataset/"+task+"/test.pkl", 'rb'))
    config['embedding_weights'] = word_embeddings
    print("#nodes: ", adj.shape[0])
    #print("id：",X_test_tid[0])
    print("test：", len(X_test[0]))
    return X_train_tid, X_train, y_train, \
           X_dev_tid, X_dev, y_dev, \
           X_test_tid, X_test, y_test, adj


def train_and_test(model, task):
    model_suffix = model.__name__.lower().strip("text")
    config['save_path'] = 'checkpoint/weights.best.' + task + "." + model_suffix

    X_train_tid, X_train, y_train, \
    X_dev_tid, X_dev, y_dev, \
    X_test_tid, X_test, y_test, adj = load_dataset(task)

    nn = model(config, adj)
    # nn.fit(X_train_tid, X_train, y_train,
    #        X_dev_tid, X_dev, y_dev)

    print("================================")
    nn.load_state_dict(torch.load(config['save_path']))

    y_pred = nn.predict(X_test_tid, X_test)
    print(classification_report(y_test, y_pred, target_names=config['target_names'], digits=3))


config = {
    'reg':0,
    'batch_size':64,
    'nb_filters':100,
    'kernel_sizes':[3, 4, 5],
    'dropout':0.5,
    'maxlen':50,
    'epochs':20,
    'num_classes':4,
    'target_names':['NR', 'FR', 'UR', 'TR']
}


if __name__ == '__main__':

    task = 'weibo'
    print("task: ", task)

    if task == 'weibo':
        config['num_classes'] = 2
        config['target_names'] = ['NR', 'FR']

    model = GCN
    train_and_test(model,task)
    #load_dataset(task)
