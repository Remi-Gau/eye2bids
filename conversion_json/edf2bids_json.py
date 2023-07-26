import subprocess
import glob, os
import numpy as np
import pandas as pd
import json

cwd = os.getcwd()
os.chdir(cwd)

######################## CONVERSION events ##############################################

#make edf file a varaible to be readable for subprocess 
edf_files_list = []
for filename_edf in glob.glob("*.EDF"):
    edf_files_list.append(filename_edf)

#convert events from edf to filename_edf+_events.asc and storing it in cwd
for file in edf_files_list:
    subprocess.run(['edf2asc', '-y' ,'-e', filename_edf, filename_edf+ "_events"]) 

#make events asc file a variable in list
events_asc_files_list=[]
for filename_events_asc in glob.glob("*_events.asc"):
    events_asc_files_list.append(filename_events_asc)    


############################ Prepare file ##################################

#read events file
with open(filename_events_asc) as f:
    events=f.readlines()

#save messages
message=[ms for ms in events if ms.startswith("MSG")] 
df_ms=pd.DataFrame([ms.split() for ms in message])    

#don't need MSG and sample columns
df_ms_reduced = pd.DataFrame(df_ms.iloc[0:, 2:])

######################### Events.json Metadata ##################################

#StimulusPresentation.ScreenResolution
screen_res = df_ms_reduced[df_ms_reduced[2] == "DISPLAY_COORDS"]
ScreenResolution = df_ms_reduced.iloc[0:1, 3:5].to_string(header=False, index=False)

#save StimulusPresentation.ScreenSize
#TODO: apparently not equal to ELCL_WINDOW_SIZES
#screen_size = df_ms_reduced[df_ms_reduced[2] == "ELCL_WINDOW_SIZES"]
#ScreenSize = screen_size.iloc[0:1, 1:3].to_string(header=False, index=False)

#TaskName
task=[ts for ts in events if ts.startswith("** RECORDED BY")]
task = ' '.join(task)
task=task.replace("** RECORDED BY ","").replace("\n","")
TaskName=task


######################## Eyetrack.json Metadata ###################################

#ManufacturersModelName
model=[ml for ml in events if ml.startswith("** EYELINK")]
model = ' '.join(model)
model=model.replace("** ","").replace("\n","")
ManufacturersModelName=model

#DeviceSerialNumber
serial=[sl for sl in events if sl.startswith("** SERIAL NUMBER:")]
serial = ' '.join(serial)
serial=serial.replace("** SERIAL NUMBER: ","").replace("\n","")
DeviceSerialNumber=serial

#SamplingFrequency
sampling_frequency = df_ms_reduced[df_ms_reduced[2] == "RECCFG"]
SamplingFrequency = int(sampling_frequency.iloc[0:1, 2:3].to_string(header=False, index=False))

#RecordedEye
eye = df_ms_reduced[df_ms_reduced[2] == "RECCFG"]
RecordedEye = eye.iloc[0:1, 5:6].to_string(header=False, index=False)
if RecordedEye == "L": 
    RecordedEye = RecordedEye.replace("L", "Left")
elif RecordedEye == "R":
    RecordedEye = RecordedEye.replace("R", "Right") 
elif RecordedEye == "LR":
    RecordedEye = RecordedEye.replace("LR", "Both")

#SampleCoordinateUnits    

#SampleCoordinateSystem

#EnvironmentCoordinates

#ScreenAOIDefinition

#AverageCalibrationError
# TODO: discuss with Remi and Martin which value when multiple calibrations; same for maximal calibration error
err_avg= df_ms_reduced[df_ms_reduced[3] == "VALIDATION"]
err_avg_num = err_avg[9].to_string(header=False, index=False)
AverageCalibrationError = sum(int(x) for x in err_avg_num)/len(err_avg_num)

#MaximalCalibrationError

#CalibrationCount
cal_count= df_ms_reduced[df_ms_reduced[3] == "CALIBRATION"]
CalibrationCount = len(cal_count.index)

#CalibrationList
#TODO: ask Remi and Martin what "time relative to first event" is and where to find it 
cal_list=df_ms[df_ms[3]=="VALIDATION"]
CalibrationList=cal_list[[4, 6, 11, 9, 1]].values.tolist()


#CalibrationPosition
## get list with calibration positions for every calibration run
cal_pos= df_ms_reduced[df_ms_reduced[2] == "VALIDATE"] 
## get number of calibration points per calibration run
cal_pos_num=int(len(cal_pos.index)/len(cal_count.index)) 
## make calibration positions for every calibration run a single list
cal_pos_list=cal_pos[8].values.tolist() 
## split list per calibration run and make it a list
cal_chunk_list=list()
for i in range(0, len(cal_pos_list), cal_pos_num):
    cal_chunk_list.append(cal_pos_list[i:i+cal_list_num])
#TODO: make values in list to integers, somehow...

#CalibrationType
cal_type= df_ms_reduced[df_ms_reduced[3] == "CALIBRATION"]
CalibrationType = cal_type.iloc[0:1, 2:3].to_string(header=False, index=False)

#CalibrationUnit
#TODO: ask Remi and Martin if always pixel for EyeLink

#EyeTrackerDistance
#TODO: ask Remi and Martin if CAMERA_LENS_FOCAL_LENGTH equals EyeTrackerDistance
track_dis= df_ms_reduced[df_ms_reduced[2] == "CAMERA_LENS_FOCAL_LENGTH"]
EyeTrackerDistance = int(track_dis.iloc[0:1, 1:2].to_string(header=False, index=False))


#EyeTrackingMethod
track_method = df_ms_reduced[df_ms_reduced[2] == "RECCFG"]
EyeTrackingMethod = track_method.iloc[0:1, 1:2].to_string(header=False, index=False)

#PupilFitMethod
pupil_fit = df_ms_reduced[df_ms_reduced[2] == "ELCL_PROC"]
PupilFitMethod = pupil_fit.iloc[0:1, 1:2].to_string(header=False, index=False)

#StartTime
start=[st for st in events if st.startswith("START")] 
df_st=pd.DataFrame([st.split() for st in start])


#StopTime
stop=[so for so in events if so.startswith("STOP")] 
df_st=pd.DataFrame([st.split() for st in start])



##################### to json ##################################################
eyetrack={
    "Manufacturer": "SR-Research",
    "ManufacturersModelName": ManufacturersModelName,
    "DeviceSerialNumber": DeviceSerialNumber,
    "SoftwareVersion": "",
    "SamplingFrequency": SamplingFrequency,
    "SampleCoordinateUnits": "",
    "SampleCoordinateSystem": "",
    "EnvironmentCoordinates": "",
    "RecordedEye": RecordedEye,
    "ScreenAOIDefinition": "",
    "CalibrationCount": CalibrationCount,
    "CalibrationList": CalibrationList, 
    "CalibrationType": CalibrationType,
    "CalibrationPosition": cal_chunk_list,
    "EyeTrackingMethod": EyeTrackingMethod,
    "PupilFitMethod": PupilFitMethod
}
print(json.dumps(eyetrack, indent=15))


events={
   "TaskName": TaskName,
   "InstitutionName": "",
   "InstitutionAddress": "",
   "StimulusPresentation": {
       "ScreenDistance": 60,
       "ScreenRefreshRate": "x",
       "ScreenResolution": ScreenResolution,
       "ScreenSize": []
   }
}
print(json.dumps(events, indent=9))


################################### not needed for jsons but save for later maybe ################################################

#NOTE: For creating tsv tables it's better to not split edf2asc in samples and events as events can be better encoded together with samples when in one ascii file,
#therefore, code below is crap


#convert samples from edf to filename_edf+_samples.asc and storing it in cwd
for file in edf_files_list:
    subprocess.run(['edf2asc', '-y' ,'-s', filename_edf, filename_edf+ "_samples"]) 

#make samples asc file a variable
samples_asc_files_list=[]
for filename_samples_asc in glob.glob("*_samples.asc"):
    samples_asc_files_list.append(filename_samples_asc)

#make samples a dataframe
#TODO: make if statement for all other variables given by samples but not required by BIDS in case values are present
samples_dataframe=pd.read_table(filename_samples_asc, index_col=False,
                  names=["eye_timestamp", "eye1_x_coordinate", "eye1_y_coordinate", "eye1_pupil_size",
                         "eye2_x_coordinate", "eye2_y_coordinate", "eye2_pupil_size"])


#save fixations 
fixation=[fe for fe in events if fe.startswith("EFIX")] 
df_fx=pd.DataFrame([fe.split() for fe in fixation])
#df_fx.rename(columns={4: "fixation_duration"})
fixation_duration = pd.DataFrame(df_fx[2],[4])

#save saccades
saccade=[sa for sa in events if sa.startswith("ESAC")] 
df_sa=pd.DataFrame([sa.split() for sa in saccade])
saccade_duration = df_sa[4]

#save blinks
blink=[bi for bi in events if bi.startswith("EBLINK")] 
df_bi=pd.DataFrame([bi.split() for bi in blink])
blink_duration = df_bi[4]

#save messages
message=[ms for ms in events if ms.startswith("MSG")] 
df_ms=pd.DataFrame([ms.split() for ms in message])

