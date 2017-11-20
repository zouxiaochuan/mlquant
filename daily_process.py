import update_raw_data
import daily_predict
import utils_common

modelPath = '../models/xgb_2017-09-29'

if __name__ == '__main__':
    update_raw_data.main()
    daily_predict.main(modelPath, 'output.txt');
    utils_common.system('python ./server/uploadScore.py output.txt')
    utils_common.system('rm -rf output.txt')
    pass
