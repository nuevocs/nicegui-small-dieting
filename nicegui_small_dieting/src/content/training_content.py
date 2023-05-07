from dataclasses import dataclass
from nicegui import ui
from ..db.supabase_utilities import as_dict_supabase

TRAINING_CATEGORY = {
    1: 'Run',
    2: 'Bike',
    3: 'KettleBell',
    4: 'FreeWeight',
}

RPE_SCALE = {
    1: "Very Light",
    2: "Light",
    3: "Light-Moderate",
    4: "Moderate-Easy",
    5: "Moderate",
    6: "Moderate-Hard",
    7: "Vigorous",
    8: "Vigorous Hard",
    9: "Very Hard",
    10: "Maximal",
}


class PhysicalTraining:
    def __init__(self):
        self.pt_name = ui.input(label="menu", placeholder="menu name")
        self.pt_category = ui.select(TRAINING_CATEGORY)
        ui.label("duration")
        self.pt_duration = ui.slider(min=0, max=300, value=0)  # in minutes
        ui.label().bind_text_from(self.pt_duration, 'value')
        ui.label("choose an intensity of your training")
        self.pt_rpe_scale = ui.select(RPE_SCALE)


@dataclass
class PhysicalTrainingData:
    pt_name: str
    pt_category: int
    pt_duration: int
    pt_rpe_scale: int
    pt_rpe_load: int


def training_content() -> None:
    def get_data_from_inputs():
        physical_training_data = PhysicalTrainingData(
            pt_name=physical_training.pt_name.value,
            pt_category=physical_training.pt_category.value,
            pt_duration=physical_training.pt_duration.value,
            pt_rpe_scale=physical_training.pt_rpe_scale.value,
            pt_rpe_load=physical_training.pt_duration.value * physical_training.pt_rpe_scale.value,
        )
        collection.append(physical_training_data)
        collection_table.update()

    def writing_data_to_db(collection):
        nbr_records = len(collection)
        ui.notify(f"{nbr_records} records has been written to the database")
        for c in collection:
            as_dict_supabase("physical_training_details", c)
        collection.clear()
        collection_table.update()

    with ui.row():
        with ui.row():
            with ui.card().tight() as card:
                ui.image('https://picsum.photos/id/75/640/100')

                with ui.card_section():
                    # adding a title
                    ui.markdown("""
                    ## Your Physical training entries
                    """).classes("text-xl text-gray-600/75")
                with ui.card_section():
                    with ui.column():
                        physical_training = PhysicalTraining()
                        ui.button("add", on_click=lambda: get_data_from_inputs())

        with ui.card().tight():
            ui.image('https://picsum.photos/id/60/640/350')
            with ui.card_section():
                with ui.column():
                    ui.markdown("""
                    ## Collection
                    """).classes("text-sm text-gray-600/75")
                    collection = []
                    header = [
                        {"name": "nutrition_name", "label": "Name", "field": "pt_name"},
                        {"name": "nutrition_amount", "label": "Duration", "field": "pt_duration"},
                        {"name": "calories", "label": "RPE Load", "field": "pt_rpe_load", "required": True,
                         "sortable": True,
                         "align": "left"},
                    ]
                    collection_table = ui.table(columns=header, rows=collection)
                    ui.button("submit", on_click=lambda: writing_data_to_db(collection))
