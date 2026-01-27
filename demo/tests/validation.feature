@django_db
Feature: Use form validation

  Background:

  Scenario: Validate a form
    Given the form index page exists
      And a form named "Event Registration" exists
     When I visit "http://localhost:8000/forms/event-registration"
      And I fill the "validation_email" input with "njourdane@laas.fr"
      And I validate the form
     Then I should see a validation info message
