# Movella

# https://www.twitch.tv/videos/2080629452?t=1h2m48s
ROLE = 'MikoverseAvatar'

# Warudo Xsens: https://docs.warudo.app/docs/mocap/xsens-mvn

# https://base.movella.com/s/article/MVN-Unreal-Live-Link-Plugin-UE5?language=en_US
# https://base.movella.com/s/article/Full-Body-Mocap-Link-Live-Link-Face-StretchSense-Vive?language=en_US
# https://movella.my.site.com/XsensKnowledgebase/s/article/Unreal-MVN-Live-Link-Plugin-Overview?language=en_US

# Biomechanical Model: https://base.movella.com/s/article/MVN-Biomechanical-Model?language=en_US
BIOMECHANICAL_SEGMENTS = [
    'Pelvis',
    'L5',
    'L3',
    'T12',
    'Sternum',
    'Neck',
    'Head',
    'RightShoulder',
    'RightUpperArm',
    'RightForeArm',
    'RightHand',
    'LeftShoulder',
    'LeftUpperArm',
    'LeftForeArm',
    'LeftHand',
    'RightUpperLeg',
    'RightLowerLeg',
    'RightFoot',
    'RightToe',
    'LeftUpperLeg',
    'LeftLowerLeg',
    'LeftFoot',
    'LeftToe'
]

BIOMECHANICAL_JOINTS = [
    'jL5S1',
    'jL4L3',
    'jL1T12',
    'jT9T8',
    'jT1C7',
    'jC1Head',
    'jRightT4Shoulder',
    'jRightShoulder',
    'jRightElbow',
    'jRightWrist',
    'jLeftT4Shoulder',
    'jLeftShoulder',
    'jLeftElbow',
    'jLeftWrist',
    'jRightHip',
    'jRightKnee',
    'jRightAnkle',
    'jRightBallFoot',
    'jLeftHip',
    'jLeftKnee',
    'jLeftAnkle',
    'jLeftBallFoot'
]

BIOMECHANICAL_ERGO =  [
    'Head_T8',
    'T8_Left_UpperArm',
    'Pelvis_T8',
    'Vertical_Pelvis',
    'Vertical_T8'
]