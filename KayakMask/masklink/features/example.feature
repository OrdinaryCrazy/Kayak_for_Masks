Feature: Update Masks

Scenario: Display all brand
  Given a set of website
  |Website               	|  Filtration Efficiency |
  |3M Vflex               |                     99%|
  |Happy Mask       	    |               	    99%|
  |POD                    |                     98%|
  |Flomask              	|               	  99.8%|
  |Wayre                 	|              	    99.9%|
  |Caraa Tailored Junior  |		                  99%|
  |Cambridge              |		                  98%|
  When I go to the home page
  Then I should see all the brand on display
  And I should see all the product items that are available to purchase 

Scenario: Purchase
  When I click the purchase link
  Then I should jump to the product page