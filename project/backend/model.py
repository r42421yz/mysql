import numpy as np;
import scipy.special;
import scipy.misc;
import scipy.ndimage;
import matplotlib.pyplot as plt;
import numpy as py;

# neural network 
class neuralNetwork:

    # initialize the neural network
    def __init__(self, inputNodes, hiddenNodes, outputNodes, learningRate):
        
        # set number of nodes
        self.iNodes = inputNodes
        self.hNodes = hiddenNodes
        self.oNodes = outputNodes
        
        # set learning rate
        self.lr = learningRate
        
        # set weights
        # self.wih = (np.random.rand(self.hNodes, self.iNodes) - 0.5)
        self.wih = np.random.normal(0.0, pow(self.iNodes, -0.5),(self.hNodes, self.iNodes))
        # self.who = (np.random.rand(self.oNodes, self.hNodes) - 0.5)
        self.who = np.random.normal(0.0, pow(self.hNodes, -0.5),(self.oNodes, self.hNodes))

        # activation function
        self.activation_function = lambda x: scipy.special.expit(x)

        pass
    
    # train the neural network
    def train(self, inputs_list, targets_list):
        # convert inputs into 2d array
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)

        # calculate error
        output_errors = targets - final_outputs
        hidden_errors = np.dot(self.who.T, output_errors)
        
        # update the weights
        self.who += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), np.transpose(hidden_outputs))
        self.wih += self.lr * np.dot((hidden_errors * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))
        pass
    
    # query the neural network
    def query(self, inputs_list):
        # convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T

        hidden_inputs = np.dot(self.wih, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = np.dot(self.who, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
    
        return final_outputs
    
    def fit(self, training_data_list, epochs=1, augment=False):
        for e in range(epochs):
            for record in training_data_list:
                all_values = record.split(',')
                # scale inputs to range 0.01 to 1.00
                inputs = (np.asarray(all_values[1:], dtype=float)/255.0 * 0.99) + 0.01
                # target output values: all 0.01, desired label 0.99
                targets = np.zeros(output_nodes) + 0.01
                targets[int(all_values[0])] = 0.99
                self.train(inputs, targets)

                if augment:
                    # anticlockwise
                    inputs_plus10_img = scipy.ndimage.rotate(inputs.reshape(28,28),10,cval=0.01, order = 1, reshape=False)
                    self.train(inputs_plus10_img.reshape(784),targets)
                    # clockwise
                    inputs_plus10_img = scipy.ndimage.rotate(inputs.reshape(28,28),-10,cval=0.01, order = 1, reshape=False)
                    self.train(inputs_plus10_img.reshape(784),targets)
    
    def evaluate(self, test_data_list):
        scorecard = []
        for record in test_data_list:
            all_values = record.split(',')
            correct_label = int(all_values[0])
            inputs = (np.asarray(all_values[1:], dtype=float)/255.0 * 0.99) + 0.01
            outputs = n.query(inputs)
            label = np.argmax(outputs)
            if(label == correct_label):
                scorecard.append(1)
            else:
                scorecard.append(0)
        scorecard_array = np.asarray(scorecard)
        return (scorecard_array.sum() / scorecard_array.size)

    @staticmethod
    def _sigmoid(x):
        return 1.0/ (1.0 + np.exp(-x))
    
    def save(self, path = 'model_weights.npz'):
        np.savez(path, wih = self.wih, who=self.who)
    
    def load(self, path = "model_weights.npz"):
        data = np.load(path)
        self.wih = data['wih']
        self.who = data['who']


    
if __name__ == "__main__":
    # inputs_nodes = 28 * 28
    input_nodes = 784
    output_nodes = 10
    hidden_nodes = 200
    learning_rate = 0.3

    n  =  neuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)

    # read the file
    training_data_file = open("../data/archive/mnist_train.csv", 'r')
    training_data_list = training_data_file.readlines()
    training_data_file.close()

    testing_data_file = open("../data/archive/mnist_test.csv", 'r')
    testing_data_list = testing_data_file.readlines()
    testing_data_file.close()

    n.fit(training_data_list, epochs=1, augment=True)
    n.save("model_weights.npz")
    performance = n.evaluate(testing_data_list)
    print("performance =", performance)
