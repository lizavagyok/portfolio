from shiny import App, render, ui
import matplotlib.pyplot as plt
from data_model import PortfolioData

# Part 1: UI
app_ui = ui.page_fluid(
    ui.h2("Object-Oriented Data Visualization"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider("n", "Number of Data Points", 10, 500, 100),
            ui.output_text("summary")
        ),
        ui.panel_main(
            ui.output_plot("plot"),
        ),
    ),
)

# Part 2: Server
def server(input, output, session):
    # Instantiate the OO Data Class
    portfolio_data = PortfolioData()

    @output
    @render.text
    def summary():
        portfolio_data.update_points(input.n())
        stats = portfolio_data.get_summary()
        return f"Mean: {stats['y']['mean']:.2f} | Std: {stats['y']['std']:.2f}"

    @output
    @render.plot(alt="A dynamic line plot")
    def plot():
        portfolio_data.update_points(input.n())
        df = portfolio_data.data
        plt.figure(figsize=(10, 6))
        plt.plot(df['x'], df['y'], marker='o', linestyle='-', color='blue')
        plt.title(f"Random Walk with {input.n()} points")
        plt.grid(True)
        return plt.gcf()

# Part 3: App
app = App(app_ui, server)
