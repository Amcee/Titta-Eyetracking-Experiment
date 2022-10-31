# Import relevant modules
import os
import pickle
import json
import pandas as pd
from psychopy.hardware import keyboard
from psychopy import visual, monitors, gui, event, core, sound
import numpy as np
import matplotlib.pyplot as plt
from titta import Titta, helpers_tobii as helpers
from os import listdir
from os.path import isfile, join, normpath, basename
import questions2 as questions

# initialize participant ID
participant_id = 1

# %%  Monitor/geometry
MY_MONITOR = 'testMonitor'  # needs to exists in PsychoPy monitor center
FULLSCREEN = False
SCREEN_RES = [2560, 1440]
SCREEN_WIDTH = 52.7  # cm
VIEWING_DIST = 63  # distance from eye to center of screen (cm)

monitor_refresh_rate = 144  # frames per second (fps)
mon = monitors.Monitor(MY_MONITOR)  # Defined in defaults file
mon.setWidth(SCREEN_WIDTH)  # Width of screen (cm)
mon.setDistance(VIEWING_DIST)  # Distance eye / monitor (cm)
mon.setSizePix(SCREEN_RES)
stimulus_duration = 3  # Stimulus duration in seconds

# make list of images
mypath = r'images for design 2'
im_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(im_list)

# %%  ET settings
et_name = 'Tobii Pro Spectrum'
# et_name = 'IS4_Large_Peripheral'
# et_name = 'Tobii Pro Nano'

dummy_mode = True
bimonocular_calibration = False

# Change any of the default dettings?e
settings = Titta.get_defaults(et_name)
settings.FILENAME = 'testfile.tsv'
settings.N_CAL_TARGETS = 5

# create Pre-test Survey
myDlg = gui.Dlg(title="Pre-test Survey")
myDlg.addField('What is your gender?:', choices=["Male", "Female", "Other"])
myDlg.addField('Age:')
myDlg.addField('How many years did you have English as a subject in school?:',
               choices=["5 or fewer", "6 to 10", "11 or more"])
myDlg.addField('What is the highest degree or level of education you have completed?:',
               choices=["Middle School", "High School", "Bachelor's Degree or higher", "Prefer not to say"])
survey = myDlg.show()  # show dialog and wait for OK or Cancel

# create file to store answers
with open('Pre-test Survey ' + str(participant_id) + '.txt', 'w') as file:
    file.write(json.dumps(survey))

# %% Connect to eye tracker and calibrate
tracker = Titta.Connect(settings)
if dummy_mode:
    tracker.set_dummy_mode()
tracker.init()

# Window set-up (this color will be used for calibration)
win = visual.Window(monitor=mon, fullscr=FULLSCREEN,
                    screen=3, size=SCREEN_RES, units='deg')

fixation_point = helpers.MyDot2(win)

images = []  # create list of stimuli images
for element in im_list:
    images.append(visual.ImageStim(win, image=mypath + '/' + element, units='norm', size=(2, 2)))

#  Calibratse
if bimonocular_calibration:
    tracker.calibrate(win, eye='left', calibration_number='first')
    tracker.calibrate(win, eye='right', calibration_number='second')
else:
    tracker.calibrate(win)

# %% Record some data
tracker.start_recording(gaze_data=True, store_data=True)

# Present fixation dot and wait for one second
for i in range(monitor_refresh_rate):
    fixation_point.draw()
    t = win.flip()
    if i == 0:
        tracker.send_message('fix on')

tracker.send_message('fix off')


s = r'sound files for design 2'
np.random.shuffle(images)  # shuffle images so they appear in a random order
counter = 0
# create dictionary for answers
answers = {}
# start timer
timer = core.Clock()
kb = keyboard.Keyboard()
for image in images:
    im_name = image.image
    # get image id
    x = os.path.normpath(im_name)
    x = os.path.basename(x)
    x = x.split('.')
    image_id = x[0]
    print(image_id)
    myMouse = event.Mouse(visible=True)  # Make it so Mouse is visible
    stim = visual.TextStim(win, r'Press "s" to hear questions again',
                           color=(1, 1, 1), colorSpace='rgb')
    # show question
    stim.draw()
    t = win.flip()
    # play soundfile of the question
    soundfile_name = image_id + ".aiff"
    mySound = sound.Sound(os.path.join(s, soundfile_name))
    mySound.play()
    print(myMouse.getPressed())
    buttons = myMouse.getPressed()
    # check if left mouse button gets pressed
    while buttons == [0, 0, 0]:
        # if s gets pressed play the sound
        keys = kb.getKeys(['s'], waitRelease=False)
        core.wait(secs=0.01, hogCPUperiod=0.01)
        if 's' in keys:
            mySound.play()
        buttons = myMouse.getPressed()
        if buttons == [1, 0, 0]:
            break
    for i in range(stimulus_duration * monitor_refresh_rate):
        image.draw()
        t = win.flip()
        keys = kb.getKeys(['s'], waitRelease=False)
        if 's' in keys:
            mySound.play()
        if i == 0:
            tracker.send_message(''.join(['onset_', im_name]))
    tracker.send_message(''.join(['offset_', im_name]))
    stim = visual.TextStim(win, r'Press "s" to hear questions again' + '\n' + 'Press "d" to answer question',
                           color=(1, 1, 1), colorSpace='rgb')
    stim.draw()
    win.flip()
    while True:
        keys = kb.getKeys(['s', 'd'], waitRelease=False)
        if 's' in keys:
            mySound.play()
        if 'd' in keys:
            break
    # create dialog window
    myDlg = gui.Dlg(title="Answer")
    myDlg.addField('Answer:', choices=questions.questions_list2[image_id][1])
    answer = myDlg.show()  # save input in answer
    answers[image_id] = answer  # save answer in answers dictionary with image_id as key

    counter += 1
    if counter == 3:
        break

print("aaaaaaaa")
print(timer.getTime())
print("aaaaaaa")
# create file to store answers
with open('answers' + str(participant_id) + '.txt', 'w') as file:
    file.write(json.dumps(answers))

win.flip()
tracker.stop_recording(gaze_data=True)

# Close window and save data
win.close()
tracker.save_data(mon)  # Also save screen geometry from the monitor object

# create Questionnaire
myDlg = gui.Dlg(title="Questionnaire")
choices = ["Very Low", "Low", "Somewhat Low", "Neutral", "Somewhat High", "High", "Very High"]
myDlg.addText('How much mental and perceptual activity was required (e.g., thinking, deciding, calculating, '
              'remembering, looking, searching, etc.)? Was the task easy or demanding, simple or complex, exacting or'
              ' forgiving?')
myDlg.addField('Mental Demand:', choices=choices)
myDlg.addText('How much time pressure did you feel due '
              'to the rate or pace at which the tasks or '
              'task elements occurred? Was the pace '
              'slow and leisurely or rapid and frantic?')
myDlg.addField('Temporal Demand:', choices=choices)
myDlg.addText('How hard did you have to work (mentally '
              'and physically) to accomplish your level of '
              'performance?')
myDlg.addField('Effort:', choices=choices)
myDlg.addText('How insecure, discouraged, irritated, '
              'stressed and annoyed versus secure, '
              'gratified, content, relaxed and complacent '
              'did you feel during the task?')
myDlg.addField('Frustration:', choices=choices)
myDlg.addText('How successful do you think you were in accomplishing the goals of the task set by the experimenter'
              '? How satisfied were you with your performance in accomplishing these goals?')
myDlg.addField('Performance:',
               choices=["Very Good", "Good", "Somewhat Good", "Neutral", "Somewhat Poor", "Poor", "Very Poor"])
questionnaire_anwers = myDlg.show()  # show dialog and wait for OK or Cancel

# create file to store answers
with open('Questionnaire' + str(participant_id) + '.txt', 'w') as file:
    file.write(json.dumps(questionnaire_anwers))

# %% Open some parts of the pickle and write et-data and messages to tsv-files.
f = open(settings.FILENAME[:-4] + '.pkl', 'rb')
gaze_data = pickle.load(f)
msg_data = pickle.load(f)
eye_openness_data = pickle.load(f)

#  Save data and messages
df_msg = pd.DataFrame(msg_data, columns=['system_time_stamp', 'msg'])
df_msg.to_csv(settings.FILENAME[:-4] + '_msg.tsv', sep='\t')

df = pd.DataFrame(gaze_data, columns=tracker.header)
df_eye_openness = pd.DataFrame(eye_openness_data, columns=['device_time_stamp',
                                                           'system_time_stamp',
                                                           'left_eye_validity',
                                                           'left_eye_openness_value',
                                                           'right_eye_validity',
                                                           'right_eye_openness_value'])

# Add the eye openness signal to the dataframe containing gaze data
df_etdata = pd.merge(df, df_eye_openness, on=['system_time_stamp'])
df_etdata.to_csv(settings.FILENAME[:-4] + '.tsv', sep='\t')

# Plot some data (e.g., the horizontal data from the left eye)
t = (df_etdata['system_time_stamp'] - df_etdata['system_time_stamp'][0]) / 1000
plt.plot(t, df_etdata['left_gaze_point_on_display_area_x'])
plt.plot(t, df_etdata['left_gaze_point_on_display_area_y'])
plt.xlabel('Time (ms)')
plt.ylabel('x/y coordinate (normalized units)')
plt.legend(['x', 'y'])
# plt.show()

plt.figure()
plt.plot(t, df_etdata['left_eye_openness_value'])
plt.plot(t, df_etdata['right_eye_openness_value'])
plt.xlabel('Time (ms)')
plt.ylabel('Eye openness (mm)')
plt.legend(['left', 'right'])
plt.show()
