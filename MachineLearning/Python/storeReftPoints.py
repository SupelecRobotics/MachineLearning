import pickle

refPts = [(0,3000),(2000,3000),(2000,1500),(778,2600),(580,2033)]

with open('RefPoints_y.dat','w') as file:

    pickler = pickle.Pickler(file)
    pickle.dump(refPts)
