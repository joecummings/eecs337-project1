import pickle

with open('actors.pickle', 'rb') as handle:
    unserialized_data = pickle.load(handle)

print(unserialized_data)