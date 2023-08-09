import re
import os
import subprocess
import time
from playwright.sync_api import Playwright, sync_playwright, expect


def test_add_line(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8080/")

    # Page Title Check
    expect(page).to_have_title(re.compile("Net Worth Tracker"))

    # Button Checks
    add_button = page.get_by_role("button", name="Add")
    edit_button = page.get_by_role("button", name="Edit")
    delete_button = page.get_by_role("button", name="Delete")

    expect(add_button).to_be_enabled()
    expect(edit_button).to_be_enabled()
    expect(delete_button).to_be_enabled()

    # Fill in the form
    add_button.click()
    page.get_by_label("Add Name").click()
    page.get_by_label("Add Name").fill("Test Name")
    page.get_by_label("Add Type").click()
    page.get_by_label("Add Type").fill("Test Type")
    page.get_by_label("Add Amount").click()
    page.get_by_label("Add Amount").fill("Test Amount")

    # Submit the Form in the dialog
    page.get_by_role("button", name="Save New Stream").click()

    # Check Values are in the table
    table = page.locator(".ag-center-cols-viewport")
    expect(table).to_contain_text("Test Name")
    expect(table).to_contain_text("Test Type")
    expect(table).to_contain_text("Test Amount")

    # ---------------------
    context.close()
    browser.close()


def test_edit_line(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8080/")

    # Page Title Check
    expect(page).to_have_title(re.compile("Net Worth Tracker"))

    # Button Checks
    add_button = page.get_by_role("button", name="Add")
    edit_button = page.get_by_role("button", name="Edit")
    delete_button = page.get_by_role("button", name="Delete")

    expect(add_button).to_be_enabled()
    expect(edit_button).to_be_enabled()
    expect(delete_button).to_be_enabled()

    # Select Test Row that was created above
    page.locator(".ag-row", has_text="Test Name").click()

    # Wait for the row with the ag-row-selected class to appear
    page.wait_for_selector(".ag-row.ag-row-focus.ag-row-selected")

    # Click Edit Button
    edit_button.click()

    # See if the edit form is prepopulated
    edit_name = page.get_by_label("Add Name")
    edit_type = page.get_by_label("Add Type")
    edit_amount = page.get_by_label("Add Amount")

    expect(edit_name).to_have_value("Test Name")
    expect(edit_type).to_have_value("Test Type")
    expect(edit_amount).to_have_value("Test Amount")

    # Edit Data in the form
    page.get_by_label("Add Name").click()
    page.get_by_label("Add Name").fill("Test Name_Updated")
    page.get_by_label("Add Type").click()
    page.get_by_label("Add Type").fill("Test Type_Updated")
    page.get_by_label("Add Amount").click()
    page.get_by_label("Add Amount").fill("Test Amount_Updated")

    # Submit the Form in the dialog
    page.get_by_role("button", name="Edit Stream").click()

    # Check Values are in the table
    table = page.locator(".ag-center-cols-viewport")
    expect(table).to_contain_text("Test Name_Updated")
    expect(table).to_contain_text("Test Type_Updated")
    expect(table).to_contain_text("Test Amount_Updated")

    # ---------------------
    context.close()
    browser.close()


def test_delete_line(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://localhost:8080/")

    # Page Title Check
    expect(page).to_have_title(re.compile("Net Worth Tracker"))

    # Button Checks
    add_button = page.get_by_role("button", name="Add")
    edit_button = page.get_by_role("button", name="Edit")
    delete_button = page.get_by_role("button", name="Delete")

    expect(add_button).to_be_enabled()
    expect(edit_button).to_be_enabled()
    expect(delete_button).to_be_enabled()

    # Select Test Row that was created above
    page.locator(".ag-row", has_text="Test Name_Updated").click()

    # Wait for the row with the ag-row-selected class to appear
    page.wait_for_selector(".ag-row.ag-row-focus.ag-row-selected")

    # Click Edit Button
    delete_button.click()

    # Check Values are in the table
    table = page.locator(".ag-center-cols-viewport")
    expect(table).not_to_contain_text("Test Name_Updated")
    expect(table).not_to_contain_text("Test Type_Updated")
    expect(table).not_to_contain_text("Test Amount_Updated")

    # ---------------------
    context.close()
    browser.close()
