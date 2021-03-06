#Imports
from dash import html
import altair as alt

from data import load_data
from app import cache


#Reading data
wind = load_data()

#Function for creating bar graph for total capacity as per province
@cache.memoize(timeout=50)
def plot_capacity(province: str = None) -> str:  
    """
    A function that displays the total capacity of wind turbines per province.
    
    Parameters:
    -----------
    prov: the 12 Canadian provinces/territories.
    
    Returns:
    --------
    An altair bar chart in html format for Dash
    """
    
    province_capacity = wind.groupby("Province/Territory", as_index=False).aggregate("sum").sort_values(by="Turbine rated capacity (kW)", ascending=False)
    province_capacity["Turbine rated capacity (kW)"] /= 1000
    province_capacity = province_capacity.rename(columns={"Turbine rated capacity (kW)": "Total Capacity (MW)","Province/Territory":"Province"})

    chart=alt.Chart(
        province_capacity, 
        title="Total Wind Capacity by Province"
    ).mark_bar().encode(
        x=alt.X("Total Capacity (MW)"),
        y=alt.Y("Province", sort=province_capacity["Province"].to_list()),
        color=alt.condition(
            alt.datum.Province == province,  
            alt.value('red'),     
            alt.value('lightgrey')),
         tooltip=["Province","Total Capacity (MW)","Total project capacity (MW)"]
    )
    return chart.to_html()

#Plot to save the output of the total capacity bar graph
plot_totalCapacity = html.Iframe(
    id='capacity-plot',
    style={
        'border-width': '0', 
        'width': '250%',
        'height': '400px', 
        "padding-left": "20px"
    },
    srcDoc=plot_capacity(province=None)
)