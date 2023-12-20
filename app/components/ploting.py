import plotly.graph_objects as go
import pandas as pd


class Plotting:
  # check verifie que la data existe bien sinon on print un message d'erreur
    def check(self, result, graph_description):
        return result if result is not None else "result pas valide"
 # process crée le plot si check est valide
    def process(self, graph_description, result):

        try:
            if Plotting.check:
                for indicateur, cle in graph_description.items():
                    name = None
                    data = result
                    type_plot = cle["type_plot"]
                    plot_options = cle["plot_options"]

                    if len(data) > 0 and type(data[-1]) == pd.core.frame.DataFrame:
                            data[-1] = data[-1][data[-1].columns[0]]

                    if len(data) > 1 and type(data[-2]) == pd.core.frame.DataFrame:
                        name = data[-2].columns[0]
                        data[-2] = data[-2][data[-2].columns[0]]


        # on éxécute le plot en fonction du type de plot
                    if type_plot == "pie":
                        #data[-1] must be the result of pd.values_counts
                        fig = go.Figure(data=[go.Pie(labels=data[-2], values=data[-1], **plot_options)])
                    elif type_plot == "indicator":
                        fig = go.Figure(go.Indicator(mode="number+delta", value=data[-1], **plot_options))
                    elif type_plot == "gauge":
                        fig = go.Figure(go.Indicator(mode="gauge+number+delta", value=data[-1], **plot_options))
                    elif type_plot == "hist":
                        print(len(data))
                        fig = go.Figure(data=[go.Histogram(x=data[-1], **plot_options)])
                    elif type_plot == "map":
                        fig = go.Figure(data=[go.Choropleth(geojson=data, **plot_options)])
                    elif type_plot == "bar":
                        print("ploting")
                        print(type(data[-1]))
                        print(data[-1])
                        print(type(data[-2]))
                        print(data[-2])
                        
                        #fig = go.Figure(data=[go.Bar(x=data[-2][data[-2].columns[0]], y=data[-1][data[-1].columns[0]], **plot_options)])
                        fig = go.Figure(data=[go.Bar(x=data[-2], y=data[-1], name=name, **plot_options)])
                        print(f"names {name}")
                    else:
                        print(f"Type de plot non supporté: {type_plot}")

                    fig.update_layout(title_text=indicateur)
                    if "filters" in graph_description and len(graph_description["filters"]) > 0:
                        for filter_ in graph_description["filters"]:
                            if filter_["name"] == "slider":
                                fig.update_xaxes(rangeslider_visible=True)
                       
                    fig.update_layout(showlegend=True)
                    return fig, None
            else:
                return "check n'est pas valide"
        except Exception as e:
            return None, f"an  error ocurred in Ploting process {e}"