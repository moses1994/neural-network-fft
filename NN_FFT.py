# Kenneth Hall 11/27/17
# Learn to perform Fourier Transformation with Neural Networks

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random

file1path = "/home/ken/Documents/tf/fourierproject/FFT/noisydata.csv"
file2path = "/home/ken/Documents/tf/fourierproject/FFT/noisydata_fft_real.csv"
file3path = "/home/ken/Documents/tf/fourierproject/FFT/noisydata_fft_imag.csv"

test1path = "/home/ken/Documents/tf/fourierproject/FFT/noisydata_test.csv"
test2path = "/home/ken/Documents/tf/fourierproject/FFT/noisydata_fft_real_test.csv"
test3path = "/home/ken/Documents/tf/fourierproject/FFT/noisydata_fft_imag_test.csv"

FLAGS = None
sample_length = 200

# Parameters
learning_rate = .0001
train_steps = 8000

def fournn(x):
    """fournn builds the graph to perform FFT with a neural network

    Args:
        x: input tensor with dimensions (num_samples, sample_length).

    Returns:
        A tensor of shape (num_samples, sample_length) where each row is
        the approximated real-values from the FFT of the corresponding
        input row.
    """

    # First fully connected layer
    with tf.name_scope('fc1'):
        W_fc1 = weight_variable([200, 400])
        b_fc1 = bias_variable([400])

        h_fc1 = tf.nn.relu(tf.matmul(x, W_fc1) + b_fc1)

    # Second fully connected layer
    with tf.name_scope('fc2'):
        W_fc2 = weight_variable([400,300])
        b_fc2 = bias_variable([300])

        h_fc2 = tf.nn.relu(tf.matmul(h_fc1, W_fc2) + b_fc2)

    # Third fully connected layer
    with tf.name_scope('fc3'):
        W_fc3 = weight_variable([300,200])
        b_fc3 = bias_variable([200])

        h_fc3 = tf.matmul(h_fc2, W_fc3) + b_fc3

    return h_fc3


# Define how we create weight variables and bias variables
def weight_variable(shape):
    """weight_variable generates a weight variable of a given shape."""
    initial = tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    """bias_variable generates a bias variable of a given shape."""
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# Create plots to show learning progress
def plot_progress(fft_truth, fft_predicted, error_plot, n):
    plt.figure(n)
    plt.subplot(311)
    plt.plot(fft_truth)
    plt.title('True FFT')
    plt.subplot(312)
    plt.plot(fft_predicted,'r')
    plt.title('Predicted FFT')
    plt.subplot(313)
    plt.plot(error_plot,'g')
    plt.title('Squared Difference Error')
    plt.show()


def main():
    # Import data and goal output data
    ## Training
    signal_data = np.loadtxt(open(file1path,"r"), delimiter=",")
    fft_real_data = np.loadtxt(open(file2path,"r"), delimiter=",")
    fft_imag_data = np.loadtxt(open(file3path,"r"), delimiter=",")
    ## Testing
    signal_data_test = np.loadtxt(open(test1path,"r"), delimiter=",")
    fft_real_data_test = np.loadtxt(open(test2path,"r"), delimiter=",")
    fft_imag_data_test = np.loadtxt(open(test3path,"r"), delimiter=",")

    #print(signal_data)

    # Set up position to hold data as it is passed in and out
    x = tf.placeholder(tf.float32, [None, 200])
    y_ = tf.placeholder(tf.float32, [None, 200])

    # Build the graph
    y_pred = fournn(x)
    # Targets (Labels) are the FFT signals
    y_true = y_

    with tf.name_scope('loss'):
        loss = tf.reduce_mean(tf.pow(y_true - y_pred, 2))

    with tf.name_scope('adam_optimizer'):
        train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)


    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        for i in range(train_steps):
            train_step.run(feed_dict={x: signal_data, y_: fft_real_data})
            l = sess.run(loss, feed_dict={x: signal_data, y_: fft_real_data})
            print('Step %i: Loss: %f' % (i, l))

            if i % 500 == 0:
                # Run some analysis and display True FFT vs. Predicted FFT
                original_fft_data_showme = np.float32(fft_real_data)
                y_showme_pred = np.float32(sess.run(y_pred, feed_dict={x: signal_data, y_: fft_real_data}))
                #print(len(y_showme_pred))
                graph_choice = random.randint(0,len(signal_data))
                error_plot = np.square(np.array(original_fft_data_showme[graph_choice]) - np.array(y_showme_pred[graph_choice]))
                plot_progress(original_fft_data_showme[graph_choice],y_showme_pred[graph_choice],error_plot,1)

                # Test step
                l = sess.run(loss, feed_dict={x: signal_data_test, y_: fft_real_data_test })
                print('Testing loss at step %i: %f' % (i, l))
                y_showme_pred_test = np.float32(sess.run(y_pred, feed_dict={x: signal_data_test, y_: fft_real_data_test}))
                graph_choice_test = random.randint(0,len(signal_data_test))
                print(len(y_showme_pred_test[graph_choice_test]))
                error_plot_test = np.square(np.array(fft_real_data_test[graph_choice_test]) - np.array(y_showme_pred_test[graph_choice_test]))
                plot_progress(fft_real_data_test[graph_choice_test],y_showme_pred_test[graph_choice_test],error_plot_test,2)


if __name__ == "__main__":
    main()
