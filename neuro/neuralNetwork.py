import os
import numpy as np
import tensorflow as tf
import tensorflow.python.keras.layers as tfl

from tensorflow.python.keras import backend as K

# Метрики


def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def f1_score(y_true, y_pred):
    precision_f1 = precision(y_true, y_pred)
    recall_f1 = recall(y_true, y_pred)
    return 2 * ((precision_f1 * recall_f1) / (precision_f1 + recall_f1 + K.epsilon()))


class NeuralNetwork:
    IMG_SIZE = (75, 75)

    model = None
    history = None
    train_dataset = None
    test_dataset = None

    base_learning_rate = 0.01
    initial_epochs = 10
    loss_function = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
    data_generator = tf.keras.preprocessing.image.ImageDataGenerator(validation_split=0.2, rescale=1.0 / 255)
    optimizer = tf.keras.optimizers.Adam(base_learning_rate)
    metrics = ['acc', f1_score, precision, recall]

    def __init__(self, filename):
        if os.path.exists(filename):
            self.model = tf.keras.models.load_model(filename)
        else:
            self.model = self.createModel(self.IMG_SIZE)
        self.model.compile(optimizer=self.optimizer, loss=self.loss_function, metrics=self.metrics)

    def train(self, directory):
        self.load_dataset(directory)
        self.history = self.model.fit(self.train_dataset, validation_data=self.test_dataset, epochs=self.initial_epochs)
        self.fine_tune()

    def export(self, filename):
        self.model.save(filename, overwrite=True, include_optimizer=True)

    def recognize(self, sample):
        if sample.ndim == 2:
            s1, s2 = self.IMG_SIZE
            new_sample = np.zeros((s1, s2, 3))
            for i in range(0, 3):
                sample.reshape(s1, s2, 1)
                np.append(new_sample, sample, axis=0)
            sample = new_sample
        res = self.model.predict(np.array([sample]))
        return self.data_generator.class_indices()[res]

    def load_dataset(self, directory):
        # Датасет для тренування
        self.train_dataset = self.data_generator.flow_from_directory(directory, target_size=self.IMG_SIZE,
                                                                    class_mode='categorical',
                                                                    subset = 'training')

        # датасет для тестування
        self.test_dataset = self.data_generator.flow_from_directory(directory,
                                                                    target_size=self.IMG_SIZE,
                                                                    class_mode='categorical',
                                                                    subset='validation')

    def fine_tune(self, fine_tune_start=250):
        tunedModel = self.model.layers[3]
        tunedModel.trainable = True

        # Заморозимо всі шари перед fine_tune_start
        for layer in tunedModel.layers[:fine_tune_start]:
            layer.trainable = False

        self.optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001 * self.base_learning_rate)
        fine_tune_epochs = 100
        total_epochs = self.initial_epochs + fine_tune_epochs

        self.model.compile(optimizer=self.optimizer, loss=self.loss_function, metrics=self.metrics)
        self.model.fit(self.train_dataset, validation_data=self.test_dataset, epochs=total_epochs, initial_epoch=self.history.epoch[-1])

    def createModel(self, image_shape=IMG_SIZE):
        """
        Аргументи:
            image_shape -- ширина та висота картинки
        Повертає:
            tf.keras.model
        """
        input_shape = image_shape + (3,)

        base_model = tf.keras.applications.InceptionV3(input_shape=input_shape,
                                 include_top=False,
                                 weights="imagenet",
                                 classes=29,
                                 classifier_activation="softmax")
        # заморозимо шари, щоб їх не тренувати
        base_model.trainable = False

        # вхідний шар
        inputs = tf.keras.Input(shape=input_shape)

        # для нормалізації інпута [-1;1]
        x = tf.keras.applications.inception_v3.preprocess_input(inputs)

        x = base_model(x, training=False)
        x = tfl.GlobalAveragePooling2D()(x)
        x = tfl.Dropout(0.2)(x)
        outputs = tfl.Dense(29, activation="softmax")(x)

        model = tf.keras.Model(inputs, outputs)

        return model
