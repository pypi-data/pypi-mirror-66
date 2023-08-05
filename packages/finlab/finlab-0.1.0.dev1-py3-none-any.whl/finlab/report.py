from IPython.display import display, HTML, IFrame, clear_output
import plotly.graph_objs as go
import datetime
import ipywidgets as widgets
import ffn
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from .chart import chart
import sys
import IPython

class Report():
    
    def __init__(self, report, data=None):
        self.__data_query = data
        self.data = report
        self.performance_panel = widgets.Output(layout=widgets.Layout(width='100%'))
        self.stock_table_panel = widgets.Output(layout=widgets.Layout(width='100%'))
        self.stock_chart_panel = widgets.Output(layout=widgets.Layout(width='100%'))
        self.edge_cases_panel = widgets.Output(layout=widgets.Layout(width='100%'))
        self.ohlc = None
        self.tab = None
        self.adj_close = None
        self.buy_color = '#ff6183'
        self.sell_color = '#58d6ac'
        self.additional_data = {}
        
    def add_additional_data(self, name, data, overlap=False):
        self.additional_data[name] = (data, overlap)
        
    def __repr__(self):

        IN_COLAB = 'google.colab' in sys.modules
        
        self.tab = widgets.Tab()
        self.tab.children = [self.performance_panel, self.stock_table_panel, self.stock_chart_panel, self.edge_cases_panel]
        self.tab.titles = ['performance', 'stock list', 'price chart', 'win loss cases']
        self.tab.set_title(0, "performance")
        self.tab.set_title(1, "stock list")
        self.tab.set_title(2, "price chart")
        self.tab.set_title(3, "win loss cases")
        
        self.generate_figure()
        self.generate_edge_cases()
        self.generate_table_according_to_date(str(max(self.data['transaction'].end_date).date()))

        display(self.tab)
        return ''

    def generate_figure(self, figure_type='widget'):

        # calculate performance
        rr = self.data['returns']
        benchmark = self.data['benchmark']
        performance = (pd.DataFrame({'benchmark': benchmark, 'strategy': rr}).ffill().pct_change()+1).cumprod().dropna(how='all')
        performance = performance.reindex(rr.index).fillna(1)
        
        nstocks = self.data['nstocks'].reindex(rr.index)
        dd = (performance.strategy/performance.strategy.cummax()) - 1
        bdd = (performance.benchmark/performance.benchmark.cummax()) - 1
        dd = dd.reindex(rr.index)
        bdd = bdd.reindex(rr.index)
        
        
        IN_COLAB = 'google.colab' in sys.modules
        if IN_COLAB:
            fig = go.Figure(make_subplots(rows=4, cols=1, shared_xaxes=True, row_heights=[2,1,1,1]))
        else:
            fig = go.FigureWidget(make_subplots(rows=4, cols=1, shared_xaxes=True, row_heights=[2,1,1,1]))

        fig.add_scatter(x=performance.index, y=performance.strategy, name='strategy', row=1, col=1, legendgroup='performnace', fill='tozeroy')
        fig.add_scatter(x=performance.index, y=performance.benchmark, name='benchmark', row=1, col=1, legendgroup='performance', line={'color': 'gray'})
        
        fig.add_scatter(x=dd.index, y=dd, name='strategy - drawdown', row=2, col=1, legendgroup='drawdown', fill='tozeroy')
        fig.add_scatter(x=bdd.index, y=bdd, name='benchmark - drawdown', row=2, col=1, legendgroup='drawdown', line={'color': 'gray'})
        
        def diff(s, period):
            return (s / s.shift(period)-1)

        fig.add_scatter(x=performance.index, y=diff(performance.strategy, 20), 
                        fill='tozeroy', name='strategy - month rolling return', 
                        row=3, col=1, legendgroup='rolling performance',)
        fig.add_scatter(x=performance.index, y=diff(performance.benchmark, 20), 
                        fill='tozeroy', name='benchmark - month rolling return', 
                        row=3, col=1, legendgroup='rolling performance', line={'color': 'rgba(0,0,0,0.2)'})

        fig.add_scatter(x=nstocks.index, y=nstocks, row=4, col=1, name='nstocks', fill='tozeroy')
        fig.update_layout(legend={'bgcolor': 'rgba(0,0,0,0)'},
                          margin=dict(l=60, r=20, t=40, b=20),
                          height=600,
                          xaxis4=dict(
                              rangeselector=dict(
                                  buttons=list([
                                      dict(count=1,
                                           label="1m",
                                           step="month",
                                           stepmode="backward"),
                                      dict(count=6,
                                           label="6m",
                                           step="month",
                                           stepmode="backward"),
                                      dict(count=1,
                                           label="YTD",
                                           step="year",
                                           stepmode="todate"),
                                      dict(count=1,
                                           label="1y",
                                           step="year",
                                           stepmode="backward"),
                                      dict(step="all")
                                  ]),
                                  x=0,
                                  y=1,
                              ),
                              rangeslider={'visible': True, 'thickness': 0.1},
                              type="date",
                          ),
                          yaxis={'tickformat':',.0%',},
                          yaxis2={'tickformat':',.0%',},
                          yaxis3={'tickformat':',.0%',},
                          #xaxis4={'rangeslider':{'visible': True, 'thickness': 0.1}}
                          #xaxis4_rangeslider_visible=True, xaxis4_rangeslider_thickness=0.1,
        )

        if IN_COLAB:
            return fig.show()

        def update_ds_image(layout, x_range):
            
            sdate = x_range[0].split()[0]
            edate = x_range[1].split()[0]
            bratio = performance.benchmark.loc[sdate:].iloc[0]
            sratio = performance.strategy.loc[sdate:].iloc[0]

            data0 = performance.strategy.values / sratio
            data1 = performance.benchmark.values / bratio

            y_min = (performance.loc[sdate:edate].min().loc[['benchmark', 'strategy']] / [bratio, sratio]).min()
            y_max = (performance.loc[sdate:edate].max().loc[['benchmark', 'strategy']] / [bratio, sratio]).max()
            
            fig.data[0]['y'] = data0
            fig.data[1]['y'] = data1
            fig.layout.yaxis.range = [y_min * 0.9, y_max * 1.1]

        fig.layout.on_change(update_ds_image, 'xaxis4.range')

        def update_point(trace, points, selector):
            if not points.xs:
                return
            fig.update_layout(shapes=[
                dict(
                  type= 'line',
                  yref= 'paper', y0= 0, y1= 1,
                  xref= 'x', x0=points.xs[0], x1=points.xs[0],line={'color': 'gray'}
                )
            ])

            self.generate_table_according_to_date(points.xs[0])
            
        fig.data[0].on_click(update_point)
        with self.performance_panel:
            clear_output(True)
            display(fig)
            test = self.data['returns'].calc_stats()
            test.name = 'strategy'
            display(test.display())
            
        return fig
    
    def generate_edge_cases(self):
        self.data['transaction'].index.name = 'stock_id'
        t = self.data['transaction'].reset_index()
        targets = t['return'].nlargest(10).index
        table_win = self.generate_stock_table(t.loc[targets])
        
        targets = t['return'].nsmallest(10).index
        table_loss = self.generate_stock_table(t.loc[targets])
        
        if self.tab is None:
            return table
        
        self.tab.children = list(self.tab.children[:3]) + [widgets.VBox([table_win, table_loss])]
        
        return table_win, table_loss
        

    def generate_table_according_to_date(self, d):
        
        panel_exist = isinstance(self.tab.children[1], widgets.VBox)
        
        if not panel_exist:
            d = self.data['returns'].index[-1]
        
        # calculate subtable of transaction
        self.data['transaction'].index.name = 'stock_id'
        t = self.data['transaction'].reset_index()
        targets = (t.start_date <= d) & ((t.end_date >= d) | (t.end_date.isna()))
        display_table = t[targets].sort_values(['stock_id'])
        table = self.generate_stock_table(display_table, d)
        daily_return = 'daily return ' + str(round((self.data['returns'][:d].iloc[-1] / self.data['returns'][:d].iloc[-2]-1)*10000)/100)+'%'
        
        # without gui
        if self.tab is None:
            return table
        
        
        
        # update gui panel
        if panel_exist:
            self.tab.children[1].children = (self.tab.children[1].children[0], table)
            self.tab.children[1].children[0].children[1].value = daily_return
            self.tab.children[1].children[0].children[0].value = d
            return table
        
        # create gui panel
        dates = self.data['returns'].loc[min(self.data['transaction'].start_date):].index.astype(str).str.split().str[0].to_list()
        date_slider =  widgets.SelectionSlider(
            options=dates,
            value=dates[-1],
            description='position',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            layout=widgets.Layout(width='50%')
        )
        date_slider.observe(lambda changes: self.generate_table_according_to_date(changes['new']), names='value')
        self.tab.children = (self.tab.children[0], widgets.VBox([widgets.HBox([date_slider, widgets.Text(daily_return)]), table]), self.tab.children[2], self.tab.children[3])
        return table
            
        
    def generate_stock_table(self, display_table, d=None):
        
        if self.adj_close is None and self.__data_query:
            
            adj_close = (self.__data_query.get("return")/100+1).cumprod()
            self.adj_close = adj_close

        # calculate present return
        if d and self.adj_close is not None:
            
            daily_return = self.adj_close.loc[:d, display_table.stock_id].iloc[-1] / self.adj_close.loc[:d, display_table.stock_id].iloc[-2]-1
            display_table['daily_return'] = daily_return.values
            display_table.loc[display_table.start_date == d, 'daily_return'] = 0
            display_table.loc['mean'] = display_table.mean()
            display_table.loc['mean', 'stock_id'] = 'mean'
            
        
        if d:
            # calculate actions
            buy_ids  = set(display_table.loc[display_table.start_date == pd.Timestamp(d)].stock_id)
            sell_ids = set(display_table.loc[display_table.end_date == pd.Timestamp(d)].stock_id)
        
        display_table.start_date = display_table.start_date.astype(str).str.split(' ').str[0]
        display_table.end_date = display_table.end_date.astype(str).str.split(' ').str[0]
        
        def color_buy_sell(val):
            if d is None:
                return 'background-color: white'
            color = self.buy_color if val in buy_ids else self.sell_color if val in sell_ids else 'white'
            return 'background-color: %s' % color

        def hover(hover_color="eeee99"):
            return dict(selector="tr:hover",
                        props=[("background-color", "%s" % hover_color)])

        styles = [
            hover(),
            #dict(selector="th", props=[("text-align", "right")]),
            dict(selector="td", props=[("text-align", "right")]),
            dict(selector="th", props=[("text-align", "right")]),
            dict(selector="table", props=[('table-layout', 'auto'), ('width', '100%')]),
            dict(selector='td', props=[('width', '100px')])
            #dict(selector="caption", props=[("caption-side", "bottom")])
        ]
        
        subtable = ['stock_id', 'start_date', 'end_date', 'start_price', 'end_price', 'return']
        percentage_col =  ['return']
        
        if 'daily_return' in display_table.columns:
            subtable.append('daily_return')
            percentage_col.append('daily_return')
        
        table_html = (display_table[subtable]
            .style
            .set_table_styles(styles)
            .applymap(color_buy_sell, subset=['stock_id'])
            .format("{:.2%}", subset=percentage_col)
            .bar(subset=percentage_col, align='zero', color=[self.buy_color, self.sell_color])
            .hide_index()
        ).render(table_title="Extending Example", )

        table_html = widgets.HTML(table_html)
        btns = [widgets.Button(description='inspect', 
                               layout=widgets.Layout(width='100%', min_height='25px'), 
                               ) for i in range(len(display_table)+1)]
        btns[0].style.button_color = 'white'
        btns[0].description = ''
        
        def call_chart(e):
            self.generate_stock_chart(int(e.description))
            if self.tab:
                self.tab.selected_index = 2

        for i, (tid, info) in enumerate(display_table.iterrows()):
            btns[i+1].on_click(call_chart)
            btns[i+1].description = str(tid)
        table = widgets.HBox([
            table_html, 
            widgets.VBox(btns, layout=widgets.Layout(height=str((len(display_table)+1) * 32)+'px', overflow='visible'))
        ])
        
        return table
        
    def generate_stock_chart(self, case_id):
        
        if self.ohlc is None:
            close = self.__data_query.get('收盤價')
            open_ = self.__data_query.get('開盤價')
            high = self.__data_query.get('最高價')
            low = self.__data_query.get('最低價')
            vol = self.__data_query.get('成交量')
            self.ohlc = {'close': close, 'open': open_, 'high': high, 'low': low, 'volume': vol}
        else:
            close, open_, high, low, vol = self.ohlc['close'], self.ohlc['open'], self.ohlc['high'], self.ohlc['low'], self.ohlc['volume']

        case = self.data['transaction'].iloc[case_id]
        sid = case.name

        dfstock = pd.DataFrame(
            np.array([open_[sid].values, close[sid].values, low[sid].values, high[sid].values, vol[sid].values]).T,
            columns=['open', 'close', 'low', 'high', 'volume'],
            index=close.index)
        
        def process_data(data):
            if isinstance(data, pd.DataFrame):
                return data[sid].loc[dfstock.index[0]: dfstock.index[-1]]
            elif isinstance(data, pd.Series):
                return data.loc[dfstock.index[0]: dfstock.index[-1]]
            elif isinstance(data, dict):
                return {name:process_data(df) for name, df in data.items()}
            elif isinstance(data, tuple):
                return (process_data(data[0]), data[1])
            else:
                raise
        
        overlaps = {name: process_data(data) for name, (data, overlap) in self.additional_data.items() if overlap}
        figures = {name: process_data(data) for name, (data, overlap) in self.additional_data.items() if not overlap}
        sdate = case.start_date
        edate = case.end_date if not pd.isnull(case.end_date) else case.start_date
        c, info = chart(dfstock,
            overlaps=overlaps,
            figures=figures,
            marks=[
                ('b', case.start_date),
                (str(round(case['return']*1000)/10) + '%', edate),
            ],
            start_date=str(sdate - datetime.timedelta(days=365)),
            end_date=str(edate + datetime.timedelta(days=365))
        )
        c.load_javascript()
        c.render()
        #html = IFrame("render.html", width="600px", height="500px")#
        html = HTML('<iframe src="render.html" height="'+str(info['height']+50)+'px" width="100%" frameBorder="0" seamless></iframe>')
        
        with self.stock_chart_panel:
            clear_output(True)
            display(html)

        IN_COLAB = 'google.colab' in sys.modules
        if IN_COLAB:
            return IPython.display.HTML(filename="render.html")
            
        return html