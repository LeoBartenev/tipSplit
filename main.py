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
        if one_input == "": one_input = 0
        if fiftyP_input == "": fiftyP_input = 0
        if twentyP_input == "": twentyP_input = 0

        st.session_state.money[0] = {"50": int(fifty_input), "20": int(twenty_input),
             "10": int(ten_input), "5": int(five_input),
             "1": int(one_input), "0.50": int(fiftyP_input), "0.20": int(twentyP_input)}
        total = (st.session_state.money[0].get("50") * 50 +
                 st.session_state.money[0].get("20") * 20 +
                 st.session_state.money[0].get("10") * 10 +
                 st.session_state.money[0].get("5") * 5 +
                 st.session_state.money[0].get("1") * 1 +
                 st.session_state.money[0].get("0.50") * 0.5 +
                 st.session_state.money[0].get("0.20") * 0.2)

dfMoney = pd.DataFrame(
   st.session_state.money
)
st.dataframe(dfMoney, use_container_width=True)
st.write(st.session_state.money)


st.write(f"total is {total}")


st.write(st.session_state.instances)