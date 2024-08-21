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


if "count" not in st.session_state:
    st.session_state.count = 0

if "lastAdded" not in st.session_state:
    st.session_state.lastAdded = ""

total = 0
class Worker:
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



st.title('Welcome to Tipslit')
st.write("let's get rich. Fast.")

formCount = 1
instances = []
with st.form("my_form", clear_on_submit=True):
    st.write("Fill this form for each worker")
    name_input = st.text_input(label="Worker's name:")
    hours_input = st.text_input(label='Hours worked:')

    # Every form must have a submit button.
    submitted = st.form_submit_button("Add to list")
    if submitted:
        st.write( name_input, "added.")
        worker = f"instance_{st.session_state.count}"
        st.session_state.previousInstances.append(name_input)
        instances.append(Worker(name_input, hours_input, 1))
        st.session_state.instances.append({"name": name_input, "hours": hours_input})
        st.session_state.count += 1

with st.form("remover tool", clear_on_submit=True):
    st.write("Fill this form to remove a worker from the list")
    name_input = st.text_input(label="Worker's name:")

    # Every form must have a submit button.
    submitted = st.form_submit_button("remove")
    if submitted:
        st.write(name_input, "removed")
        st.session_state.instances = [instance for instance in st.session_state.instances
                                      if not (instance.get("name") == name_input)]


df = pd.DataFrame(
   st.session_state.instances
)
st.dataframe(df, use_container_width=True)
if st.button("remove last"):
    st.session_state.instances = [instance for instance in st.session_state.instances
                                  if not (instance.get("name") == st.session_state.previousInstances[-1])]
    st.session_state.previousInstances = st.session_state.previousInstances[:-1]
    st.rerun()
if st.button("reset form"):
    st.session_state.instances = []
    st.rerun()


with st.form("my_form2"):
    st.write("Fill this form with the collected tips")
    fifty_input = st.text_input(label="50:", value=0)
    twenty_input = st.text_input(label='20:', value=0)
    ten_input = st.text_input(label="10:", value=0)
    five_input = st.text_input(label='5:', value=0)
    two_input = st.text_input(label='2:', value=0)
    one_input = st.text_input(label='1:', value=0)
    fiftyP_input = st.text_input(label='0.50:', value=0)
    twentyP_input = st.text_input(label='0.20:', value=0)




    # Every form must have a submit button.
    submitted = st.form_submit_button("Update")
    if submitted:
        st.write( name_input, "added.")
        #if empty string, return 0
        if fifty_input == "": fifty_input = 0
        if twenty_input == "": twenty_input = 0
        if ten_input == "": ten_input = 0
        if five_input == "": five_input = 0
        if two_input == "": one_input = 0
        if one_input == "": one_input = 0
        if fiftyP_input == "": fiftyP_input = 0
        if twentyP_input == "": twentyP_input = 0

        st.session_state.money[0] = {
            "50": int(fifty_input), "20": int(twenty_input),
            "10": int(ten_input), "5": int(five_input),
            "1": int(one_input), "2": int(two_input),
            "0.50": int(fiftyP_input), "0.20": int(twentyP_input)}
        total = (st.session_state.money[0].get("50") * 50 +
                 st.session_state.money[0].get("20") * 20 +
                 st.session_state.money[0].get("10") * 10 +
                 st.session_state.money[0].get("5") * 5 +
                 st.session_state.money[0].get("2") * 2 +
                 st.session_state.money[0].get("1") * 1 +
                 st.session_state.money[0].get("0.50") * 0.5 +
                 st.session_state.money[0].get("0.20") * 0.2)

dfMoney = pd.DataFrame(
   st.session_state.money
)
st.dataframe(dfMoney, use_container_width=True)


st.write(f"total is {total}")



st.write(st.session_state.money)
st.write(st.session_state.instances)

def sortBiggerFirst(listOfWorkers):
    return sorted(listOfWorkers, key=lambda worker: worker.leftToPay, reverse=True)

def splitTips():
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
    listOfValues = []

    for entry in st.session_state.instances:
        name = entry.get("name")
        hours = float(entry.get("hours"))
        instances[name] = Worker(name, hours, 1)



    listOfWorkers = Worker.instances

    totalTips = 0
    for tender in cashList:
        totalTips += tender.value * tender.quantity
    totalLeftToPay = totalTips
    st.write(f'totaltips is {totalTips}')

    totalHours = 0
    for worker in listOfWorkers:
        totalHours += int(worker.hours) * worker.rate
    st.write(f'total full rate hour is {totalHours}')

    for worker in listOfWorkers:
        worker.ratioOfTotalTip = worker.hours * worker.rate / totalHours
        worker.totalTip = totalTips * worker.ratioOfTotalTip
        worker.leftToPay = worker.totalTip
        st.write(
            f'{worker.name} percent of total tip is {worker.ratioOfTotalTip * 100}%, its totalTip is {worker.totalTip}')

    st.write(f'total hours is {totalHours}, total tips is {totalTips}')

    test = 0
    for worker in listOfWorkers:
        test += worker.totalTip

    st.write(f'total of all worker tips is {test}')

    sortedList = sorted(listOfWorkers, key=lambda worker: worker.totalTip, reverse=True)
    totalWorkers = len(sortedList)

    for tender in cashList:
        st.write(f'there is {tender.quantity} units of {tender.value} value')
        while (tender.quantity > 0):
            tempListOfWorkers = sortBiggerFirst(listOfWorkers)
            for worker in tempListOfWorkers:
                if worker.leftToPay >= tender.value:
                    worker.breakdown[tender.indexForBreakdown] += 1
                    worker.leftToPay -= tender.value
                    tender.quantity -= 1
                    # print(
                    #    f'left to pay for {worker.name} is {worker.leftToPay} breakdown is {worker.breakdown} current tender is {tender.value}')
                    if tender.quantity == 0:
                        break
                else:
                    break

            if (tender.value < 1) & (tempListOfWorkers[0].leftToPay < 1):
                break
            if (tender.value > tempListOfWorkers[0].leftToPay):
                break

    for worker in listOfWorkers:
        st.write(f'\nWorker {worker.name} is owed {worker.totalTip} by the pool')
        totalWorkerTip = 0
        index = 0
        for tender in worker.breakdown:
            totalWorkerTip += tender * cashList[index].value
            index += 1
        st.write(f'its been awarded {totalWorkerTip}, with {worker.leftToPay} left')
        worker.tipsPaid = totalWorkerTip
        for tender in cashList:
            st.write(
                f'Worker {worker.name} was awarded {worker.breakdown[cashList.index(tender)]} tenders of {tender.value} value')
    st.write([tender.quantity for tender in cashList])

    for instances in Worker.instances:
        whiteSpace = 20 - len(instances.name)
        st.write(
            f'{whiteSpace * " "}{instances.name} is owed {round(instances.totalTip, 2)} pounds, and has been paid {instances.tipsPaid} bill breakdown is {instances.breakdown[0:4]}, coins is {instances.breakdown[4:]}')

    doubleCheckTotal = 0
    paidTips = 0

    for worker in Worker.instances:
        doubleCheckTotal += worker.totalTip
        paidTips += worker.totalTip - worker.leftToPay

    st.write(f'\nsum of all owed tips is {totalTips}')
    st.write(f'sum of all total tips by instance is {doubleCheckTotal}')
    st.write(f'sum of all paid tips is {paidTips}')

if st.button("DO IT"):
    splitTips()