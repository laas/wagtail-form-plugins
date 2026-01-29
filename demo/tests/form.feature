@django_db
Feature: Create some basic forms

  Background:

  Scenario: Visit the index form page
    Given the form index page exists
     When I visit "/forms"
     Then I should see the form index page

  Scenario: Create a form page
   #=== TODO ===
