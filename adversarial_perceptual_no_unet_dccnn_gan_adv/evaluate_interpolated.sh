ALPHA=${1}
MODEL='adversarial_perceptuall_no_unet'
DATASET_TYPE='cardiac'
BASE_PATH='/media/hticpose/drive2/Balamurali/'

<<ACC_FACTOR_2x
ACC_FACTOR='2x'
TARGET_PATH=${BASE_PATH}'datasets/'${DATASET_TYPE}'/validation/acc_'${ACC_FACTOR}
PREDICTIONS_PATH=${BASE_PATH}'experiments/'${DATASET_TYPE}'/acc_'${ACC_FACTOR}'/'${MODEL}'/results_alpha_'${ALPHA}
REPORT_PATH=${BASE_PATH}'experiments/'${DATASET_TYPE}'/acc_'${ACC_FACTOR}'/'${MODEL}'/'
echo python evaluate.py --target-path ${TARGET_PATH} --predictions-path ${PREDICTIONS_PATH} --report-path ${REPORT_PATH} 
python evaluate.py --target-path ${TARGET_PATH} --predictions-path ${PREDICTIONS_PATH} --report-path ${REPORT_PATH} 
ACC_FACTOR_2x


#<<ACC_FACTOR_4x
ACC_FACTOR='4x'
TARGET_PATH=${BASE_PATH}'datasets/'${DATASET_TYPE}'/validation/acc_'${ACC_FACTOR}
PREDICTIONS_PATH=${BASE_PATH}'experiments_reconseg/'${DATASET_TYPE}'/reconstruction/acc_'${ACC_FACTOR}'/'${MODEL}'/results_alpha_'${ALPHA}
REPORT_PATH=${BASE_PATH}'experiments_reconseg/'${DATASET_TYPE}'/reconstruction/acc_'${ACC_FACTOR}'/'${MODEL}'/'
echo python evaluate_interpolated.py --target-path ${TARGET_PATH} --predictions-path ${PREDICTIONS_PATH} --report-path ${REPORT_PATH}  
python evaluate_interpolated.py --target-path ${TARGET_PATH} --predictions-path ${PREDICTIONS_PATH} --report-path ${REPORT_PATH} 
#ACC_FACTOR_4x

<<ACC_FACTOR_8x
ACC_FACTOR='8x'
TARGET_PATH=${BASE_PATH}'datasets/'${DATASET_TYPE}'/validation/acc_'${ACC_FACTOR}
PREDICTIONS_PATH=${BASE_PATH}'experiments_reconseg/'${DATASET_TYPE}'/reconstruction/acc_'${ACC_FACTOR}'/'${MODEL}'/results'
REPORT_PATH=${BASE_PATH}'experiments_reconseg/'${DATASET_TYPE}'/reconstruction/acc_'${ACC_FACTOR}'/'${MODEL}'/'
echo python evaluate.py --target-path ${TARGET_PATH} --predictions-path ${PREDICTIONS_PATH} --report-path ${REPORT_PATH} 
python evaluate.py --target-path ${TARGET_PATH} --predictions-path ${PREDICTIONS_PATH} --report-path ${REPORT_PATH} 
ACC_FACTOR_8x


