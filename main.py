import os
import pandas as pd
from nicegui import ui
from database import db

ui.dark_mode().enable()

# Initialize the SQLite Database
if not os.path.exists("networth.db"):
    print("Database does not exist... Creating Database")
    db.initialize_database()

select_data = []
my_data = db.get_all_items()
line_df = db.get_dataframe()

# App Title
ui.label("Net Worth Calculator").classes("text-4xl")
ui.splitter(horizontal=True)

# Data Entry and Table
ui.label("Line Items").classes("text-2xl")
my_table: ui.aggrid = ui.aggrid(
    {
        "defaultColDef": {"flex": 1},
        "columnDefs": [
            {"headerName": "Name", "field": "name"},
            {"headerName": "Type", "field": "type"},
            {"headerName": "Status", "field": "status"},
            {
                "headerName": "Amount",
                "field": "amount",
                "valueFormatter": lambda params: f"${float(params.value):.2f}",
            },
            {"headerName": "ID", "field": "id", "hide": True},
        ],
        "rowData": sorted(db.get_all_items(), key=lambda data: data["name"]),
        "rowSelection": "multiple",
    }
).classes("m-auto")


def add_new_data() -> None:
    """
    Adds a new line item to the database and updates the table with the new data.

    This function creates a new line item in the database using the values entered
    by the user in the `add_name`, `add_type`, and `add_amount` fields. It then
    retrieves all items from the database, sorts them by name, and updates the table
    with the new data. Finally, it displays a notification to the user that the new
    item has been added and closes the `new_data_dialog`.
    """

    db.create_line_item(
        name=add_name.value,
        type=add_type.value,
        status=add_status.value,
        amount=f"{float(add_amount.value):.2f}",
    )

    my_table.options["rowData"] = sorted(
        db.get_all_items(), key=lambda data: data["name"]
    )

    ui.notify(f"{add_name.value} Added!", color="green")

    # Close Dialog and Reset Values (inputs will reset themselves)
    new_data_dialog.close()
    add_status.set_value(None)
    add_amount.set_value(None)

    # Update Table
    my_table.update()


def update_data() -> None:
    """
    Updates an existing line item in the database and refreshes the table with the updated data.

    This function updates an existing line item in the database using the values entered by the
    user in the `edit_name`, `edit_type`, and `edit_amount` fields. It then retrieves all items
    from the database, sorts them by name, and updates the table with the new data. Finally, it
    displays a notification to the user that the selected item has been updated and closes the
    `edit_data_dialog`.
    """
    db.update_line_item(
        id=select_data["id"],
        name=edit_name.value,
        type=edit_type.value,
        status=edit_status.value,
        amount=f"{float(edit_amount.value):.2f}",
    )

    my_table.options["rowData"] = sorted(
        db.get_all_items(), key=lambda data: data["name"]
    )

    ui.notify(f"Updated {select_data['name']}")

    edit_data_dialog.close()
    my_table.update()


# Dialog for Adding Input
with ui.dialog() as new_data_dialog:
    with ui.card():
        add_name = ui.input(label="Add Name")
        add_type = ui.input(label="Add Type")
        add_status = ui.select(
            label="Add Status", options=["Asset", "Liability"], value=None
        ).classes("w-full")
        add_amount = ui.number(label="Add Amount", format="%.2f", value=None).on(
            "blur", lambda: add_amount.update()
        )
        ui.button("Save New Stream", on_click=add_new_data)

# Dialog for Editing Input
with ui.dialog() as edit_data_dialog:
    with ui.card():
        edit_name = ui.input(label="Edit Name")
        edit_type = ui.input(label="Edit Type")
        edit_status = ui.select(
            label="Edit Status", options=["Asset", "Liability"]
        ).classes("w-full")
        edit_amount = ui.number(label="Edit Amount", format="%.2f").on(
            "blur", lambda: edit_amount.update()
        )
        ui.button("Edit Stream", on_click=update_data)


def opendata(e) -> None:
    # Open Dialog to add new data to table
    new_data_dialog.open()


async def removedata() -> None:
    """
    Removes a selected line item from the database and refreshes the table with the
    updated data.

    This function retrieves the selected row from the table and uses the
    `db.select_line_item` function to find the corresponding line item in the database.
    It then deletes the line item from the database using the `db.delete_line_item`
    function. Finally, it displays a notification to the user that the selected item
    has been removed, retrieves all items from the database, sorts them by name, and
    updates the table with the new data.
    """

    row = await my_table.get_selected_row()

    if not row:
        ui.notify("No Data was Selected")
        return

    db.delete_line_item(row["id"])

    ui.notify(f"Removed {row['name']}", color="red")

    my_table.options["rowData"] = sorted(
        db.get_all_items(), key=lambda data: data["name"]
    )

    my_table.update()


async def editdata() -> None:
    """
    Opens the edit data dialog and populates it with the data from the selected row in the table.

    This function retrieves the selected row from the table and stores it in the global `select_data`
    variable. If no row is selected, it displays a notification to the user and returns without doing
    anything. Otherwise, it sets the values of the `edit_name`, `edit_type`, and `edit_amount` fields
    in the `edit_data_dialog` to the values f
    """
    global select_data
    select_data = await my_table.get_selected_row()

    if not select_data:
        ui.notify("No Data was Selected")
        return

    edit_name.set_value(select_data["name"])
    edit_type.set_value(select_data["type"])
    edit_status.set_value(select_data["status"])
    edit_amount.set_value(select_data["amount"])

    edit_data_dialog.open()


# CRUD Buttons
with ui.row() as button_row:
    ui.button("Add", color="green", on_click=lambda e: opendata(e))
    ui.button("Edit", on_click=editdata)
    ui.button("Delete", color="red", on_click=removedata)

ui.splitter(horizontal=True)

# Reporting
ui.label("Net Worth Breakdown").classes("text-2xl")

sum_liabilties = line_df.loc[line_df["status"] == "Liability", "amount"].sum()
sum_assets = line_df.loc[line_df["status"] == "Asset", "amount"].sum()
net_worth = sum_assets - sum_liabilties

with ui.row().classes("w-full justify-evenly") as tile_row:
    with ui.card().classes("w-1/4 place-content-center") as total_items:
        ui.label("Net Worth").classes("text-xl").classes("m-auto")
        ui.label(f"${float(net_worth):,.2f}").classes("text-center").classes("m-auto")
    with ui.card().classes("w-1/4 place-content-center") as total_assets:
        ui.label("Total Assets").classes("text-xl").classes("m-auto")
        ui.label(f"${float(sum_assets):,.2f}").classes("m-auto")
    with ui.card().classes("w-1/4 place-content-center") as total_liabilities:
        ui.label("Total Liabilities").classes("text-xl").classes("m-auto")
        ui.label(f"${float(sum_liabilties):,.2f}").classes("m-auto")

ui.run(title="Net Worth Tracker", favicon="assets\\asset.png")
