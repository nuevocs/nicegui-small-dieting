from nicegui import ui
from dataclasses import dataclass

NUTRITION_CATEGORY = {
    1: 'Dairy',
    2: 'Meat',
    3: 'Vegetable',
    4: 'Fruit',
    5: 'Grain',
    6: 'Fat',
}
PROTEIN = 4
FAT = 9
CARBOHYDRATE = 4
SITE_TITLE = "Small Dieting Projects"


def page_layout_consumbles():
    with ui.header(elevated=True).style('background-color: #3874c8').classes('items-center justify-between'):
        ui.label(SITE_TITLE).classes("text-xl text-center")
        ui.button(on_click=lambda: right_drawer.toggle()).props('flat color=white icon=menu')
    with ui.footer().style('background-color: #3874c8'):
        ui.label('copyright nuevocs.dev').classes("text-sm text-center")
    with ui.right_drawer(fixed=False).style('background-color: #fcfcfc; width:"350"').props(
            'bordered mini-to-overlay width="250" show-if-above="False"') as right_drawer:
        with ui.column():
            ui.label('MENU').classes("text-xl text-gray-600/75 text-center")
            ui.link('Main', main_content)
            ui.link('Training', ptpage_content)


class Nutrition:
    def __init__(self):
        with ui.column():
            # for future use. I want to use this to select the menu from the database
            # self.nutrition_name = ui.select([1,2])
            # self.nutrition_category = ui.select([1,2])
            self.nutrition_name = ui.input(label="menu", placeholder="menu name")
            self.nutrition_category = ui.select(NUTRITION_CATEGORY)
        with ui.column().classes('w-full'):
            self.nutrition_protein_title = ui.label("protein")
            self.nutrition_protein = ui.slider(min=0, max=100, value=0)
            self.nutrition_protein_label = ui.label().bind_text_from(self.nutrition_protein, 'value')
        with ui.column().classes('w-full'):
            self.nutrition_fat_title = ui.label("fat")
            self.nutrition_fat = ui.slider(min=0, max=100, value=0)
            self.nutrition_fat_label = ui.label().bind_text_from(self.nutrition_fat, 'value')
        with ui.column().classes('w-full'):
            self.nutrition_carbohydrate_title = ui.label("carb")
            self.nutrition_carbohydrate = ui.slider(min=0, max=300, value=0)
            self.nutrition_carbohydrate_label = ui.label().bind_text_from(self.nutrition_carbohydrate, 'value')
        with ui.column().classes('w-full'):
            self.nutrition_amount = ui.number(label="quantity",  on_change=lambda: self.current_calories())

    def current_calories(self):
        global PROTEIN, FAT, CARBOHYDRATE
        carolies = self.nutrition_protein.value * PROTEIN * self.nutrition_amount.value + self.nutrition_fat.value * FAT * self.nutrition_amount.value + self.nutrition_carbohydrate.value * CARBOHYDRATE * self.nutrition_amount.value
        ui.notify(f"Calories: {carolies}")


class PhysicalTraining:
    def __init__(self):
        self.pt_name = 0
        self.pt_category = 0
        self.pt_duration = 0
        self.pt_intensity = 0


@dataclass
class NutritionData:
    name: str
    category: str
    protein: int
    fat: int
    carbohydrate: int
    amount: int
    calories: float


@ui.page('/physical-training')
async def ptpage_content():
    page_layout_consumbles()

@ui.page('/')
async def main_content():
    def get_data_from_inputs():
        global PROTEIN, FAT, CARBOHYDRATE
        nutrition_data = NutritionData(
            name=nutrition.nutrition_name.value,
            category=nutrition.nutrition_category.value,
            protein=nutrition.nutrition_protein.value,
            fat=nutrition.nutrition_fat.value,
            carbohydrate=nutrition.nutrition_carbohydrate.value,
            amount=nutrition.nutrition_amount.value,
            calories=nutrition.nutrition_protein.value * PROTEIN * nutrition.nutrition_amount.value + nutrition.nutrition_fat.value * FAT * nutrition.nutrition_amount.value + nutrition.nutrition_carbohydrate.value * CARBOHYDRATE * nutrition.nutrition_amount.value
        )
        collection.append(nutrition_data)
        collection_table.update()
        print(nutrition_data)

    page_layout_consumbles()

    with ui.row():
        with ui.card().tight() as card:
            ui.image('https://picsum.photos/id/75/640/100')

            with ui.card_section():
                # adding a title
                ui.markdown("""
                ## Your nutrition entries
                """).classes("text-xl text-gray-600/75")
            with ui.card_section():
                with ui.column():
                    nutrition = Nutrition()
                    ui.button("add", on_click=lambda: get_data_from_inputs())


        with ui.card():
            with ui.card_section():
                with ui.column():
                    ui.markdown("""
                    ## Collection
                    """).classes("text-sm text-gray-600/75")
                    collection = []
                    header = [
                        {"name": "name", "label": "Name", "field": "name"},
                        {"name": "amount", "label": "Amount", "field": "amount"},
                        {"name": "calories", "label": "Calories", "field": "calories", "required": True,
                         "sortable": True,
                         "align": "left"},
                    ]
                    collection_table = ui.table(columns=header, rows=collection)
                    ui.button("submit", on_click=lambda: print(collection))


ui.run()
