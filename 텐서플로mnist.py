import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt

# 1. 데이터셋 로드 (MNIST)
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 2. 데이터 전처리
# 데이터 정규화: 0-255 범위의 픽셀 값을 0-1로 변환
x_train, x_test = x_train / 255.0, x_test / 255.0

# 3. 모델 구성
model = models.Sequential([
    layers.Reshape((28, 28, 1), input_shape=(28, 28)),  # 28x28 이미지를 1채널로 reshape
    layers.Conv2D(32, (3, 3), activation='relu'),  # 합성곱 레이어
    layers.MaxPooling2D((2, 2)),  # 풀링 레이어
    layers.Conv2D(64, (3, 3), activation='relu'),  # 또 다른 합성곱 레이어
    layers.MaxPooling2D((2, 2)),  # 풀링 레이어
    layers.Conv2D(64, (3, 3), activation='relu'),  # 또 다른 합성곱 레이어
    layers.Flatten(),  # 1차원으로 펼침
    layers.Dense(64, activation='relu'),  # 완전 연결층
    layers.Dense(10, activation='softmax')  # 10개의 클래스 (0-9 숫자)
])

# 4. 모델 컴파일
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 5. 모델 훈련
model.fit(x_train, y_train, epochs=5)

# 6. 모델 평가
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f"테스트 정확도: {test_acc}")

# 7. 예측 결과 시각화
predictions = model.predict(x_test)
plt.imshow(x_test[0], cmap=plt.cm.binary)
plt.title(f"예측: {np.argmax(predictions[0])}, 실제: {y_test[0]}")
plt.show()