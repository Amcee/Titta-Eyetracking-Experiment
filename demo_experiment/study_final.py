# Import relevant modules
import os
import pickle
import json
import pandas as pd
from psychopy.hardware import keyboard
from psychopy import visual, monitors, gui, sound, core, event
import numpy as np
import matplotlib.pyplot as plt
from titta import Titta, helpers_tobii as helpers
from os import listdir
from os.path import isfile, join
from questions import questions

# initialize participant ID
participant_id = 2

# %%  Monitor/geometry
MY_MONITOR = 'testMonitor'  # needs to exists in PsychoPy monitor center
SCREEN_ID = 1
FULLSCREEN = False
SCREEN_RES = [1920, 1080]
SCREEN_WIDTH = 52.7  # cm
VIEWING_DIST = 63  # distance from eye to center of screen (cm)
image_size = (1.5, 2)

monitor_refresh_rate = 60  # frames per second (fps)
mon = monitors.Monitor(MY_MONITOR)  # Defined in defaults file
mon.setWidth(SCREEN_WIDTH)  # Width of screen (cm)
mon.setDistance(VIEWING_DIST)  # Distance eye / monitor (cm)
mon.setSizePix(SCREEN_RES)
stimulus_duration = 3  # Stimulus duration in seconds

# %%  ET settings
et_name = 'Tobii Pro Spectrum'
# et_name = 'IS4_Large_Peripheral'
# et_name = 'Tobii Pro Nano'

dummy_mode = False
bimonocular_calibration = False

# Change any of the default dettings?e
settings = Titta.get_defaults(et_name)
settings.FILENAME = 'testfile by participant' + str(participant_id) + '.tsv'
settings.N_CAL_TARGETS = 5


# create demographic survey
def create_pre_test_survey():
    # create Pre-test Survey
    myDlg = gui.Dlg(title="Pre-test Survey", screen=SCREEN_ID)
    myDlg.cancelbutton.clicked.connect(myDlg.accept)
    myDlg.addField('What is your gender?:', choices=["Male", "Female", "Other", "Prefer not to say"])
    myDlg.addField('Age:',
                   choices=[18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
                            40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, "Prefer not to say"])
    myDlg.addField('How many years did you have English as a subject in school?:',
                   choices=["5 or fewer", "6 to 10", "11 or more", "Prefer not to say"])
    myDlg.addField('How confident are you in your English skills?:',
                   choices=["Very confident", "A little confident", "Not at all confident", "Prefer not to say"])
    myDlg.addField('What is your dominant reading directionality?:',
                   choices=["Left to right", "Right to left", "Top to bottom", "Bidirectional", "Prefer not to say"])
    myDlg.addField('What is the highest degree or level of education you have completed?:',
                   choices=["High School", "Bachelor's Degree", "Master's Degree", "Doctors Degree",
                            "Prefer not to say"])
    myDlg.addField('Do you have corrected eyesight (glasses, contact lenses, etc.)?:',
                   choices=["Yes", "No", "Prefer not to say"])
    myDlg.addField('Are you colorblind?:',
                   choices=["Yes, Red-green color blindness", "Yes, Blue-yellow color blindness", "Yes, Complete color "
                                                                                                  "blindness", "No",
                            "Prefer not to say"])

    survey = myDlg.show()  # show dialog and wait for OK or Cancel
    if myDlg.OK:  # or if ok_data is not None
        print(survey)

    # create file to store answers
    with open('Pre-test Survey by participant ' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(survey))


# create NASA-TLX Questionnaire
def create_questionnaire():
    myDlg = gui.Dlg(title="Questionnaire", screen=SCREEN_ID)
    choices = ["Very Low", "Low", "Somewhat Low", "Neutral", "Somewhat High", "High", "Very High"]
    myDlg.addText('How much mental and perceptual activity was required (e.g., thinking, deciding, calculating, '
                  'remembering, looking, searching, etc.)?')
    myDlg.addField('Mental Demand:', choices=choices)
    myDlg.addText('How much time pressure did you feel due '
                  'to the rate or pace at which the tasks or '
                  'task elements occurred?')
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
                  '? ')
    myDlg.addField('Performance:',
                   choices=["Very Good", "Good", "Somewhat Good", "Neutral", "Somewhat Poor", "Poor", "Very Poor"])
    questionnaire_anwers = myDlg.show()  # show dialog and wait for OK or Cancel
    if myDlg.OK:  # or if ok_data is not None
        return questionnaire_anwers
    else:
        print('user cancelled')


# let participant pause the experiment before each design (between each 20-questions-block)
def pause(text):
    win = visual.Window(monitor=mon, fullscr=FULLSCREEN, allowGUI=True,
                        screen=3, size=SCREEN_RES, units='deg')
    stim = visual.TextStim(win, text + "\n \n Click the left mouse button to start the experiment",
                           color=(1, 1, 1), colorSpace='rgb')
    # show instruction
    stim.draw()
    t = win.flip()
    buttons = myMouse.getPressed()
    # check for left mouse button and start design when it gets pressed
    while buttons != [1, 0, 0]:
        buttons = myMouse.getPressed()
        if buttons == [1, 0, 0]:
            break
    stim = visual.TextStim(win, "starting...",
                           color=(1, 1, 1), colorSpace='rgb')
    stim.draw()
    t = win.flip()
    core.wait(1, 0.5)
    win.close()


# design_id == 1: Question image question
# design_id == 2: Question image
# design_id == 3: Image question image
# design_id == 4: Image question
# design_id == 5: Sound
def design(design_id):
    if design_id == 1:
        text = "For this design you will see the question before the image and after"
    elif design_id == 2:
        text = "For this design you will see the question before the image but not after"
    elif design_id == 3:
        text = "For this design you will see the image then the question and then the image again"
    elif design_id == 4:
        text = "For this design you will see the image and then the question after"
    elif design_id == 5:
        text = "For this design you will hear the question 2 times before the image and 1 time after the image"

    pause(text)

    tracker.send_message(''.join(['design ', str(design_id), ' start']))

    # make list of images
    mypath = ''.join(['images for design ', str(design_id)])
    s = r'sound files for design 5'
    im_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(im_list)

    np.random.shuffle(im_list)  # shuffle images so they appear in a random order
    # create dictionary for answers
    answers = {}
    myMouse.setVisible(1)
    kb = keyboard.Keyboard()


    for element in im_list:
        # Window set-up (this color will be used for calibration)
        win = visual.Window(monitor=mon, fullscr=FULLSCREEN, allowGUI=True,
                            screen=3, size=SCREEN_RES, units='deg')
        # get image id
        x = os.path.normpath(element)
        x = os.path.basename(x)
        x = x.split('.')
        image_id = x[0]
        print(image_id)
        image = visual.ImageStim(win, image=mypath + '/' + element, units='norm', size=image_size)
        # for design 1,2 show questions
        if design_id == 1 or design_id == 2:
            stim = visual.TextStim(win, questions.questions[image_id][0] +
                                   '\n'
                                   '\n Click the left mouse button to see the image',
                                   color=(1, 1, 1), colorSpace='rgb')
        # for design 5 show different instruction and play sound twice
        elif design_id == 5:
            # play soundfile of the question
            soundfile_name = image_id + ".aiff"
            mySound = sound.Sound(os.path.join(s, soundfile_name))
            mySound.play()
            stim = visual.TextStim(win, 'Click the left mouse button to hear the question again',
                                   color=(1, 1, 1), colorSpace='rgb')
            stim.draw()
            t = win.flip()
            buttons = myMouse.getPressed()
            # check for left mouse button and move on when it gets pressed
            while buttons != [1, 0, 0]:
                buttons = myMouse.getPressed()
                if buttons == [1, 0, 0]:
                    break
            # play soundfile of the question again
            mySound.stop()
            mySound.play()
            core.wait(0.3, 0.2)
            stim = visual.TextStim(win, 'Click the left mouse button to see the image',
                                   color=(1, 1, 1), colorSpace='rgb')
        # for designs 3,4,5 show instructions
        elif design_id == 3 or design_id == 4:
            stim = visual.TextStim(win, 'Click the left mouse button to see the image',
                                   color=(1, 1, 1), colorSpace='rgb')
        # show question/instruction
        stim.draw()
        t = win.flip()
        tracker.send_message(''.join(['onset_', element, '_question1']))
        buttons = myMouse.getPressed()
        # check for left mouse button and move on when it gets pressed
        while buttons != [1, 0, 0]:
            buttons = myMouse.getPressed()
            if buttons == [1, 0, 0]:
                break
        tracker.send_message(''.join(['offset_', element, '_question1']))

        # show image for 3 seconds
        for i in range(stimulus_duration * monitor_refresh_rate):
            image.draw()
            t = win.flip()
            if design_id == 5:
                keys = kb.getKeys(['s'], waitRelease=False)
                if 's' in keys:
                    mySound.stop()
                    mySound.play()
            if i == 0:
                tracker.send_message(''.join(['onset_', element]))
        tracker.send_message(''.join(['offset_', element]))
        # for design_id 2,5 show only instruction
        if design_id == 2 or design_id == 5:
            # for design 5 play sound again
            if design_id == 5:
                mySound.play()
            stim = visual.TextStim(win, 'Click the left mouse button to answer question',
                                   color=(1, 1, 1), colorSpace='rgb')
            tracker.send_message(''.join(['onset_', element, '_question2']))
            stim.draw()
            win.flip()
        # for design 1,4 show question and instruction
        if design_id == 4 or design_id == 1:
            stim = visual.TextStim(win, questions.questions[image_id][0] +
                                   '\n'
                                   '\n Click the left mouse button to answer question',
                                   color=(1, 1, 1), colorSpace='rgb')
            tracker.send_message(''.join(['onset_', element, '_question2']))
            stim.draw()
            win.flip()
        # for design 3 wait for mouse press then show image again
        if design_id == 3:
            stim = visual.TextStim(win, questions.questions[image_id][0] +
                                   '\n'
                                   '\n Click the left mouse button to see the image',
                                   color=(1, 1, 1), colorSpace='rgb')
            tracker.send_message(''.join(['onset_', element, '_question2']))
            stim.draw()
            win.flip()
            # check for left mouse button and move an when it gets pressed
            buttons = myMouse.getPressed()
            while buttons != [1, 0, 0]:
                buttons = myMouse.getPressed()
                if buttons == [1, 0, 0]:
                    break
            tracker.send_message(''.join(['offset_', element, '_question2']))
            # show image
            for i in range(stimulus_duration * monitor_refresh_rate):
                image.draw()
                t = win.flip()
                if i == 0:
                    tracker.send_message(''.join(['onset_', element, '2']))
            tracker.send_message(''.join(['offset_', element, '2']))
            win.flip()
            # show instructions after image
            stim = visual.TextStim(win, 'Click the left mouse button to answer question',
                                   color=(1, 1, 1), colorSpace='rgb')
            tracker.send_message(''.join(['onset_', element, '_question3']))
            stim.draw()
            win.flip()
        # check for left mouse button and move on when it gets pressed
        buttons = myMouse.getPressed()
        while buttons != [1, 0, 0]:
            buttons = myMouse.getPressed()
            if buttons == [1, 0, 0]:
                break
        if design_id == 1 or design_id == 4 or design_id == 2 or design_id == 5:
            tracker.send_message(''.join(['offset_', element, '_question2']))
        if design_id == 3:
            tracker.send_message(''.join(['offset_', element, '_question3']))
        win.close()
        # create dialog window
        myDlg = gui.Dlg(title="Answer", screen=SCREEN_ID)
        questions.questions[image_id][1].append("I am not sure")
        myDlg.addField('Answer:', choices=questions.questions[image_id][1])
        answer = myDlg.show()  # save input in ok_data
        answers[image_id] = answer


    # create file to store answers
    with open('Answers for design ' + str(design_id) + ' by participant' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(answers))

    tracker.send_message(''.join(['design ', str(design_id), ' end']))

    questionnaire_anwers = create_questionnaire()

    # create file to store answers
    with open('Questionnaire for design ' + str(design_id) + ' by participant ' + str(participant_id) + '.txt',
              'w') as file:
        file.write(json.dumps(questionnaire_anwers))


# Training for participants, data will not be recorded
def training():
    # Window set-up (this color will be used for calibration)
    win = visual.Window(monitor=mon, fullscr=FULLSCREEN, allowGUI=True,
                        screen=3, size=SCREEN_RES, units='deg')

    # Define mouse
    myMouse = event.Mouse()

    # make list of images
    mypath = r'images for training'
    im_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(im_list)

    np.random.shuffle(im_list)  # shuffle images so they appear in a random order
    counter = 0
    # create dictionary for answers
    answers = {}

    stim = visual.TextStim(win,
                           "The order of question and image will change between different designs "
                           "\n"
                           "\n Images will always be shown for 3 seconds "
                           "\n"
                           "\n Questions and instructions will be shown until you press the left mouse button"
                           "\n"
                           "\n There will now be 3 example questions which will not be tracked",
                           color=(1, 1, 1), colorSpace='rgb')
    # show question
    stim.draw()
    t = win.flip()
    buttons = myMouse.getPressed()
    # check for left mouse button and move on when it gets pressed
    while buttons != [1, 0, 0]:
        buttons = myMouse.getPressed()
        if buttons == [1, 0, 0]:
            break
    win.close()

    # clear events and wait so mouse clicks get reset
    event.clearEvents()
    core.wait(0.1, 0.1)
    for element in im_list:
        # Window set-up (this color will be used for calibration)
        win = visual.Window(monitor=mon, fullscr=FULLSCREEN, allowGUI=True,
                            screen=3, size=SCREEN_RES, units='deg')
        # get image id
        x = os.path.normpath(element)
        x = os.path.basename(x)
        x = x.split('.')
        image_id = x[0]
        print(image_id)
        image = visual.ImageStim(win, image=mypath + '/' + element, units='norm', size=image_size)
        stim = visual.TextStim(win, questions.questions[image_id][0] +
                               "\n"
                               "\n Click the left mouse button to see the image",
                               color=(1, 1, 1), colorSpace='rgb')
        # show question
        stim.draw()
        t = win.flip()
        # check for left mouse button and move an when it gets pressed
        buttons = myMouse.getPressed()
        while buttons != [1, 0, 0]:
            buttons = myMouse.getPressed()
            if buttons == [1, 0, 0]:
                break
        for i in range(stimulus_duration * monitor_refresh_rate):
            image.draw()
            t = win.flip()
        stim = visual.TextStim(win, questions.questions[image_id][0] +
                               "\n"
                               "\n Click the left mouse button to answer the question",
                               color=(1, 1, 1), colorSpace='rgb')
        stim.draw()
        win.flip()
        # check for left mouse button and move an when it gets pressed
        buttons = myMouse.getPressed()
        while buttons != [1, 0, 0]:
            buttons = myMouse.getPressed()
        # create dialog window
        win.close()
        myDlg = gui.Dlg(title="Answer", screen=SCREEN_ID)
        questions.questions[image_id][1].append("I am not sure")
        myDlg.addField('Answer:', choices=questions.questions[image_id][1])
        answer = myDlg.show()  # save input in ok_data
        answers[image_id] = answer


create_pre_test_survey()


training()


# Window set-up (this color will be used for calibration)
win = visual.Window(monitor=mon, fullscr=FULLSCREEN, allowGUI=True,
                    screen=3, size=SCREEN_RES, units='deg')
# Define mouse
myMouse = event.Mouse()
stim = visual.TextStim(win, "click the left mouse button to begin",
                       color=(1, 1, 1), colorSpace='rgb')
stim.draw()
t = win.flip()
buttons = myMouse.getPressed()
# check for left mouse button and move an when it gets pressed
while buttons != [1, 0, 0]:
    buttons = myMouse.getPressed()
    if buttons == [1, 0, 0]:
        break
stim = visual.TextStim(win, "starting...",
                       color=(1, 1, 1), colorSpace='rgb')
stim.draw()
t = win.flip()
core.wait(1, 0.5)

# %% Connect to eye tracker and calibrate
tracker = Titta.Connect(settings)
if dummy_mode:
    tracker.set_dummy_mode()
tracker.init()

fixation_point = helpers.MyDot2(win)

#  Calibrate
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
        tracker.send_message(''.join(['onset_', 'baseline']))

tracker.send_message(''.join(['offset_', 'baseline']))

win.close()

# for counterbalancing implementing latin square
if participant_id % 5 == 1:
    design(design_id=1)
    design(design_id=2)
    design(design_id=3)
    design(design_id=5)
    design(design_id=4)
elif participant_id % 5 == 2:
    design(design_id=2)
    design(design_id=3)
    design(design_id=4)
    design(design_id=1)
    design(design_id=5)
elif participant_id % 5 == 3:
    design(design_id=3)
    design(design_id=5)
    design(design_id=2)
    design(design_id=4)
    design(design_id=1)
elif participant_id % 5 == 4:
    design(design_id=4)
    design(design_id=1)
    design(design_id=5)
    design(design_id=2)
    design(design_id=3)
elif participant_id % 5 == 0:
    design(design_id=5)
    design(design_id=4)
    design(design_id=1)
    design(design_id=3)
    design(design_id=2)

tracker.stop_recording(gaze_data=True)

# Close window and save data
win.close()
tracker.save_data(mon)  # Also save screen geometry from the monitor object

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
