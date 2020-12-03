# iris k-means clustering!
# clustering on sepal width and sepal length
import pandas as pd
import matplotlib.pyplot as plt
import random
import math

class main:
    def __init__(self):
        self.epochs = 10
        self.clusters = 3

        self.indexes = {'Iris-setosa':0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
        self.colors = {0: 'ro', 1: 'bo', 2: 'go'}
        self.labels = {0: 'Iris-setosa', 1: 'Iris-versicolor', 2: 'Iris-virginica'}
        self.centroid_colors = {0: 'rx', 1: 'bx', 2: 'gx'}
        data = self.load_data()
        data = self.split_data(data)
        #self.analyse_data(data)  #IF YOU WANNA SEE THE DATA
        centroids = self.init_centroids(data)
        centroids = self.train(data, centroids)
        #self.analyse_clusters(data, centroids)
        centroids = self.rearrange_centroids(data, centroids)
        self.show_clusters(data, centroids)

    def train(self, data, centroids):
        print 'Epoch %s had error of %.3f.' % (0, self.cost(data, centroids))
        #self.analyse_clusters(data, centroids)

        for epoch in range(self.epochs):
            klasses = [[] for x in range(self.clusters)]
            # here we put all the data into their cluster bins
            for tupl in data:
                klasses[self.klass(tupl, centroids)].append(tupl)

            new_centroids = []
            for klass in klasses:
                centroid_newX, centroid_newY = 0, 0
                for tupl in klass:
                    centroid_newX += tupl[0]
                    centroid_newY += tupl[1]
                new_centroids.append([centroid_newX / len(klass), centroid_newY / len(klass)])
            centroids = new_centroids
            print 'Epoch %s had error of %.3f.' % (epoch, self.cost(data, centroids))
        #self.analyse_clusters(data, centroids)
        return centroids

    def klass(self, tupl, centroids):
        distances = [self.distance(tupl, centroid) for centroid in centroids]
        return distances.index(min(distances))

    def cost(self, data, centroids):
        # we are using squared distance!
        return sum([min([self.distance(tupl, centroid)**2 for centroid in centroids]) for tupl in data])

    def distance(self, tupl, centroid):
        return math.sqrt((tupl[0]-centroid[0])**2 + (tupl[1]-centroid[1])**2)

    def init_centroids(self, data):
        return [[data[x][0], data[x][1]] for x in random.sample(range(0, len(data)), self.clusters)]

    def split_data(self, data):
        return [[tupl[0], tupl[1], self.indexes[tupl[4]]] for tupl in data]

    def rearrange_centroids(self, data, centroids):
        bins = [[0]*3 for x in range(3)]
        rearranged_centroids = [0]*3
        for tupl in data:
            distances = [self.distance(tupl, centroid) for centroid in centroids]
            binn = distances.index(min(distances))
            bins[binn][tupl[2]] += 1
        for i in range(3):
            binn = bins[i]
            rearranged_centroids[binn.index(max(binn))] = centroids[i]
        return rearranged_centroids

    def show_clusters(self, data, centroids):
        for tupl in data:
            distances = [self.distance(tupl, centroid) for centroid in centroids]
            klass = distances.index(min(distances))
            plt.plot(tupl[0], tupl[1], self.colors[klass], markersize = 3)
        for centroid in centroids:
            plt.plot(centroid[0], centroid[1], self.centroid_colors[centroids.index(centroid)], markersize = 12)
        plt.xlabel('Sepal Width')
        plt.ylabel('Sepal Length')
        plt.show()

    def analyse_clusters(self, data, centroids):
        for tupl in data:
            plt.plot(tupl[0], tupl[1], self.colors[tupl[2]], markersize = 3)
        for centroid in centroids:
            plt.plot(centroid[0], centroid[1], 'kx',markersize = 12)
        #plt.title('Iris Sepal Width vs Length')
        plt.xlabel('Sepal Width')
        plt.ylabel('Sepal Length')
        plt.show()

    def analyse_data(self, data):
        first = [True]*3
        for tupl in data:
            if first[tupl[2]]:
                plt.plot(tupl[0], tupl[1], self.colors[tupl[2]], markersize = 3, label = self.labels[tupl[2]])
                first[tupl[2]] = False
            else:
                plt.plot(tupl[0], tupl[1], self.colors[tupl[2]], markersize = 3)
        plt.title('Iris Sepal Width vs Length')
        plt.xlabel('Sepal Width')
        plt.ylabel('Sepal Length')
        plt.legend()
        plt.show()

    def load_data(self):
        return pd.read_csv("irisdata.txt").values

runProgram = main()