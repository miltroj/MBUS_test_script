from plotly import tools
import plotly.offline as offline
import plotly.graph_objs as go
import time

def create_chart(y1, y2, x_time):
    # trace_1 = (x_time,
    #             y1)
    # trace_2 = (x_time,
    #             y2)
    #
    # fig = tools.make_subplots(rows=2 , cols=1)
    #
    # fig.append_trace(trace_1 , 1,1)
    # fig.append_trace(trace_2 , 2,1)
    #
    # fig['layout'].update(height=600, width=600, title='i <3 subplots')
    # offline.plot(fig, filename='simple-subplot')
    #
    offline.plot({'data': [{'y': y1, 'x': x_time, 'mode': 'lines+markers', 'name': 'przeplyw chwilowy'},
                           {'y': y2, 'x': x_time, 'mode': 'lines+markers', 'name': 'przeplyw calkowity'}],
                  'layout': {'title': 'Przeplywy',
                             'font': dict(size=16)}})

    #
    # offline.plot({'data': [{'y': y1, 'x': x_time, 'mode': 'lines+markers', 'name': 'pierwszy'},
    #                        {'y': y2, 'x': x_time, 'mode': 'lines+markers', 'name': 'drugi'}],
    #               'layout': {'title': 'Przebiegi',
    #                          'font': dict(size=16)}} , {'data2': [{'y': y1, 'x': x_time, 'mode': 'lines+markers', 'name': 'pierwszy2'},
    #                {'y': y2, 'x': x_time, 'mode': 'lines+markers', 'name': 'drugi2'}],
    #               'layout': {'title': 'Przebiegi222',
    #                          'font': dict(size=16)}})


def create_avg_flow_chart(y1, x_time):
    offline.plot({'data': [{'y': y1, 'x': x_time, 'mode': 'lines+markers', 'name': 'przeplyw chwilowy'},],
                  'layout': {'title': 'AVG Flow',
                             'font': dict(size=16)}})
    time.sleep(1)

def create_overall_flow_chart(y1, x_time):
    offline.plot({'data': [{'y': y1, 'x': x_time, 'mode': 'lines+markers', 'name': 'przeplyw chwilowy'},],
                  'layout': {'title': 'Overall Flow',
                             'font': dict(size=16)}})
    time.sleep(1)

#region events charts
def ret_events_ocred_tab(table_of_events,count):
    temp_table = []
    # print("Len %r" %count)
    for tab_events in table_of_events:
        # print("event %r count %r" %(tab_events,count))
        if tab_events[count] is 0:
            temp_table.append(0)
        elif tab_events[count] is 1:
            temp_table.append( tab_events[count] + count )
    return temp_table

def evnts_len_check(tab_data,tab_all):
    if len(tab_data[0]) > 8:
        tab_events = tab_all
        chart_name = 'Events saved'
    else:
        tab_events = tab_all[:8]
        chart_name = 'Actual events'
    return tab_events, chart_name

def create_chart_events(tab_data, x_time):
    temp_dict_table = []
    tab_all_events  = ['pole magnetyczne', 'silne oswietlenie', 'odlaczenie', 'brak przeplywu', 'przeplyw minimalny',
                       'przeplyw maksymalny', 'przeplyw wsteczny', 'wyciek', 'reset procesora', 'blad wskazowki',
                       'niskie nap baterii', 'uszkodzony detektor']
    tab_given_events, chart_name = evnts_len_check(tab_data,tab_all_events)
    for count in range(len(tab_given_events)):
        temp_tb_element = ret_events_ocred_tab(tab_data,count)
        # print("%r" %tab_given_events[ count ])
        temp_dict_table.append( {'y': temp_tb_element, 'x': x_time, 'mode': 'lines+markers', 'name': tab_given_events[ count ] } )
    offline.plot({'data': temp_dict_table,
                  'layout': {'title': chart_name,
                         'font': dict(size=16)}})
#endregion
if __name__ == '__main__':

    x_8 = [[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0]]
    x_16 = [[1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],[1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    y1 = [[1,2,3,4,5,6,7],[i for i in range(3,10)]]
    y11 = [1,2,3,4,5,6,7]
    y2 = [i for i in range(1,7)]

    # create_two_charts(y1,y2,x)
    # for ele in x:
    #     print(ele[0])
    # # print(x[0][0])
    create_chart_events(x_8,y11)
    time.sleep(2)
    create_chart_events(x_16,y11)