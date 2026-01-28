@django_db
Feature: Use form validation

  Background:

  Scenario: Validate a form
    Given the form index page exists
      And a form named "Event Registration" exists

     When I visit "http://localhost:8000/forms/event-registration"
      And I fill the "validation_email" input with "hello@example.fr"
      And I validate the form

     Then I should see a token-validation info message
      And I should receive an email
      And the email subject should contain "validation"
      And the email should be sent from "contact@example.com"
      And the email should be sent to "hello@example.fr"
      And the email body should contain a link

     When I click on that link
     Then I should see a token-validation success message

     When I validate the form
     Then the page title should be "Event Registration"
      And the page should contain a form-thank-you element
