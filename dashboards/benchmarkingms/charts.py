import plotly.graph_objects as go

def scatterChart(self, column):
        subject, score, nombreLotes = [], [], []
        for index, row in self.datasource.getDf().iterrows():
            subject.append(row["farmname"])
            score.append(row[column])
            nombreLotes.append(row["name"])
        data = [dict(
            type = 'scatter',   
            x = subject,
            y = score,
            customdata = nombreLotes,
            mode = 'markers',
            marker = dict(symbol = 'star', size = 13, line = dict(color='white', width=1.5), color = '#3e703f'))]
        fig = go.Figure(data = data)
        fig.update_traces(
            hovertemplate = 'Lote: %{customdata} <br>Valor: %{y: .2f}<extra></extra>'
        )
        fig.update_layout(
            hoverlabel = dict(
                font_size = 16,
                font_family = "Roboto"
            ),margin = dict(l=0, r=0, b=0, t=0), font=dict(size = 13)
        )
        return fig
        