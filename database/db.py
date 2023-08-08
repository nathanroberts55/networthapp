from typing import List
from sqlmodel import SQLModel, Session, create_engine, select
from models.line_item import LineItem

sqlite_file_name = "networth.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)

session = Session(engine)


def initialize_database() -> None:
    """
    Initializes the database by creating all necessary tables.

    This function uses the `create_all` method of the `SQLModel.metadata`
    object to create all tables defined in the `SQLModel` models. This
    function should be called before any other database operations are
    performed to ensure that the database is properly set up.
    """
    SQLModel.metadata.create_all(engine)


def get_all_items() -> List[dict]:
    """
    Retrieves all line items from the database and returns them as a list of dictionaries.

    This function uses a `select` statement to retrieve all rows from the `LineItem` table
    in the database. It then converts each row to a dictionary and returns a list of all
    dictionaries.


    Returns:
        List[dict]: A list of dictionaries, where each dictionary represents a line item
                    in the database.
    """
    line_items = session.exec(select(LineItem)).all()
    return [dict(item) for item in line_items]


def create_line_item(name: str, type: str, amount: str) -> dict:
    """Creates a new line item in the database and returns it as a dictionary.

    This function creates a new `LineItem` object with the specified `name`,
    `type`, and `amount` attributes, adds it to the database session, and
    commits the changes to the database. It then refreshes the object to ensure
    that it has been properly saved and returns it as a dictionary.

    Args:
        name (str): The name of the line item to be created.
        type (str): The type of the line item to be created.
        amount (str): The amount of the line item to be created.

    Returns:
        dict: A dictionary representation of the newly created line item.
    """
    new_item = LineItem(name=name, type=type, amount=amount)

    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return dict(new_item)


def get_line_item(name: str, type: str, amount: str) -> dict:
    """This function retrieves a line item from the database based on the
    provided name, type, and amount.

    Args:
        name (str): The name of the line item to retrieve.
        type (str): The type of the line item to retrieve.
        amount (str): The amount of the line item to retrieve.

    Returns:
        dict: A dictionary representation of the retrieved line item.
    """
    line_item = session.exec(
        select(LineItem).where(
            LineItem.name == name, LineItem.type == type, LineItem.amount == amount
        )
    ).first()

    return dict(line_item)


def update_line_item(
    name: str,
    type: str,
    amount: str,
    updated_name: str,
    updated_type: str,
    updated_amount: str,
) -> None:
    """This function updates a line item in the database based on the provided name,
    type, and amount. The line item is updated with the new values for name, type,
    and amount.

    Args:
        name (str): The name of the line item to update.
        type (str): The type of the line item to update.
        amount (str): The amount of the line item to update.
        updated_name (str): The new name for the line item.
        updated_type (str): The new type for the line item.
        updated_amount (str): The new amount for the line item.
    """
    line_item = session.exec(
        select(LineItem).where(
            LineItem.name == name, LineItem.type == type, LineItem.amount == amount
        )
    ).first()

    line_item.name = updated_name
    line_item.type = updated_type
    line_item.amount = updated_amount

    session.add(line_item)
    session.commit()
    session.refresh(line_item)


def delete_line_item(line_item_id: int) -> None:
    """This function deletes a line item from the database based on the provided line item ID.

    Args:
        line_item_id (int): The ID of the line item to delete.
    """
    line_item = session.exec(select(LineItem).where(LineItem.id == line_item_id)).one()

    session.delete(line_item)
    session.commit()
