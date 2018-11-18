# -*- coding: utf-8 -*-
"""Image_classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iuwi5Zge2myS2trKpnps85SKxj3JKj8L
"""

import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.optim as optim
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_val_score, GridSearchCV
import pickle
import sklearn
from __future__ import print_function
# %matplotlib inline

print('The scikit-learn version is {}.'.format(sklearn.__version__))
print('The PyTorch version is {}.'.format(torch.__version__))
print('The NumPy version is {}.'.format(np.__version__))
print('The Matplotlib version is {}.'.format(mpl.__version__))

transform = transforms.Compose(
             [transforms.ToTensor(), 
              transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

# load training dataset
trainset = torchvision.datasets.ImageFolder(root='./tr', transform=transform)

trainloader = torch.utils.data.DataLoader(trainset, batch_size=5,
                                          shuffle=True, num_workers=2)

# load testing dataset
testset = torchvision.datasets.ImageFolder(root='./ts', transform=transform)

testloader = torch.utils.data.DataLoader(testset, batch_size=5,
                                         shuffle=False, num_workers=2)

!ls

classes = ('00', '01', '02', '03',
           '04', '05', '06', '07', '08', '09')

def plot_images(img):
    img = img / 2 + 0.5  # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)), interpolation='nearest')

# get some random training images
dataiter = iter(trainloader)
images, labels = dataiter.next()

# Plot images
plot_images(torchvision.utils.make_grid(images, nrow=5, padding=1))


# print labels
print(' '.join('%8s' % classes[labels[j]] for j in range(5)))

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

net = Net()
print(net)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

def training(num_iterations):
    for epoch in range(num_iterations): # loop over the dataset multiple times
        print('Training: Epoch - (%d)'%(epoch))
        running_loss = 0.0
        
        for i, data in enumerate(trainloader, 0):
            # Get the inputs
            inputs, labels = data
            
            # wrap them in Variable
       #     inputs, labels = Variable(inputs), Variable(labels)
            
            # zero the parameter gradients
            optimizer.zero_grad()
            
            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            
            # Print statistics
            #running_loss += loss.data[0]
            running_loss += loss.item()
            
            if i % 2000 == 1999: # print every 2000 mini-batches
                print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
                
                running_loss = 0.0
                
    print('Finished Training')

training(num_iterations=5)

# plot some images from the test dataset
dataiter = iter(trainloader)
images, labels = dataiter.next()

# plot images
plot_images(torchvision.utils.make_grid(images,nrow=5, padding=1))

print('GroundTruth: \n', ' '.join('%8s' % classes[labels[j]] for j in range(5)))

# predict class labels for test images
#outputs = net(Variable(images))
outputs = net(images)

#_, predicted = torch.max(outputs.data, 1)
_, predicted = torch.max(outputs, 1)

print('Predicted: \n', ' '.join('%8s' % classes[predicted[j]]
                              for j in range(5)))

correct = 0
total = 0
for data in trainloader:
    images, labels = data
    outputs = net(Variable(images))
    _, predicted = torch.max(outputs.data, 1)
    total += labels.size(0)
    correct += (predicted == labels).sum()
print('Accuracy of the network: %d %%' % (
    100 * correct / total))



import csv


with open('prediction.csv', 'w') as csvfile:
    fieldnames = ['filename', 'classid']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for
        writer.writerow({' filename': 'i', 'classid': 'Beans'})

