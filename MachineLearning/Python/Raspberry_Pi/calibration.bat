plink pi@169.254.22.56 -pw raspberry cd ~/progCamera; ./stream2PC
:plink pi@169.254.22.57 -pw raspberry cd ~/progCamera; ./stream2PC

python robotsCalibration.py 0
:python robotsCalibration.py 1
pscp -pw raspberry RobotsFinder_0.dat pi@169.254.22.56:/home/pi/progCamera
:pscp -pw raspberry RobotsFinder_1.dat pi@169.254.22.56:/home/pi/progCamera

:pscp -pw raspberry RobotsFinder_0.dat pi@169.254.22.57:/home/pi/progCamera
:pscp -pw raspberry RobotsFinder_1.dat pi@169.254.22.57:/home/pi/progCamera


python perspectiveCalibration.py m
pscp -pw raspberry PerspectiveTransformer_m.dat pi@169.254.22.56:/home/pi/progCamera

:python perspectiveCalibration.py l
:pscp -pw raspberry PerspectiveTransformer_m.dat pi@169.254.22.57:/home/pi/progCamera


plink pi@169.254.22.56 -pw raspberry cd ~/progCamera;sudo ./startScript
:plink pi@169.254.22.57 -pw raspberry cd ~/progCamera;sudo ./startScript

PAUSE