import streamlit as st
import pandas as pd
import numpy as np

if "instances" not in st.session_state:
    st.session_state.instances = []

if "previousInstances" not in st.session_state:
    st.session_state.previousInstances = []

if "workerInstances" not in st.session_state:
    st.session_state.workerInstances = []

if "money" not in st.session_state:
    st.session_state.money = [{}]

if "lastAdded" not in st.session_state:
    st.session_state.lastAdded = ""

if "workerFilledFlag" not in st.session_state:
    st.session_state.workerFilledFlag = False

if "moneyFilledFlag" not in st.session_state:
    st.session_state.moneyFilledFlag = False

class Worker:
    # this is the class that holds the data concerning each worker
    instances = []

    def __init__(self, name, hours, rate):
        self.name = name
        self.hours = hours
        self.rate = rate
        # breakdown is the breakdown of the
        # exact number of money by different
        # value of tender, from 50 pounds to 20 pence
        self.breakdown = [0, 0, 0, 0, 0, 0, 0, 0]
        self.ratioOfTotalTip = 0
        self.totalTip = 0
        self.tipsPaid = 0
        self.leftToPay = 0
        self.__class__.instances.append(self)

    # TODO create a reset instances method




class Tender:
    def __init__(self, quantity, value, indexForBreakdown):
        self.quantity = quantity
        self.value = value
        self.indexForBreakdown = indexForBreakdown

def add_worker(name, hours):
    # adds a worker from session memory
    if (isinstance(name, str)) and (isinstance(float(hours), float)):
        st.write(name, "added.")
        st.session_state.previousInstances.append(name)
        st.session_state.instances.append({"name": name, "hours": hours})
        st.session_state.workerFilledFlag = True
        st.write(len(st.session_state.instances))
        st.write(st.session_state.instances)
    else:
        st.write("Looks like the form isn't properly filled.")

def remove_worker(name):
    # removes the worker from session memory
    if name in st.session_state.previousInstances:
        st.write(name, "removed")
        st.session_state.instances = [instance for instance in st.session_state.instances
                                      if not (instance.get("name") == name)]
        st.session_state.previousInstances.remove(name)
        if len(st.session_state.instances) == 0:
            st.session_state.workerFilledFlag = False
        # rerun to display the data properly
        st.rerun()
    else:
        st.write(name, " is not in the list")

def remove_last_worker_added():
    # removes the last worker added with the top form
    st.session_state.instances = [instance for instance in st.session_state.instances
                                  if not (instance.get("name") == st.session_state.previousInstances[-1])]
    st.session_state.previousInstances = st.session_state.previousInstances[:-1]
    if len(st.session_state.instances) == 0:
        st.session_state.workerFilledFlag = False
    st.rerun()

def reset_worker_instance_data():
    #empty the currently held worker's datas
    st.session_state.instances = []
    st.session_state.previousInstances = []
    st.session_state.workerFilledFlag = False
    st.rerun()

def update_money_instance(fifty, twenty, ten, five, two, one, fiftyP, twentyP):
    st.session_state.money[0] = {
        "50": int(fifty), "20": int(twenty),
        "10": int(ten), "5": int(five),
        "2": int(two), "1": int(one),
        "0.50": int(fiftyP), "0.20": int(twentyP)}
    st.write(f"total is {get_total_money()}")
    st.session_state.moneyFilledFlag = True

def get_total_money():
    #returns the sum of all tenders in st.session_state.money
    return (st.session_state.money[0].get("50") * 50 +
                 st.session_state.money[0].get("20") * 20 +
                 st.session_state.money[0].get("10") * 10 +
                 st.session_state.money[0].get("5") * 5 +
                 st.session_state.money[0].get("2") * 2 +
                 st.session_state.money[0].get("1") * 1 +
                 st.session_state.money[0].get("0.50") * 0.5 +
                 st.session_state.money[0].get("0.20") * 0.2)


st.title('Welcome to TipSplit')
st.write("Because doing math after a long shift is not fun.")

with st.expander("How to use this app"):
    st.write('''
        First form has to be filled with a unique worker's name, and the number of hour worked. When you press 
        "Add to list" you will see what you added in the table below.
    ''')
    st.write('''
            The Second form lets you remove a worker from the table. Just enter the worker's name, and press 
            "remove". Below the table, you also have a button that removes the last entered entry, and 
            one that resets the whole thing.
        ''')
    st.write('''
        The last form gathers the number of coins and bills that have to be added to the tip pool. 
        For each respective value, enter how many bills/coins of the respective value you collected. 
        Press update, and you'll see under the form a table with all of it.
    ''')
    st.write('''
        When you added all workers, and the money that has to be shared, press "DO IT", and the app will 
        display how to split the tips. The last table will appear, each line representing a 
        worker, and how many bills/coins it's owed.''')
    st.write('''
    Lastly, if you're nice and fill everything as intended, it works lmao, but if for some reason 
    you broke the app, on the top right of your screen, you can tap on the three dot and rerun. Refresh the
    whole thing if it's not enough. Or just count like a caveman.''')
    st.write("Known issues:")
    st.write('''
       While you can download the last table, on mobile it doesn't always automatically
       get the .csv extension, which makes it unrecognisable on your phone. To read it you need to add ".csv"
       to the end of the file name''')

# this creates a form
with st.form("my_form", clear_on_submit=True):
    st.write("Fill this form for each worker")

    name_input = st.text_input(label="Worker's name:")
    hours_input = st.text_input(label='Hours worked:')

    # this creates a button in the form
    submitted = st.form_submit_button("Add to list")
    if submitted:
        add_worker(name_input, hours_input)


with st.form("remover tool", clear_on_submit=True):
    st.write("Fill this form to remove a worker from the list")

    name_input = st.text_input(label="Worker's name:")

    submitted = st.form_submit_button("remove")
    if submitted:
        remove_worker(name_input)


uploaded_file = st.file_uploader("Upload an existing team log")
if uploaded_file is not None:
    df1 = pd.read_csv(uploaded_file)
    df1 = df1.iloc[:, 1:]
    #if you upload a file you reset the session_state
    st.session_state.instances = []
    for i, j in df1.iterrows():

        #instances.append(Worker(j["name"], j["hours"], 1))
        nextIndex = str(len(st.session_state.instances))
        st.session_state.instances.append({
            "name" : j["name"],
            "hours" : j["hours"],
        })
        #st.write(j["hours"])
        #st.write(j["name"])
    #st.write(df1)
    #st.write(st.session_state.instances)


    st.session_state.workerFilledFlag = True

st.write("You can see the workers you added here.")
df = pd.DataFrame(st.session_state.instances)
st.dataframe(df, use_container_width=True)

# TODO use a data editor instead of a dataframe
#st.data_editor(df, use_container_width=True)
if st.button("remove last"):
    remove_last_worker_added()

if st.button("reset form"):
    reset_worker_instance_data()

with st.form("my_form2"):
    st.write("Fill this form with the collected tips")
    fifty_input = st.text_input(label="Number of 50 notes:", value=0)
    twenty_input = st.text_input(label='Number of 20 notes:', value=0)
    ten_input = st.text_input(label="Number of 10 notes:", value=0)
    five_input = st.text_input(label='Number of 5 notes:', value=0)
    two_input = st.text_input(label='Number of 2 coins:', value=0)
    one_input = st.text_input(label='Number of 1 coins:', value=0)
    fiftyP_input = st.text_input(label='Number of 0.50 coins:', value=0)
    twentyP_input = st.text_input(label='Number of 0.20 coins:', value=0)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Update")
    if submitted:
        #if empty string, return 0
        if fifty_input == "": fifty_input = 0
        if twenty_input == "": twenty_input = 0
        if ten_input == "": ten_input = 0
        if five_input == "": five_input = 0
        if two_input == "": one_input = 0
        if one_input == "": one_input = 0
        if fiftyP_input == "": fiftyP_input = 0
        if twentyP_input == "": twentyP_input = 0

        update_money_instance(fifty_input, twenty_input,
                              ten_input, five_input,
                              two_input, one_input,
                              fiftyP_input, twentyP_input)

# shows a table with the money summary
dfMoney = pd.DataFrame(
   st.session_state.money
)
st.dataframe(dfMoney, use_container_width=True)






def sortBiggerFirst(listOfWorkers):
    # returns a list of Workers, biggest leftToPay first
    return sorted(listOfWorkers, key=lambda worker: worker.leftToPay, reverse=True)

def splitTips():
    #check if the forms have been filled
    if st.session_state.moneyFilledFlag and st.session_state.workerFilledFlag:
        # create the tip pool
        twentyP = Tender(st.session_state.money[0].get("0.20"), 0.2, 7)
        fiftyP = Tender(st.session_state.money[0].get("0.50"), 0.5, 6)
        pound = Tender(st.session_state.money[0].get("1"), 1, 5)
        twoPound = Tender(st.session_state.money[0].get("2"), 2, 4)
        fivePound = Tender(st.session_state.money[0].get("5"), 5, 3)
        tenPound = Tender(st.session_state.money[0].get("10"), 10, 2)
        twentyPound = Tender(st.session_state.money[0].get("20"), 20, 1)
        fiftyPound = Tender(st.session_state.money[0].get("50"), 50, 0)

        cashList = [fiftyPound, twentyPound, tenPound, fivePound, twoPound, pound, fiftyP, twentyP]

         # believe it or not, this loops through the statesessions worker values
        # to create workers objects
        instances = {}
        # creates the Worker objects
        for entry in st.session_state.instances:
            name = entry.get("name")
            hours = float(entry.get("hours"))
            instances[name] = Worker(name, hours, 1)

        # Accessing the static list of workers
        listOfWorkers = Worker.instances

        totalTips = 0
        for tender in cashList:
            totalTips += tender.value * tender.quantity
        st.write(f'total tips is {totalTips}')

        totalHours = 0
        for worker in listOfWorkers:
            totalHours += float(worker.hours) * worker.rate
        st.write(f'total full rate hours is {totalHours}')

        # initialise each worker split of the tip pool
        for worker in listOfWorkers:
            worker.ratioOfTotalTip = worker.hours * worker.rate / totalHours
            worker.totalTip = totalTips * worker.ratioOfTotalTip
            worker.leftToPay = worker.totalTip

        # distribute each type of tender, starting with the larger
        for tender in cashList:
            while (tender.quantity > 0):
                # prioritise whoever is owed more first
                tempListOfWorkers = sortBiggerFirst(listOfWorkers)
                for worker in tempListOfWorkers:
                    if worker.leftToPay >= tender.value:
                        worker.breakdown[tender.indexForBreakdown] += 1
                        worker.leftToPay -= tender.value
                        worker.tipsPaid += tender.value
                        tender.quantity -= 1
                        if tender.quantity == 0:
                            break
                    else:
                        break
                if (tender.value > tempListOfWorkers[0].leftToPay):
                    break

        paidTips = 0

        for worker in Worker.instances:
            paidTips += worker.totalTip - worker.leftToPay

        st.write(f'\nsum of all owed tips is {totalTips}')
        st.write(f'sum of all paid tips is {paidTips}')

        tipBoardData = []
        for instance in Worker.instances:
            tipBoardData.append({
                "name" : instance.name,
                "50" : instance.breakdown[0],
                "20" : instance.breakdown[1],
                "10" : instance.breakdown[2],
                "5" : instance.breakdown[3],
                "2" : instance.breakdown[4],
                "1" : instance.breakdown[5],
                "0.5" : instance.breakdown[6],
                "0.2" : instance.breakdown[7],
                "owed" : round(instance.totalTip, 2),
                "paid" : instance.tipsPaid,
                "hours" : instance.hours,
                "% of tips" : (instance.ratioOfTotalTip * 100),

            })

        TPD = pd.DataFrame(
            tipBoardData
        )
        st.write("Tips summary:")
        st.dataframe(TPD, use_container_width=True)

        cashLeftBoard = [{
            "50" : cashList[0].quantity,
            "20": cashList[1].quantity,
            "10": cashList[2].quantity,
            "5": cashList[3].quantity,
            "2": cashList[4].quantity,
            "1": cashList[5].quantity,
            "0.50": cashList[6].quantity,
            "0.20": cashList[7].quantity,

        }]

        CLB = pd.DataFrame(cashLeftBoard)
        st.write("what remains in the tip pool:")
        st.dataframe(CLB, use_container_width=True)
        st.write("You might need to break bigger bills as I'm just an app and cannot always split it.")
    else:
        st.write("fill all the forms first you naughty sausage!")
if st.button("DO IT"):
    splitTips()

