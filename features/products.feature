Feature: The product service back-end
    As a Product Manager
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | description     | price | available | category   |
        | Hat        | A red hat       | 59.95 | True      | Clothing   |
        | Shoes      | Blue shoes      | 120.50| True      | Clothing   |
        | Big Mac    | 1/4 lb burger   | 5.99  | False     | Food       |
        | Sheets     | Full bed sheets | 87.00 | True      | Clothing   |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Product Demo REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "home page"
    And I set the "Name" to "Hammer"
    And I set the "Description" to "Claw hammer"
    And I set the "Price" to "34.95"
    And I set the "Available" to "True"
    And I set the "Category" to "Tools"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Description" field should be empty

Scenario: Read a Product
    When I visit the "home page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should not see "404 Not Found"
    And I should see "Hat" in the results
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should not see "404 Not Found"
    And I should see "Hat" in the "Name" field
    And I should see "A red hat" in the "Description" field
    And I should see "True" in the "Available" field
    And I should see "Clothing" in the "Category" field

Scenario: Update a Product
    When I visit the "home page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should not see "404 Not Found"
    And I should see "Hat" in the results
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should not see "404 Not Found"
    And I should see "Hat" in the "Name" field
    When I change "Name" to "Fedora"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Fedora" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "Fedora" in the results
    And I should not see "Hat" in the results

Scenario: Delete a Product
    When I visit the "home page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should not see "404 Not Found"
    And I should see "Hat" in the results
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    When I press the "Clear" button
    And I press the "Search" button
    Then I should not see "Hat" in the results

Scenario: List all products
    When I visit the "home page"
    And I press the "Search" button
    Then I should not see "404 Not Found"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results

Scenario: Search for products by Category
    When I visit the "home page"
    And I set the "Category" to "Clothing"
    And I press the "Search" button
    Then I should not see "404 Not Found"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Sheets" in the results
    And I should not see "Big Mac" in the results

Scenario: Search for products by Availability
    When I visit the "home page"
    And I set the "Available" to "True"
    And I press the "Search" button
    Then I should not see "404 Not Found"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Sheets" in the results
    And I should not see "Big Mac" in the results

Scenario: Search for products by Name
    When I visit the "home page"
    And I set the "Name" to "Hat"
    And I press the "Search" button
    Then I should not see "404 Not Found"
    And I should see "Hat" in the results
    And I should not see "Shoes" in the results
    And I should not see "Big Mac" in the results
    And I should not see "Sheets" in the results