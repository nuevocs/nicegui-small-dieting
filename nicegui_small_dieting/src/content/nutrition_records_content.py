from nicegui import ui
from ..db.supabase_utilities import as_dict_supabase, select_filtered
from ..util.datetime_related_func import get_today_date
import pandas as pd


def nutrition_records_content() -> None:
    data = select_filtered("nutrition_details",
                           "date, nutrition_name, nutrition_protein, nutrition_fat, nutrition_carbohydrate, nutrition_calories",
                           "date", get_today_date())
    data = pd.DataFrame(data)
    group_by = data.groupby('date').sum()
    data.to_csv("data.csv")
    group_by.to_csv("grpby.csv")

    # print(group_by)

    chart_calories_by_date = ui.chart({
        'title': False,
        'chart': {'type': 'column'},
        'xAxis': {'categories': group_by.index.tolist()},
        'series': [
            {'name': 'Calories', 'data': group_by["nutrition_calories"].tolist()},
        ],
    }).classes('w-full h-64')
    chart_pfc_by_date = ui.chart({
        'title': False,
        'chart': {'type': 'bar'},
        'xAxis': {'categories': group_by.index.tolist()},
        'series': [
            {'name': 'Protein', 'data': group_by["nutrition_protein"].tolist()},
            {'name': 'Fat', 'data': group_by["nutrition_fat"].tolist()},
            {'name': 'Carb', 'data': group_by["nutrition_carbohydrate"].tolist()},
        ],
    }).classes('w-full h-64')
