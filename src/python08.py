import pickle
import json

if __name__ == '__main__':
    a = [1, 2, 3, 4]
    a1 = pickle.dumps(a)
    print(a1)
    print(pickle.loads(a1))

    a2 = json.dumps(a)
    print(a2)
    print(json.loads(a2))

    print(json.__doc__)
    print(dir(json))
    print(json.__all__)

