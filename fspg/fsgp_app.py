import streamlit as st
import asyncio

st.title('FSGP Application')

# State initialization
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.time1 = 0
    st.session_state.time2 = 0
    st.session_state.timer1State = False
    st.session_state.progress1 = 100
    st.session_state.currLaps1 = ""
    st.session_state.lapsNeeded = ""
    st.session_state.currDist1 = 0
    st.session_state.currSpeed1 = 0
    st.session_state.totalDist1 = 0

st.subheader("Timer 1")
def onClick():
    st.session_state.timer1State = not st.session_state.timer1State

def onReset():
    st.session_state.timer1State = False
    st.session_state.time1 = 0

buttonContainer = st.empty()
if st.session_state.timer1State:
    button1 = buttonContainer.button("Stop", on_click=onClick)
else:
    button1 = buttonContainer.button("Start", on_click=onClick)

rst1 = st.button("Reset", on_click=onReset)

timer1 = st.empty()
h = st.session_state.time1//3600
m = (st.session_state.time1//60) % 60
s = st.session_state.time1//1 % 60
timer1.write(f"{h:02d}:{m:02d}:{s:02d}")

st.subheader("Speed and Progress")
def calculateCurrLapDistance():
    testData = [100, 50, 250, 30]
    if st.session_state.currLaps1 == "":
        currLaps = 0
    try:
        currLaps = int(st.session_state.currLaps1)
    except:
        return
    if currLaps > len(testData):
        currLaps = len(testData)
    totalDist = 0
    for i in range(currLaps):
        totalDist += testData[i]
    st.session_state.currDist1 = totalDist
    st.session_state.currSpeed1 = st.session_state.currDist1/max(st.session_state.time1, 1)
    if st.session_state.totalDist1 != 0:
        st.session_state.progress1 = min(int(100*st.session_state.currDist1/st.session_state.totalDist1), 100)
    else:
        st.session_state.progress1 = 100

def calculateTotalDistance():
    testData = [100, 50, 250, 30]
    if st.session_state.lapsNeeded == "":
        totalLaps = 0
    try:
        totalLaps = int(st.session_state.lapsNeeded)
    except:
        return
    if totalLaps > len(testData):
        totalLaps = len(testData)
    totalDist = 0
    for i in range(totalLaps):
        totalDist += testData[i]
    st.session_state.totalDist1 = totalDist
    if st.session_state.totalDist1 != 0:
        st.session_state.progress1 = min(int(100*st.session_state.currDist1/st.session_state.totalDist1), 100)
    else:
        st.session_state.progress1 = 100
    

st.text_input("Current lap:", key="currLaps1" , on_change=calculateCurrLapDistance())
st.text_input("Number of laps needed:", key="lapsNeeded", on_change=calculateTotalDistance())

currSpeed1 = st.empty()
currSpeed1.write(f"Current speed: {st.session_state.currSpeed1:.2f} m/s")
progress1 = st.empty()
progress1.progress(st.session_state.progress1)

async def stopwatch(timer1):
    while True:
        if st.session_state.timer1State:
            h = st.session_state.time1//3600
            m = (st.session_state.time1//60) % 60
            s = st.session_state.time1//1 % 60
            timer1.write(f"{h:02d}:{m:02d}:{s:02d}")
            st.session_state.currSpeed1 = st.session_state.currDist1/max(st.session_state.time1, 1)
            currSpeed1.write(f"Current speed: {st.session_state.currSpeed1:.2f} m/s")
            st.session_state.time1 += 1

        await asyncio.sleep(1)
    
asyncio.run(stopwatch(timer1))