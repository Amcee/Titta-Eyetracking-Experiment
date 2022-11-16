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
from questions import questions1, questions2, questions3, questions4, questions5, questionsTraining

# initialize participant ID
participant_id = 1

# %%  Monitor/geometry
MY_MONITOR = 'testMonitor'  # needs to exists in PsychoPy monitor center
SCREEN_ID = 1
FULLSCREEN = False
SCREEN_RES = [1920, 1080]
SCREEN_WIDTH = 52.7  # cm
VIEWING_DIST = 68  # distance from eye to center of screen (cm)

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


# create NASA-TLX Questionnaire
def create_questionnaire():
    myDlg = gui.Dlg(title="Questionnaire", screen=SCREEN_ID)
    choices = ["Very Low", "Low", "Somewhat Low", "Neutral", "Somewhat High", "High", "Very High"]
    myDlg.addText('How much mental and perceptual activity was required (e.g., thinking, deciding, calculating, '
                  'remembering, looking, searching, etc.)? Was the task easy or demanding, simple or complex, '
                  'exacting or forgiving?')
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
    if myDlg.OK:  # or if ok_data is not None
        print(questionnaire_anwers)
    else:
        print('user cancelled')


# let participant pause the experiment before each design (between each 20-questions-block)
def pause():
    stim = visual.TextStim(win, "click the left mouse button to start the experiment",
                           color=(1, 1, 1), colorSpace='rgb')
    # show instruction
    stim.draw()
    t = win.flip()
    buttons = myMouse.getPressed()
    # check for left mouse button and start design when it gets pressed
    while buttons == [0, 0, 0]:
        buttons = myMouse.getPressed()
        if buttons == [1, 0, 0]:
            break
    stim = visual.TextStim(win, "starting...",
                           color=(1, 1, 1), colorSpace='rgb')
    stim.draw()
    t = win.flip()
    core.wait(1, 0.5)


# Design order: Task Image Task
def design1():
    pause()

    tracker.send_message('design 1 start')

    # make list of images
    mypath = r'images for design 1'
    im_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(im_list)

    images = []  # create list of stimuli images
    for element in im_list:
        images.append(visual.ImageStim(win, image=mypath + '/' + element, units='norm', size=(2, 2)))

    np.random.shuffle(images)  # shuffle images so they appear in a random order
    counter = 0
    # create dictionary for answers
    answers = {}
    for image in images:
        win.flip()
        im_name = image.image
        # get image id
        x = os.path.normpath(im_name)
        x = os.path.basename(x)
        x = x.split('.')
        image_id = x[0]
        print(image_id)
        stim = visual.TextStim(win, questions1.questions_list[image_id][0],
                               color=(1, 1, 1), colorSpace='rgb')
        # show question
        stim.draw()
        t = win.flip()
        buttons = myMouse.getPressed()
        # check for left mouse button and move an when it gets pressed
        while buttons == [0, 0, 0]:
            buttons = myMouse.getPressed()
            if buttons == [1, 0, 0]:
                break
        for i in range(stimulus_duration * monitor_refresh_rate):
            image.draw()
            t = win.flip()
            if i == 0:
                tracker.send_message(''.join(['onset_', im_name]))
        tracker.send_message(''.join(['offset_', im_name]))
        stim.draw()
        win.flip()
        # create dialog window
        myDlg = gui.Dlg(title="Answer", screen=2)
        myDlg.addField('Answer:', choices=questions1.questions_list[image_id][1])
        answer = myDlg.show()  # save input in ok_data
        answers[image_id] = answer

        counter += 1
        if counter == 3:
            break

    # create file to store answers
    with open('Answers for design 1 by participant' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(answers))

    win.flip()

    tracker.send_message('design 1 end')

    create_questionnaire()

    # create file to store answers
    with open('Questionnaire for design 1 by participant ' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(questionnaire_anwers))


# Sound design
def design2():
    pause()

    tracker.send_message('design 2 start')

    # make list of images
    mypath = r'images for design 2'
    im_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(im_list)

    images = []  # create list of stimuli images
    for element in im_list:
        images.append(visual.ImageStim(win, image=mypath + '/' + element, units='norm', size=(2, 2)))

    s = r'sound files for design 2'
    np.random.shuffle(images)  # shuffle images so they appear in a random order
    counter = 0
    # create dictionary for answers
    answers = {}
    kb = keyboard.Keyboard()
    for image in images:
        kb.clearEvents()
        win.flip()
        im_name = image.image
        # get image id
        x = os.path.normpath(im_name)
        x = os.path.basename(x)
        x = x.split('.')
        image_id = x[0]
        print(image_id)
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
        kb.clearEvents()
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
        kb.clearEvents()
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
        kb.clearEvents()
        # create dialog window
        myDlg = gui.Dlg(title="Answer", screen=2)
        myDlg.addField('Answer:', choices=questions2.questions_list2[image_id][1])
        answer = myDlg.show()  # save input in answer
        answers[image_id] = answer  # save answer in answers dictionary with image_id as key

        counter += 1
        if counter == 3:
            break

    # create file to store answers
    with open('Answers for design 2 by participant' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(answers))

    win.flip()

    tracker.send_message('design 2 end')

    create_questionnaire()

    # create file to store answers
    with open('Questionnaire for design 2 by participant ' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(questionnaire_anwers))


# Design order: Task Image
def design3():
    pause()

    tracker.send_message('design 3 start')

    # make list of images
    mypath = r'images for design 3'
    im_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(im_list)

    images = []  # create list of stimuli images
    for element in im_list:
        images.append(visual.ImageStim(win, image=mypath + '/' + element, units='norm', size=(2, 2)))

    np.random.shuffle(images)  # shuffle images so they appear in a random order
    counter = 0
    # create dictionary for answers
    answers = {}
    for image in images:
        win.flip()
        im_name = image.image
        # get image id
        x = os.path.normpath(im_name)
        x = os.path.basename(x)
        x = x.split('.')
        image_id = x[0]
        print(image_id)
        stim = visual.TextStim(win, questions3.questions_list3[image_id][0],
                               color=(1, 1, 1), colorSpace='rgb')
        # show question
        stim.draw()
        t = win.flip()
        buttons = myMouse.getPressed()
        # check for left mouse button and move an when it gets pressed
        while buttons == [0, 0, 0]:
            buttons = myMouse.getPressed()
            if buttons == [1, 0, 0]:
                break
        for i in range(stimulus_duration * monitor_refresh_rate):
            image.draw()
            t = win.flip()
            if i == 0:
                tracker.send_message(''.join(['onset_', im_name]))
        tracker.send_message(''.join(['offset_', im_name]))
        win.flip()
        # create dialog window
        myDlg = gui.Dlg(title="Answer", screen=2)
        myDlg.addField('Answer:', choices=questions3.questions_list3[image_id][1])
        answer = myDlg.show()  # save input in ok_data
        answers[image_id] = answer

        counter += 1
        if counter == 3:
            break

    # create file to store answers
    with open('Answers for design 3 by participant' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(answers))

    win.flip()

    tracker.send_message('design 3 end')

    create_questionnaire()

    # create file to store answers
    with open('Questionnaire for design 3 by participant ' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(questionnaire_anwers))


# Design order: Image Task Image
def design4():
    pause()

    tracker.send_message('design 4 start')

    # make list of images
    mypath = r'images for design 4'
    im_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(im_list)

    images = []  # create list of stimuli images
    for element in im_list:
        images.append(visual.ImageStim(win, image=mypath + '/' + element, units='norm', size=(2, 2)))

    np.random.shuffle(images)  # shuffle images so they appear in a random order
    counter = 0
    # create dictionary for answers
    answers = {}
    for image in images:
        win.flip()
        im_name = image.image
        # get image id
        x = os.path.normpath(im_name)
        x = os.path.basename(x)
        x = x.split('.')
        image_id = x[0]
        print(image_id)
        stim = visual.TextStim(win, questions4.questions_list4[image_id][0],
                               color=(1, 1, 1), colorSpace='rgb')
        buttons = myMouse.getPressed()
        # check for left mouse button and move an when it gets pressed
        while buttons == [0, 0, 0]:
            buttons = myMouse.getPressed()
            if buttons == [1, 0, 0]:
                break
        # show image
        for i in range(stimulus_duration * monitor_refresh_rate):
            image.draw()
            t = win.flip()
            if i == 0:
                tracker.send_message(''.join(['onset_', im_name, '1']))
                # need to add a number at the end because the same picture gets shown twice at each trial
        tracker.send_message(''.join(['offset_', im_name, '1']))
        # show question
        stim.draw()
        t = win.flip()
        buttons = myMouse.getPressed()
        # check for left mouse button and move an when it gets pressed
        while buttons == [0, 0, 0]:
            buttons = myMouse.getPressed()
            if buttons == [1, 0, 0]:
                break
        # show image
        for i in range(stimulus_duration * monitor_refresh_rate):
            image.draw()
            t = win.flip()
            if i == 0:
                tracker.send_message(''.join(['onset_', im_name, '2']))
        tracker.send_message(''.join(['offset_', im_name, '2']))
        win.flip()
        # create dialog window
        myDlg = gui.Dlg(title="Answer", screen=2)
        myDlg.addField('Answer:', choices=questions4.questions_list4[image_id][1])
        answer = myDlg.show()  # save input in ok_data
        answers[image_id] = answer

        counter += 1
        if counter == 3:
            break

    # create file to store answers
    with open('Answers for design 4 by participant ' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(answers))

    win.flip()

    tracker.send_message('design 4 end')

    create_questionnaire()

    # create file to store answers
    with open('Questionnaire for design 4 by participant ' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(questionnaire_anwers))


# Design order: Image Task
def design5():
    pause()

    tracker.send_message('design 5 start')

    # make list of images
    mypath = r'images for design 5'
    im_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print(im_list)

    images = []  # create list of stimuli images
    for element in im_list:
        images.append(visual.ImageStim(win, image=mypath + '/' + element, units='norm', size=(2, 2)))

    np.random.shuffle(images)  # shuffle images so they appear in a random order
    counter = 0
    # create dictionary for answers
    answers = {}
    for image in images:
        win.flip()
        im_name = image.image
        # get image id
        x = os.path.normpath(im_name)
        x = os.path.basename(x)
        x = x.split('.')
        image_id = x[0]
        print(image_id)
        stim = visual.TextStim(win, questions5.questions_list5[image_id][0],
                               color=(1, 1, 1), colorSpace='rgb')
        buttons = myMouse.getPressed()
        # check for left mouse button and move an when it gets pressed
        while buttons == [0, 0, 0]:
            buttons = myMouse.getPressed()
            if buttons == [1, 0, 0]:
                break
        for i in range(stimulus_duration * monitor_refresh_rate):
            image.draw()
            t = win.flip()
            if i == 0:
                tracker.send_message(''.join(['onset_', im_name]))
        tracker.send_message(''.join(['offset_', im_name]))
        stim.draw()
        win.flip()
        # create dialog window
        myDlg = gui.Dlg(title="Answer", screen=2)
        myDlg.addField('Answer:', choices=questions5.questions_list5[image_id][1])
        answer = myDlg.show()  # save input in ok_data
        answers[image_id] = answer

        counter += 1
        if counter == 3:
            break

    # create file to store answers
    with open('Answers for design 5 by participant ' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(answers))

    win.flip()

    tracker.send_message('design 5 end')

    create_questionnaire()

    # create file to store answers
    with open('Questionnaire for design 5 by participant ' + str(participant_id) + '.txt', 'w') as file:
        file.write(json.dumps(questionnaire_anwers))


# create Pre-test Survey
myDlg = gui.Dlg(title="Pre-test Survey", screen=SCREEN_ID)
myDlg.addField('What is your gender?:', choices=["Male", "Female", "Other"])
myDlg.addField('Age:')
myDlg.addField('How many years did you have English as a subject in school?:',
               choices=["5 or fewer", "6 to 10", "11 or more"])
myDlg.addField('What is the highest degree or level of education you have completed?:',
               choices=["Middle School", "High School", "Bachelor's Degree or higher", "Prefer not to say"])
survey = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # or if ok_data is not None
    print(survey)
else:
    print('user cancelled')

# create file to store answers
with open('Pre-test Survey by participant ' + str(participant_id) + '.txt', 'w') as file:
    file.write(json.dumps(survey))

# Window set-up (this color will be used for calibration)
win = visual.Window(monitor=mon, fullscr=FULLSCREEN,
                    screen=2, size=SCREEN_RES, units='deg')

# Define mouse and make it so Mouse is visible
myMouse = event.Mouse(visible=True)

# Training for participants, data will not be recorded
# make list of images
mypath = r'images for training'
im_list = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(im_list)

images = []  # create list of stimuli images
for element in im_list:
    images.append(visual.ImageStim(win, image=mypath + '/' + element, units='norm', size=(2, 2)))

np.random.shuffle(images)  # shuffle images so they appear in a random order
counter = 0
# create dictionary for answers
answers = {}

stim = visual.TextStim(win,
                       "The order of question and image will change between the different designs "
                       "\n Images will always be shown for 3 seconds "
                       "\n questions will be shown until you press the left mouse button",
                       color=(1, 1, 1), colorSpace='rgb')
# show question
stim.draw()
t = win.flip()
buttons = myMouse.getPressed()
# check for left mouse button and move an when it gets pressed
while buttons == [0, 0, 0]:
    buttons = myMouse.getPressed()
    if buttons == [1, 0, 0]:
        break

for image in images:
    win.flip()
    im_name = image.image
    # get image id
    x = os.path.normpath(im_name)
    x = os.path.basename(x)
    x = x.split('.')
    image_id = x[0]
    print(image_id)
    stim = visual.TextStim(win, questionsTraining.questions_Training[image_id][0],
                           color=(1, 1, 1), colorSpace='rgb')
    # show question
    stim.draw()
    t = win.flip()
    buttons = myMouse.getPressed()
    # check for left mouse button and move an when it gets pressed
    while buttons == [0, 0, 0]:
        buttons = myMouse.getPressed()
        if buttons == [1, 0, 0]:
            break
    for i in range(stimulus_duration * monitor_refresh_rate):
        image.draw()
        t = win.flip()
    stim.draw()
    win.flip()
    # create dialog window
    myDlg = gui.Dlg(title="Answer", screen=2)
    myDlg.addField('Answer:', choices=questionsTraining.questions_Training[image_id][1])
    answer = myDlg.show()  # save input in ok_data
    answers[image_id] = answer

stim = visual.TextStim(win, "click the left mouse button to begin",
                       color=(1, 1, 1), colorSpace='rgb')
stim.draw()
t = win.flip()
buttons = myMouse.getPressed()
# check for left mouse button and move an when it gets pressed
while buttons == [0, 0, 0]:
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
        tracker.send_message('fix on')
        tracker.send_message(''.join(['onset_', 'baseline']))

tracker.send_message('fix off')
tracker.send_message(''.join(['offset_', 'baseline']))

# for counterbalancing implementing latin square
if participant_id % 5 == 1:
    design1()
    design2()
    design3()
    design5()
    design4()
elif participant_id % 5 == 2:
    design2()
    design3()
    design4()
    design1()
    design5()
elif participant_id % 5 == 3:
    design3()
    design5()
    design2()
    design4()
    design1()
elif participant_id % 5 == 4:
    design4()
    design1()
    design5()
    design2()
    design3()
elif participant_id % 5 == 0:
    design5()
    design4()
    design1()
    design3()
    design2()

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
