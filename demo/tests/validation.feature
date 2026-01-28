@django_db
Feature: Use form validation

  Background:

  Scenario: Validate a form
    Given the form index page exists
      And a form named "Event Registration" exists

     When I visit "http://localhost:8000/forms/event-registration"
      And I fill the "validation_email" input with "hello@example.fr"
      And I validate the form

     Then I should see the token-validation info message
     And  I should receive a validation email from contact@example.com to hello@example.fr

     When I click on the validation link
     Then I should see the token-validation success message

     When I validate the form
     Then the page title should be "Event Registration"
      And the page should contain a form-thank-you element
