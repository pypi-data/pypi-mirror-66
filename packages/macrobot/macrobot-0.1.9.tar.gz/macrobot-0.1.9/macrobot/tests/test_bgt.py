import os


def test_bgt_pipeline():
    os.chdir("..")
    #result = os.system('python run_pipeline.py -s C:/Users/lueck/PycharmProjects/BluVision/tests/macrobot/images/bgt/ -d C:/Users/lueck/PycharmProjects/BluVision/tests/macrobot/results/ -p bgt' )
    result = os.system('mb -s C:\ -d C:\ -p bgt')

    print ('ok')

test_bgt_pipeline()