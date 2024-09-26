import numpy as np
import matplotlib.pyplot as plt

# 加载预测和真实数据
predictions = np.load('C:/informer/Informer2020/results/informer_custom_ftM_sl96_ll48_pl24_dm512_nh8_el1_dl1_df2048_atprob_fc5_ebtimeF_dtTrue_mxTrue_TaiwanFutures_Prediction_0/pred.npy')
true_values = np.load('C:/informer/Informer2020/results/informer_custom_ftM_sl96_ll48_pl24_dm512_nh8_el1_dl1_df2048_atprob_fc5_ebtimeF_dtTrue_mxTrue_TaiwanFutures_Prediction_0/true.npy')

# 加载 StandardScaler 的均值和标准差
scaler_mean = np.load('C:/informer/Informer2020/scaler_mean.npy')
scaler_scale = np.load('C:/informer/Informer2020/scaler_scale.npy')

# 恢复原始价格数据
predictions_rescaled = predictions * scaler_scale[-1] + scaler_mean[-1]
true_values_rescaled = true_values * scaler_scale[-1] + scaler_mean[-1]

# 绘制预测值和真实值的对比图
plt.figure(figsize=(10, 6))
plt.plot(true_values_rescaled.flatten(), label='True Prices')
plt.plot(predictions_rescaled.flatten(), label='Predicted Prices')
plt.title('Predicted vs True Prices')
plt.xlabel('Time Steps')
plt.ylabel('Price')
plt.legend()
plt.show()
