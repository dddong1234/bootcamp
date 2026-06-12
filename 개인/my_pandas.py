import pandas as pd
from sklearn.preprocessing import StandardScaler
lst = [1,2,3,4,5,6,7]
data = pd.DataFrame(lst)
X = data

X_train = data[0:4]
X_test = data[4:8]
scaler = StandardScaler()

X_train_IQR = IQR.fit(X_train)
X_test_IQR = IQR.transform(X_test)

