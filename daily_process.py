import update_raw_data
import daily_predict
import utils_common
import sys

modelPath = '../models/xgb_2018-01-31'

if __name__ == '__main__':
    if len(sys.argv)>1:
        dt = sys.argv[1]
    else:
        dt = None
        pass
    #update_raw_data.main()
    daily_predict.main(modelPath, 'output.txt', dt=dt)
    utils_common.system('python ./server/uploadScore.py output.txt')
    #utils_common.system('rm -rf output.txt')
    pass
