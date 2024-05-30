import streamlit as st
import pandas as pd
from utils.utils import *

def metriche():
    col1,col2,col3=st.columns(3)
    #st.markdown(f"{st.session_state['connection']}")
    #payment_info=execute_query(st.session_state["connection"],"SELECT SUM(amount) AS 'Total Amount', MAX(amount) AS 'Max Payment', AVG(amount) AS 'Average Payment' FROM payments;")
    q1=execute_query(st.session_state["connection"],"SELECT DISTINCT COUNT(*) as con FROM AGENZIA;")
    q2=execute_query(st.session_state["connection"],"SELECT COUNT(DISTINCT Citta_Indirizzo) as con FROM AGENZIA;")
    q3=execute_query(st.session_state["connection"],"WITH TAB AS (SELECT COUNT(*) as MAXI, Citta_Indirizzo FROM AGENZIA GROUP BY Citta_Indirizzo) SELECT Citta_Indirizzo as ci FROM TAB WHERE MAXI=(SELECT MAX(MAXI) FROM TAB)")

    nAgenzie=[dict(zip(q1.keys(), result)) for result in q1]
    nCitta=[dict(zip(q2.keys(), result)) for result in q2]
    nomeCitta=[dict(zip(q3.keys(), result)) for result in q3]
    col1.metric("Numero di agenzie", f"{nAgenzie[0]['con']}")
    col2.metric("Numero di città", f"{nCitta[0]['con']}")
    col3.metric("Nome di città", f"{nomeCitta[0]['ci']}")
    #creare una struttura dati adatti dal risultato della query
    #payment_info_dict= [dict(zip(payment_info.keys(), result)) for result in payment_info]
    #aggiungere come metriche orizzontali i parametri selezionati
    #col1.metric('Importo Totale',f"$ {compact_format(payment_info_dict[0]['Total Amount'])}")
    #col2.metric('Pagamento Massimo',f"$ {compact_format(payment_info_dict[0]['Max Payment'])}")
    #col3.metric('Pagamento Medio',f"$ {compact_format(payment_info_dict[0]['Average Payment'])}")



def mappa(map):
    q=execute_query(st.session_state["connection"],"SELECT Latitudine AS lat, longitudine AS LON FROM CITTA, AGENZIA WHERE Citta_Indirizzo=Nome;")
    df = pd.DataFrame(q, columns=['lat', 'lon'])
    map.map(df)

def tabella():
    cityName=st.text_input("Filtra per città")
    if cityName=='':
        query="SELECT Citta_Indirizzo,CONCAT(Via_Indirizzo,' ',Numero_Indirizzo) AS 'Indirizzo' FROM AGENZIA;"
    else:
        query=f"SELECT Citta_Indirizzo,CONCAT(Via_Indirizzo,' ',Numero_Indirizzo) AS 'Indirizzo' FROM `AGENZIA` WHERE Citta_Indirizzo='{cityName}'"

    cityInfo=execute_query(st.session_state["connection"],query)
    df_info=pd.DataFrame(cityInfo)
    st.dataframe(df_info,use_container_width=True)



if __name__ == "__main__":
    st.title("📈 Agenzia")

    #creazione dei tab distinti
    
    #se la connessione al DB è avvenuta, mostrare i dati
    if check_connection():
        metriche()
        map=st.expander("mappa")
        mappa(map)
        tabella()

