@django_db
Feature: Create some basic forms

  Background:

  Scenario: Visit the index form page
    Given the form index page exists
     When I visit "/forms"
     Then the page title should be "Forms"
      And I should see the title "Forms"

  Scenario: Create a form page
   #=== TODO ===
