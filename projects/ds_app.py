from shiny import App, render, ui
import matplotlib.pyplot as plt
from ds_model import OECDDataProcessor
import os

# Initialize data processor
# For local and Posit Cloud, ensure the path is correct
csv_path = os.path.join(os.path.dirname(__file__), "data", "alc_tob.csv")
processor = OECDDataProcessor(csv_path)

# UI
app_ui = ui.page_fluid(
    ui.h2("OECD Health Risk Factors Analysis"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select("country", "Select Country", choices=processor.get_countries(), selected="United States"),
            ui.input_select("measure", "Select Health Measure", choices=processor.get_measures(), selected="Alcohol consumption"),
        ),
        ui.card(
            ui.card_header("Trend Visualization"),
            ui.output_plot("trend_plot"),
        ),
        ui.card(
            ui.card_header("Data Summary"),
            ui.output_table("data_summary")
        )
    )
)

# Server
def server(input, output, session):
    
    def get_filtered_df():
        return processor.filter_data(input.country(), input.measure())

    @output
    @render.plot
    def trend_plot():
        df = get_filtered_df()
        if df.empty:
            plt.text(0.5, 0.5, "No data available for this selection", ha='center')
            return plt.gcf()
            
        plt.figure(figsize=(10, 5))
        plt.plot(df['year'], df['value'], marker='s', color='darkred', linewidth=2)
        plt.title(f"{input.measure()} in {input.country()}")
        plt.xlabel("Year")
        plt.ylabel(df['units'].iloc[0] if not df.empty else "Value")
        plt.grid(alpha=0.3)
        return plt.gcf()

    @output
    @render.table
    def data_summary():
        df = get_filtered_df()
        return df[['year', 'value', 'units', 'method']].tail(10)

app = App(app_ui, server)
