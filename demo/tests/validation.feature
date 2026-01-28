@django_db
Feature: Use form validation
 Background:

  Scenario: Check form validation page
    Given a form named "Event Registration" exists
     When I visit "/forms/event-registration"
     Then I should see the form page "Event Registration"
      And I should see an email input named "validation_email"
      And I should see 1 input in total

  Scenario: Validate a form
    Given a form named "Event Registration" exists

     When I visit "/forms/event-registration"
      And I fill the "validation_email" input with "hello@example.fr"
      And I validate the form

     Then I should see the token-validation info message
     And  I should receive a validation email from contact@example.com to hello@example.fr

     When I click on the validation link
     Then I should see the token-validation success message

     When I validate the form
     Then the page title should be "Event Registration"
      And the page should contain a form-thank-you element
