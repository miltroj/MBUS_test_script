from plotly import tools
import plotly.offline as offline
import plotly.graph_objs as go

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


def create_two_charts(y1, y2, x_time):
    offline.plot({'data': [{'y': y1, 'x': x_time, 'mode': 'lines+markers', 'name': 'przeplyw chwilowy'},],
                  'layout': {'title': 'Przeplywy',
                             'font': dict(size=16)}})
    offline.plot({'data1': [{'y': y2, 'x': x_time, 'mode': 'lines+markers', 'name': 'przeplyw calkowity'}],
                  'layout': {'title': 'Przeplywy',
                             'font': dict(size=16)}})

if __name__ == '__main__':

    x = [1,2,3,4,5,6,7]
    y1 = [i for i in range(100,107)]
    y2 = [i for i in range(1,7)]

    create_two_charts(y1,y2,x)