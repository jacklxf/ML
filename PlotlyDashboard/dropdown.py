import dashimport dash_core_components as dccimport dash_html_components as htmldropdown=dash.Dash()dropdown.layout=html.Div([html.Label('Dropdown'),                     dcc.Dropdown(                         options=[                             {'lable':'New York City','value':'NYC'},                             {'label':'Montreal','value':'MTL'},                             {'label':'San Francisco','value':'SF'}                         ],                         value='MTL'                     ),                     html.Label('Multi-Select Dropdown'),                     dcc.Dropdown(                         options=[                             {'lable':'New York City','value':'NYC'},                             {'label':'Montreal','value':'MTL'},                             {'label':'San Francisco','value':'SF'}                         ]                     ),                     html.Label('Radio Items'),                     dcc.RadioItems(                         options=[                             {'lable': 'New York City', 'value': 'NYC'},                             {'label': 'Montreal', 'value': 'MTL'},                             {'label': 'San Francisco', 'value': 'SF'}                         ]                     ),                     html.Label('Sider'),                     dcc.Slider(                         min=0,                         max=9,                         marks={i:'Label{}'.format(i) if i ==1 else str(i) for i in range(1,6)},                         value=5,                        ),                     ],style={'columnCount':2})if __name__=='__main__':    dropdown.run_server(debug=True)