import os
from nicegui import ui
from database import db

ui.dark_mode().enable()

# Initialize the SQLite Database
if not os.path.exists("networth.db"):
    print("Database does not exist... Creating Database")
    db.initialize_database()

select_data = []
my_data = db.get_all_items()

my_table: ui.aggrid = ui.aggrid(
    {
        "defaultColDef": {"flex": 1},
        "columnDefs": [
            {"headerName": "Name", "field": "name"},
            {"headerName": "Type", "field": "type"},
            {"headerName": "Amount", "field": "amount"},
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
        name=add_name.value, type=add_type.value, amount=add_amount.value
    )

    my_table.options["rowData"] = sorted(
        db.get_all_items(), key=lambda data: data["name"]
    )

    ui.notify(f"{add_name.value} Added!", color="green")

    new_data_dialog.close()
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
        select_data["name"],
        select_data["type"],
        select_data["amount"],
        updated_name=edit_name.value,
        updated_type=edit_type.value,
        updated_amount=edit_amount.value,
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
        add_amount = ui.input(label="Add Amount")
        ui.button("Save New Stream", on_click=add_new_data)

# Dialog for Editing Input
with ui.dialog() as edit_data_dialog:
    with ui.card():
        edit_name = ui.input(label="Add Name")
        edit_type = ui.input(label="Add Type")
        edit_amount = ui.input(label="Add Amount")
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

    line_item = db.select_line_item(row["name"], row["type"], row["amount"])

    print(line_item)

    db.delete_line_item(line_item_id=line_item["id"])

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
    edit_amount.set_value(select_data["amount"])

    edit_data_dialog.open()


# CRUD Buttons
with ui.row() as button_row:
    ui.button("Add", color="green", on_click=lambda e: opendata(e))
    ui.button("Edit", on_click=editdata)
    ui.button("Delete", color="red", on_click=removedata)


ui.run(title="Net Worth Tracker", favicon="assets\\asset.png")
