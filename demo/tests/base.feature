@django_db
Feature: Create some basic forms

  Background:

  Scenario: Visit the index form page
    Given the form index page exists
     When I visit "http://localhost:8000/forms"
     Then the page title should be "Forms"
      And I should see the title "Forms"

  Scenario: Create an empty form
    Given the form index page exists
      And a form named "Event Registration" exists
     When I visit "http://localhost:8000/forms/event-registration"
     Then the template used should be "demo/form_page.html"
      And the page title should be "Event Registration"
      And I should see an email input named "validation_email"
      And I should see 1 input in total
