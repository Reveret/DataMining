import pickle


def save_data(cluster):
    std_out = "saved_clusters.p"
    pickle.dump(cluster, open(std_out, "wb"))


def load_data():
    std_in = "saved_clusters.p"
    try:
        data = pickle.load(open(std_in, "rb"))
    except Exception as e:
        data = None
    return data