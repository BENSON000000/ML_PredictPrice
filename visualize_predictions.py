import numpy as np
import matplotlib.pyplot as plt

# 加載預測數據和真實數據
predictions = np.load('C:/informer/Informer2020/results/informer_custom_ftM_sl96_ll48_pl24_dm512_nh8_el1_dl1_df2048_atprob_fc5_ebtimeF_dtTrue_mxTrue_TaiwanFutures_Prediction_0/pred.npy')
true_values = np.load('C:/informer/Informer2020/results/informer_custom_ftM_sl96_ll48_pl24_dm512_nh8_el1_dl1_df2048_atprob_fc5_ebtimeF_dtTrue_mxTrue_TaiwanFutures_Prediction_0/true.npy')

# 加載scaler的mean和scale
scaler_mean = np.load('C:/informer/Informer2020/scaler_mean.npy')
scaler_scale = np.load('C:/informer/Informer2020/scaler_scale.npy')

# 反轉標準化
predictions = predictions * scaler_scale + scaler_mean
true_values = true_values * scaler_scale + scaler_mean

# 畫圖比較預測值和真實值
plt.figure(figsize=(10,6))
plt.plot(true_values.flatten(), label='True Prices', color='blue')
plt.plot(predictions.flatten(), label='Predicted Prices', color='red')
plt.legend()
plt.title('Predicted vs True Prices')
plt.xlabel('Time')
plt.ylabel('Price')
plt.show()
