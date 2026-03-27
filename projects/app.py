from shiny import App, render, ui
import matplotlib.pyplot as plt
import numpy as np

# Part 1: UI
app_ui = ui.page_fluid(
    ui.h2("Shiny for Python on Posit Connect"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider("n", "N", 0, 100, 20),
        ),
        ui.panel_main(
            ui.output_plot("plot"),
        ),
    ),
)

# Part 2: Server
def server(input, output, session):
    @output
    @render.plot(alt="A histogram")
    def plot():
        np.random.seed(19680801)
        x = 100 + 15 * np.random.randn(437)
        plt.hist(x, input.n(), density=True)
        return plt.gcf()

# Part 3: App
app = App(app_ui, server)
