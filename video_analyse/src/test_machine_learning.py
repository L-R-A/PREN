import os
import numpy as np
import keras.api._v2.keras as keras
import time
import helper as hp
import cv2
from PIL import Image


# MODEL_PATH = "../model/v1_no_base_50000.keras"
# MODEL_PATH = "../tmp/models/v2_no_base_100000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_10000.keras"
# MODEL_PATH = "../tmp/models/v3_no_base_100000.keras"
# MODEL_PATH = "../tmp/models/v1_no_base_150000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_10000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_20000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_30000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_40000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_50000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_60000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_70000.keras"
# MODEL_PATH = "../tmp/models/v5_no_base_120000.keras"

# MODEL_PATH = "../tmp/models/v6_no_base_50000.keras"
# MODEL_PATH = "../tmp/models/v7_no_base_50000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_10000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_20000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_30000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_50000.keras"
# MODEL_PATH = "../tmp/models/v2_E25_50000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_90000.keras"

# MODEL_PATH = "../tmp/models/v2_E25_PAT4_10000.keras"
# MODEL_PATH = "../tmp/models/v1_E50_PAT5_10000.keras"

# MODEL_PATH = "../tmp/models/v1_E25_PAT4_20000.keras" # 95.6%

# MODEL_PATH = "../tmp/models/v1_E50_PAT4_LR05_PAT1_10000.keras"

# MODEL_PATH = "../tmp/models/v2_E25_PAT4_20000.keras" 
# MODEL_PATH = "../tmp/models/v2_E50_PAT4_10000.keras"
# MODEL_PATH = "../tmp/models/v2_E50_PAT4_LR_10000.keras"

# MODEL_PATH = "../tmp/models/v1_E25_PAT4_30000.keras"

# MODEL_PATH = "../tmp/models/v1_E25_PAT4_LRF08_10000.keras"
# MODEL_PATH = "../tmp/models/v1_E25_PAT4_LRF04_10000.keras"

# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL0001_LR05_PAT1_10000.keras" # 96.25
# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL0001_LR05_PAT1_20000.keras"

# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL00001_LR05_PAT1_10000.keras"
# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL0001_LR05_PAT1_DATASET2_10000.keras" # 96.99%
# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL0001_LR05_PAT1_TRANSLATE_10000.keras"

# MODEL_PATH = "../tmp/models/v1_E50_PAT4_DEL0001_LR05_PAT1_DATASET3_10000.keras" # 95
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATE_30000.keras"
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_30000.keras" # 97%
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_50000.keras" # 97%

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_30000.keras" # 99.34% -> 98.66
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_4_30000.keras" # 98%
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_4_NOCROP_30000.keras" # 99.35 -> 271 - 98.99558498896248


# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_3_NOCROP_30000.keras" # 99.73 -> 98.64
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_5_NOCROP_30000.keras" # 99.73 -> 98.64

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_3_NOCROP_120x90_30000.keras" # 99.61 -> 98.82
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_120x90_30000.keras"
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_4_NOCROP_120x90_30000.keras"
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEXY_1_3_NOCROP_30000.keras"

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_4_NOCROP_50000.keras" # 98.86 

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL00001_LR05_PAT1_TRANSLATEY_4_NOCROP_30000.keras"
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_4_NOCROP_AUG_30000.keras" # 98.83830022075055

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_ZOOM_NOCROP_30000.keras"

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_ZOOM_80x60_NOCROP_30000.keras" #89.76545253863135
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_ZOOM_TRANSLATE_80x60_NOCROP_30000.keras" #89.40397350993378
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_ZOOM_NOBLUR_80x60_NOCROP_30000.keras"
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_4_NOCROP_NOBLUR_30000.keras" #98.27262693156733

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_80x60_50000.keras" # 343 - 98.89900662251655
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_DO03_80x60_50000.keras" # 336 - 98.9514348785872
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_DO04_80x60_50000.keras" # 381 - 98.85761589403974
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_50000.keras" # 269 - 99.10044150110376
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-3_A_E-6_80x60_50000.keras" # 813 - 97.39238410596026

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-5_A_E-8_80x60_50000.keras"
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_30000.keras" 

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_DO03_NO_REGULIZATION_80x60_50000.keras"
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 1219 - 96.2603519668737
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_60000.keras" # 878 - 97.39906832298136
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_60000.keras" # 924 - 97.22308488612836
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 882 - 97.44047619047619
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-3_A_E-7_40x30_100000.keras" # 649 - 98.14958592132506
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-2_A_E-7_40x30_100000.keras" # 618 - 98.27898550724638
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_SAME_1_NOCROP_DO03_REGULIZATION_L2_K_E-3_A_E-7_40x30_100000.keras" # 933 - 97.2851966873706
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_1_NOCROP_DO04_REGULIZATION_L2_K_E-3_A_E-7_40x30_100000.keras" # 817 - 97.4223602484472
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_1_FLOAT_NOCROP_DO03_REGULIZATION_L2_K_E-3_A_E-7_40x30_100000.keras" # 889 - 97.27743271221532
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_NO_TRANSLATE_NOCROP_DO03_REGULIZATION_L2_K_E-3_A_E-7_40x30_100000.keras" # 1088 - 96.74171842650104
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_v2_NOCROP_DO03_REGULIZATION_L2_K_E-3_A_E-7_40x30_100000.keras" # 1358 - 96.04813664596273
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_v2_NOCROP_DO03_REGULIZATION_L2_K_E-3_A_E-7_40x30_50000.keras" # 1109 - 96.77018633540372


# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-3_A_E-7_80x60_50000.keras" # 325 - 99.01656314699792
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR05_PAT1_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_30000.keras" # 667 - 98.10041407867494
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR02_LRSV2_PAT1_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_50000.keras" # 499 - 98.48084886128365
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR03_LRSV2_PAT1_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_50000.keras" # 336 - 99.02173913043478
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR04_LRSV2_PAT1_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_50000.keras" # 551 - 98.41873706004141
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR03_LRSV2_PAT3_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_50000.keras" # 403 - 98.8457556935817

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_00001_03_LRSV2_PAT2_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_50000.keras" 

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_096_STEP_5000_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_50000.keras" # 574 - 98.34368530020704
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_096_STEP_4000_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_50000.keras" # 816 - 97.64492753623189
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_092_STEP_5000_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_50000.keras" # 610 - 98.3410973084886
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_096_STEP_1000_TRANSLATEY_2_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_80x60_50000.keras" #  549 - 98.1547619047619


# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_096_STEP_2000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 935 - 97.36542443064182
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_092_STEP_2000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 711 - 97.9192546583851
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_088_STEP_2000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 828 - 97.6733954451345
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_084_STEP_2000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 749 - 97.93219461697723
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_080_STEP_2000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 1458 - 95.62370600414079

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_080_STEP_3000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 845 - 97.59057971014492
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_076_STEP_3000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 869 - 97.46894409937889
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_088_STEP_3000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 840 - 97.63198757763975
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_092_STEP_3000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 968 - 96.99792960662526
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_3000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras"  # 669 - 98.0072463768116
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_3500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras"  # 719 - 97.99430641821947
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_3250_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 748 - 97.81832298136646
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_2750_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 934 -  97.2489648033126
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_3750_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 703 - 98.10300207039337


# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_4000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 1496 - 95.3131469979296
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_4000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 913 - 97.23084886128365
# MODEL_PATH = "../tmp/models/v3_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_4000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 456 - 98.71894409937889
# MODEL_PATH = "../tmp/models/v4_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_4000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 665 - 98.08488612836439
# MODEL_PATH = "../tmp/models/v5_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_4000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_50000.keras" # 741 - 97.80797101449275

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_4000_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 956 - 97.16873706004141

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_7500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 1019 - 97.0419254658385
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_7500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 763 - 97.8623188405797
# MODEL_PATH = "../tmp/models/v3_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_7500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 439 - 98.60766045548654
# MODEL_PATH = "../tmp/models/v4_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_7500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 662 - 98.14182194616977
# MODEL_PATH = "../tmp/models/v4_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_7500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 662 - 98.1418219461697

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_2500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_30000.keras"
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_DECAY_RATE_090_STEP_2500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_30000.keras" # 723 - 97.82608695652173

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_STEP_2500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 271 - 99.25983436853002 | 256 - 98.74537037037037
# MODEL_PATH = "../tmp/models/v1_1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_150000.keras" # 276 - 99.29093567251462 | 227 | 98.87962962962963
# MODEL_PATH = "../tmp/models/v1_2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_300000.keras"# 283 - 99.26656920077973 | 238 | 98.82407407407408
MODEL_PATH = "../tmp/models/v1_1_2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-3_A_E-7_40x30_200000.keras" # 270 - 99.30068226120858


# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_STEP_2500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 533 - 98.56968810916179
# MODEL_PATH = "../tmp/models/v3_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_STEP_2500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 525 - 98.53070175438596
# MODEL_PATH = "../tmp/models/v4_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_STEP_2500_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 665 - 98.23343079922027

# MODEL_PATH = "../tmp/models/v5_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 786 - 97.94346978557505
# MODEL_PATH = "../tmp/models/v6_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 371 - 99.05701754385964
# MODEL_PATH = "../tmp/models/v7_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_40x30_100000.keras" # 429 - 98.89863547758284

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-3_A_E-7_40x30_100000.keras" # 471 - 98.74512670565302
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-3_A_E-7_40x30_100000.keras" # 807 - 97.69736842105263

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_100000.keras" # 987 - 97.49756335282652
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_100000.keras" # 1137 - 96.93713450292398

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_05_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_100000.keras" # 1252 - 96.67884990253411

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_100000.keras" # 799 - 97.91910331384015
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_100000.keras" # 745 - 97.77046783625731

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_03_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 858 - 97.8167641325536

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 488 - 98.60623781676414
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras"  # 615 - 98.3552631578947
# MODEL_PATH = "../tmp/models/v3_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 1140 - 97.06140350877193

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_075_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 826 - 97.74853801169591
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_075_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 763 - 98.07748538011695
# MODEL_PATH = "../tmp/models/v3_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_075_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 682 - 98.17251461988305
# MODEL_PATH = "../tmp/models/v4_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_075_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 890 - 97.67787524366472
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_075_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 957 - 97.38304093567251
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 1244

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 958 - 97.42933723196882

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_STATIC_05_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 4084 - 81.83723196881091
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_0_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 1804 - 94.53216374269006
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_STATIC_NEGATIVE_05_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 1171 - 96.88109161793372
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_STATIC_NEGATIVE_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 729 - 98.15302144249513
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_STATIC_NEGATIVE_1_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 1179 - 96.71539961013646
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_STATIC_NEGATIVE_125_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 1283 - 96.26218323586744
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_STATIC_NEGATIVE_150_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 1523 - 95.32651072124756
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_150_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 961 - 97.46345029239767

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_100_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_50000.keras" # 984 - 97.43908382066277

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_100_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_100000.keras" # 813 - 97.77534113060429
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_100_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_100000.keras" # 819 -  97.57797270955166
# MODEL_PATH = "../tmp/models/v3_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_100_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_100000.keras" # 683 -  98.18469785575049 | 348 - 98.3611111111111

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_100_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 579 - 98.28947368421052 | 339 - 98.35185185185185 
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_100_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 760 - 97.89230019493178 | 507 - 97.43518518518519
# MODEL_PATH = "../tmp/models/v3_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_100_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 394 - 98.97417153996102 | 280 - 98.60185185185185
# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_STATIC_NEGATIVE_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 669 - 98.2553606237816  | 416 - 98.07407407407408
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_STATIC_NEGATIVE_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 816 - 97.61695906432749
# MODEL_PATH = "../tmp/models/v4_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 836  - 97.65107212475634
# MODEL_PATH = "../tmp/models/v5_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 676 - 98.09697855750487
# MODEL_PATH = "../tmp/models/v6_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 473 - 98.70614035087719
# MODEL_PATH = "../tmp/models/v7_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_050_075_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 637 - 98.29191033138402

# MODEL_PATH = "../tmp/models/v1_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_060_090_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras" # 595 - 98.44541910331384
# MODEL_PATH = "../tmp/models/v2_E100_PAT4_DEL0001_LR_SCHEDULER_PAT_3_FACTOR_05_TRANSLATEY_NEGATIVE_060_090_NOCROP_DO03_REGULIZATION_L2_K_E-4_A_E-7_32x24_150000.keras"



# MODEL_PATH = "./raspberry/model.keras"



BUNDLES = [
    # {   
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([1, 3, 2, 2, 3, 3, 1, 0]),
    #     'name': 'f640e372-95ce-4fc9-a614-cbddb3e5710b'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([1, 3, 2, 2, 3, 3, 1, 0]),
    #     'name': 'a5119e66-947d-45e0-b229-549b1ca79393'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([1, 3, 2, 2, 3, 3, 1, 0]),
    #     'name': 'f33fa7bf-4a55-47c1-85bf-3c62ea456efc'
    # },       
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([1, 3, 2, 2, 3, 3, 1, 0]),
    #     'name': '6137b988-bfa4-4aa8-8034-f91382cbd425'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([1, 1, 2, 2, 3, 3, 3, 0]),
    #     'name': 'a2ce3e86-8590-4986-8c36-07e931b1dfaa'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([3, 1, 3, 2, 3, 0, 3, 3]),
    #     'name': '958960b8-aeb3-403f-89ba-862ec773bd51'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([3, 1, 3, 2, 3, 0, 3, 3]),
    #     'name': '51cd8bf3-1ea3-4bc4-aa5e-f7c117f0d3a6'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 1, 3, 2, 2, 1, 3, 3]),
    #     'name': '46ae10ae-bf46-46a8-81b0-a69dfdef9d51'
    # }, 
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([2, 3, 0, 1, 3, 3, 2, 1]),
    #     'name': '29b57f52-82b5-422d-af4b-186e72f509b2'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 1, 3, 3, 3, 3, 3, 3]),
    #     'name': '635eabd2-6084-4413-bcb8-f80bd05556d4'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([3, 2, 0, 0, 3, 1, 1, 3]),
    #     'name': 'dfbdb9fe-0e53-4d8e-829c-6cfd0a968bc1'
    # },
    # # {
    # #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    # #     'result': np.array([1, 2, 0, 0, 0, 1, 1, 2]),
    # #     'name': '22710caf-0412-4d7a-b986-4d2e599c5efc'
    # # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 0, 1, 2, 1, 2, 0, 1]),
    #     'name': 'd95bcdb3-0dee-452e-9979-8268f9345d66'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 0, 1, 2, 1, 2, 0, 1]),
    #     'name': '91cbc884-e0cf-49fa-9c9f-1175986c4716'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 0, 1, 2, 1, 2, 0, 1]),
    #     'name': '4cb8d403-328f-4e44-8f50-e6b5ed25a1e2'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([3, 0, 1, 2, 3, 2, 0, 3]),
    #     'name': 'd00b6d45-25d6-4baf-909a-fe36c1af2f90'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([3, 0, 1, 2, 3, 2, 0, 3]),
    #     'name': '3a83a9f6-35e6-4aef-9302-36895b42aa92'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([1, 0, 1, 2, 1, 2, 0, 0]),
    #     'name': 'a44f06a7-7a0a-4e3f-827a-936fdbe1bdff'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([1, 0, 2, 2, 0, 1, 1, 0]),
    #     'name': 'b535d337-68fe-4ebe-a7c6-8146c962b401'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([1, 0, 2, 2, 0, 1, 1, 0]),
    #     'name': 'cd30bc4b-735b-4e2b-99c6-e497c3d5cc1b'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([2, 0, 3, 0, 3, 1, 3, 1]),
    #     'name': '9087d8e9-2e84-4dda-a786-5697aae54552'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([2, 0, 3, 0, 3, 1, 3, 1]),
    #     'name': '0eeb1650-c02f-421e-97c6-b90e395a2f25'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([3, 0, 0, 0, 3, 1, 2, 3]),
    #     'name': '4c20a053-09c2-4b7c-a9c7-269fcac8a0d6'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([1, 1, 3, 0, 3, 1, 3, 3]),
    #     'name': 'ec511388-1d57-4b0b-accd-3e8bc5ba4b70'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([1, 1, 2, 1, 3, 3, 2, 3]),
    #     'name': 'b2d4eb7e-835d-40ee-9f47-803cf33e2aae'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([2, 3, 0, 1, 3, 3, 3, 3]),
    #     'name': '5ad4c890-fbe0-491f-9674-8cfa78f0cfd1'
    # },
    # # {
    # #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    # #     'result': np.array([2, 3, 3, 1, 3, 3, 3, 0]),
    # #     'name': '3901c79d-3576-4a63-a8b5-52f7c0774731'
    # # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([2, 2, 0, 0, 0, 3, 1, 3]),
    #     'name': '9734b4dc-58ab-4173-881f-e8225841b0a4'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 3, 1, 0, 3, 3, 3, 2]),
    #     'name': '1aea8b2e-9a2c-440a-aa40-5ba9d9dcd66b'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 3, 1, 0, 3, 3, 3, 2]),
    #     'name': '14fef918-6182-460a-9fec-209d6713cef2'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 3, 1, 0, 3, 3, 3, 2]),
    #     'name': '118f28a9-0e96-4b76-8555-2b179548df84'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 3, 1, 0, 3, 3, 3, 2]),
    #     'name': 'bd0b56b5-7733-471e-a668-614d1fe27680'
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 2, 1, 0, 2, 3, 3, 3]),
    #     'name': '9e1d6d46-b25b-4c97-b32b-f894cd6dc768'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 2, 1, 0, 2, 3, 3, 3]),
    #     'name': 'ffa4b114-5afd-49a1-ac63-17b1d745eed4'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 3, 3, 0, 1, 3, 3, 3]),
    #     'name': 'c9576ced-c378-43f2-bf11-cdb345827b01'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 3, 3, 0, 1, 3, 3, 3]),
    #     'name': 'c9576ced-c378-43f2-bf11-cdb345827b01'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 3, 3, 0, 1, 3, 3, 3]),
    #     'name': '4cc63b14-cb83-488f-94cc-a3722d889765'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([3, 2, 3, 0, 3, 2, 3, 3]),
    #     'name': '12ebb097-d21b-4f76-85a6-ec2fbc2214b5'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([3, 2, 3, 0, 3, 2, 3, 3]),
    #     'name': '15b26e4f-c007-49e5-bb01-4ecd6e07e0c0'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([3, 2, 1, 0, 3, 3, 3, 3]),
    #     'name': 'da980db5-c50a-4461-8ac9-2580d125e922'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([3, 2, 1, 0, 3, 3, 3, 3]),
    #     'name': '50ac6cd9-6a4b-4675-be07-f36b01dca54d'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 2, 3, 0, 1, 3, 3, 3]),
    #     'name': '0bdcd001-d58a-48a0-abf9-f75aa1f517fb'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 2, 0, 0, 2, 1, 3, 3]),
    #     'name': '930e6c7f-bcaa-4f73-af54-683d662ff5a7'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 2, 0, 0, 2, 1, 3, 3]),
    #     'name': '230ec0d8-cbcf-4051-8a07-6b489f2e0500'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 2, 0, 0, 2, 1, 3, 3]),
    #     'name': '09cdcd28-ec1c-4150-b1f2-c43acedd0343'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 2, 0, 0, 2, 1, 3, 3]),
    #     'name': 'aefaa95f-c37f-44ac-aa5d-9522ec4e771e'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 2, 0, 0, 2, 1, 3, 3]),
    #     'name': 'ba3448f2-c84c-4f41-b1d0-89c0df823b7c'   
    # },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([0, 2, 0, 0, 2, 1, 3, 3]),
    #     'name': 'test2'   
    # },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([0, 2, 0, 0, 2, 1, 3, 3]),
        'name': '7b923782-f604-4306-ad58-3f3461a36d76'   
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([0, 2, 0, 0, 2, 1, 3, 3]),
        'name': '3a792a40-8f13-4c81-b3a7-34241360ee0b'   
    }, 
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([0, 2, 3, 0, 0, 3, 3, 3]),
        'name': '8d90cdbb-18e0-4aa6-9882-3c9e8d41e930'  
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([3, 2, 3, 0, 3, 3, 3, 1]),
        'name': '60689463-e400-48d8-8638-7325d9031e18'  
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([2, 3, 3, 0, 3, 3, 3, 0]),
        'name': '2d43a087-e77e-4e41-84cc-009124cd00e3'  
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([2, 3, 1, 3, 0, 3, 0, 3]),
        'name': '036c447b-e18f-41e5-bbc5-b3f7ceec0545'  
    }, 
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([0, 2, 2, 0, 0, 3, 1, 3]),
        'name': '80747358-0e05-4310-84ad-7ec4eff62942'     
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([0, 2, 1, 2, 3, 0, 0, 3]),
        'name': 'd749fc9c-3343-4adc-9286-1efdcf4fdb93'     
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([0, 2, 1, 2, 3, 0, 0, 3]),
        'name': 'af85df3a-8503-44ec-a321-93d8c35a5eef'    
    },
    # {
    #     'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
    #     'result': np.array([2, 0, 2, 1, 0, 3, 0, 3]),
    #     'name': '9ab3c5e8-1e9e-4863-a3b0-cd966c758560'    # VERY SHITTY PLACED
    # }
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([2, 0, 2, 1, 0, 3, 0, 3]),
        'name': '3a9921a1-74cb-4c75-a3cd-f70fea582a6f'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([2, 0, 2, 1, 0, 3, 0, 3]),
        'name': '53f6cc9b-0551-4b7b-a7ca-6755baeb1eeb'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([2, 0, 2, 1, 0, 3, 0, 3]),
        'name': 'f7cc00ed-27bc-47f5-aca3-0cfd83091176'
    },
    {
        'path': os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tmp', 'ressources'),
        'result': np.array([2, 0, 1, 2, 3, 0, 3, 0]),
        'name': '98e2963c-1dc7-4687-844e-0f76f0bedf09'
    }        
]


IMAGE_HEIGHT_PX = 30
IMAGE_WIDTH_PX = 40
NORMALIZE_VALUE = 255
IN_DEBUG_MODE = False

color_mapping = { 'red': 0, 'yellow': 1, 'blue': 2, '': 3 }
label_mapping = { 0: 'red', 1: 'yellow', 2: 'blue', 3: ''}

def check_time_passed(start_time, interval):
    current_time = time.time()
    elapsed_time = current_time - start_time
    return elapsed_time >= interval

def normalize_images(images):
    return images / NORMALIZE_VALUE

def predict(model, input):
    return model.predict([input[:, 0], input[:, 1]])

def compare_arrays(arr1, arr2, not_3_err):
    # Convert arrays to numpy arrays if they are not already
    arr1 = np.array(arr1)
    arr2 = np.array(arr2)
    
    # Find differing values and their positions
    differing_values = np.where(arr1 != arr2)[0]

    
    # Prepare the result
    result = []
    for i, pos in enumerate(differing_values):
        if arr2[pos] != 3:
            not_3_err = not_3_err + 1
        
        result.append(f"{i+1}. Pos: {pos}, Value: {arr2[pos]}")
    
    return result, not_3_err
    
def print_table(data):
    headers = ["Bundle", "ID", "Actual", "Prediction", "Accuracy", "Diff"]
    col_width = [max(len(str(d[col])) for d in data) for col in headers]

    separator = "+".join(["-" * (w + 2) for w in col_width])
    print(separator)
    print("| {:s} | {:s} | {:s} | {:s} | {:s} |".format(*headers, *col_width)) 
    print(separator)

    counter = 0

    for row in data:
        actual_value_str = str(row["Actual"])
        prediction = row["Prediction"]
        accuracy = row.get("Accuracy")

        if accuracy > 87.5 or accuracy == 0:
            continue
        
        counter = counter + 1
        print("| %s | %d | %s | %s | %.2f | %s |" % (row["Bundle"], row["ID"], actual_value_str, prediction, accuracy, row["Diff"]))  
    print(separator)
    print("Amount (<= 87.5%): " + str(counter))
    print("Total: " + str(len(data)))

def main():
    model = keras.models.load_model(os.path.join(os.path.dirname(os.path.abspath(__file__)), MODEL_PATH))

    if IN_DEBUG_MODE:
        model.summary()

    images = []

    for bundle in BUNDLES:
        filenames = sorted(os.listdir(os.path.join(bundle['path'], bundle['name'])))

        for i, filename in enumerate(filenames):
            full_path = os.path.join(bundle['path'], bundle['name'], filename)
            image = Image.open(full_path)
            image = image.resize((IMAGE_WIDTH_PX, IMAGE_HEIGHT_PX))
            image = np.array(image)[:, :, ::-1]
            # image = image[0:115, 10:150]
            image = hp.Preprocess.start(image)

            # image = hp.Video.zoom(image, IMAGE_HEIGHT_PX, IMAGE_WIDTH_PX)

            # image = hp.Preprocess.convert_to_BGR(image)

            # image = hp.Augmentation.black_spots(image, 100)

            if IN_DEBUG_MODE:
                hp.Out.image_show("Image", image, IN_DEBUG_MODE)

                while True:
                    if cv2.waitKey(1) & 0xFF == ord('q'): 
                        break
            
            normalized = normalize_images(image)
                       

            if i % 2 == 0:
                images.append([normalized])
            else:
                images[len(images) - 1].append(normalized)    
    images = np.array(images)

    predictions = np.argmax(predict(model, images), axis=-1)

    data = []

    total_accuracy = 0

    not_3_err = 0

    index = 0


    for bundle in BUNDLES:
        files = os.listdir(os.path.join(bundle['path'], bundle['name']))
        id = 0
        for i in range(0, int(len(files) / 2)):
            intersection = np.sum(bundle['result'] == predictions[index])
            coverage_percent = (intersection / len(bundle['result'])) * 100
            diff, not_3_err = compare_arrays(bundle['result'], predictions[index], not_3_err)

            data.append({"Bundle": bundle['name'], "ID": id + 1, "Actual": np.array2string(bundle['result']), "Prediction": np.array2string(predictions[index]), "Accuracy": coverage_percent, "Diff": diff})
            index = index + 1
            total_accuracy = total_accuracy + coverage_percent
            id = id + 1

    print_table(data)

    print(f"\n\n Total Accuracy: {total_accuracy / index}")
    print(f"\n Total errors confusing colors: " + str(not_3_err))

if __name__ == "__main__":
    main()

