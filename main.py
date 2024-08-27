import streamlit as st
import pandas as pd
import numpy as np

if "instances" not in st.session_state:
    st.session_state.instances = [{"name": "name", "hours": "0"}]

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


class Tender:
    def __init__(self, quantity, value, indexForBreakdown):
        self.quantity = quantity
        self.value = value
        self.indexForBreakdown = indexForBreakdown


def update_worker_instances(data):
    st.session_state.instances = [worker for worker in data
                                  if worker["name"] and worker["hours"]]
    st.session_state.workerFilledFlag = True


def reset_worker_instance_data():
    # empty the currently held worker's datas
    st.session_state.instances =  [{ "name" : "name", "hours" : "0"}]
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
    # returns the sum of all tenders in st.session_state.money
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
        You can use the file uploader to import a previous dataset. If you don't have one, you can create 
        one in the next form"
    ''')
    st.write('''
            The Second form create, add, edit data regarding the team you're splitting tips with.
            Give a unique name for every worker, and write how many hours they worked on the right of the same line.
            When everything is added, press update, and double check the infos in the summary below.
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

uploaded_file = st.file_uploader("Upload an existing team log")
if uploaded_file is not None:
    df1 = pd.read_csv(uploaded_file)
    # if you upload a file you reset the session_state
    st.session_state.instances = []
    for i, j in df1.iterrows():
        nextIndex = str(len(st.session_state.instances))
        st.session_state.instances.append({
            "name": j["name"],
            "hours": j["hours"],
        })
    st.session_state.workerFilledFlag = True


st.write("You can add and edit worker's data here.")
edited_df = st.data_editor(
    st.session_state.instances,
    key="editor",
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "name" : st.column_config.TextColumn("name"),
        "hours" : st.column_config.NumberColumn("hours")
    },


)

if st.button("Update"):
    if edited_df is not None and not edited_df == st.session_state.instances:
        # This will only run if
        # 1. Some widget has been changed (including the dataframe editor), triggering a
        # script rerun, and
        # 2. The new dataframe value is different from the old value
        update_worker_instances(edited_df)
        st.rerun()


st.write("You can see the workers you added here.")
df = pd.DataFrame(st.session_state.instances).iloc[:, 1:]
st.dataframe(st.session_state.instances, use_container_width=True)


with st.form("my_form2"):
    st.write("Fill this form with the collected tips")
    fifty_input = st.number_input(label="Number of 50 notes:", value=0, min_value=0)
    twenty_input = st.number_input(label='Number of 20 notes:', value=0, min_value=0)
    ten_input = st.number_input(label="Number of 10 notes:", value=0, min_value=0)
    five_input = st.number_input(label='Number of 5 notes:', value=0, min_value=0)
    two_input = st.number_input(label='Number of 2 coins:', value=0, min_value=0)
    one_input = st.number_input(label='Number of 1 coins:', value=0, min_value=0)
    fiftyP_input = st.number_input(label='Number of 0.50 coins:', value=0, min_value=0)
    twentyP_input = st.number_input(label='Number of 0.20 coins:', value=0, min_value=0)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Update")
    if submitted:
        # if empty string, return 0
        #if fifty_input == "": fifty_input = 0
        #if twenty_input == "": twenty_input = 0
        #if ten_input == "": ten_input = 0
        #if five_input == "": five_input = 0
        #if two_input == "": one_input = 0
        #if one_input == "": one_input = 0
        #if fiftyP_input == "": fiftyP_input = 0
        #if twentyP_input == "": twentyP_input = 0

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
    # check if the forms have been filled
    if st.session_state.moneyFilledFlag and st.session_state.workerFilledFlag:
        # create the tip pool
        twenty_p = Tender(st.session_state.money[0].get("0.20"), 0.2, 7)
        fifty_p = Tender(st.session_state.money[0].get("0.50"), 0.5, 6)
        pound = Tender(st.session_state.money[0].get("1"), 1, 5)
        two_pound = Tender(st.session_state.money[0].get("2"), 2, 4)
        five_pound = Tender(st.session_state.money[0].get("5"), 5, 3)
        ten_pound = Tender(st.session_state.money[0].get("10"), 10, 2)
        twenty_pound = Tender(st.session_state.money[0].get("20"), 20, 1)
        fifty_pound = Tender(st.session_state.money[0].get("50"), 50, 0)

        cash_list = [fifty_pound, twenty_pound, ten_pound, five_pound, two_pound, pound, fifty_p, twenty_p]

        # believe it or not, this loops through the statesessions worker values
        # to create workers objects
        instances = {}
        # creates the Worker objects
        for entry in st.session_state.instances:
            name = entry.get("name")
            hours = float(entry.get("hours"))
            instances[name] = Worker(name, hours, 1)

        # Accessing the static list of workers
        list_of_workers = Worker.instances

        total_tips = 0
        for tender in cash_list:
            total_tips += tender.value * tender.quantity
        st.write(f'total tips is {total_tips}')

        total_hours = 0
        for worker in list_of_workers:
            total_hours += float(worker.hours) * worker.rate
        st.write(f'total full rate hours is {total_hours}')

        # initialise each worker split of the tip pool
        for worker in list_of_workers:
            worker.ratioOfTotalTip = worker.hours * worker.rate / total_hours
            worker.totalTip = total_tips * worker.ratioOfTotalTip
            worker.leftToPay = worker.totalTip

        # distribute each type of tender, starting with the larger
        for tender in cash_list:
            while tender.quantity > 0:
                # prioritise whoever is owed more first
                temp_list_of_workers = sortBiggerFirst(list_of_workers)
                for worker in temp_list_of_workers:
                    if worker.leftToPay >= tender.value:
                        worker.breakdown[tender.indexForBreakdown] += 1
                        worker.leftToPay -= tender.value
                        worker.tipsPaid += tender.value
                        tender.quantity -= 1
                        if tender.quantity == 0:
                            break
                    else:
                        break
                if tender.value > temp_list_of_workers[0].leftToPay:
                    break

        paid_tips = 0

        for worker in Worker.instances:
            paid_tips += worker.totalTip - worker.leftToPay

        st.write(f'\nsum of all owed tips is {total_tips}')
        st.write(f'sum of all paid tips is {paid_tips}')

        tips_summary_data = []
        for instance in Worker.instances:
            tips_summary_data.append({
                "name": instance.name,
                "50": instance.breakdown[0],
                "20": instance.breakdown[1],
                "10": instance.breakdown[2],
                "5": instance.breakdown[3],
                "2": instance.breakdown[4],
                "1": instance.breakdown[5],
                "0.5": instance.breakdown[6],
                "0.2": instance.breakdown[7],
                "owed": round(instance.totalTip, 2),
                "paid": instance.tipsPaid,
                "hours": instance.hours,
                "% of tips": (instance.ratioOfTotalTip * 100),

            })

        tips_summary = pd.DataFrame(tips_summary_data)
        st.write("Tips summary:")
        st.dataframe(tips_summary, use_container_width=True)

        cash_summary_data = [{
            "50": cash_list[0].quantity,
            "20": cash_list[1].quantity,
            "10": cash_list[2].quantity,
            "5": cash_list[3].quantity,
            "2": cash_list[4].quantity,
            "1": cash_list[5].quantity,
            "0.50": cash_list[6].quantity,
            "0.20": cash_list[7].quantity,

        }]

        cash_summary = pd.DataFrame(cash_summary_data)
        st.write("what remains in the tip pool:")
        st.dataframe(cash_summary, use_container_width=True)
        st.write("You might need to break bigger bills as I'm just an app and cannot always split it.")
    else:
        st.write("fill all the forms first you naughty sausage!")


if st.button("DO IT"):
    splitTips()

