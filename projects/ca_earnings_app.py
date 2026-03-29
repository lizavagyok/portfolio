from shiny import App, render, ui, reactive
import matplotlib.pyplot as plt
import seaborn as sns
from ca_earnings_model import CAEarningsProcessor
import os

# Initialize data processor
csv_path = os.path.join(os.path.dirname(__file__), "data", "ca_earnings.csv")
processor = CAEarningsProcessor(csv_path)

# UI
app_ui = ui.page_fluid(
    ui.h2("California Earnings Analysis (2014)"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_select(
                "plot_type", 
                "Select Visualization", 
                choices={
                    "earnings_edu": "Earnings by Education & Gender",
                    "union_gap": "Gender Gap by Union Membership",
                    "heatmap": "Hourly Wage Heatmap (Top Occupations)"
                }
            ),
            ui.panel_conditional(
                "input.plot_type == 'earnings_edu'",
                ui.input_checkbox_group(
                    "edu_levels", 
                    "Filter Education Levels",
                    choices=processor.get_education_levels(),
                    selected=processor.get_education_levels()
                )
            ),
            ui.hr(),
            ui.markdown("""
            **Data Source:** 2014 CPS MORG (California Subset)
            
            This interactive dashboard explores how earnings are influenced by education, gender, and union membership.
            """)
        ),
        ui.card(
            ui.output_plot("main_plot"),
            full_screen=True
        ),
        ui.card(
            ui.card_header("Key Statistics Summary"),
            ui.output_table("stats_table")
        )
    )
)

# Server
def server(input, output, session):
    
    @output
    @render.plot
    def main_plot():
        plt.style.use('seaborn-v0_8-whitegrid')
        
        if input.plot_type() == "earnings_edu":
            data = processor.get_earnings_by_edu_gender(input.edu_levels())
            data_melted = data.reset_index().melt(id_vars='education', var_name='gender', value_name='earnwke')
            
            plt.figure(figsize=(10, 6))
            sns.barplot(data=data_melted, x='education', y='earnwke', hue='gender', 
                        order=[e for e in processor.EDU_ORDER if e in input.edu_levels()],
                        palette='muted')
            plt.title('Average Weekly Earnings by Education and Gender')
            plt.ylabel('Weekly Earnings ($)')
            plt.xlabel('Education Level')
            plt.xticks(rotation=15)
            plt.tight_layout()
            return plt.gcf()
            
        elif input.plot_type() == "union_gap":
            gap_data = processor.get_gender_gap_by_union()
            
            plt.figure(figsize=(8, 6))
            sns.barplot(x=gap_data.index, y=gap_data['Gender Gap (%)'], palette='coolwarm')
            plt.title('Gender Wage Gap: Union vs. Non-Union Members')
            plt.ylabel('Wage Gap (%)')
            plt.xlabel('Union Member')
            plt.ylim(0, 25)
            for i, gap in enumerate(gap_data['Gender Gap (%)']):
                plt.text(i, gap + 0.5, f'{gap:.1f}%', ha='center', fontweight='bold')
            plt.tight_layout()
            return plt.gcf()
            
        elif input.plot_type() == "heatmap":
            heatmap_data = processor.get_heatmap_data()
            
            plt.figure(figsize=(12, 10))
            sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="Greens", 
                        cbar_kws={'label': 'Mean Hourly Wage ($)'})
            plt.title('Mean Hourly Wage by Occupation and Education')
            plt.ylabel('Occupation')
            plt.xlabel('Education Level')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            return plt.gcf()

    @output
    @render.table
    def stats_table():
        if input.plot_type() == "earnings_edu":
            return processor.get_earnings_by_edu_gender(input.edu_levels()).reset_index()
        elif input.plot_type() == "union_gap":
            return processor.get_gender_gap_by_union().reset_index()
        elif input.plot_type() == "heatmap":
            return processor.get_heatmap_data().reset_index().head(10)

app = App(app_ui, server)
